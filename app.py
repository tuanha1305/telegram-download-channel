import logging
import time

import backoff
import toml
from telethon import TelegramClient
from telethon.tl.types import MessageMediaDocument
from telethon.errors import SessionPasswordNeededError
from telethon.errors import SessionExpiredError
import os
import asyncio

_logger = logging.getLogger(__name__)

_is_backoff_v2 = next(backoff.expo()) is None


def create_exp_backoff_generator(*args, **kwargs):
    gen = backoff.expo(*args, **kwargs)
    if _is_backoff_v2:
        gen.send(None)
    return gen


class TelegramDownloader:
    def __init__(self, phone, api_id, api_hash, target_channels, download_dir, filter_extensions, num_threads=3):
        self.client = TelegramClient(phone, api_id, api_hash)
        self.target_channels = target_channels
        self.download_dir = download_dir
        if not os.path.exists(self.download_dir):
            os.makedirs(self.download_dir)
            _logger.info(f"Created directory: {self.download_dir}")
        self.phone = phone
        self.filter_extensions = tuple(filter_extensions)
        self.num_threads = num_threads
        self.max_retry_time = 64

    async def start(self):
        await self.client.start(self.phone)
        _logger.info("Client Created")
        # Ensure authorization
        if not await self.client.is_user_authorized():
            await self.client.send_code_request(self.phone)
            try:
                await self.client.sign_in(self.phone, input('Enter the code: '))
            except SessionPasswordNeededError:
                await self.client.sign_in(password=input('Password: '))
            except Exception as e:
                _logger.info(f"Failed to authenticate: {e}")
                return
        await self.process_channels()

    async def download_file(self, message):
        for delay in create_exp_backoff_generator(self.max_retry_time):
            file_name = message.file.name
            file_path = os.path.join(self.download_dir, file_name)
            try:
                # Check if the file exists and compare sizes
                if os.path.exists(file_path):
                    local_file_size = os.path.getsize(file_path)
                    if local_file_size == message.file.size:
                        _logger.info(f'File {file_name} already exists and is of the same size. Skipping download.')
                        break  # Skip re-download
                    else:
                        _logger.info(f'File {file_name} exists but sizes differ. Removing and re-downloading.')
                        os.remove(file_path)

                _logger.info(f'Downloading {file_name}')
                path = await message.download_media(file=self.download_dir)
                _logger.info(f'Downloaded {path}')
                break  # Break the retry loop on successful download
            except Exception as e:
                _logger.error(f'Error downloading {file_name}: {e}')
                await asyncio.sleep(delay)  # Use asyncio.sleep for async delay

    async def download_files_from_channel(self, channel):
        tasks = set()
        async for message in self.client.iter_messages(channel):
            if message.media and isinstance(message.media, MessageMediaDocument):
                file_name = message.file.name
                if file_name and file_name.endswith(self.filter_extensions):
                    tasks.add(asyncio.create_task(self.download_file(message)))

                    if len(tasks) >= self.num_threads:
                        _, tasks = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)

        if tasks:
            await asyncio.wait(tasks)

    async def process_channels(self):
        try:
            async for dialog in self.client.iter_dialogs():
                if any(target_name.lower() in dialog.name.lower() for target_name in self.target_channels):
                    _logger.info(f'Found channel: {dialog.name}')
                    await self.download_files_from_channel(dialog.entity)
        except SessionExpiredError:
            _logger.error('Session expired. Attempting to re-authenticate.')
            await self.start()
        _logger.info('Download complete!')


async def main():
    # Load configuration
    try:
        config = toml.load("config/config.toml")
    except Exception as e:
        _logger.error(f'Failed to load config.toml: {e}')
        exit(1)

    # validate config
    required_keys = ['phone', 'api_id', 'api_hash', 'target_channel_names', 'download_directory', 'filter_extensions']
    missing_keys = [key for key in required_keys if key not in config]
    if missing_keys:
        _logger.error(f'Missing configuration keys: {", ".join(missing_keys)}')
        exit(1)

    download_directory = config['download_directory']
    # Ensure download directory exists
    if not os.path.exists(download_directory):
        os.makedirs(download_directory)
    downloader = TelegramDownloader(config['phone'], config['api_id'], config['api_hash'],
                                    config['target_channel_names'], config['download_directory'],
                                    config['filter_extensions'])
    await downloader.start()


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger()

    fh = logging.FileHandler('app.log')
    fh.setLevel(logging.INFO)

    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)

    logger.addHandler(fh)
    logger.addHandler(ch)

    # run main app
    asyncio.run(main())

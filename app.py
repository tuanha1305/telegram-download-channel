import time

import backoff
import toml
from telethon import TelegramClient, events, sync
from telethon.tl.types import InputPeerChannel, MessageMediaDocument
from telethon.errors import SessionPasswordNeededError
import os
import asyncio

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
        self.phone = phone
        self.filter_extensions = tuple(filter_extensions)
        self.num_threads = num_threads
        self.max_retry_time = 64

    async def start(self):
        await self.client.start(self.phone)
        print("Client Created")
        # Ensure authorization
        if not await self.client.is_user_authorized():
            await self.client.send_code_request(self.phone)
            try:
                await self.client.sign_in(self.phone, input('Enter the code: '))
            except SessionPasswordNeededError:
                await self.client.sign_in(password=input('Password: '))
            except Exception as e:
                print(f"Failed to authenticate: {e}")
                return
        await self.process_channels()

    async def download_file(self, message):
        for delay in create_exp_backoff_generator(self.max_retry_time):
            file_name = message.file.name
            file_path = os.path.join(self.download_dir, file_name)
            try:
                if os.path.exists(file_path):
                    print(f'File {file_name} already exists. Removing and downloading a new copy.')
                    os.remove(file_path)

                print(f'Downloading {file_name}')
                path = await message.download_media(file=self.download_dir)
                print(f'Downloaded {path}')
                break
            except Exception as e:
                print(f'Error downloading {file_name}: {e}')
                time.sleep(delay)

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
        async for dialog in self.client.iter_dialogs():
            if any(target_name.lower() in dialog.name.lower() for target_name in self.target_channels):
                print(f'Found channel: {dialog.name}')
                await self.download_files_from_channel(dialog.entity)


async def main():
    # Load configuration
    try:
        config = toml.load("config/config.toml")
    except Exception as e:
        print(f'Failed to load config.toml: {e}')
        exit(1)

    # validate config
    required_keys = ['phone', 'api_id', 'api_hash', 'target_channel_names', 'download_directory', 'filter_extensions']
    missing_keys = [key for key in required_keys if key not in config]
    if missing_keys:
        print(f'Missing configuration keys: {", ".join(missing_keys)}')
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
    asyncio.run(main())

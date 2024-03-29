import toml
from telethon import TelegramClient, events, sync
from telethon.tl.types import InputPeerChannel, MessageMediaDocument
from telethon.errors import SessionPasswordNeededError
import os
import asyncio


class TelegramDownloader:
    def __init__(self, phone, api_id, api_hash, target_channels, download_dir, filter_extensions):
        self.client = TelegramClient(phone, api_id, api_hash)
        self.target_channels = target_channels
        self.download_dir = download_dir
        self.phone = phone
        self.filter_extensions = tuple(filter_extensions)

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

    async def download_zip_files_from_channel(self, channel):
        async for message in self.client.iter_messages(channel):
            if message.media and isinstance(message.media, MessageMediaDocument):
                file_name = message.file.name
                if file_name and file_name.endswith(self.filter_extensions):
                    path = await message.download_media(file=self.download_dir)
                    print(f'Downloaded {path}')

    async def process_channels(self):
        async for dialog in self.client.iter_dialogs():
            if any(target_name.lower() in dialog.name.lower() for target_name in self.target_channels):
                print(f'Found channel: {dialog.name}')
                await self.download_zip_files_from_channel(dialog.entity)


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
    downloader = TelegramDownloader(config['phone'], config['api_id'], config['api_hash'], config['target_channel_names'], config['download_directory'], config['filter_extensions'])
    await downloader.start()

if __name__ == '__main__':
    asyncio.run(main())

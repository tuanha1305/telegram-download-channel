
# Telegram Channel Downloader

This project is a Python script that automatically downloads files from specified Telegram channels. It uses the Telethon library to interact with Telegram's API, allowing users to search for channels by name and download all `.zip` files posted in those channels to a local directory.

## Features

- Download all files from specified Telegram channels.
- Easy configuration via `config.toml` for API credentials and target channels.
- Uses async/await for efficient file downloading.

## Prerequisites

Before you begin, ensure you have met the following requirements:

- Python 3.6 or higher installed on your system.
- A Telegram account and the creation of a Telegram API application for `api_id` and `api_hash`.
- Installation of required Python packages: `telethon`, `toml`.

## Installation

To install the required Python packages, run the following command:

```bash
pip install -r requirements.txt
```

## Configuration

1. Rename `config.example.toml` to `config.toml`.
2. Fill in your `api_id`, `api_hash`, `phone`, and desired `target_channel_names` and `download_directory` in `config.toml`.

Example `config.toml`:

```toml
phone = "+1234567890"
api_id = "123456"
api_hash = "abcdef1234567890abcdef987654321"
target_channel_names = ["Example Channel 1", "Example Channel 2"]
download_directory = "Downloaded_Files"
filter_extensions = [".zip"]
```

## Usage

To run the script, navigate to the script's directory in your terminal and execute:

```bash
python app.py
```

Follow any on-screen instructions to authenticate with Telegram if required.

## Contributing to the Project

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

Distributed under the MIT License. See `LICENSE` for more information.

## Contact

Your Name - tuanictu97@gmail.com

Project Link: [https://github.com/tuanha1305/telegram-download-channel.git](https://github.com/yourusername/telegram-channel-downloader)

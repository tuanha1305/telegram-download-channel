
# Telegram Channel Downloader

This project is a Python script that automatically downloads files from specified Telegram channels. It uses the Telethon library to interact with Telegram's API, allowing users to search for channels by name and download all files posted in those channels to a local directory.

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

## Register Telegram Application Developer

### Step 1: Register as a Telegram Developer

1. Visit the [Telegram API](https://my.telegram.org/auth) page.
2. Log in using your Telegram account.
3. Follow the on-screen instructions to register as a developer.

Note: Keep your developer credentials secure and do not share them publicly.

### Step 2: Create a New Application

1. After registering as a developer, navigate to the [API development tools](https://my.telegram.org/apps) section.
2. Click on "Create a new application".
3. Fill in the application details:
   - **App title**: [Your application's name]
   - **Short name**: [A shorter version of your application's name, if necessary]
   - **URL**: [Your application's URL, if applicable]
   - **Platform**: [Choose the platform your application will run on]
   - **Description**: [A brief description of your application]
4. Agree to the terms and conditions and click "Create Application".

### Step 3: Obtain Your API Keys

After creating your application, you will be presented with your API keys:

- **App ID**: A unique identifier for your application.
- **API Hash**: A hash key required for API access.

**Important**: Keep these keys confidential as they are essential for interacting with the Telegram API.

## Configuration

1. Rename `config.example.toml` to `config.toml`.
2. Fill in your `api_id`, `api_hash`, `phone`, and desired `target_channel_names` and `download_directory` in `config.toml`.

Example `config/config.toml`:

```toml
phone = "+1234567890"
api_id = "123456"
api_hash = "abcdef1234567890abcdef987654321"
target_channel_names = ["Example Channel 1", "Example Channel 2"]
download_directory = "Downloaded_Files"
filter_extensions = [".zip"]
num_threads = 3
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

Tuan Ha Anh - tuanictu97@gmail.com

Project Link: [https://github.com/tuanha1305/telegram-download-channel.git](https://github.com/yourusername/telegram-channel-downloader)

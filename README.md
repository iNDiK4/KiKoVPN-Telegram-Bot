# KiKoVPN Telegram Bot

KiKoVPN is a cute assistant for safe and anonymous internet browsing. This bot will help you set up a VPN and ensure your privacy.

## Dependencies

The bot requires the following dependencies:

- Python 3.11
- pyTelegramBotAPI 4.9.1

Install the dependencies using pip:

```bash
pip install pyTelegramBotAPI==4.9.1
```

## Configuration

Before running the bot, you need to configure it with your own API tokens and other settings.

1. **Telegram Bot API Token**: Obtain your bot API token from BotFather on Telegram. Replace the placeholder in the code with your actual token:

```python
API_TOKEN = 'YOUR_BOT_API_TOKEN'
```

2. **Admin IDs**: Replace the placeholder admin IDs with the actual Telegram user IDs of the administrators:

```python
admin_ids = [123456789, 987654321]  # Replace with real admin IDs
```

3. **Telegram Channel URL**: Replace the placeholder URL with the actual URL of your Telegram channel:

```python
channel_url = "https://t.me/your_channel"
```

## Usage

### Running the Bot

1. Clone the repository and navigate to its directory:

```bash
git clone https://github.com/iNDiK4/KiKoVPN-Telegram-Bot.git
cd KiKoVPN-Telegram-Bot
```

2. Create a virtual environment and activate it:

```bash
python -m venv venv
source venv/bin/activate  # For Windows use `venv\Scripts\activate`
```

3. Install the dependencies:

```bash
pip install -r requirements.txt
```

4. Run the bot:

```bash
python bot.py
```

### Functionality

#### Language Selection

Upon first launch, the bot will prompt you to select a language: Russian or English. The selected language will be saved and used in subsequent sessions.

#### Main Menu

The main menu includes the following sections:

- **VPN CFG**: List of available VPN configurations.
- **About Us**: Information about the KiKoVPN team.
- **Privacy**: Privacy policy.
- **Channel**: Link to the Telegram channel.

#### Admin Panel

Administrators have access to an additional "Admin Panel" button in the main menu. The admin panel includes the following functions:

- **➕ Admin**: Add a new administrator.
- **➖ Admin**: Remove an administrator.
- **✏️ Channel**: Change the Telegram channel link.
- **Users**: View a list of all bot users.

### Configuration Files

The bot creates and uses the following files:

- **users.txt**: List of all bot users.
- **languages.txt**: List of users and their selected languages.

### Example Usage

1. Run the bot and select a language.
2. In the main menu, choose the desired section.
3. Administrators can access the admin panel to manage the bot.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

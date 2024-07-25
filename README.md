# DFWM Antimat Telegram Bot

This repository contains the DFWM (Don't F**k With Me) Antimat Telegram Bot, designed to detect and handle offensive language in Telegram chat groups.

## Features

- Detects offensive language in real-time.
- Automatically warns users who use offensive language and deletes the message.
- Supports adding custom offensive words.
- Provides admin capabilities for managing the bot's behavior.

## Getting Started

### Prerequisites

- Python 3.11 or higher
- Telegram Bot API token (You can get this from [BotFather](https://core.telegram.org/bots#botfather) on Telegram)
- `pipenv` for managing dependencies

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/OfficialCodeVoyage/DFWM_antimat_telegram_bot.git
   cd DFWM_antimat_telegram_bot
    ```
2. Install the dependencies:
   
 ```bash
pipenv install
 ```

3. Create a .env file and add your Telegram Bot API token:

   ```bash
   echo "bot_token=your-telegram-bot-api-token" > .env
   ```
4. Add a bad_words.json file with an initial list of offensive words:

```json
[
    "badword1",
    "badword2"
]

```

## Usage

1. Activate the virtual environment:

```bash
pipenv shell
```

2. Run the bot:
   ```bash
   python bot.py
   ```

## Commands

/start: Start the bot and get a welcome message.
/addbadword <word>: Add a new word to the list of offensive words (Admins only or selected users).

##  Configuration
The list of offensive words is stored in bad_words.json.

## Contributing
Contributions are welcome! Please fork the repository and create a pull request.



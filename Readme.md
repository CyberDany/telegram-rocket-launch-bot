# RocketLaunchBot

![Rocket](/screenshots/Rocket.jpg)

## Description

RocketLaunchBot is a Telegram bot crafted to pinpoint the exact frame of a rocket launch using user interaction and a bisection algorithm. This project showcases coding practices for maintainable code, the ability to adapt to new programming paradigms, and an understanding of classic algorithms. It was developed as part of a selection process for a company, demonstrating practical application of theoretical computer science concepts.

## Features and Technologies

- **Bisection Algorithm**: Employs a methodical approach to determine the exact launch frame with minimal user interaction.
- **User Interaction**: Users provide input based on the images shown to guide the bisection process.
- **Technology**: Implemented in Python, leveraging the `python-telegram-bot` library for Telegram API interactions.

## Prerequisites

Before using this bot, create one using Telegram's BotFather to obtain an API token. Then, create a `.env` file at the root of the project with the following content:

<pre><code>TELEGRAM_TOKEN=your_api_token_here</code></pre>


## Installation and Setup

To install and set up RocketLaunchBot, execute the following steps:

1. Clone the repository:

<pre><code>git clone https://github.com/CyberDany/telegram-rocket-launch-bot.git</code></pre>

2. Navigate to the project directory and create a virtual environment:

<pre><code>cd RocketLaunchBot
python3 -m venv venv
source venv/bin/activate</code></pre>

3. Install the required dependencies:

<pre><code>pip install -r requirements.txt</code></pre>

4. Run the bot:

<pre><code>python bot.py</code></pre>

## Usage

Interact with the public bot by clicking the following link to Telegram: [Link to bot](https://t.me/rocket_launcher_bot). Start the conversation with the command `/start`.

Here are some usage examples on different platforms:

<p align="center">
  <img src="/screenshots/MobileAppKeyboard.jpg" alt="Mobile example" width="300"/>
</p>

- Mobile example: ![Mobile example](/screenshots/MobileAppKeyboard.jpg)
- Desktop app example: ![Desktop example](/screenshots/DesktopAppKeyboard.png)
- Browser example: ![Browser example](/screenshots/WebAppKeyboard.png)

## Maintainability

The project is structured to enhance maintainability through the following practices:

- **Modular Design**: Code is organized into separate modules within the `api`, `utils`, and `assets` directories, enabling isolation of functionality and ease of management.
- **Clear Abstraction**: Each module (`api_client.py`, `bisection.py`, `images_utils.py`, `telegram_utils.py`) encapsulates specific tasks, ensuring that components can be understood and modified independently.
- **Reusable Components**: Utilities are designed to be reusable, such as the `telegram_utils.py` which can be adapted for other bots with minimal changes.

## License

This project is free to use and is available under the [MIT License](LICENSE).


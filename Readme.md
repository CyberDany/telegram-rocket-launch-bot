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

In the mobile view the keyboard with the user's options are displayed immediately without the need to press the keyboard button.

<p align="center">
  <img src="/screenshots/MobileAppKeyboard.jpg" alt="Mobile example" width="300"/><br>
  <em>Example of the bot in the mobile app</em>
</p>

In the same way, in the desktop application the keyboard will appear with the options that the user has available at that moment. 

<p align="center">
  <img src="/screenshots/DesktopAppKeyboard.png" alt="Desktop example" width="300"/><br>
  <em>Example of the bot in the Desktop app</em>
</p>

In the case of the Web browser, it is necessary to click on the button at the bottom to display the options to the user.

<p align="center">
  <img src="/screenshots/WebAppKeyboard.png" alt="Browser example" width="300"/><br>
  <em>Example of the bot in the Browser</em>
</p>

## Implementation Summary

The RocketLaunchBot's logic operates as a finite state machine, utilizing specific states to guide the user through the frame identification process.

- **INITIAL State**: The bot awaits user input, specifically looking for the commands 'Ready' to proceed with the image search or 'Abort' to end the session.
- **SEARCHING State**: In this state, the bot engages with the user to determine if the rocket has launched. It presents images and awaits a 'Yes' or 'No' response. If the user responds 'Abort', the session is terminated.
- **SOLUTION State**: Once the correct frame is identified, the bot transitions to the solution state, where it presents the conclusive image showing the rocket launch.

User inputs such as 'Ready', 'Yes', 'No', 'Abort', and 'Restart' are integral to navigating through these states, ensuring a dynamic yet structured interaction flow.

## Example of use

After pressing /start, the Initial State is switched to Initial State. Here the user has two options available, 'Ready' and 'Abort'.

<p align="center">
  <img src="/screenshots/example01.png" alt="example" width="300"/><br>
  <em>INITIAL State</em>
</p>

After pressing Ready, the Searching State starts. It will start showing the images to the user and will have the options 'Yes' and 'No' to indicate the launch status. It also has the options 'Restart' and 'Abort'.

<p align="center">
  <img src="/screenshots/example02.png" alt="example" width="300"/><br>
  <em>SEARCHING State</em>
</p>

If the user presses abort, it will be indicated by a message and looks like the following image:

<p align="center">
  <img src="/screenshots/example03.png" alt="example" width="300"/><br>
  <em>Abort</em>
</p>

If the user presses Restart, it restarts from the beginning as shown in the following picture

<p align="center">
  <img src="/screenshots/example04.png" alt="example" width="300"/><br>
  <em>Abort</em>
</p>

At the end of the search process, the final result is displayed as follows

<p align="center">
  <img src="/screenshots/example05.png" alt="example" width="300"/><br>
  <em>Abort</em>
</p>


## Maintainability

The project is structured to enhance maintainability through the following practices:

- **Modular Design**: Code is organized into separate modules within the `api`, `utils`, and `assets` directories, enabling isolation of functionality and ease of management.
- **Clear Abstraction**: Each module (`api_client.py`, `bisection.py`, `images_utils.py`, `telegram_utils.py`) encapsulates specific tasks, ensuring that components can be understood and modified independently.
- **Reusable Components**: Utilities are designed to be reusable, such as the `telegram_utils.py` which can be adapted for other bots with minimal changes.

## License

This project is free to use and is available under the [MIT License](LICENSE).


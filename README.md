# 🖥️ PC Control Bot 🤖

![Banner](https://via.placeholder.com/1200x400.png?text=PC+Control+Bot+Banner)

**PC Control Bot** is a powerful Telegram bot that allows you to **remotely control your PC** with ease. Whether you want to launch apps, monitor system performance, or execute commands, this bot has you covered! 🚀

---

## ✨ Features

- **Remote Control**: Launch apps, monitor system performance, and execute commands from anywhere.
- **System Monitoring**: Check RAM usage, CPU temperature, and more.
- **Media Control**: Play, pause, skip, or rewind media playback.
- **File Management**: Zip folders and send them directly to Telegram.
- **Network Scanning**: Scan available Wi-Fi networks (Linux only).
- **Custom Commands**: Execute any shell command remotely.

---

## 🛠️ Installation

### Prerequisites
- Python 3.8+
- Telegram Bot Token (from [BotFather](https://core.telegram.org/bots#botfather))
- Required Python libraries: `python-telegram-bot`, `psutil`, `pyautogui`, `zipfile`, `subprocess`, `platform`, `json`, `socket`

### Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/pc-control-bot.git
   cd pc-control-bot

2. Install dependencies:
    ```bash
    Copy

    pip install -r requirements.txt

3. Set up your Telegram bot token:

        Replace TOKEN in the script with your bot token.

        Replace AUTHORIZED_USER_ID with your Telegram user ID.

4. Run the bot:
    ```bash
    Copy

    python pc_control_bot.py

### 🎮 Usage
Commands

    /start: Start the bot and show the main menu.

    /help: Show the help message.

    /zipfolder <path>: Zip a folder and send it.

    /scannetworks: Scan available Wi-Fi networks (Linux only).

    /systeminfo: Get system information.

    /cmd <command>: Execute a terminal command.

    /media <play|pause|next|previous>: Control media playback.

    /launch <app>: Launch an application (e.g., firefox, obs, obsidian).

### Inline Buttons

    💾 RAM Usage: Show RAM usage.

    🌡 CPU Temperature: Show CPU temperature.

    📸 Take Screenshot: Take a screenshot.

    📂 Zip Folder: Zip a folder.

    📡 Scan Networks: Scan Wi-Fi networks.

    📊 System Info: Get system information.

    🎵 Media Play/Pause/Next/Previous: Control media playback.

### 🛠️ Technologies Used

    Python: Core programming language.

    Telegram Bot API: For bot communication.

    psutil: For system monitoring.

    pyautogui: For taking screenshots.

    subprocess: For executing shell commands.


### 📞 Contact

For questions or feedback, feel free to reach out:

    Telegram: @hollymollyv

import os
import zipfile
import psutil
import pyautogui
import subprocess
import platform
import json
import socket
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# Telegram Bot Token
TOKEN = "bot token"
AUTHORIZED_USER_ID = user-tg  # Replace with your Telegram user ID

# List of apps to launch
APPS = {
    "Firefox": "firefox",
    "OBS": "obs",
    "Obsidian": "obsidian",
    "Code": "nvim",  # NeoVim jaja
    "Terminal": "alacritty",  # alacritty the best xd
    "Audio": "pavucontrol",
}

# 🔐 Authorization check
def is_authorized(update: Update) -> bool:
    user_id = update.effective_user.id if update.effective_user else None
    return user_id == AUTHORIZED_USER_ID

# 🎉 Start Command with Inline Buttons
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_authorized(update):
        return

    welcome_text = """
    🤖 Welcome to PC Control Bot! 🎮
    Use the commands below or choose an action from the buttons.
    """

    # Add app list to the welcome message
    app_list = "\n".join([f"- {app}" for app in APPS.keys()])
    welcome_text += f"\n\n📂 Available Apps:\n{app_list}"

    keyboard = [
        [InlineKeyboardButton("💾 RAM Usage", callback_data='ram_usage')],
        [InlineKeyboardButton("🌡 CPU Temperature", callback_data='cpu_temp')],
        [InlineKeyboardButton("📸 Take Screenshot", callback_data='take_screenshot')],
        [InlineKeyboardButton("📂 Zip Folder", callback_data='zip_folder')],
        [InlineKeyboardButton("📡 Scan Networks", callback_data='scan_networks')],
        [InlineKeyboardButton("📊 System Info", callback_data='system_info')],
        [
            InlineKeyboardButton("🎵 Media Play", callback_data='media_play'),
            InlineKeyboardButton("⏸ Media Pause", callback_data='media_pause'),
        ],
        [
            InlineKeyboardButton("⏩ Media Next", callback_data='media_next'),
            InlineKeyboardButton("⏪ Media Previous", callback_data='media_previous'),
        ],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(welcome_text, reply_markup=reply_markup)

# 🆘 Help Command
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_authorized(update):
        return

    help_text = """
    🤖 PC Control Bot Help 🎮

    Available Commands:
    /start - Start the bot and show the main menu.
    /help - Show this help message.
    /zipfolder <path> - Zip a folder and send it.
    /scannetworks - Scan available Wi-Fi networks (Linux only).
    /systeminfo - Get system information.
    /cmd <command> - Execute a terminal command.
    /media <play|pause|next|previous> - Control media playback.
    /launch <app> - Launch an application (e.g., firefox, obs, obsidian).

    Inline Buttons:
    💾 RAM Usage - Show RAM usage.
    🌡 CPU Temperature - Show CPU temperature.
    📸 Take Screenshot - Take a screenshot.
    📂 Zip Folder - Zip a folder.
    📡 Scan Networks - Scan Wi-Fi networks.
    📊 System Info - Get system information.
    🎵 Media Play/Pause/Next/Previous - Control media playback.
    """

    await update.message.reply_text(help_text)

# 📂 Zip Folder Command
async def zip_folder(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_authorized(update):
        return

    # Check if the update is from a callback query or a command
    if update.callback_query:
        await update.callback_query.message.reply_text("❌ Please provide a folder path. Example: /zipfolder /path/to/folder")
        return
    elif not context.args:
        await update.message.reply_text("❌ Please provide a folder path. Example: /zipfolder /path/to/folder")
        return

    folder = ' '.join(context.args)
    folder = os.path.expanduser(folder)
    folder = os.path.abspath(folder)

    if not os.path.exists(folder):
        await update.message.reply_text("❌ Error: Folder does not exist! Please check the path.")
        return
    elif not os.path.isdir(folder):
        await update.message.reply_text("❌ Error: The provided path is not a directory!")
        return

    zip_name = os.path.join(os.path.dirname(folder), f"{os.path.basename(folder)}.zip")
    with zipfile.ZipFile(zip_name, "w", zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(folder):
            for file in files:
                full_path = os.path.join(root, file)
                arcname = os.path.relpath(full_path, folder)
                zipf.write(full_path, arcname)
    
    await update.message.reply_text(f"✅ Folder zipped successfully: {zip_name}")
    await context.bot.send_document(chat_id=update.effective_chat.id, document=open(zip_name, "rb"))

# 📡 Scan Networks Command (Linux Compatibility)
async def scan_networks(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_authorized(update):
        return

    try:
        # Linux alternative to scan Wi-Fi networks
        result = subprocess.check_output("nmcli dev wifi list", shell=True).decode("utf-8")
    except Exception as e:
        result = f"❌ Error scanning networks: {str(e)}"
    
    with open("networks.txt", "w") as f:
        f.write(result)

    # Check if the update is from a callback query or a command
    if update.callback_query:
        await update.callback_query.message.reply_text("📡 Networks scanned. Sending the file...")
        await context.bot.send_document(chat_id=update.effective_chat.id, document=open("networks.txt", "rb"))
    else:
        await update.message.reply_text("📡 Networks scanned. Sending the file...")
        await context.bot.send_document(chat_id=update.effective_chat.id, document=open("networks.txt", "rb"))

# 📊 Get System Info Command
async def get_system_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_authorized(update):
        return

    system_info = {
        "OS": platform.system(),
        "OS Version": platform.version(),
        "OS Release": platform.release(),
        "Architecture": platform.architecture(),
        "Processor": platform.processor(),
        "CPU Cores": psutil.cpu_count(logical=False),
        "Logical CPUs": psutil.cpu_count(logical=True),
        "RAM": f"{round(psutil.virtual_memory().total / (1024 ** 3))} GB",
        "Disks": [{disk.device: f"{disk.fstype}, {disk.opts}" for disk in psutil.disk_partitions()}],
        "Network Name": socket.gethostname(),
    }

    with open("system_info.txt", "w") as f:
        f.write(json.dumps(system_info, indent=4))

    # Check if the update is from a callback query or a command
    if update.callback_query:
        await update.callback_query.message.reply_text("📊 System info gathered. Sending the file...")
        await context.bot.send_document(chat_id=update.effective_chat.id, document=open("system_info.txt", "rb"))
    else:
        await update.message.reply_text("📊 System info gathered. Sending the file...")
        await context.bot.send_document(chat_id=update.effective_chat.id, document=open("system_info.txt", "rb"))

# 🎵 Media Control Commands
async def media_control(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_authorized(update):
        return

    # Get the command from context.args or callback data
    if context.args:
        command = context.args[0].lower()
    elif update.callback_query:
        command = update.callback_query.data.replace("media_", "")
    else:
        await update.message.reply_text("❌ Unknown media control command. Use play, pause, next, or previous.")
        return

    if command == "play":
        subprocess.call(["playerctl", "play"])
        await update.message.reply_text("▶️ Media playback started.")
    elif command == "pause":
        subprocess.call(["playerctl", "pause"])
        await update.message.reply_text("⏸ Media playback paused.")
    elif command == "next":
        subprocess.call(["playerctl", "next"])
        await update.message.reply_text("⏩ Skipped to next track.")
    elif command == "previous":
        subprocess.call(["playerctl", "previous"])
        await update.message.reply_text("⏪ Returned to previous track.")
    else:
        await update.message.reply_text("❌ Unknown media control command. Use play, pause, next, or previous.")

# 🌡 CPU Temperature Command
async def cpu_temp(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_authorized(update):
        return

    try:
        # Example for Linux using the 'sensors' command
        temp_output = subprocess.check_output("sensors", shell=True).decode("utf-8")
        # Extract CPU temperature (this is a simple example, adjust as needed)
        cpu_temp = "🌡 CPU Temperature:\n" + temp_output
    except Exception as e:
        cpu_temp = f"❌ Error retrieving CPU temperature: {str(e)}"

    # Check if the update is from a callback query or a command
    if update.callback_query:
        await update.callback_query.message.reply_text(cpu_temp)
    else:
        await update.message.reply_text(cpu_temp)

# 💾 RAM Usage Command
async def ram_usage(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_authorized(update):
        return

    ram_info = psutil.virtual_memory()
    ram_usage_text = f"💾 RAM Usage:\nTotal: {round(ram_info.total / (1024 ** 3), 2)} GB\nUsed: {round(ram_info.used / (1024 ** 3), 2)} GB\nFree: {round(ram_info.free / (1024 ** 3), 2)} GB"

    # Check if the update is from a callback query or a command
    if update.callback_query:
        await update.callback_query.message.reply_text(ram_usage_text)
    else:
        await update.message.reply_text(ram_usage_text)

# 📸 Take Screenshot Command
async def take_screenshot(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_authorized(update):
        return

    try:
        # Take a screenshot
        screenshot = pyautogui.screenshot()
        screenshot_path = "screenshot.png"
        screenshot.save(screenshot_path)

        # Check if the update is from a callback query or a command
        if update.callback_query:
            await update.callback_query.message.reply_text("📸 Screenshot taken. Sending the file...")
            await context.bot.send_photo(chat_id=update.effective_chat.id, photo=open(screenshot_path, "rb"))
        else:
            await update.message.reply_text("📸 Screenshot taken. Sending the file...")
            await context.bot.send_photo(chat_id=update.effective_chat.id, photo=open(screenshot_path, "rb"))
    except Exception as e:
        # Check if the update is from a callback query or a command
        if update.callback_query:
            await update.callback_query.message.reply_text(f"❌ Error taking screenshot: {str(e)}")
        else:
            await update.message.reply_text(f"❌ Error taking screenshot: {str(e)}")

# 🚀 Launch App Command
async def launch_app(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_authorized(update):
        return

    if not context.args:
        await update.message.reply_text("❌ Please provide an app name. Example: /launch firefox")
        return

    app_name = context.args[0].lower()
    if app_name not in APPS:
        await update.message.reply_text(f"❌ App '{app_name}' not found in the app list.")
        return

    try:
        subprocess.Popen([APPS[app_name]])
        await update.message.reply_text(f"🚀 Launched {app_name} successfully!")
    except Exception as e:
        await update.message.reply_text(f"❌ Error launching {app_name}: {str(e)}")

# ⌨ Execute Custom Shell Commands
async def execute_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_authorized(update):
        return

    if not context.args:
        await update.message.reply_text("❌ Please provide a command. Example: /cmd ls")
        return

    command = ' '.join(context.args)

    try:
        # Execute the command and capture the output
        output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT).decode("utf-8")
    except subprocess.CalledProcessError as e:
        # If the command fails, capture the error output
        output = f"❌ Command failed with error:\n{e.output.decode('utf-8')}"
    except Exception as e:
        # Handle any other exceptions
        output = f"❌ An error occurred: {str(e)}"

    # Send the output back to the user
    await update.message.reply_text(f"🖥 Command Output:\n```{output}```", parse_mode="Markdown")

# 🚀 Main Function
def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("zipfolder", zip_folder))
    app.add_handler(CommandHandler("scannetworks", scan_networks))
    app.add_handler(CommandHandler("systeminfo", get_system_info))
    app.add_handler(CommandHandler("cmd", execute_command))
    app.add_handler(CommandHandler("media", media_control))
    app.add_handler(CommandHandler("launch", launch_app))  # Add this line

    # Inline buttons for quick actions
    app.add_handler(CallbackQueryHandler(scan_networks, pattern='^scan_networks$'))
    app.add_handler(CallbackQueryHandler(zip_folder, pattern='^zip_folder$'))
    app.add_handler(CallbackQueryHandler(get_system_info, pattern='^system_info$'))
    app.add_handler(CallbackQueryHandler(cpu_temp, pattern='^cpu_temp$'))
    app.add_handler(CallbackQueryHandler(ram_usage, pattern='^ram_usage$'))
    app.add_handler(CallbackQueryHandler(take_screenshot, pattern='^take_screenshot$'))
    app.add_handler(CallbackQueryHandler(media_control, pattern='^media_'))  # Add this line

    app.run_polling()

if __name__ == "__main__":
    main()

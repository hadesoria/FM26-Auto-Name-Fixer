# ⚽ Football Manager 2026 Auto Name Fixer

A lightweight, fully automated tool that applies the "Real Name Fix" for Football Manager 2026. Tired of manually hunting down `database` directories, digging into `db` folders, deleting fake license files (`.lnc`, `.edt`, `.dbc`), and repeatedly copying name fix files every time there is a game update? 

This application automates the entire process in one click!

## ✨ Features

- **One-Click Installation**: Select your Name Fix file, and the tool does the rest.
- **Universal Store Support**: Automatically scans and detects FM 2026 installations whether from **Steam**, **Epic Games**, or **Xbox Game Pass** (deep UWP `Content` folders supported!).
- **ZIP or Folder Input**: You don't even need to extract your downloaded Name Fix. Just point the tool directly to the `.zip` file (like the one from Sortitoutsi), and it handles extraction automatically.
- **Smart Memory**: Remembers your directories perfectly. The next time a game update comes out, you literally just open the app and click "APPLY FIX". Your original paths are saved locally.
- **Complete Cleanup**: Safely wipes the `.lnc`, `.edt`, and `.dbc` data from **all** database versions (2300, 2400, 2500, 2600) to ensure fake names do not leak through, then securely copies the real name fix files.
- **Editor Data Management**: Identifies and automatically relocates `.fmf` files straight to your `Documents/Sports Interactive/Football Manager 2026/editor data` directory.

## 🚀 Usage (For Users)

If you just want to use the tool, you don't need Python or any coding knowledge!

1. Download the latest `FM26_Auto_Name_Fixer` from the [Releases](#) tab.
2. Download your preferred FM26 Real Name Fix (e.g. from Sortitoutsi or FMScout).
3. Double-click the `.exe` file.
4. If it didn't find them automatically, ensure the Game Path and Documents Path are correct.
5. Click **Select ZIP** (or Folder) and point it to the Name Fix you downloaded.
6. Click **APPLY FIX**.

Done! Start your game to enjoy real club names, real competitions, and real staff.

## 💻 Developer Guide

If you'd like to build the project from source or contribute to the application:

### Requirements

- **Python 3.10+**

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/fm26-auto-name-fixer.git
   cd fm26-auto-name-fixer
   ```
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
   *(Note: The main requirement is `customtkinter`)*

3. Run the GUI:
   ```bash
   python main.py
   ```

### Building the Executable

This project uses `pyinstaller` to create a standalone binary.

```bash
pip install pyinstaller
pyinstaller --noconsole --onefile main.py --name FM26_Auto_Name_Fixer
```
The compiled executable will be located in the `/dist` directory.

## ⚠️ Disclaimer

This tool is a community project and is not affiliated with Sports Interactive, SEGA, or any other official Football Manager entity. Please ensure you always download your Name Fix data from trusted community sites.

## 🤝 Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

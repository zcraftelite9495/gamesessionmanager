# --------------------------------------------------------------------------------
# Z's Game Session Manager
# --------------------------------------------------------------------------------
# Created, Designed, and Programmed by ZcraftElite
# -----------------------------------------------------

# -------------------------------------
# Version Information
# -------------------------------------

gsmversion = "2.1.0"
gsmstage = "beta"

# -------------------------------------
# Library Checker
# -------------------------------------

# Function to check if the libraries required for this project are installed
def checkLibs():
    import importlib.util

    # List of libraries to check
    required_libraries = [
        'os',
        'platform',     
        'sys',
        'subprocess',
        'pathlib',
        'shutil',
        'argparse',
        'datetime',
        'gspread',
        'oauth2client.client',
        'oauth2client.file',
        'oauth2client.tools',
        'webbrowser',
        'flask',
        'PyQt5.QtGui',
        'PyQt5.QtWidgets',
        'PyQt5.QtCore',
        'PyQt5.QtWebEngineWidgets',
        'pygame',
        'pygetwindow'
    ]

    missing_libraries = []

    # Check if libraries are importable
    for lib in required_libraries:
        if importlib.util.find_spec(lib) is None:
            missing_libraries.append(lib)

    if missing_libraries:
        print("The following libraries are missing or not installable:")
        for missing_lib in missing_libraries:
            print(f"- {missing_lib}")
        quit()

# -------------------------------------
# Important OS Functions
# -------------------------------------

def setupWindowsAppID():
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID('zcraftelite.gamesessionmanager.main.latest')
    lpBuffer = wintypes.LPWSTR()
    AppUserModelID = ctypes.windll.shell32.GetCurrentProcessExplicitAppUserModelID
    AppUserModelID(ctypes.cast(ctypes.byref(lpBuffer), wintypes.LPWSTR))
    appid = lpBuffer.value
    ctypes.windll.kernel32.LocalFree(lpBuffer)
    if appid is not None:
        print("Successfully Set Windows APPID: " + appid)

def setupEnvironmentVariables():
    os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "1"

# -------------------------------------
# Imports
# -------------------------------------

checkLibs()
try:
    import os, sys, argparse, platform, subprocess, threading, signal, requests, time
    import pygetwindow as gw
    termWindow = gw.getActiveWindow()
    termWindow.minimize()

    setupEnvironmentVariables()

    import ctypes
    from ctypes import wintypes

    from pathlib import Path
    from datetime import datetime, timedelta

    import gspread
    from oauth2client.client import flow_from_clientsecrets
    from oauth2client.file import Storage
    from oauth2client.tools import run_flow

    import webbrowser

    from flask import Flask, session, render_template, request, redirect, url_for, flash, send_from_directory, jsonify

    from plyer import notification

    import pygame
    from PyQt5.QtWidgets import QApplication, QDialog, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QMainWindow, QWidget, QSystemTrayIcon, QMenu, QAction, QWidgetAction
    from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineSettings
    from PyQt5.QtCore import Qt, QUrl, QRect, QTimer, QSize
    from PyQt5.QtGui import QIcon, QPalette, QColor, QFont, QPixmap, QImage, QPainter
except ImportError as e:
    raise ImportError(f"One or more required libraries failed to load: {e}")

# -------------------------------------
# Base Functions
# -------------------------------------

within_other_function = 0

def format_text(text, alignment):
    # Get the current terminal width
    try:
        width = os.get_terminal_size().columns
    except OSError:
        # Fallback width in case getting terminal size fails (e.g., in non-terminal environments)
        width = 80

    if alignment == 'left':
        return text.ljust(width)
    elif alignment == 'right':
        return text.rjust(width)
    elif alignment == 'center':
        return text.center(width)
    else:
        raise ValueError("Alignment must be 'left', 'right', or 'center'.")

def format_texts(*texts_with_alignments):
    # Get the current terminal width
    try:
        width = os.get_terminal_size().columns
    except OSError:
        width = 80  # Fallback width

    combined_text = ""
    for text, alignment in texts_with_alignments:
        if alignment == 'left':
            formatted_text = text.ljust(width // len(texts_with_alignments))
        elif alignment == 'right':
            formatted_text = text.rjust(width // len(texts_with_alignments))
        elif alignment == 'center':
            formatted_text = text.center(width // len(texts_with_alignments))
        else:
            raise ValueError("Alignment must be 'left', 'right', or 'center'.")

            combined_text += formatted_text
    
    return combined_text

# Function to clear the terminal screen
def clear_screen():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

# Function that prints a divider across the screen width
def screen_line():
    print("-" * os.get_terminal_size().columns)  # Line across the terminal width

# Predefined function to create a header for the terminal screens
def main_title(title_heading):
    print(format_texts(("Z's Game Session Manager", 'left'), (gsmversion, 'right')))
    print("Created, Designed, and Programmed by ZcraftElite")
    screen_line()
    print(format_text(title_heading, 'center'))
    screen_line()
    prerelease_warning(gsmstage)
    print("")

# Function to show a warning when using a alpha/beta version of the terminal app
def prerelease_warning(stage):
    if stage == "beta":
        print(format_texts(("Warning: You are using a Beta version of Game Session Manager.", 'center')))
        print(format_texts(("Features are eperimental and some bugs are expected.", 'center')))
        screen_line()
        return True
    elif stage == "alpha":
        print(format_texts(("Warning: You are using a Alpha version of Game Session Manager.", 'center')))
        print(format_texts(("Features are highly experimental and lots of bugs are excpected.", 'center')))
        screen_line()
        return True

def request_admin_permissions():
    """Request admin privileges for directory creation if needed."""
    if platform.system() == 'Windows':
        # On Windows, use 'runas' to request admin privileges
        subprocess.run(['runas', '/user:Administrator', sys.executable] + sys.argv)
    elif platform.system() == 'Linux' or platform.system() == 'Darwin':  # Darwin is for macOS
        # On Linux/macOS, use 'sudo' to request admin privileges
        subprocess.run(['sudo', sys.executable] + sys.argv)
    else:
        raise EnvironmentError("Unsupported OS: " + platform.system())

# -------------------------------------
# Configuration Files Setup
# -------------------------------------

class configurationSetup:
    def __init__(self):
        self.executabledir = os.path.dirname(os.path.abspath(__file__))
        self.executable = os.path.join(self.executabledir, "GameSessionManager.py")
        self.dir = os.path.join(self.executabledir, "config") # Sets the configuration path
        self.asset_dir = os.path.join(self.executabledir, "assets")
        self.sheet_id_file = os.path.join(self.dir, "sheetid.txt") # Sets the path for the sheetid.txt file
        self.token_file = os.path.join(self.dir, "token.json") # Sets the path for the token.json file
        self.credentials_file = os.path.join(self.dir, "credentials.json") # Sets the path for the credentials.json file
        
    def getAsset(self, asset):
        return os.path.join(self.asset_dir, asset)

config = configurationSetup() # Sets the config variable to the class for easier importing throughout the code

# -------------------------------------
# Google Sheets API Functions
# -------------------------------------

# Sets the configuration directory before loading credentials
configurationSetup()

# Define the scope for Google Sheets API
scope = ["https://www.googleapis.com/auth/spreadsheets"]

# Check and load the sheet ID from the sheetid.txt file
sheet_id = None
if os.path.exists(config.sheet_id_file):
    with open(config.sheet_id_file, 'r') as file:
        sheet_id = file.readline().strip()  # Read the first line and remove any trailing newline or spaces

# Load credentials
def get_credentials():
    creds = None
    if os.path.exists(config.token_file):
        creds = Storage(config.token_file).get()
    if not creds or creds.invalid:
        flow = flow_from_clientsecrets(config.credentials_file, scope)
        creds = run_flow(flow, Storage(config.token_file))
    return creds

# Authorize and connect to Google Sheets
creds = get_credentials()
client = gspread.authorize(creds)

# Open the Google Sheets by ID
spreadsheet = client.open_by_key(sheet_id)
log_sheet = client.open_by_key(sheet_id).worksheet("Game Sessions")
totals_sheet = client.open_by_key(sheet_id).worksheet("Game Totals (All Time)")
gamecover_sheet = client.open_by_key(sheet_id).worksheet("Game Covers")

# Function to get the developer name based on the game name
def get_developer_name(game_name):
    # Get all values from the Game Totals sheet
    totals_data = totals_sheet.get_all_values()
    
    # Search for the game name in column F and get the developer name from column G
    for row in totals_data:
        if row[5] == game_name:  # Column F is index 5
            return row[6]  # Column G is index 6 (developer name)
    
    return ""  # Return empty string if not found

def longest_consecutive_days(sheet, game_name):
    # Create a dictionary to store the dates on which the game was played
    game_dates = set()
    
    # Iterate through the sheet and collect the dates for the specified game
    for row in sheet:
        if row[1] == game_name:  # Check if the game name matches
            try:
                # Convert the date from MM/DD/YYYY format to a datetime object
                game_date = datetime.strptime(row[0], "%m/%d/%Y").date()
                game_dates.add(game_date)
            except ValueError:
                continue  # If there's an error in date format, skip that row
    
    # If no sessions for the game are found
    if not game_dates:
        return 0
    
    # Sort the dates in ascending order
    sorted_dates = sorted(game_dates)
    
    # Find the longest streak of consecutive days
    max_streak = 1
    current_streak = 1
    for i in range(1, len(sorted_dates)):
        # Check if the current date is the day after the previous date
        if (sorted_dates[i] - sorted_dates[i - 1]).days == 1:
            current_streak += 1
        else:
            # If not consecutive, reset the current streak
            current_streak = 1
        
        # Update the max streak if the current streak is longer
        max_streak = max(max_streak, current_streak)
    
    return max_streak


# Formats the time difference for the last played date
def format_time_difference(last_played_date_str):
    # Convert string to datetime
    try:
        last_played_date = datetime.strptime(last_played_date_str, '%m/%d/%Y %I:%M:%S %p')
    except:
        return "Never Played"

    now = datetime.now()
    time_diff = now - last_played_date

    # Calculate the difference in seconds, minutes, etc.
    seconds = time_diff.total_seconds()
    if seconds < 60:
        count = int(seconds)
        return f"{count} second{'s' if count != 1 else ''} ago"
    elif seconds < 3600:
        minutes = seconds // 60
        count = int(minutes)
        return f"{count} minute{'s' if count != 1 else ''} ago"
    elif seconds < 86400:
        hours = seconds // 3600
        count = int(hours)
        return f"{count} hour{'s' if count != 1 else ''} ago"
    elif seconds < 604800:
        days = seconds // 86400
        count = int(days)
        return f"{count} day{'s' if count != 1 else ''} ago"
    elif seconds < 2592000:  # Approximate weeks
        weeks = seconds // 604800
        count = int(weeks)
        return f"{count} week{'s' if count != 1 else ''} ago"
    elif seconds < 31536000:  # Approximate months
        months = seconds // 2592000
        count = int(months)
        return f"{count} month{'s' if count != 1 else ''} ago"
    else:
        years = seconds // 31536000
        count = int(years)
        return f"{count} year{'s' if count != 1 else ''} ago"

# Get today's date in MM/DD/YYYY format
def date_to_gs_format(dt):
    # Base date for Google Sheets
    base_date = datetime(1899, 12, 30)
    # Calculate the difference in days
    delta = dt.date() - base_date.date()  # Only get the date part
    # Convert to serial number format
    serial_number = delta.days  # Only the integer part for the date
    return serial_number

def time_to_gs_format(time_str):
    try:
        # Use strptime to parse the input and validate the format
        time_obj = datetime.strptime(time_str, "%I:%M:%S %p")  # e.g., "03:45:30 PM"
        # Convert time to Google Sheets format (fraction of a day)
        # Google Sheets considers time as a fraction of a day, so divide by 24
        return time_obj.hour / 24 + time_obj.minute / 1440 + time_obj.second / 86400
    except ValueError:
        print("Invalid time format. Please use 'hh:mm:ss AM/PM' format.")

def add_ordinal_suffix(rank):
    if 10 <= rank % 100 <= 20:  # Special case for teens
        suffix = "th"
    else:
        suffix = {1: "st", 2: "nd", 3: "rd"}.get(rank % 10, "th")
    print("Ordinal Added")
    return f"{rank}{suffix}"

def clear_last_row():
    # Get the total number of rows in the sheet
    last_row = sheet.row_count

    # Get all values and find the last row that is empty
    values = sheet.get_all_values()
    last_non_empty_row = len(values)

    # Clear the last empty row
    if last_row > last_non_empty_row:
        sheet.clear('A' + str(last_non_empty_row + 1) + ':Z' + str(last_row))  # Clear columns from A to Z (adjust as needed)

    del values

# Format columns in the Google Sheets
def format_columns():
    batch_update_request = {
        "requests": [
            # Format elapsed time column in "Game Sessions"
            {
                "repeatCell": {
                    "range": {
                        "sheetId": log_sheet.id,
                        "startRowIndex": 0,
                        "endRowIndex": log_sheet.row_count,
                        "startColumnIndex": 6,  # Column G
                        "endColumnIndex": 7      # One column wide
                    },
                    "cell": {
                        "userEnteredFormat": {
                            "numberFormat": {
                                "type": "NUMBER",
                                "pattern": "[hh]:mm:ss"
                            }
                        }
                    },
                    "fields": "userEnteredFormat.numberFormat"
                }
            },
            # Format start and end time columns in "Game Sessions"
            {
                "repeatCell": {
                    "range": {
                        "sheetId": log_sheet.id,
                        "startRowIndex": 0,
                        "endRowIndex": log_sheet.row_count,
                        "startColumnIndex": 4,  # Column E
                        "endColumnIndex": 6      # Column F
                    },
                    "cell": {
                        "userEnteredFormat": {
                            "numberFormat": {
                                "type": "TIME",
                                "pattern": "hh:mm:ss AM/PM"
                            }
                        }
                    },
                    "fields": "userEnteredFormat.numberFormat"
                }
            },
            # Format date column in "Game Sessions"
            {
                "repeatCell": {
                    "range": {
                        "sheetId": log_sheet.id,
                        "startRowIndex": 0,
                        "endRowIndex": log_sheet.row_count,
                        "startColumnIndex": 0,  # Column A
                        "endColumnIndex": 1
                    },
                    "cell": {
                        "userEnteredFormat": {
                            "numberFormat": {
                                "type": "DATE",
                                "pattern": "MM/dd/yyyy"
                            }
                        }
                    },
                    "fields": "userEnteredFormat.numberFormat"
                }
            },
            # Format price column in "Game Sessions" (Column D)
            {
                "repeatCell": {
                    "range": {
                        "sheetId": log_sheet.id,
                        "startRowIndex": 0,
                        "endRowIndex": log_sheet.row_count,
                        "startColumnIndex": 3,  # Column D
                        "endColumnIndex": 4
                    },
                    "cell": {
                        "userEnteredFormat": {
                            "numberFormat": {
                                "type": "CURRENCY",
                                "pattern": "$#,##0.00"
                            }
                        }
                    },
                    "fields": "userEnteredFormat.numberFormat"
                }
            }
        ]
    }

    # Use the batch_update method on the spreadsheet object
    spreadsheet.batch_update(batch_update_request)

# -------------------------------------
# Audio Support
# -------------------------------------

class AudioSystem():
    def __init__(self):
        self.isInit = False

    # Initializes the pygame music library
    def init(self):
        if not self.isInit:
            pygame.mixer.init()
            self.isInit = True

    def play(self, filename):
        self.init()
        self.sound = pygame.mixer.Sound(config.getAsset(filename))
        self.sound.play()

    # Plays an asset on loop
    def playLoop(self, filename):
        self.init()
        pygame.mixer.music.load(config.getAsset(filename))
        pygame.mixer.music.play(-1, 0.0)

    # Stops playing current asset
    def stop(self):
        self.init()
        pygame.mixer.music.stop()

audioSystem = AudioSystem()

# -------------------------------------
# WebApp Code
# -------------------------------------

class WebWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        # Set the window title and icon
        self.setWindowTitle("Z's Game Session Manager")
        self.setWindowIcon(QIcon(config.getAsset("gameControllerIcon-Pink.png")))

        # Create a QWebEngineView and enable the changing of settings
        self.webview = QWebEngineView()
        webviewSettings = self.webview.settings()
        webviewSettings.setAttribute(QWebEngineSettings.ShowScrollBars, False)

        # Sets & Tracks URL changes for the app and then loads it
        self.appURL = f"http://{WebserverHostedIP}:{WebserverPort}"
        self.webview.setUrl(QUrl.fromUserInput(self.appURL))
        self.webview.urlChanged.connect(self.checkUrl)

        # Set up a central widget with no margins
        central_widget = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)  # Remove margins
        layout.addWidget(self.webview)
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        # Resize the window to 90% of the screen size
        screen = QApplication.primaryScreen()
        screen_size = screen.availableGeometry()
        width = int(screen_size.width() * 0.9)
        height = int(screen_size.height() * 0.9)
        self.resize(width, height)

        # Move the window to the center of the screen
        center_x = screen_size.left() + (screen_size.width() - width) // 2
        center_y = screen_size.top() + (screen_size.height() - height) // 2
        self.move(center_x, center_y)

        # Timer for startup sound
        self.startupSoundTimer1 = QTimer(self)
        self.startupSoundTimer1.setSingleShot(True)
        self.startupSoundTimer1.timeout.connect(self.startupSound)
        self.startupSoundTimer1.start(500)

        # Add a button in the bottom-right corner
        self.addReturnToSiteButton()

        # Create the system tray icon
        self.setupTrayIcon()

        # Show on screen
        self.raise_()

    def addReturnToSiteButton(self):
        # Create the button
        self.button = QPushButton("Back to Site", self)
        self.button.setStyleSheet("""
        QPushButton {
            background-color: #FF69B4;
            border: none;
            border-radius: 15px;
            color: white;
            padding: 10px;
            font-size: 14px;
            font-weight: bold;
        }
        QPushButton:hover {
            background-color: #FF1493;
        }
        """)
        self.button.setFixedSize(100, 40)
        self.button.clicked.connect(lambda: self.webview.setUrl(QUrl.fromUserInput(self.appURL)))

        self.button.setVisible(False)

        # Define spacing from the edges
        margin = 20

        # Position the button slightly spaced from the bottom-right corner
        self.button.move(self.width() - self.button.width() - margin, self.height() - self.button.height() - margin)
        self.button.setParent(self)

        # Make the button stay on top of the webview
        self.button.raise_()

        # Adjust the button's position when the window is resized
        self.resizeEvent = self.updateButtonPosition

    def updateButtonPosition(self, event):
        # Define spacing from the edges
        margin = 20
        self.button.move(self.width() - self.button.width() - margin, self.height() - self.button.height() - margin)

    def checkUrl(self, url):
        # Extract the base URL (scheme + host)
        base_url = QUrl(self.appURL)
        
        # Compare the host and scheme of the current URL with the base URL
        if url.scheme() == base_url.scheme() and url.host() == base_url.host():
            self.button.setVisible(False)  # Hide the button if it's the same base URL
        else:
            self.button.setVisible(True)   # Show the button for different URLs

    def setupTrayIcon(self):
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QIcon(config.getAsset("gameControllerIcon-White.png")))  # Icon
        self.tray_icon.setToolTip(f"Z's Game Session Manager - v{gsmversion}")  # Tooltip

        trayMenu = QMenu(self)  # Sets up the menu itself

        # Apply CSS to the menu
        trayMenu.setStyleSheet("""
            QMenu {
                background-color: #2c2f33;
                border: 1px solid #4a4a4a;
                color: white;
                font: bold 12px 'Segoe UI', sans-serif;
                border-radius: 10px;
                padding: 5px;
            }

            QMenu::item {
                padding: 10px 20px;
                background-color: transparent;
                border-radius: 5px;
            }

            QMenu::item:disabled {
                color: #8a8a8a;
                background-color: transparent;
            }

            QMenu::item:selected:enabled {
                background-color: #d47799;
                color: white;
                border-radius: 5px;
            }

            QMenu::separator {
                height: 2px;
                background-color: #4a4a4a;
                margin: 5px 0;
            }

            QMenu::icon {
                padding-right: 10px;
            }

            QPushButton {
                padding: 5px;
                background-color: transparent;
                border: none;
            }

            QPushButton:hover {
                background-color: #d47799;
                color: white;
                border-radius: 5px;
            }

            QLabel {
                color: white;
                font: bold 12px 'Segoe UI', sans-serif;
            }

            [class="titleLabel"] {
                color: #8a8a8a;
                background-color: transparent;
            }
        """)

        # Title Widget Setup
        titleWidget = QWidget(self)
        titleLayout = QVBoxLayout(titleWidget)
        titleLayout.setAlignment(Qt.AlignCenter)  # Center-align the content

        # Title Label
        titleLabel = QLabel(f"Z's Game Session Manager v{gsmversion}", titleWidget)
        titleLabel.setAlignment(Qt.AlignCenter)  # Center-align text
        titleLabel.setProperty("class", "titleLabel")
        titleLabel2 = QLabel(f"{gsmclientType}", titleWidget)
        titleLabel2.setAlignment(Qt.AlignCenter)
        titleLabel2.setProperty("class", "titleLabel")
        titleLayout.addWidget(titleLabel)
        titleLayout.addWidget(titleLabel2)

        # Add Title Widget to Tray Menu
        titleWidgetAction = QWidgetAction(self)
        titleWidgetAction.setDefaultWidget(titleWidget)
        trayMenu.addAction(titleWidgetAction)

        trayMenu.addSeparator()  # Separator

        # Button Widget Setup
        buttonWidget = QWidget(self)
        buttonLayout = QVBoxLayout(buttonWidget)  # Use QVBoxLayout to stack the label and buttons vertically
        buttonLayout.setAlignment(Qt.AlignCenter)  # Center the content

        # Add Browsing Controls label
        label = QLabel("Browsing Controls", buttonWidget)
        label.setAlignment(Qt.AlignCenter)  # Center align the label text
        buttonLayout.addWidget(label)

        # Buttons Layout
        buttonsLayout = QHBoxLayout()  # Separate layout for buttons
        buttonsLayout.setAlignment(Qt.AlignCenter)  # Center the buttons horizontally

        # Home Button
        trayIcon_homeButton = QPushButton()
        trayIcon_homeButton.setToolTip("Home")
        trayIcon_homeButton.setIcon(QIcon(config.getAsset("trayMenu/homeIcon.svg")))
        trayIcon_homeButton.setIconSize(QSize(20, 20))
        trayIcon_homeButton.setFlat(True)
        trayIcon_homeButton.clicked.connect(lambda: self.webview.setUrl(QUrl.fromUserInput(self.appURL)))
        buttonsLayout.addWidget(trayIcon_homeButton)

        # Refresh Button
        trayIcon_refreshButton = QPushButton()
        trayIcon_refreshButton.setToolTip("Refresh")
        trayIcon_refreshButton.setIcon(QIcon(config.getAsset("trayMenu/refreshIcon.svg")))
        trayIcon_refreshButton.setIconSize(QSize(20, 20))
        trayIcon_refreshButton.setFlat(True)
        trayIcon_refreshButton.clicked.connect(lambda: self.webview.reload())
        buttonsLayout.addWidget(trayIcon_refreshButton)

        # Add the buttons layout to the main layout
        buttonLayout.addLayout(buttonsLayout)

        # Button Widget
        trayMenu_action = QWidgetAction(self)
        trayMenu_action.setDefaultWidget(buttonWidget)
        trayMenu.addAction(trayMenu_action)

        trayMenu.addSeparator()  # Separator

        # Add "About" Action
        aboutAction = QAction("About", self)
        aboutAction.triggered.connect(self.showAboutDialog)
        aboutAction.setIcon(QIcon(config.getAsset("trayMenu/aboutIcon.svg")))
        trayMenu.addAction(aboutAction)

        # Exit Button
        trayIcon_exitButton = QAction("Exit", self)
        trayIcon_exitButton.triggered.connect(QApplication.instance().quit)
        trayIcon_exitButton.setIcon(QIcon(config.getAsset("trayMenu/exitIcon.svg")))
        trayMenu.addAction(trayIcon_exitButton)

        self.tray_icon.setContextMenu(trayMenu)
        self.tray_icon.show()

    def showAboutDialog(self):
        aboutDialog = QDialog(self)
        aboutDialog.setWindowTitle("About Z's Game Session Manager")
        aboutDialog.setStyleSheet("""
            QDialog {
                background-color: #2c2f33;
                color: white;
                font: bold 12px 'Segoe UI', sans-serif;
                border-radius: 10px;
            }
            QLabel {
                color: white;
                padding: 10px;
            }
            QPushButton {
                background-color: #d47799;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 5px 15px;
                font: bold 12px 'Segoe UI', sans-serif;
            }
            QPushButton:hover {
                background-color: #a34d73;
            }
        """)

        layout = QVBoxLayout(aboutDialog)
        aboutText = QLabel(
            "Z's Game Session Manager\n"
            f"Version: {gsmversion}\n"
            f"Client Type: {gsmclientType}\n"
            "Developed by ZenaComerford/ZcraftElite."
        )
        aboutText.setAlignment(Qt.AlignLeft)
        layout.addWidget(aboutText)

        closeButton = QPushButton("Close")
        closeButton.clicked.connect(aboutDialog.accept)
        layout.addWidget(closeButton)

        aboutDialog.exec_()

    def eventFilter(self, source, event):
        if isinstance(source, QMenu):
            # If the event is a mouse press and it's outside the menu, close the menu
            if event.type() == QEvent.MouseButtonPress:
                if not source.rect().contains(event.pos()):
                    source.close()  # Close the menu if clicked outside
        return super().eventFilter(source, event)

    def setEmojiImage(self, emoji):
        image = QImage(70, 70, QImage.Format_ARGB32)
        image.fill(QColor(255, 255, 255, 0))  # Transparent background

        # Use QPainter to draw the emoji onto the image
        painter = QPainter(image)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setFont(QFont("Arial", 40))  # You can adjust the font size here
        painter.drawText(image.rect(), Qt.AlignCenter, emoji)
        painter.end()

        pixmap = QPixmap.fromImage(image)

        return pixmap

    def closeEvent(self, event):
        # Stop the Flask web server when the window is closed
        os.kill(os.getpid(), signal.SIGINT)  # This sends a SIGINT signal to terminate the Flask server
        event.accept()

    def startupSound(self):
        audioSystem.play("nt5.ogv")


# Run the application
def runWebApp():
    app = QApplication(sys.argv)
    app.setApplicationName("Z's Game Session manager")
    app.setOrganizationName("zcraftelite")
    app.setApplicationVersion(gsmversion)
    window = WebWindow()
    window.show()
    window.raise_()
    sys.exit(app.exec_())

# -------------------------------------
# Launcher Code
# -------------------------------------

# Defines the function that launches the dialog box asking which version to run
# This is intended for me to use when using my code as a desktop shortcut
def launcher():
    audioSystem.playLoop("launcherMusic.mp3")

    class VersionDialog(QDialog):
        def __init__(self):
            super().__init__()
            self.selected_version = None  # Initialize the variable to store the selected version

            self.setWindowTitle("Choose Version")
            self.setWindowIcon(QIcon(config.getAsset("gameControllerIcon-Pink.png")))
            self.setFixedSize(340, 350)
            self.setWindowFlag(Qt.WindowStaysOnTopHint)
            self.setAttribute(Qt.WA_DeleteOnClose)

            # Create layout
            layout = QVBoxLayout()

            # Create a label for the gamesessionmanager itself
            self.mainLabel = QLabel("Z's Game Session Manager")
            self.mainLabel.setAlignment(Qt.AlignCenter)
            self.mainLabel.setStyleSheet("font-size: 21px; font-weight: bold; color: #000;")
            layout.addWidget(self.mainLabel)

            # Create and add the version label
            self.versionLabel = QLabel("v" + gsmversion)
            self.versionLabel.setAlignment(Qt.AlignCenter)
            self.versionLabel.setStyleSheet("font-size: 12px; font-weight: bold; color: #000; margin: 0 0 0 0")
            layout.addWidget(self.versionLabel)
            
            # Create and add the controller icon
            icon_label = QLabel(self)
            pixmap = QPixmap(config.getAsset("gameControllerIcon.png"))  # Load the icon image
            icon_label.setPixmap(pixmap.scaled(150, 150, Qt.KeepAspectRatio))  # Resize the icon
            icon_label.setAlignment(Qt.AlignCenter)
            layout.addWidget(icon_label)  # Add icon label to the layout

            # Create and add the version label
            self.label = QLabel("Choose a version")
            self.label.setAlignment(Qt.AlignCenter)
            self.label.setStyleSheet("font-size: 18px; font-weight: bold; color: #000;")
            layout.addWidget(self.label)

            # Create a horizontal layout for buttons
            button_group_1 = QHBoxLayout()

            # Web Button
            web_button = QPushButton("Web")
            self.style_button(web_button, "FF69B4", "FF1493")
            web_button.clicked.connect(lambda: self.setLaunch('web'))
            button_group_1.addWidget(web_button) # Formats horizontally for compactness

            # Webapp Button
            webapp_button = QPushButton("App (NEW)")
            self.style_button(webapp_button, "FF69B4", "FF1493")
            webapp_button.clicked.connect(lambda: self.setLaunch('app'))
            button_group_1.addWidget(webapp_button) # Formats horizontally for compactness

            # Terminal Button
            terminal_button = QPushButton("Terminal (deprecated)")
            self.style_button(terminal_button, "FF69B4", "FF1493")
            terminal_button.clicked.connect(lambda: self.setLaunch('terminal'))

            # Cancel Button
            cancel_button = QPushButton("Cancel")
            self.style_button(cancel_button, "FF4C4C", "FF0000")
            cancel_button.clicked.connect(lambda: self.setLaunch(''))  # Quit the application on click

            # Button Layout
            layout.addLayout(button_group_1)
            layout.addWidget(terminal_button)
            layout.addWidget(cancel_button)

            # Sets the layout
            self.setLayout(layout)

            self.easterEgg()

        def easterEgg(self):
            # Little easter egg to ask if your enjoying the windows XP tour music that plays in the backround
            def eggPt1():
                self.label.setText("Enjoying the music?")

            def eggPt2():
                self.label.setText("It's an eXPerience!")

            def eggPt3():
                self.label.setText("Choose a version :P")

            self.easterEggTimer1 = QTimer(self)
            self.easterEggTimer1.setSingleShot(True)
            self.easterEggTimer1.timeout.connect(eggPt1)
            self.easterEggTimer1.start(10000)

            self.easterEggTimer2 = QTimer(self)
            self.easterEggTimer2.setSingleShot(True)
            self.easterEggTimer2.timeout.connect(eggPt2)
            self.easterEggTimer2.start(20000)

            self.easterEggTimer3 = QTimer(self)
            self.easterEggTimer3.setSingleShot(True)
            self.easterEggTimer3.timeout.connect(eggPt3)
            self.easterEggTimer3.start(30000)


        def style_button(self, button, background_color, background_hover_color):
            button.setStyleSheet(f"""
                QPushButton {{
                    background-color: #{background_color};
                    border: none;
                    border-radius: 15px;
                    color: white;
                    padding: 10px;
                    font-size: 14px;
                    font-weight: bold;
                }}
                QPushButton:hover {{
                    background-color: #{background_hover_color};
                }}
            """)

        def setLaunch(self, choice):
            self.to_launch = choice  # Store the selected version
            self.accept()  # Close the dialog

    app = QApplication(sys.argv)
    app.setApplicationName("Z's Game Session manager")
    app.setOrganizationName("zcraftelite")
    app.setApplicationVersion(gsmversion)
    app.setWindowIcon(QIcon(config.getAsset("gameControllerIcon-Pink.png")))
    dialog = VersionDialog()
    if dialog.exec_() == QDialog.Accepted:
        audioSystem.stop()
        return dialog.to_launch

# -------------------------------------
# Flask Webserver Code
# -------------------------------------

# --------- Setting Variables ---------

# Defines the defaults (opens in default browser)
useDefaultBrowser = True

# Configures the IP & Port
WebserverIP = "0.0.0.0" # Sets the IP address to be used for the webserver, use 0.0.0.0 to utilize all possible addresses
WebserverPort = "5000"

# Sets the IP the site is hosted on
if WebserverIP == "0.0.0.0":
    WebserverHostedIP = "localhost"
else:
    WebserverHostedIP = WebserverIP

# Configures weather or not the app reloads when a change is detected\
if 'reloaderMode' not in globals():
    reloaderMode = False

# Initialize Flask app
app = Flask(__name__)
app.secret_key = 'urmum'  # In actual development, you would change this to a secure secret key

# - Key Definitions & Webserver Setup -

# Function to launch the site
def launchWebServer():
    notification.notify(title="Z's Game Session Manager - WebServerNotification", message=f"Web Server started in {gsmclientType} mode", app_name="Z's Game Session Manager", app_icon=config.getAsset("favicon.ico"), timeout=5)
    if useDefaultBrowser:
        webbrowser.open("http://" + WebserverHostedIP + ":" + WebserverPort)
        startFlaskApp()
    else:
        webServerThread = threading.Thread(target=startFlaskApp)
        webServerThread.daemon = True
        webServerThread.start()
        runWebApp()
    
def startFlaskApp():
    app.run(host=WebserverIP, port=WebserverPort, debug=True, use_reloader=reloaderMode)

# Context Processor (Loads all common variables/functions into the templates)
@app.context_processor
def inject_globals():
    return dict(version=gsmversion, stage=gsmstage, clientType=gsmclientType) # Global Variables

# Error handler
@app.errorhandler(Exception)
def handle_exception(e):
    print(e)
    return redirect(url_for('error_page'))

# ----------- API Endpoints -----------

# Serves the /assets folder
@app.route('/assets/<path:filename>')
def assets(filename):
    return send_from_directory(os.path.join(config.executabledir, 'assets'), filename)

# Serves the /scripts folder
@app.route('/script/<path:filename>')
def script(filename):
    return send_from_directory(os.path.join(config.executabledir, 'scripts'), filename)

# Serves game info
@app.route('/api/get_game_info')
def get_game_info():
    # Get parameters from query string, with default values if not provided
    game_name = request.args.get('game_name', None)
    refresh_totals = request.args.get('totalsRefresh', None)

    # If game_name is not provided, return an error
    if not game_name:
        return jsonify({"success": False, "message": "Game name not provided"})

    # Call the helper function
    result = fetch_game_info(game_name, refresh_totals)
    
    # Return the result as JSON
    return jsonify(result)

def fetch_data_and_generate_js():
    totals_data = totals_sheet.get_all_values()

    # Process data (excluding header row)
    game_names = [row[5] for row in totals_data[1:]]
    hours_played = [float(row[10]) for row in totals_data[1:]]
    # Create a dictionary to store the data
    chart_data = {
        "games": game_names,
        "hours": hours_played
    }

    # Write the data to a JSON file
    with open(config.getAsset("json_data.json"), 'w') as json_file:
        json.dump(chart_data, json_file)

    print("Data saved to chart_data.json")


def fetch_game_info(game_name, refresh_totals=True, totals_data=totals_sheet.get_all_values(), session_log=log_sheet.get_all_values(), gamecovers = gamecover_sheet.get_all_values()):
    # Find the matching game
    if refresh_totals:
        totals_data = totals_sheet.get_all_values()
        session_log = log_sheet.get_all_values()

    for row in totals_data[1:]:  # Skip header row
        if row[5].strip().lower() == game_name.strip().lower():  # Assuming row[5] contains game name
            game_info = {
                "game_name": row[5],
                "developer": row[6],
                "total_playtime": f"{row[0]} ({row[10]} hours)",
                "playtime_rank": int(row[18]),
                "platforms": row[14],
                "total_price_paid": row[7],
                "total_value_played": row[11],
                "last_played_formatted": format_time_difference(row[8]),
                "noncalculative_last_played_formatted": row[9],
                "last_played_date": row[8],
                "average_session_length": row[12],
                "session_length": row[17],
                "session_count": f"{sum(1 for r in session_log if r[1] == row[5])} sessions",
                "cover_url": web_get_game_cover(row[5], gamecovers),
                "icon_url": web_get_icon(row[5], gamecovers),
                "logo_url": web_get_logo(row[5], gamecovers)
            }
            return {"success": True, "game": game_info}
    
    # If no game was found
    return {"success": False, "message": "Game not found"}

# API to handle adding entries
@app.route('/api/add_entry', methods=['POST'])
def add_entry_api():
    data = request.json

    game_name = data.get('game_name')
    game_platform = data.get('game_platform')
    custom_date = data.get('custom_date', '').strip()
    start_time = data.get('start_time')
    end_time = data.get('end_time')

    if not game_name or not game_platform or not start_time or not end_time:
        return jsonify({"error": "Missing required fields"}), 400
    
    if custom_date:
        try:
            custom_date_stripped = datetime.strptime(custom_date, "%m/%d/%Y")
        except ValueError:
            try:
                custom_date_stripped = datetime.strptime(custom_date, "%Y-%d-%m")
            except ValueError:
                return False
        date = date_to_gs_format(custom_date_stripped)
    else:
        date = date_to_gs_format(datetime.now())

    developer_name = get_developer_name(game_name)

    # Create the new entry for the log sheet
    new_entry = [date, game_name, game_platform, 0, time_to_gs_format(start_time), time_to_gs_format(end_time), "=", developer_name]

    all_values = log_sheet.get_all_values()
    last_filled_row = len(all_values)  # This gives the count of all rows, which includes empty ones

    log_sheet.append_row(new_entry)  # Add the entry to the sheet

    new_row_number = last_filled_row + 1  # Add 1 to the last filled row
    log_sheet.update_cell(new_row_number, 7, f"=F{new_row_number}-E{new_row_number}")

    format_columns()

    # Send success notification
    notification.notify(title="Z's Game Session Manager - Submitted", message=f"Submitted a game session for {game_name} that lasted {fetch_game_info()['game']['session_length']}.", app_name="Z's Game Session Manager", timeout=5)

    return jsonify({"message": "Entry added successfully!"}), 200

def web_get_game_cover(game_name, gamecover_data):
    for cover in gamecover_data:
        if cover[0] == game_name:
            if cover[1] != "":
                return cover[1]
            else:
                return "https://i.ibb.co/xFQYtHT/cover.png"

def web_get_icon(game_name, gamecover_data):
    for icon in gamecover_data:
        if icon[0] == game_name:
            if icon[3] != "":
                return icon[3]
            else:
                return "https://i.ibb.co/8bxNVYq/icon.png"

def web_get_logo(game_name, gamecover_data):
    for logo in gamecover_data:
        if logo[0] == game_name:
            if logo[2] != "":
                return logo[2]
            else:
                return "https://i.ibb.co/m9jQQJg/logo.png"

def set_gamesWithIcons_data():
    global games
    global games_with_icons
    totals_data = totals_sheet.get_all_values()
    gamecovers = gamecover_sheet.get_all_values()
    
    games = [row[5] for row in totals_data[1:] if len(row) > 5]
    games_with_icons = {
        game: web_get_icon(game, gamecovers) for game in games
    }

# --------------- Pages ---------------

# Error Page
@app.route('/error')
def error_page():
    return render_template('error.html')

# Flask route for index
@app.route('/')
def index():
    # Get all games data
    totals_data = totals_sheet.get_all_values()
    log_data = log_sheet.get_all_values()

    # Set up chart data
    game_names = [row[5] for row in totals_data[1:] if float(row[10]) > 0]
    hours_played = [float(row[10]) for row in totals_data[1:] if float(row[10]) > 0]

    # Get the total time played for all games
    times = [row[6] for row in log_data[1:] if len(row) > 6]
    def time_to_seconds(time_str):
        h, m, s = map(int, time_str.split(':'))
        return h * 3600 + m * 60 + s
    total_seconds = sum(time_to_seconds(time) for time in times)
    total_hours_played = f"{round((total_seconds // 3600), 2):,}"

    # Function to convert HH:MM:SS to total seconds
    def time_to_seconds(time_str):
        h, m, s = map(int, time_str.split(':'))
        return h * 3600 + m * 60 + s

    # Sum up all the times in seconds
    total_seconds = sum(time_to_seconds(time) for time in times)

    # List to store games with their last played date
    games_with_dates = []

    # Skip the first row by starting from index 1 and iterate through the rest
    for row in totals_data[1:]:
        try:
            # Skip rows with empty "last_played" value
            last_played_str = row[8]  # Assuming row[8] has the "Last Played" date
            if not last_played_str:  # Skip if "Last Played" is empty
                continue
            
            # Parse the last_played date from the string
            last_played_date = datetime.strptime(last_played_str, "%m/%d/%Y %I:%M:%S %p")
            games_with_dates.append((last_played_date, row))
        except Exception as e:
            print(f"Error parsing date for game {row[5]}: {e}")
            continue

    # Sort games by last played date in descending order
    games_with_dates.sort(key=lambda x: x[0], reverse=True)

    # Extract the most recent games
    most_recent_games = games_with_dates[:5]  # Top 5 most recent games

    # Prepare the JSON-like library for injection
    more_games = {}
    for i, game in enumerate(most_recent_games[1:], start=2):  # Skip the 1st (already rendered)
        game_name = game[1][5]  # Assuming row[5] has the game name
        last_played = game[0].strftime("%m/%d/%Y %I:%M:%S %p")  # Format the date
        last_played_formatted = format_time_difference(last_played)
        more_games[f"lastplayed{i}"] = fetch_game_info(game_name, False)["game"]

    # Render the template with the most recent game and additional games
    if most_recent_games:
        latest_game = most_recent_games[0][1]  # The most recently played game
        game_name = latest_game[5]
        response = fetch_game_info(game_name)
        data = response
        if data["success"]:
            game_info = data["game"]
            return render_template('index.html', game=game_info, more_games=more_games, chart_games=game_names, chart_hours=hours_played, total_hours_played=total_hours_played)

    # Fallback if no games are found
    return render_template('index.html', game=None, more_games={})

# Flask route for checking game info
@app.route('/check_game_info', methods=['GET', 'POST'])
def check_game_info():
    set_gamesWithIcons_data()
    return render_template('check_game_info.html', games_with_icons=games_with_icons)

@app.route('/list_games', methods=['GET'])
def list_games():
    totals_data = totals_sheet.get_all_values()
    log_data = log_sheet.get_all_values()
    gamecover_data = gamecover_sheet.get_all_values()
    games_info = []

    for row in totals_data[1:]:
        game_name = row[5]
        data = fetch_game_info(game_name, False)
        if data["success"]:
            game_info = data["game"]
        games_info.append(game_info)

    return render_template('list_games.html', games_info=games_info)

# Flask route for adding entry
@app.route('/add_entry', methods=['GET', 'POST'])
def add_entry():
    set_gamesWithIcons_data()
    if request.method == 'POST':
        game_name = request.form['game_name']
        game_platform = request.form['game_platform']
        custom_date = request.form.get('custom_date', '').strip()
        start_time = request.form['start_time']
        end_time = request.form['end_time']
        
        # Prepare data to send to API
        data = {
            "game_name": game_name,
            "game_platform": game_platform,
            "custom_date": custom_date,
            "start_time": start_time,
            "end_time": end_time
        }

        response = requests.post(f"{request.host_url}api/add_entry", json=data)

        if response.status_code == 200:
            flash("Entry added successfully!")
        else:
            flash("Error: " + response.json().get('error'))

        return redirect(url_for('index'))

    return render_template('add_entry.html', games_with_icons=games_with_icons)


@app.route('/submit_stopwatch', methods=['POST'])
def submit_stopwatch():
    game_name = request.form['game_name']
    game_platform = request.form['game_platform']
    start_time = request.form['start_time']
    end_time = request.form['end_time']

    # Prepare data to send to API
    data = {
        "game_name": game_name,
        "game_platform": game_platform,
        "start_time": start_time,
        "end_time": end_time
    }

    # Call the API endpoint
    response = requests.post(f"{request.host_url}api/add_entry", json=data)

    if response.status_code == 200:
        flash("Entry added successfully!")
    else:
        flash("Error: " + response.json().get('error'))

    return redirect(url_for('index'))

@app.route('/stopwatch')
def stopwatch():
    set_gamesWithIcons_data()
    return render_template('stopwatch.html', version=gsmversion, games_with_icons=games_with_icons)

@app.route('/changelog')
def changelog():
    return render_template('changelog.html')

@app.route('/about')
def about():
    return render_template('about.html')

# -------------------------------------
# Terminal Output Code
# -------------------------------------

# Function to add a log entry
def add_log_entry():
    # Get the last row with data in the log sheet
    last_row = len(log_sheet.col_values(1))  # Count of filled cells in the first column

    # Ask for the game name
    game_name = input("Enter the name of the game: ")

    # Ask for the game platform
    game_platform = input("Enter the platform used: ")

    # Prompt the user to decide if they want to enter a custom date
    use_custom_date = input("Do you want to enter a custom date? (yes/no): ").strip().lower()

    if use_custom_date == 'yes':
        custom_date_input = input("Enter the date in MM/DD/YYYY format: ")
        try:
            # Parse the input and convert it to datetime
            custom_date = datetime.strptime(custom_date_input, "%m/%d/%Y")
            date = date_to_gs_format(custom_date)  # Save the custom date in the desired format
        except ValueError:
            print("Invalid date format. Using the current date instead.")
            date = date_to_gs_format(datetime.now())
    else:
        date = date_to_gs_format(datetime.now())  # Use the current date

    # Get the developer name from the totals sheet
    developer_name = get_developer_name(game_name)

    start_time = time_to_gs_format(input("Enter Start Time (hh:mm:ss AM/PM): "))
    end_time = time_to_gs_format(input("Enter End Time (hh:mm:ss AM/PM): "))

    # Create a new entry, filling in undefined columns with blanks
    new_entry = [date, game_name, game_platform, 0, start_time, end_time, f"=", developer_name]  # Fill other columns with empty strings

    # Get all values in the sheet
    all_values = log_sheet.get_all_values()
    
    # Find the last filled row
    last_filled_row = len(all_values)  # This gives the count of all rows, which includes empty ones
    
    # Append the new entry
    log_sheet.append_row(new_entry)  # Add the entry to the sheet

    # Since we appended a row, we need to get the new last filled row
    new_row_number = last_filled_row + 1  # Add 1 to the last filled row

    # Update the eighth column with a formula
    log_sheet.update_cell(new_row_number, 7, f"=F{new_row_number}-E{new_row_number}")

    format_columns()

    print(f"Entry added: {new_entry}")

# Function to check the playtime of a certain game
def get_game_info(game_name):
    # Gets the data from the game totals
    totals_data = totals_sheet.get_all_values()
    log_data = log_sheet.get_all_values()

    print("")

    def get_session_count():
        session_count = 0
        for row in log_data:
            if row[1] == game_name:
                session_count += 1

        return session_count

    for row in totals_data:
        if row[5] == game_name:
            print("Game Name:              " + row[5])
            print("Developer:              " + row[6])
            print("Total Playtime:         " + row[0] + " (" + row[10] + " hours)")
            print("Platforms played on:    " + row[14])
            print("Total Price Paid:       " + row[7])
            print("Total Value Played:     " + row[11])
            print("Last Played:            " + row[9] + " (" + row[8] + ")")
            print("Session Count:         ", get_session_count(), "sessions")
            print("Average Session Length: " + row[12])

    input("")

# Main interface function
def main_menu():
    while True:
        clear_screen()
        
        # Resets the variable that tracks if functions are being ran inside another function
        global within_other_function
        within_other_function = 0

        # Display the interface
        main_title("Main Menu")
        print(format_text("NOTE: As of update v2.1.0, the terminal version is deprecated", 'center'))
        print(format_text("Terminal updates will return in a later patch", 'center'))

        
        # Menu options
        print("[1] Add an entry to the log")
        print("[2] Check game information")
        print("[E] Exit")
        
        # Get user input
        choice = input("\nEnter your choice: ")
        
        if choice == '1':
            within_other_function = 1
            clear_screen()
            main_title("Add an entry to the log")
            add_log_entry()
        if choice == '2':
            within_other_function = 1
            clear_screen()
            main_title("Check game information")
            game_name = input("\nEnter the name of the game: ")
            get_game_info(game_name)
        elif choice in ['E', 'e']:
            print("Exiting the program...")
            break
        else:
            print("\nInvalid choice. Please try again.")
            input("Press Enter to continue...")

# -------------------------------------
# Main Entry Point & Argument Parser
# -------------------------------------

if __name__ == "__main__":

    if platform.system() == 'Windows':
        setupWindowsAppID()

    parser = argparse.ArgumentParser(
        description=f"Z's Game Session Manager {gsmversion}",
        epilog="Created, Programmed, and Designed by ZcraftElite"
    )
    parser.add_argument('--terminal', action='store_true', help='Run the terminal version within the current terminal')
    parser.add_argument('--web', action='store_true', help='Run the web version directly')
    parser.add_argument('--app', action='store_true', help='Run the web version within an app')
    parser.add_argument('--use-reloader', action='store_true', help='Use the reloader for the web/app version')

    args = parser.parse_args()

    # Ensure that only one argument [of these choices] (or none) is provided
    if sum([args.terminal, args.web, args.app]) > 1:
        print("Error: This argument must be the only argument to run properly.")
        print("")
        parser.print_help()
        sys.exit(1)  # Exit with an error code

    # Ensure that arguments meant for Web/App use are used with the Web/App modes
    if sum([args.use_reloader]) > 1 and not (args.web or args.app):
        print("Invalid argument configuration!")
        print("")
        parser.print_help()
        sys.exit(1) # Exit with an error code

    if args.terminal:
        gsmclientType = "Terminal Interface"
    elif args.web:
        gsmclientType = "Web Interface"
    elif args.app:
        gsmclientType = "App Interface"

    # Perform respective startup actions
    if args.terminal:
        termWindow.restore()
        main_menu()
    elif args.web or args.app:
        print("Launching web version...")
        if args.app:
            useDefaultBrowser = False
        if args.use_reloader:
            reloaderMode = True
        launchWebServer()
    else:
        launch_choice = launcher()
        if launch_choice == 'web':
            gsmclientType = "Web Interface"
            # Replace with actual web app run logic
            print("Launching web version...")
            launchWebServer()
        elif launch_choice == 'terminal':
            termWindow.restore()
            gsmclientType = "Terminal Interface"
            main_menu()
        elif launch_choice == 'app':
            gsmclientType="App Interface"
            useDefaultBrowser = False
            launchWebServer()
        else:
            print("No valid choice made. Exiting.")
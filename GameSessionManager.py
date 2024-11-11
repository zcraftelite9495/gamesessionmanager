# --------------------------------------------------------------------------------
# Z's Game Session Manager
# --------------------------------------------------------------------------------
# Created, Designed, and Programmed by ZcraftElite
# -----------------------------------------------------

# -------------------------------------
# Version
# -------------------------------------

gsmversion = "2.0.0"

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
        'PyQt5.QtCore'
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
# Imports
# -------------------------------------

checkLibs()
try:
    import os
    import sys
    import argparse
    import platform
    import subprocess
    from pathlib import Path
    from datetime import datetime, timedelta

    import gspread
    from oauth2client.client import flow_from_clientsecrets
    from oauth2client.file import Storage
    from oauth2client.tools import run_flow

    import webbrowser

    from flask import Flask, render_template, request, redirect, url_for, flash

    from PyQt5.QtGui import QPixmap
    from PyQt5.QtWidgets import QApplication, QDialog, QLabel, QPushButton, QVBoxLayout, QHBoxLayout
    from PyQt5.QtCore import Qt
except ImportError as e:
    raise ImportError(f"One or more required libraries failed to load: {e}")

# -------------------------------------
# Base Functions
# -------------------------------------

within_other_function = 0

def format_text(text, alignment):
    """
    Formats the given text with specified alignment: left, right, or center.

    Parameters:
        text (str): The text to format.
        alignment (str): The alignment type. Can be 'left', 'right', or 'center'.

    Returns:
        str: The formatted text.
    """
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
    """
    Formats multiple pieces of text with specified alignments and prints them in the same row.

    Parameters:
        *texts_with_alignments (tuple): A tuple containing (text, alignment) pairs.

    Returns:
        str: The combined formatted text for display.
    """
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

def main_title(title_heading):
    print(format_texts(("Z's Game Session Manager", 'left'), (gsmversion, 'right')))
    print("Created, Designed, and Programmed by ZcraftElite")
    screen_line()
    print(format_text(title_heading, 'center'))
    screen_line()
    print("")

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
# Configuration Files Checker
# -------------------------------------

# Checks to see if configuration directory & files exist
def configChecker():
    """Sets the configuration directory, ensuring it has admin privileges if needed."""
    # Define the base directory for config files based on the OS
    if platform.system() == 'Windows':
        config_dir = Path(os.environ.get('APPDATA', '')).joinpath('gamesessionmanager')
    elif platform.system() == 'Linux' or platform.system() == 'Darwin':  # Darwin is for macOS
        config_dir = Path.home().joinpath('.config', 'gamesessionmanager')
    else:
        raise EnvironmentError("Unsupported OS: " + platform.system())
    
    # Check if the directory exists, and if not, create it
    if not config_dir.exists():
        try:
            config_dir.mkdir(parents=True, exist_ok=True)
        except PermissionError:
            print(f"Permission denied. Requesting admin privileges to create the directory: {config_dir}")
            request_admin_permissions()
            return set_config_directory()  # Retry after admin permissions

    # Check for the files
    missing_files = []
    executable_dir = Path(__file__).parent  # Directory of the current script or executable
    files_to_check = ['credentials.json', 'sheetid.txt']
    
    # Check if the files exist in the config directory
    for file_name in files_to_check:
        file_path = config_dir.joinpath(file_name)
        if not file_path.exists():
            # If the file is missing in the config directory, check the executable directory
            executable_file_path = executable_dir.joinpath(file_name)
            if executable_file_path.exists():
                print(f"Found {file_name} in executable directory, copying to config directory.")
                # Copy file without using shutil
                with open(executable_file_path, 'rb') as source_file:
                    with open(file_path, 'wb') as dest_file:
                        dest_file.write(source_file.read())
            else:
                missing_files.append(file_name)
    
    # If any files are missing, raise an error
    if missing_files:
        raise FileNotFoundError(f"Missing files: {', '.join(missing_files)}")
    
    # Change the current working directory to the config directory
    os.chdir(config_dir)
    
    # Now the current directory is the one containing your configuration files
    print(f"Configuration directory set to: {config_dir}")
    return config_dir

# -------------------------------------
# Google Sheets API Functions
# -------------------------------------

# Define the scope for Google Sheets API
scope = ["https://www.googleapis.com/auth/spreadsheets"]

# Call the function to set the configuration directory
configChecker()

# Get the sheet ID from the sheetid.txt file
if os.path.exists("sheetid.txt"):
    with open("sheetid.txt", 'r') as file:
        sheet_id = file.readline().strip()  # Read the first line and remove any trailing newline or spaces

# Load credentials
def get_credentials():
    creds = None
    if os.path.exists("token.json"):
        creds = Storage("token.json").get()
    if not creds or creds.invalid:
        flow = flow_from_clientsecrets("credentials.json", scope)
        creds = run_flow(flow, Storage("token.json"))
    return creds

# Authorize and connect to Google Sheets
creds = get_credentials()
client = gspread.authorize(creds)

executable_dir = Path(__file__).parent
os.chdir(executable_dir)

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
# Launcher Code
# -------------------------------------

# Defines the function that launches the dialog box asking which version to run
# This is intended for me to use when using my code as a desktop shortcut
def launcher():
    class VersionDialog(QDialog):
        def __init__(self):
            super().__init__()
            self.selected_version = None  # Initialize the variable to store the selected version

            self.setWindowTitle("Choose Version")
            self.setFixedSize(300, 250)  # Increase size to fit the new button
            self.setWindowFlag(Qt.WindowStaysOnTopHint)
            self.setAttribute(Qt.WA_DeleteOnClose)

            # Create layout
            layout = QVBoxLayout()
            
            # Create and add the icon label
            icon_label = QLabel(self)
            pixmap = QPixmap("./assets/gameControllerIcon.png")  # Load the icon image
            icon_label.setPixmap(pixmap.scaled(150, 150, Qt.KeepAspectRatio))  # Resize the icon
            icon_label.setAlignment(Qt.AlignCenter)
            layout.addWidget(icon_label)  # Add icon label to the layout

            # Create and add the version label
            label = QLabel("Choose a version")
            label.setAlignment(Qt.AlignCenter)
            label.setStyleSheet("font-size: 18px; font-weight: bold; color: #000;")
            layout.addWidget(label)

            # Create a horizontal layout for buttons
            button_layout = QHBoxLayout()

            # Create buttons
            web_button = QPushButton("Web")
            terminal_button = QPushButton("Terminal")
            
            # Style buttons
            self.style_button(web_button)
            self.style_button(terminal_button)

            # Add buttons to the horizontal layout
            button_layout.addWidget(web_button)
            button_layout.addWidget(terminal_button)

            # Create the Cancel button
            cancel_button = QPushButton("Cancel")
            cancel_button.setStyleSheet("""
                QPushButton {
                    background-color: #FF4C4C; 
                    border: none;
                    border-radius: 15px; 
                    color: white; 
                    padding: 10px; 
                    font-size: 14px; 
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #FF0000;
                }
            """)
            cancel_button.clicked.connect(QApplication.quit)  # Quit the application on click

            # Add the Cancel button under the other buttons
            layout.addLayout(button_layout)
            layout.addWidget(cancel_button)

            # Connect buttons to actions
            web_button.clicked.connect(lambda: self.set_version('web'))
            terminal_button.clicked.connect(lambda: self.set_version('terminal'))

            # Set the main layout for the dialog
            self.setLayout(layout)

        def style_button(self, button):
            button.setStyleSheet("""
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

        def set_version(self, choice):
            self.selected_version = choice  # Store the selected version
            self.accept()  # Close the dialog

    app = QApplication(sys.argv)
    dialog = VersionDialog()
    if dialog.exec_() == QDialog.Accepted:
        chosen_version = dialog.selected_version  # Get the selected version
        return chosen_version

# -------------------------------------
# Flask Webserver Code
# -------------------------------------

# Configures the IP & Port
WebserverIP = "0.0.0.0" # Sets the IP address to be used for the webserver, use 0.0.0.0 to utilize all possible addresses
WebserverPort = "5000"

# Sets the IP the site is hosted on
if WebserverIP == "0.0.0.0":
    WebserverHostedIP = "localhost"
else:
    WebserverHostedIP = WebserverIP

# Initialize Flask app
app = Flask(__name__)
app.secret_key = 'your_secret_key'  # In actual development, you would change this to a secure secret key

# Function to launch the website in a new tab
def open_site():
    webbrowser.open("http://" + WebserverHostedIP + ":" + WebserverPort)

# Error handler
@app.errorhandler(Exception)
def handle_exception(e):
    print(e)
    return redirect(url_for('error_page'))

@app.route('/error')
def error_page():
    return render_template('error.html')

# Flask route for index
@app.route('/')
def index():
    return render_template('index.html', version=gsmversion)

# Flask route for adding entry
@app.route('/add_entry', methods=['GET', 'POST'])
def add_entry():
    if request.method == 'POST':
        game_name = request.form['game_name']
        game_platform = request.form['game_platform']
        custom_date = request.form.get('custom_date', '').strip()
        start_time = request.form['start_time']
        end_time = request.form['end_time']
        
        def date_to_gs_format(dt):
            base_date = datetime(1899, 12, 30)
            delta = dt.date() - base_date.date()
            return delta.days
        
        if custom_date:
            date = date_to_gs_format(datetime.strptime(custom_date, "%m/%d/%Y"))
        else:
            date = date_to_gs_format(datetime.now())

        developer_name = get_developer_name(game_name)

        new_entry = [date, game_name, game_platform, 0, time_to_gs_format(start_time), time_to_gs_format(end_time), f"=", developer_name]
        
        all_values = log_sheet.get_all_values()
        
        last_filled_row = len(all_values)  # This gives the count of all rows, which includes empty ones
        
        log_sheet.append_row(new_entry)  # Add the entry to the sheet

        new_row_number = last_filled_row + 1  # Add 1 to the last filled row

        log_sheet.update_cell(new_row_number, 7, f"=F{new_row_number}-E{new_row_number}")
        
        format_columns()

        flash("Entry added successfully!")
        return redirect(url_for('index'))
    
    return render_template('add_entry.html', version=gsmversion)

# Flask route for checking game info
@app.route('/check_game_info', methods=['GET', 'POST'])
def check_game_info():
    if request.method == 'POST':
        game_name = request.form['game_name']
        game_info = web_get_game_info(game_name)
        return render_template('game_info.html', game_info=game_info)
    
    return render_template('check_game_info.html', version=gsmversion)

def web_get_game_info(game_name):
    totals_data = totals_sheet.get_all_values()
    for row in totals_data:
        if row[5] == game_name:
            return {
                "game_name": row[5],
                "developer": row[6],
                "total_playtime": (row[0] + " (" + row[10] + " hours)"),
                "platforms": row[14],
                "total_price_paid": row[7],
                "total_value_played": row[11],
                "last_played": row[9],
                "average_session_length": row[12],
                "session_count": str(sum(1 for r in log_sheet.get_all_values() if r[1] == game_name)) + " sessions",
                "cover_url": web_get_game_cover(game_name, gamecover_sheet.get_all_values())
            }
    return None

def web_get_game_cover(game_name, gamecover_data):
    for cover in gamecover_data:
        if cover[0] == game_name:
            if cover[1] != "":
                return cover[1]
            else:
                return "https://i.ibb.co/XJb2VPw/Z-s-Playtime-Tracker-Cover.png"

@app.route('/list_games', methods=['GET'])
def list_games():
    games_info = web_get_all_games_info()
    return render_template('list_games.html', games_info=games_info, version=gsmversion)

def web_get_all_games_info():
    totals_data = totals_sheet.get_all_values()
    log_data = log_sheet.get_all_values()
    gamecover_data = gamecover_sheet.get_all_values()
    games_info = []
    for row in totals_data[1:]:
        game_name = row[5]
        game_info = {
            "game_name": row[5],
            "developer": row[6],
            "total_playtime": (row[0] + " (" + row[10] + " hours)"),
            "platforms": row[14],
            "total_price_paid": row[7],
            "total_value_played": row[11],
            "last_played": (row[9] + " (" + row[8] + ")"),
            "average_session_length": row[12],
            "session_count": str(sum(1 for r in log_data if r[1] == game_name)) + " sessions",
            "cover_url": web_get_game_cover(game_name, gamecover_data)
        }
        games_info.append(game_info)
    return games_info

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
    parser = argparse.ArgumentParser(
        description=f"Z's Game Session Manager {gsmversion}",
        epilog="Created, Programmed, and Designed by ZcraftElite"
    )
    parser.add_argument('--launcher', action='store_true', help='Launch the version selection popup')
    parser.add_argument('--web', action='store_true', help='Run the web version directly')

    args = parser.parse_args()

    # Ensure that --launcher is the only argument provided
    if args.launcher and (len(sys.argv) > 2):
        print("Error: --launcher must be the only argument.")
        print("")
        parser.print_help()
        sys.exit(1)  # Exit with an error code

    if args.launcher:
        version_choice = launcher()
        if version_choice == 'web':
            # Replace with actual web app run logic
            print("Launching web version...")
            open_site()
            app.run(host=WebserverIP, port=WebserverPort, debug=True, use_reloader=False)
        elif version_choice == 'terminal':
            main_menu()
        else:
            print("No valid choice made. Exiting.")
    elif args.web:
        print("Launching web version...")
        open_site()
        app.run(host=WebserverIP, port=WebserverPort, debug=True, use_reloader=False)
    else:
        main_menu()
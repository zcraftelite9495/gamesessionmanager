# Game Session Manager

<img src="https://img.shields.io/badge/Version-2.1.0--beta--2-blue" alt="Version Badge"> <img src="https://img.shields.io/badge/Development_Stage-beta-blue" alt="Development Stage Badge">
<img src="https://wakatime.com/badge/user/018db32b-732a-4704-b635-68d311538b3f/project/8d41e1a9-a75f-44c4-9094-7c557ccc6b79.svg" alt="wakatime"> <img src="https://img.shields.io/github/languages/top/zcraftelite9495/gamesessionmanager" alt="Top Language"> <img src="https://img.shields.io/github/stars/zcraftelite9495/gamesessionmanager" alt="Stars Badge"> <img src="https://img.shields.io/github/forks/zcraftelite9495/gamesessionmanager" alt="Forks Badge">

This is a program I created in my free time to help interface with my Google Sheet for tracking all my game playtime across various platforms. It’s a personal project that I wanted to share with others on GitHub.

**Important Note:** This script is designed to work specifically with my custom Google Sheet. In order for it to function properly, you will need to use the exact same sheet. You can view and make a copy of my Google Sheet [here](https://docs.google.com/spreadsheets/d/1cYQ8B-lnzHLaO32mFZJTweRy8vqjr0Wm2kmcHEcFP8A/edit?gid=329820141#gid=329820141).

## Features

- Easily log and track playtime for different video games.
- Choice of using a terminal interface or a simple web interface.
- Automatically formats Google Sheets for better organization and readability.
- Supports multiple gaming platforms and allows for custom date entries.

## Feature Roadmap

- Impliment a way to type a game name and then hit a start session and end session button, eliminating the need to manually enter times, and allowing users to let it track sessions more easily

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## Additional Links

- [Changelog](changelog.md)
- [Copyright Information](COPYINFO.md)
- [License](LICENSE.md)

## Installation

To get started with the Game Session Manager, you can use it in two ways:

1. **Clone the repository:**
   
   **Download Source**
   Go to the `releases` tab to easily find the latest stable, beta, or alpha release.
   There you can download and extract the `.zip` file to get the repo

   **Use Fully Compiled File**
   Additionally, you can download the `GSMFull.py` file.

2. **Install the required libraries:**

   Make sure you have Python 3.x installed. Then, install the necessary libraries using pip:

   ```bash
   pip install gspread oauth2client Flask PyQt5
   ```

3. **Set up Google Sheets API:**

   - Follow [this guide](https://developers.google.com/sheets/api/quickstart/python) to create a project and enable the Google Sheets API.
   - Download your `credentials.json` file and place it in the project directory.
   - Create a text file named `sheetid.txt` and add the Google Sheet ID from your sheet (the part of the URL after `/d/`) Should look like this: `1cYQ8B-lnzHLaO32mFZJTweRy8vqjr0Wm2kmcHEcFP8A`.

## Usage

To run the application, you can choose between a terminal interface or a web interface. Additionally, you can use a desktop shortcut with the Launcher to easily choose between versions.

### Terminal Interface

To launch the terminal version:

```bash
python gamesessionmanager.py
```

### Web Interface

To launch the web version directly:

```bash
python gamesessionmanager.py --web
```

### Launcher

To use the launcher:

```bash
python gamesessionmanager.py --launcher
```

or create a desktop shortcut with the same code (including the directory the file is located in, of course).

## Contributing

While this is primarily a personal project, I welcome any feedback or suggestions! If you have ideas for improvements or features, feel free to fork the repository and submit a pull request.

1. Fork the repository.
2. Create your feature branch: `git checkout -b feature/AmazingFeature`
3. Commit your changes: `git commit -m 'Add some AmazingFeature'`
4. Push to the branch: `git push origin feature/AmazingFeature`
5. Open a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

If you have any questions or just want to chat about the project, feel free to reach out:

- **Name:** ZcraftElite
- **GitHub:** [zcraftelite9495](https://github.com/zcraftelite9495)
- **Email:** [zcomer4dthesecond@gmail.com](mailto:zcomer4dthesecond@gmail.com) (Warning: I barely check my email)
- **Discord:** [zcraftelite](https://discord.com/users/926788037785047050)


---

Thanks for checking out my Game Session Manager! I hope you find it interesting. Happy gaming!
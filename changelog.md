# 📜 Changelog

## 🔑 Key
**Entries**
- 🐛 **Bugfix**: Fixes for bugs and errors.  
- ➕ **Addition**: New features or content.  
- 🔄 **Change**: Modifications or updates to existing features.  
- ⛔ **Removal**: Features or content that were removed.  

**Release Stages**
- 🔵 **Beta**: Changes in beta releases.  
- 🔴 **Alpha**: Changes in alpha releases.  
- 🟢 **Stable**: Changes in stable releases.
- ✅ **Published**: Release has been published on github.
- ⏳ **Pending**: Release is in development.
- ❌ **Unpublished/Doesn't Exist**: Release doesn't exist or is unpublished.

## 📂 Releases

* 🟢✅ v2.0.0
* 🟢⏳ v2.1.0
    * 🔵✅ v2.1.0-beta-1
        * 🔴❌ v2.1.0-beta-1-pre1
    * 🔵✅ v2.1.0-beta-2
        * 🔴✅ v2.1.0-beta-2-pre1
        * 🔴✅ v2.1.0-beta-2-pre2

## ℹ️ How Versions Work
Versions with most of my projects follow the following format with numbers:

**0.0.0 (-beta) (-pre#)**
* the first number being the major version (incompatible API with older versions or giant update)
* the second number being the feature release version (Compatible with older releases, just adds new features)
* The third number being the patch release version (For after-development bugfixes and patches)
* Then, if the version is currently under current development, it will have -beta
* Then, if the version is currently under complex development with very unstable features, it will be a pre-beta, using `pre(Prerelease Number)`

---

### 📜🟢 Changelog: 2.0.0 (Stable)
* ➕ Started using GitHub to host the project on my profile. (Initial Release)

---

### 📜🔵 Changelog: 2.1.0-beta-1 (Beta)
* 🐛 Fixed bugs with the old configuration file system failing to function.
* 🔄 Changed configuration directory to the `config` folder within the folder that `GameSessionManager.py` file is stored.
* ➕ Introduced a new class of functions to better manage program configuration.
* 🐛 Fixed a bug where the popup launcher was unable to locate assets when the working directory was not the directory `GameSessionManager.py` was stored in.
* ➕ Added in a variable within `GameSessionManager.py` that can easily enable/disable the webserver restarting the program when a change is made to the `GameSessionManager.py` file.
* 🔄 Changed the default security key to `urmom` for the funny.

---

### 📜🔴 Changelog: 2.1.0-beta-2-pre1 (Alpha)
* ➕ Started utilizing the GitHub releases feature for better version tracking.
* ➕ Started a plain changelog for me to personally keep better track of changes I make between versions.
* 🐛 Fixed a bug with my default value for the reloaderMode variable.
* ➕ Introduced Stopwatch Tracking (Beta).
* ➕ Added a warning to the footer (in the web version) when the user is running an Alpha or Beta version of the program.
* ➕ Added a warning to the titlebar (in the terminal version) when the user is running an Alpha or Beta version of the program.
* ➕ Added the program name and the current version under alongside the copyright information.
END OF VERSION

---

### 📜🔴 Changelog: 2.1.0-beta-2-pre2 (Alpha)
* 🔄 Changed the changelog to `.md` (Markdown) format for better readability.
* 🔄 Updated the ReadMe (`README.md`).
* 🔄 Changed the heading of the Stopwatch Mode page to `Log using Stopwatch Mode (BETA)`.
* 🔄 Changed the heading of the Add Entry page to `Log Manually`.
* 🔄 Changed the values of the submit buttons on the logging pages to make more sense.
* 🔄 Reformatted the Stopwatch Mode stopwatch to look more aesthetically better by adding formatted buttons and placing the start/stop buttons next to the stopwatch.
* ➕ Added a dropdown labeled `Log Now` to contain the links to stopwatch mode and the add entry page.
* ➕ Added a `cancel` button to the Stopwatch Mode that will submit without resetting the page.
* 🐛 Fixed heading design mistake on the Stopwatch Mode page.
* ➕ Added the site icon to the header and made the site title clickable (takes you to `/`).
* 🔄 Completely redesigned the homepage for a more modern, more put-together feel.
END OF VERSION

---

### 📜🔵 Changelog: 2.1.0-beta-2 (Beta)
* 🔄 Changed the style of disabled inputs (Primarily used in Stopwatch Mode) to be grayed out.
* 🔄 Changed each `label` for the `input`s to add a red `*` at the end of each label, ensuring that it appears before any `:`s.
* 🐛 Fixed the name for the Stopwatch Mode page in the titlebar.
* ➕ Implemented a function to show your last played game on the homepage under the main menu area (this was a lot harder than you would think).
* ➕ Added a new icon for the last played game section of the homepage.
* 🔄 Moved the scripts from `base.html` to individual .js files.
* ➕ Added placeholders to inputs to teach the user how to correctly input the values, instead of adding them to the labels.
* 🔄 Changed the custom date output to a date input, for aesthetic purposes.
* ➕ Added custom icons all around the web interface for aesthetic purposes.
* 🔄 Updated the README to include copyright acknowledgement for the icons used.
* ➕ Added the `LICENSE` and the cooler `LICENSE.md` to the repo for copyright.
* ➕ Added the `COPYINFO.md` file to contain copyright info about works used within the repo.
* ➕ Added emojis to most markdown files for some spark.
* 🔄 Redesigned the changelog to make it more beautiful.
* ⛔ 

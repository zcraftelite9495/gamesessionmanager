### Changelog: 2.1.0-beta-1 (Beta)
* Fixed bugs with the old configuration file system failing to function.
* Changed configuration directory to the `config` folder within the folder that `GameSessionManager.py` file is stored.
* Introduced a new class of functions to better manage program configuration.
* Fixed a bug where the popup launcher was unable to locate assets when the working directory was not the directory `GameSessionManager.py` was stored in.
* Added in a variable within `GameSessionManager.py` that can easily enable/disable the webserver restarting the program when a change is made to the `GameSessionManager.py` file.
* Changed the default security key to `urmom` for the funny.

### Changelog: 2.1.0-beta-2-pre1 (Alpha)
* Started utilizing the GitHub releases feature for better version tracking.
* Started a plain changelog for me to personally keep better track of changes I make between versions.
* Fixed an bug with my default value for the reloaderMode variable.
* Introduced Stopwatch Tracking (Beta).
* Added a warning to the footer (in the web version) when the user is running an Alpha or Beta version of the program.
* Added a warning to the titlebar (in the terminal version) when the user is running an Alpha or Beta version of the program.
* Added the program name and the current version under alongside the copyright information.
END OF VERSION

### Changelog: 2.1.0-beta-2-pre2 (Alpha)
* Changed the changelog to `.md` (Markdown) format for better readibility.
* Updated the ReadMe (`README.md`)
* Changed the heading of the Stopwatch Mode page to `Log using Stopwatch Mode (BETA)`.
* Changed the heading of the Add Entry page to `Log Manually`.
* Changed the values of the submit buttons on the logging pages to make more sense.
* Reformatted the Stopwatch Mode stopwatch to look more aesthetically better by adding formatted buttons and placing the start/stop buttons next to the stopwatch.
* Added a dropdown labbeled `Log Now` to contain the links to stopwatch mode and the add entry page.
* Added a `cancel` button to the Stopwatch Mode that will submit without resetting the page.
* Fixed heading design mistake on the Stopwatch Mode page.
* Added the site icon to the header and made the site title clickable (takes you to `/`).
* Completely redesigned the homepage for a more modern more put-together feel.
END OF VERSION
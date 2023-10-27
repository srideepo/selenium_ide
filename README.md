# selenium_ide
A custom python based selenium IDE (eventually with docker and jupyter)

Features:
v1.0
-python based
-allows debugging in local (existing) browser session
-runs selenium using pytest
-bootstrapped webdriver instance using plugins
-supports browsers - chrome, firefox, edge

Usage:
Open one of the supported browser locally in debug mode
`./chrome.exe --remote-debugging-port=9222 --user-data-dir="%APPDATA%\ChromeProfile"`

`./firefox.exe -marionette -start-debugger-server` 2828 #only use 2828

`./msedge.exe --remote-debugging-port=9444 --user-data-dir="%APPDATA%\EdgeProfile"`

run the app by `python main.py ./mytests`

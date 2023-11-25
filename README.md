# SimpleFin Alerts

This tool is gives a quick check for SimpleFin accounts in Error Status, with optional Apprise notifications.

## Setup

* You will need to generate a SimpleFin Setup Token, and have that handy.

* If you want to use Apprise Notifications, you will need to have the [Apprise API](https://github.com/caronc/apprise-api) installed and running, and have the URL handy (typically in the form: https://example.com/notify/apprise ), as well as the Apprise Tag created and configured that you want to send it to.

* The status of the accounts is printed to terminal, where the program is run, so it can be used manually. If you decide to use Apprise API, then you can set a system cron and it will send the status of the accounts via the chosen Apprise tag.

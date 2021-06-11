# update-auth-methods
update-auth-methods.py is an interactive tool for [updating Tenable.IO user authentication methods](https://developer.tenable.com/reference#users-update-auths).

This can be especially useful if:
- You have enabled SAML authentication and want to disable local Tenable.IO authentication.
- You have created an API user and want to disable GUI login.

WARNING: It is possible to lockout accounts with this tool. Do not use this tool if you do not understand how it works.
## Requirements
* Python3
## Installation
update-auth-methods.py is a dependency free, standalone Python program. Just download it and run it.
### git
```
$ git clone https://github.com/andrewspearson/update-auth-methods.git
```
### curl
```
$ curl https://raw.githubusercontent.com/andrewspearson/update-auth-methods/main/update-auth-methods.py -O
```

**NOTE:** macOS users running Python 3.6+ will need to [install certificates](https://bugs.python.org/issue28150).
TLDR, run this command:
```
$ /Applications/Python {version}/Install Certificates.command
```
This seems to only be an issue on macOS.
## Usage
update-auth-methods.py will update the authentication methods for all users in a user group.

It will accept arguments to set a web proxy and disable SSL verification, like this:
```
$ update-auth-methods.py --proxy '127.0.0.1:8080' --insecure
```
These arguments are not required. Disabling SSL verification is HIGHLY discouraged.

Example:
![](https://raw.githubusercontent.com/andrewspearson/file-server/main/repositories/update-auth-methods/update-auth-methods.gif)

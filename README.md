# update-auth-methods
update-auth-methods.py is an interactive script for [updating Tenable.IO user authentication methods](https://developer.tenable.com/reference#users-update-auths).
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
![](https://andrewspearson.github.io/file-server/repositories/update-auth-methods/update-auth-methods.gif)

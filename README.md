Anime AutoMove
==============

Requirement
-----------
1. `python3` for making this program works.
2. `sqlite3` to store sync status of files.
3. `vixie-cron` working to automate tasks.

Description
-----------
This application sort new downloaded anime file from a folder to another.<br/>This script rely on fansub convention to works.<br/>
Missing directory will be automatically created if needed.

Exemple of use : To layout a folder in format expected by Plex Media Server.

How it works
------------
There is two main mechanism in this program:

1. (learn) Setup new sort rule. One suggestion will be made based on file name but the destination folder can be customized.
2. (execute) Application of rules to move for real the anime in the goods directory

It works only if your file follow this convention :
```
[<team>] <anime_anime> - <Number Ep> + v<Version><other_data>.<extension>
```

You can also manage rules :

1. (deleting) if you made any error during config.
2. (show) if you wanna know what you have setup by using learn operation.
3. (cleanup) to speed up process by removing old rules not matched since a long time.

Operation are not overly automated to ensure simple code and better control over file destination.

Automation
----------
Samples are included along to show you how to make things

Install
-------
```bash
python3 setup.py install (or develop)
```

FreeBSD users
=============

- The support of `sqlite3` isn't bundled within `python3` you will also need to install `py-sqlite3`.
- Ensure local are properly configured on client and server side. Hint : Customize your `/etc/login.conf` or `~/.login.conf`.<br/>See: https://www.freebsd.org/doc/handbook/using-localization.html

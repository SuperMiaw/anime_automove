Anime AutoMove
==============

Requirement
-----------
1. `python3` for making this program works.
2. `sqlite3` to store sync status of files.
3. `vixie-cron` working to automate tasks.

Description
-----------
That utility help to organize your new animes you may have downloaded with another program.<br/>It will try to extract anime name
using fansub popular conventions and move them to another directory.

Quite usefull for a media center like Plex Media Server, missing directory will be created if needed and you will be ensured to not have to do it manually.

How it works
------------
There is two main mechanism in this program:

1. (learn) try to guess new required rules according to what you have in drop folder.
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

Python3
-------
The support of sqlite3 isn't bundled within `python3` you will have to install `py-sqlite3` to make it
works.

Locale
------
Ensure local are properly configured on client and server side, else you will get into trouble.
You can customize your `/etc/login.conf` or `~/.login.conf`.
see : https://www.freebsd.org/doc/handbook/using-localization.html


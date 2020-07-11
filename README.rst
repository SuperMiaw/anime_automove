Anime AutoMove
==============

Requirement
-----------
1. `python3` for making this program works.
2. `sqlite3` to store sync status of files.
3. `vixie-cron` working to automate tasks.

Description
-----------
That utility help to organize your new animes you may have downloaded with another program. It try to extract anime name
using fansub popular conventions and move them to another directory where maybe your media center is scanning them.
It's a quite usefull for solution for Plex Media Server cause you may have not to create anymore new folder layout and
keep moving file yourself which it can be tiresome if you have many.

How it works
------------
There is two main mechanism in this program:

1. (learn) try to guess new required rules according to what you have in drop folder.
2. (execute) Application of rules to move for real the anime in the goods directory

It works only if you file follow this convention :
[<team>] <anime_anime> - <Number Ep> + v<Version><other_data>.<extension>

You can also manage rules :

1. (deleting) if you made any error during config.
2. (show) if you wanna know what you have setup by using learn operation.
3. (cleanup) to speed up process by removing old rules not matched since a long time.

Automation
----------
Set-up cron properly to run and kill the program at the wanted hours...
Samples are included along to show you how to make things

Install
-------
python2.7 setup.py install (or develop)


FreeBSD users
=============

Additional requirement
----------------------
It seems that the support of sqlite3 isn't bundled within `python-2.7` you may have to install `py-sqlite3` to make it
works.

Locale
------
If you use many foreign char don't forget to customise your `/etc/login.conf`
or `~/.login.conf`
see : https://www.freebsd.org/doc/handbook/using-localization.html

import os
import traceback
from argparse import ArgumentParser

import sys

import signal

from anime_automove.feature import Learn, Execute, Remove, Show
from anime_automove.util.app import Config
from anime_automove.util.dal import init


def main():
    """Run the main program"""

    # ARGS
    #
    parser = ArgumentParser()
    parser.add_argument('-c', '--configuration',
                        help="Configuration of the program",
                        required=True)

    action_grp = parser.add_mutually_exclusive_group(required=True)
    action_grp.add_argument('-l','--learn',
                            help="Suggest new anime rules that are found in source directory",
                            action="store_true")
    action_grp.add_argument('-e', '--execute',
                            help="Move anime according to stored rules",
                            action="store_true")
    action_grp.add_argument('-s', '--show',
                            help="Show all stored rule",
                            action="store_true")
    action_grp.add_argument('-d', '--delete',
                            help="Try to delete rule by pattern",
                            action="store")
    action_grp.add_argument('--cleanup',
                            help="Try to remove old rules that aren't matched since a while (according to conf.)",
                            action="store")

    args = parser.parse_args()

    # CONFIG FILE
    #
    cfg = Config(path=args.configuration)
    init(config=cfg)

    # LOCALE
    #
    if sys.stdout.encoding is None:
        print >> sys.stderr, "Encoding for output seems missing... "
        "You should set env variable PYTHONIOENCODING=UTF-8. "
        "Example: running 'export PYTHONIOENCODING=UTF-8' before calling this program"
        exit(1)

    # DIRECTORY
    #
    if not os.path.exists(cfg.src_dir):
        raise Exception("The source directory '%s' doesn't exist, check your config." % cfg.src_dir)
    if not os.path.isdir(cfg.src_dir):
        raise Exception("The source directory '%s' isn't a directory, check your config." % cfg.src_dir)

    if not os.path.exists(cfg.tgt_dir):
        raise Exception("The target directory '%s' doesn't exist, check your config." % cfg.tgt_dir)
    if not os.path.isdir(cfg.tgt_dir):
        raise Exception("The target directory '%s' isn't a directory, check your config." % cfg.tgt_dir)

    # PID LOCK
    #
    pid = str(os.getpid())

    if os.path.isfile(cfg.lock_file):
        if cfg.verbose:
            print "Lock file found (%s), stopping program..." % cfg.lock_file
        sys.exit()
    else:
        if cfg.verbose:
            print "Starting operations..."
            print "Creating lock file (%s)" % cfg.lock_file
        file(cfg.lock_file, 'w').write(pid)

    # EXIT HANDLER
    #
    remote = None

    def handler(signum=None, frame=None):
        print "Exiting..."
        print remote

        if remote.process is not None:
            try:
                remote.process.terminate()
            except:
                print "Operation stopped"

        os.unlink(cfg.lock_file)
        exit(0)

    # signal.SIGHUP, signal.SIGQUIT
    for sig in [signal.SIGTERM, signal.SIGINT]:
        signal.signal(sig, handler)

    try:
        if args.learn:
            # learning new rules
            learn = Learn(config=cfg)

            animes = learn.find_distinct_names()
            print "Searching new animes... %s candidates !" % len(animes)

            for anime in animes:
                if learn.exist(anime):
                    print "Ignored (exist): %s" % anime
                else:
                    learn.suggest_add_name(anime)

        elif args.execute:
            # Applying rules
            execute = Execute(config=cfg)

            animes = execute.find_all()

            for anime in animes:
                execute.apply(anime)

        elif args.show:
            # Show all stored rules
            show = Show(config=cfg)
            show.show_all()

        elif args.delete:
            # Removing rule by pattern
            remove = Remove(config=cfg)

            print "Trying to remove rule (pattern='%s')" % args.delete
            success = remove.remove(pattern=args.delete)

            if success:
                print "Rule removed..."
            else:
                print "Rule not found !"

        elif args.cleanup:
            # Cleaning up old rules
            remove = Remove(config=cfg)

            print "Cleaning rules older than %s days..." % cfg.rule_cleanup_days
            success = remove.cleanup(cfg.rule_cleanup_days)

        else:
            # (No actions)
            print "You haven't asked any action... Printing Help."
            parser.print_help()

    except:
        print "Fatal error"
        traceback.print_exc()

    if os.path.isfile(cfg.lock_file):
        if cfg.verbose:
            print "Removing lock file (%s)" % cfg.lock_file

        os.unlink(cfg.lock_file)

    exit(0)


if __name__ == '__main__':
    main()





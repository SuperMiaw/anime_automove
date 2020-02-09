import os

import shutil

from anime_automove.util.dal import RuleAccess, Rule
from anime_automove.util.file import Anime
from util.app import Config


class Learn:
    """Learn and suggest new rules for moving files"""

    def __init__(self, config):
        """Setup
        :type config: Config
        :param config:

        :rtype: Set<Anime>
        :return:
        """
        self._config = config

    def find_distinct_names(self):
        """Find distinct anime 'name' in 'source_directory'

        :rtype set[string]
        :returns all compatible animes name candidate to learning
        """
        src_dir = self._config.src_dir

        if not os.path.exists(src_dir):
            raise Exception("The source directory '%s' doesn't exist, check your config." % src_dir)
        if not os.path.isdir(src_dir):
            raise Exception("The source directory '%s' isn't a directory, check your config." % src_dir)

        matches = set()
        items = os.listdir(self._config.src_dir)

        for item in items:
            item_path = os.path.join(self._config.src_dir, item)

            if os.path.isfile(item_path):
                anime = Anime.parts(item)

                if anime:
                    matches.add(anime.name)

        return matches

    def exist(self, name):
        """Indicate, if a pattern is already defined

        :type name: String
        :param name:

        :rtype: Boolean
        :return: True if found
        """

        rule_access = RuleAccess()
        if rule_access.find_by_pattern(pattern=name) is None:
            return False
        return True

    def suggest_add_name(self, name):
        """Prompt user about adding a new rule

        :type name: String
        :param name:

        :return: Nothing
        """
        tgt_dir = self._config.tgt_dir

        print "Found new file '%s' !" % name

        should_add = None
        while True:
            should_add = raw_input("Create rule for '%s' ? [(y)/n] " % name)
            if should_add in ('', 'y', 'n'):
                break

        if should_add == 'n':
            return

        destination = raw_input("Destination folder : [%s] in '%s' (customize sub_folders) : " % (tgt_dir, name))\
            .strip().decode('utf8')

        rule_access = RuleAccess()
        new_rule = Rule(pattern=name, destination=destination or name, is_regex=False)
        rule_access.add(new_rule)

        print "notice: new rule added if name '%s' then move to '%s'" % (name, os.path.join(tgt_dir,destination or name))
        return


class Execute:
    """Move files according to rules"""

    def __init__(self, config):
        """Setup

        :type config: Config
        :param config: Application configuration
        :return:
        """
        self._config = config

    def find_all(self):
        """Find all anime in source directory (non recursive)

        :rtype Anime[]
        :returns: array of composition of compatible files with rules

        """
        matches = []

        items = os.listdir(self._config.src_dir)
        for item in items:
            item_path = os.path.join(self._config.src_dir, item)

            if os.path.isfile(item_path):
                anime = Anime.parts(item)

                if anime:
                    matches.append(anime)

        return matches

    def apply(self, anime):
        """Try to apply rule to one anime

        :type anime: Anime
        :param anime:

        :rtype Boolean
        :return: True if succeeded and a rule match
        """
        rule_access = RuleAccess()

        rule = rule_access.find_by_pattern(anime.name)
        if rule is None:
            print "warning: no rule for '%s' (run '-d' to learn new rules))" % anime.name
            return False

        # Updating record for cleanup routines
        rule_access.update_last_match(anime.name)

        full_tgt_dir = os.path.join(self._config.tgt_dir, rule.destination)
        if not os.path.exists(full_tgt_dir):
            print "notice: create folder '%s' in '%s'" % (rule.destination, self._config.tgt_dir)
            os.makedirs(full_tgt_dir)

        if not os.path.isdir(full_tgt_dir):
            print "warning: '%s' is not a directory. rule will be skipped until you fix it !" % full_tgt_dir
            return False

        full_tgt_file = os.path.join(full_tgt_dir, anime.name)
        if os.path.exists(full_tgt_file):
            print "warning: destination file '%s' already exist ! aborting..." % full_tgt_dir
            return

        full_src_file = os.path.join(self._config.src_dir, anime.fullname)
        print "notice: moving '%s' to '%s'" % (full_src_file, full_tgt_dir)
        shutil.move(full_src_file, full_tgt_dir)

        return True


class Remove:
    """Rule management operation linked to deleting"""

    def __init__(self, config):
        """Initialize remove operations

        :type config: Config
        :param config:

        :return: Nothing
        """

        self._config = config

    def remove(self, pattern):
        """Remove a rules from database by pattern

        :type pattern: String
        :param pattern:

        :rtype Boolean
        :return: Success of operation
        """
        rule_access = RuleAccess()

        rule = rule_access.find_by_pattern(pattern)
        if rule is None:
            return False

        rule_access.remove(pattern)
        return True

    def cleanup(self, days):
        """Cleanup rules older than XXX days in database

        :type days: Number
        :param days:

        :rtype Boolean
        :return Success of cleaning, If false is returned then the setting isn't enable or invalid
        """
        rules_access = RuleAccess()

        if self._config.rule_cleanup_days is None or self._config.rule_cleanup_days < 1:
            if self._config.verbose:
                print "warning: cleanup has not been set or is invalid"
            return False

        rules_access.remove_older_than(self._config.rule_cleanup_days)
        return True


class Show:
    """Display all stored rules"""

    def __init__(self, config):
        """Initialize configuration

        :type config: Config
        :param config:

        :return: Nothing
        """
        self._config = config

    def show_all(self):
        rule_access = RuleAccess()

        print "## General"
        print "Scan directory : %s" % self._config.src_dir
        print ""

        print "## Rules stored"

        rules = rule_access.get_all()
        count = 0
        for rule in rules:
            tgt_full_path = os.path.join(self._config.tgt_dir, rule.destination)

            print "Pattern '%s':" % rule.pattern
            print "* Move to: '%s' " % tgt_full_path
            print "* Last Match: %s" % rule.last_match
            print ""
            count += 1

        print "##"
        print "Total rules : %s" % count

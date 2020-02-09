# -*- coding: utf-8 -*-
"""Utils to works on file
"""
import re


class Anime:
    """Helps to works on anime filename"""

    name_regex = re.compile("^\[.*\](.*)-\s*(\d+)(?:v(\d+))?.*\.\w{3}$")
    """Parse anime name which look like...
     [<fansub name>]
     <anime name>(1)
     "-"
     <episode number> (2)
     "v"
     <revision number> (3)
     <whatever...>
     <.extension>
    """

    def __init__(self, filename):
        """Decompose an anime filename"""
        parts = Anime.name_regex.match(filename).groups()

        self.name = parts[0].strip()
        self.number = parts[1]
        self.revision = parts[2]
        self.fullname = filename

    @staticmethod
    def _is_match(filename):
        """indicate if a filename looks like an anime one"""
        if Anime.name_regex.match(filename):
            return True

        return False

    @staticmethod
    def parts(filename):
        """Factory method to get parts of filename as an anime"""
        if not Anime.name_regex.match(filename):
            return None

        return Anime(filename)
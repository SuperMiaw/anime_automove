import pkg_resources

from configobj import ConfigObj
from validate import Validator


class Config:
    """Configuration applicable to any part of program"""

    def __init__(self, path):
        """Load configuration from file
        :param path: path to the configuration file that should be loaded
        :return:
        """
        self._cfg = None

        self._load(path)

    @property
    def src_dir(self):
        """Where the file/directory should be searched"""
        return self._cfg['source']['directory']

    @property
    def tgt_dir(self):
        """Base folder of where the files should be moved to"""
        return self._cfg['target']['directory']

    @property
    def lock_file(self):
        """File that indicate the program is already running"""
        return self._cfg['global']['lock_file']

    @property
    def database_file(self):
        """Where the database should be store (sqlite)"""
        return self._cfg['global']['database_file']

    @property
    def verbose(self):
        """Indicate if more information should be printed (troubleshooting purpose)"""
        return self._cfg['global']['verbose']

    @property
    def rule_cleanup_days(self):
        """Indicate how much time a rule should be keeped
        :rtype Number
        """
        return self._cfg['global']['rule_cleanup_days']

    def _load(self, path):
        """Handle configuration loading and validation"""
        validator = Validator()

        # Note: if a raw string is passed as 'configspec' argument, 'ConfigObj' consider it as a file to open so we have
        # to make a 'list' from it
        stream = pkg_resources.resource_stream(__name__, "../res/conf.spec")
        spec = stream.read().splitlines()

        cfg = ConfigObj(path, configspec=spec, encoding='utf8')

        if not cfg.validate(validator):
            print("Invalid configuration file !")
            print(cfg.validate(validator, preserve_errors=True))

            exit(2)


        self._cfg = cfg

from datetime import date, timedelta

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, Unicode, Date, Sequence, Boolean
from sqlalchemy.orm import sessionmaker


Base = declarative_base()
Session = sessionmaker()


def init(config):
    """Setup database. If not run nothing will work properly !

    :param config:
    :return:
    """

    connection_str = 'sqlite:///' + config.database_file
    if config.verbose:
        engine = create_engine(connection_str, echo=True)
        Base.metadata.create_all(engine)
        Session.configure(bind=engine)
    else:
        engine = create_engine(connection_str, echo=False)
        Base.metadata.create_all(engine)
        Session.configure(bind=engine)


# region Database objects

class Rule(Base):
    """Describe how a rule should be"""

    __tablename__ = 'rule'
    """Table Name"""

    id = Column(Integer, Sequence('rule_id_seq'), primary_key=True)
    """Identifier"""

    pattern = Column(Unicode, nullable=False)
    """Pattern to match"""

    is_regex = Column(Boolean, nullable=False, default=False)
    """Define is pattern is a custom regex"""

    destination = Column(Unicode, nullable=False)
    """Folder where to move the file"""

    last_match = Column(Date, nullable=False, default=date.today())
    """Last time the rule was matched or created or updated"""

    def __repr__(self):
        return "<Rule(pattern='%s', is_regex='%s', destination='%s', last_match'%s')>" % (self.pattern, self.is_regex, self.destination, self.last_match)

# endregion


# region Database access

class RuleAccess:
    """Manage rule access"""

    def __init__(self):
        pass

    def add(self, rule, erase=True):
        """Add a new rule

        :type rule: Rule
        :param rule: Rule

        :rtype Rule
        :return: New created rule or updated one
        """

        session = Session()
        old_rule = self.find_by_pattern(rule.pattern)

        if old_rule is not None:
            raise Exception("Similar rule exist so you can't add it")

        session.add(rule)
        session.commit()

        return rule

    def get_all(self):
        """Recover all rules stored from database

        :rtype Rule[]
        :returns
        """
        session = Session()
        rules = session.query(Rule).order_by(Rule.pattern).all()

        return rules

    def find_by_pattern(self, pattern):
        """Return matching rule to pattern

        :type pattern: String
        :param pattern:

        :return: Matching rule
        """
        session = Session()
        rule = session.query(Rule).filter_by(pattern=pattern).first()
        """:type rule: Rule"""

        return rule

    def update_last_match(self, pattern):
        """Update last match date of the pattern

        :type pattern: String
        :param pattern:

        :rtype Boolean
        :return: Success of updating
        """
        session = Session()
        rule = session.query(Rule).filter_by(pattern=pattern).first()
        """:rtype rule: Rule"""

        if rule is None:
            return False

        rule.last_match = date.today()
        session.commit()
        return True

    def remove(self, pattern):
        """Remove an existing rule by pattern

        :type pattern: String
        :param pattern:
        :return:
        """
        session = Session()
        rule = session.query(Rule).filter_by(pattern=pattern).first()
        """:type rule: rule"""

        if rule:
            session.delete(rule)
            session.commit()
            return True

        return False

    def remove_older_than(self, days):
        """Remove all older entry that may be useless

        :type days: int
        :param days: Number of days elapsed
        """
        session = Session()
        limit = date.today() + timedelta(days=days)

        old_rules = session.query(Rule).filter(Rule.last_match >= limit)

        for rule in old_rules:
            session.delete(rule)

        session.commit()

# endregion

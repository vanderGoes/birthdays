from __future__ import unicode_literals

import re

from ..person import PersonSource


class NBASource(PersonSource):

    def split_full_name(self, force=False):
        if (not self.full_name or (self.first_name and self.last_name)) or force:
            return
        match = re.match("(?P<last_name>\w+), (?P<initials>[A-Z.]+) ?(?P<prefix>[\w\s]+)?", self.full_name)
        if match is not None:
            self.last_name = match.group("last_name")
            self.initials = match.group("initials")
            self.prefix = match.group("prefix")
        if self.prefix and self.last_name:
            self.last_name = "{} {}".format(self.prefix, self.last_name)


class BIGSource(PersonSource):
    pass


from ..person import PersonSource


class SoccerSource(PersonSource):

    def split_full_name(self):
        super(SoccerSource, self).split_full_name()
        self.initials = self.first_name if len(self.first_name) <= 20 else None
        self.first_name = None

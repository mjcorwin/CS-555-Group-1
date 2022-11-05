from datetime import datetime


class Individual:
    # Mapping of tags to instance variables
    GEDCOM_TAG_VARIABLE_MAPPING = {
        "NAME": "name",
        "SEX": "sex",
        "BIRT": "birth",
        "DEAT": "death",
        "FAMC": "family_child",
        "FAMS": "family_spouse",
    }

    # TODO: Can an individual have mulitple FAMC or FAMS records?
    def __init__(self, id):
        self.id = id
        self.name = None
        self.sex = None
        self.birth = False
        self.birth_date = None
        self.death = False
        self.death_date = None
        self.family_child = None
        self.family_spouse = None

    def track(self, level, tag, args, last_tag=None):
        # We track omitted args as a boolean flag e.g. birth, death
        args = args or True

        # Date is the only level two tag
        if level != 2:
            variable_name = self.GEDCOM_TAG_VARIABLE_MAPPING[tag]
        else:
            variable_name = self.GEDCOM_TAG_VARIABLE_MAPPING[last_tag] + "_date"
            args = datetime.strptime(args, "%d %b %Y").date()

        # Dynamically set attribute based on mapping
        setattr(self, variable_name, args)

    def age(self):
        age_date = self.death_date or datetime.now().date()

        return int(timedelta_to_years(age_date - self.birth_date))

    def alive(self):
        return self.death

    def last_name(self):
        return self.name.split("/")[1]

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        if isinstance(other, Individual):
            return self.id == other.id

        return False


def timedelta_to_years(delta):
    seconds_in_year = 365.25 * 24 * 60 * 60
    return int(delta.total_seconds() / seconds_in_year)

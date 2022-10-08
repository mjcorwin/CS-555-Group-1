from copy import deepcopy

from .family import Family
from .individual import Individual


class Parser:
    # Valid GEDCOM tags with allowed levels
    GEDCOM_TAG_LEVEL_DICT = {
        "INDI": 0,
        "NAME": 1,
        "SEX": 1,
        "BIRT": 1,
        "DEAT": 1,
        "FAMC": 1,
        "FAMS": 1,
        "FAM": 0,
        "MARR": 1,
        "HUSB": 1,
        "WIFE": 1,
        "CHIL": 1,
        "DIV": 1,
        "DATE": 2,
        "HEAD": 0,
        "TRLR": 0,
        "NOTE": 0,
    }

    def __init__(self, file):
        self.file = file
        self.individuals = {}
        self.families = {}

    def parse(self):
        last_record = None
        last_tag = None

        with open(self.file) as f:
            for line in f:
                line = line.strip()

                (level, tag, args) = self.tokenize(line)

                # For now we skip invalid records ignoring args
                # Not all tags require arguments
                if not self.is_valid(level, tag):
                    continue

                # If we see level 0, we know a record is being created or finished
                if level == 0:
                    self.save(last_record)
                    last_record = None
                    last_tag = None

                    # Create new records
                    if tag == "INDI":
                        last_record = Individual(args)
                    elif tag == "FAM":
                        last_record = Family(args)
                else:
                    last_record.track(level, tag, args, last_tag)
                    last_tag = tag

        # Save end state if no other 0 record is encountered
        self.save(last_record)

    def tokenize(self, line):
        tokens = line.split(" ", 2)
        level = int(tokens[0])
        tag = tokens[1]
        args = tokens[2] if len(tokens) == 3 else None

        if level == 0 and args in ["INDI", "FAM"]:
            tag, args = args, tag

        return (level, tag, args)

    def is_valid(self, level, tag):
        return (
            tag in self.GEDCOM_TAG_LEVEL_DICT
            and self.GEDCOM_TAG_LEVEL_DICT[tag] == level
        )

    def save(self, record):
        # If no record created yet, nothing to save
        if record:
            if isinstance(record, Individual):
                self.individuals[record.id] = deepcopy(record)
            elif isinstance(record, Family):
                self.families[record.id] = record

from datetime import datetime


class Family:
    # Mapping of tags to instance variables
    GEDCOM_TAG_VARIABLE_MAPPING = {
        "MARR": "married",
        "DIV": "divorced",
        "HUSB": "husband_id",
        "WIFE": "wife_id",
        "CHIL": "children_ids",
    }

    def __init__(self, id):
        self.id = id
        self.married = False
        self.married_date = None
        self.divorced = False
        self.divorced_date = None
        self.husband_id = None
        self.wife_id = None
        self.children_ids = []

    def track(self, level, tag, args, last_tag=None):
        # We track omitted args as a boolean flag e.g. marriage, divorce
        args = args or True

        # Date is the only level two tag
        if level != 2:
            variable_name = self.GEDCOM_TAG_VARIABLE_MAPPING[tag]
        else:
            variable_name = self.GEDCOM_TAG_VARIABLE_MAPPING[last_tag] + "_date"
            args = datetime.strptime(args, "%d %b %Y")

        # CHIL is a special tag as it is stored as a list
        if tag == "CHIL":
            self.children_ids.append(args)
        else:
            # Dynamically set attribute based on mapping
            setattr(self, variable_name, args)

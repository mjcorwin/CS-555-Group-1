from os import path
from prettytable import PrettyTable
from datetime import datetime
import copy

INPUT_FILE_PATH = path.join(path.dirname(path.realpath(__file__)), "gedcom_example.txt")
OUTPUT_FILE_PATH = path.join(path.dirname(path.realpath(__file__)), "results.txt")

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


def is_valid(level, tag):
    return tag in GEDCOM_TAG_LEVEL_DICT and GEDCOM_TAG_LEVEL_DICT[tag] == level


def parse_line(line):
    tokens = line.split(" ", 2)
    level = int(tokens[0])
    tag = tokens[1]
    args = tokens[2] if len(tokens) == 3 else ""

    if level == 0 and args in ["INDI", "FAM"]:
        tag, args = args, tag

    return (level, tag, args)


def track_individual(individual, tag, args):
    individual[tag] = args


def track_family(family, tag, args):
    family[tag] = args


def timedelta_to_years(delta):
    seconds_in_year = 365.25 * 24 * 60 * 60
    return int(delta.total_seconds() / seconds_in_year)


def individuals_to_table(individuals):
    individuals.sort(key=lambda i: i.get("ID"))

    pt = PrettyTable()
    pt.field_names = [
        "ID",
        "Name",
        "Gender",
        "Birthday",
        "Age",
        "Alive",
        "Death",
        "Child",
        "Spouse",
    ]

    pt_rows = []

    for i in individuals:
        birthday = datetime.strptime(i.get("BIRT"), "%d %b %Y")
        deathday = datetime.now()

        if i.get("DEAT"):
            deathday = datetime.strptime(i.get("DEAT"), "%d %b %Y")

        pt_rows.append(
            [
                i.get("ID"),
                i.get("NAME"),
                i.get("SEX"),
                i.get("BIRT"),
                timedelta_to_years(deathday - birthday),
                "Y" if i.get("DEAT") else "N",
                i.get("DEAT"),
                i.get("FAMC"),
                i.get("FAMS"),
            ]
        )

    pt.add_rows(pt_rows)

    return pt


def families_to_table(individuals, family_records):
    pt = PrettyTable()
    pt.field_names = [
        "ID",
        "Married",
        "Divorced",
        "Husband ID",
        "Husband Name",
        "Wife ID",
        "Wife Name",
        "Children",
    ]

    families = {}

    for i in individuals:
        family_id = i.get("FAMC") or i.get("FAMS")

        if family_id not in families:
            families[family_id] = {"ID": family_id}

        family = families[family_id]

        if "CHILDREN" not in family:
            family["CHILDREN"] = []

        # Child in family
        if i.get("FAMC"):
            family["CHILDREN"].append(i.get("ID"))

        if i.get("FAMS"):
            if i.get("SEX") == "M":
                family["HUSBAND_ID"] = i.get("ID")
                family["HUSBAND_NAME"] = i.get("NAME")

            elif i.get("SEX") == "F":
                family["WIFE_ID"] = i.get("ID")
                family["WIFE_NAME"] = i.get("NAME")

    for f in family_records:
        id = f.get("ID")
        if id in families:
            families[id]["MARRIED"] = f.get("MARR")
            families[id]["DIVORCED"] = f.get("DIV")

    family_list = list(families.values())
    family_list.sort(key=lambda f: f.get("ID"))

    for f in family_list:
        row = [
            f.get("ID"),
            f.get("MARRIED"),
            f.get("DIVORCED"),
            f.get("HUSBAND_ID"),
            f.get("HUSBAND_NAME"),
            f.get("WIFE_ID"),
            f.get("WIFE_NAME"),
            f.get("CHILDREN"),
        ]

        pt.add_row(row)

    return pt


def main():
    individual = {}
    individuals = []

    family = {}
    families = []

    with open(INPUT_FILE_PATH) as infile:
        last_tag = None

        for line in infile:
            line = line.strip()

            (level, tag, args) = parse_line(line)

            # For now we skip invalid records
            if not is_valid(level, tag):
                continue

            # If we see another level 0, we know the individual or family record is finished
            if individual and level == 0:
                individuals.append(copy.deepcopy(individual))
                individual = {}
                last_tag = None

            elif family and level == 0:
                families.append(copy.deepcopy(family))
                family = {}
                last_tag = None

            # If we see an individual start tracking information
            if tag == "INDI":
                individual = {"ID": args}
            elif tag == "FAM":
                family = {"ID": args}

            if individual:
                if level == 1:
                    track_individual(individual, tag, args)
                elif level == 2:
                    track_individual(individual, f"{last_tag}", args)

            elif family:
                if level == 1:
                    track_family(family, tag, args)
                elif level == 2:
                    track_family(family, f"{last_tag}", args)

            last_tag = tag

    with open("gedcom_results.txt", "w") as outfile:
        individual_table = individuals_to_table(individuals)
        family_table = families_to_table(individuals, families)

        outfile.write("INDIVIDUALS\n")
        outfile.write(individual_table.get_string())
        outfile.write("\nFAMILIES\n")
        outfile.write(family_table.get_string())


if __name__ == "__main__":
    main()

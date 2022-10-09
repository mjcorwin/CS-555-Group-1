from prettytable import PrettyTable
from datetime import datetime

SECONDS_IN_YEAR = 365.25 * 24 * 60 * 60
DATE_FORMAT = "%Y-%m-%d"


def print_individuals(individuals, sort=True):
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

    for i in individuals:
        pt.add_row(
            [
                i.id,
                i.name,
                i.sex,
                datetime.strftime(i.birth_date, DATE_FORMAT),
                i.age(),
                i.alive(),
                datetime.strftime(i.death_date, DATE_FORMAT) if i.death_date else "N/A",
                f"{{'{i.family_child}'}}" if i.family_child else "N/A",
                f"{{'{i.family_spouse}'}}" if i.family_spouse else "N/A",
            ]
        )

    if sort:
        pt.sortby = "ID"

    return pt.get_string()


def print_families(families, individuals, sort=True):
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

    for f in families:
        husband = individuals[f.husband_id]
        wife = individuals[f.wife_id]

        children = ", ".join([f"'{id}'" for id in sorted(f.children_ids)])

        pt.add_row(
            [
                f.id,
                datetime.strftime(f.married_date, DATE_FORMAT),
                f.divorced,
                husband.id,
                husband.name,
                wife.id,
                wife.name,
                f"{{{children}}}",
            ]
        )

    if sort:
        pt.sortby = "ID"

    return pt.get_string()


def timedelta_to_years(delta):
    seconds_in_year = 365.25 * 24 * 60 * 60
    return int(delta.total_seconds() / seconds_in_year)

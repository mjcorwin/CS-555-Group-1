from prettytable import PrettyTable
from enum import Enum

US13_Problems = []

class EUS13_FAILURE(Enum):
    US13_FAIL_BIRTHDAYS_GT_2_DAYS_LT_8_MONTHS = 0


class cUS13_Failure:
    hSibling = None
    tSibling = None
    Failure_Type = None

    def __init__(self):
        self.hSibling = None
        self.tSibling = None
        self.Failure_Type = None


def US13_Test(hParser):
    US13_Problems.clear()

    for family in hParser.families.values():
        children = []

        for child_id in family.children_ids:
            children.append(hParser.individuals[child_id])

        for i in range(0, len(children) - 1):
            for j in range(i + 1, len(children) - 1):
                sibling1 = children[i]
                sibling2 = children[j]

                # initialize siblings birthdays
                hSiblingDate1 = sibling1.birth_date
                tSiblingDate2 = sibling2.birth_date


                # Initialize >= 3 days and <= 8 months to output anomalies
                daysDelta = (hSiblingDate1 - tSiblingDate2).days
                monthsDelta = (hSiblingDate1.year - tSiblingDate2.year) * 12 + hSiblingDate1.month - tSiblingDate2.month

                if daysDelta >= 2 and monthsDelta <= 8:
                    NewFailureEntry = cUS13_Failure()
                    NewFailureEntry.hSibling = sibling1
                    NewFailureEntry.tSibling = sibling2
                    NewFailureEntry.Failure_Type = (
                        EUS13_FAILURE.US13_FAIL_BIRTHDAYS_GT_2_DAYS_LT_8_MONTHS
                    )

                    US13_Problems.append(NewFailureEntry)


def US13_DisplayResults(hParser):
    print("")
    print("US13 test failures:")

    pt = PrettyTable()
    pt.field_names = [
        "Sibling A ID",
        "Sibling A Birthday",
        "Sibling B ID",
        "Sibling B Birthday",
        "Siblings Birthday Difference (Days)",
        "Failure type",
    ]

    for i in US13_Problems:
        pt.add_row(
            [
                i.hSibling.id,
                i.hSibling.birth_date,
                i.tSibling.id,
                i.tSibling.birth_date,
                (i.hSibling.birth_date - i.tSibling.birth_date).days,
                str(i.Failure_Type),
            ]
        )

    print(pt.get_string())
    return pt.get_string()


def Execute(hParser):
    US13_Test(hParser)
    return US13_DisplayResults(hParser)

from datetime import date
from prettytable import PrettyTable
from gedcom.individual import *
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


def US13_Days(date1, date2):
    return (date1 - date2).days


def US13_Months(date1, date2):
    return (date1.year - date2.year) * 12 + date1.month - date2.month

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

                hSiblingDate1 = sibling1.birth_date
                tSiblingDate2 = sibling2.birth_date

                #Bad Smell #1: (refactor): abstract difference of days/months via functions
                daysDelta = US13_Days(hSiblingDate1, tSiblingDate2)
                monthsDelta = US13_Months(hSiblingDate1, tSiblingDate2)

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
        #Bad Smell #4 (refactor): abstain from repetitive usage;
        sibling_A_ID = i.hSibling.id
        sibling_A_DOB = i.hSibling.birth_date

        sibling_B_ID = i.tSibling.id
        sibling_B_DOB = i.tSibling.birth_date

        diff_A_B_DOB = US13_Days(sibling_A_DOB, sibling_B_DOB)
        pt.add_row(
            [
                sibling_A_ID,
                sibling_A_DOB,
                sibling_B_ID,
                sibling_B_DOB,
                diff_A_B_DOB,
                str(i.Failure_Type),
            ]
        )

    print(pt.get_string())
    return pt.get_string()


def Execute(hParser):
    US13_Test(hParser)
    return US13_DisplayResults(hParser)

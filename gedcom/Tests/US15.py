from datetime import datetime
from datetime import date
from gedcom import individual
from prettytable import PrettyTable
from enum import Enum

DATE_FORMAT = "%Y-%m-%d"

#  US08: Children should be born after marriage of parents
# (and not more than 9 months after their divorce)

US15_Problems = {}


class EUS15_FAILURE(Enum):
    US15_FAIL_GT_EQ_15 = 0  # Child found that was born before marriage
    # US15 = (1,)  # Child found that has no birth
    # US08_FAIL_AF_DIVR = 2  # Child found that was born beyond 9 months of divorce


class cUS15_Failure:
    hIndividual = None
    hFamily = None
    Failure_Type = None

    def __init__(self):
        self.hIndividual = None
        self.hFamily = None
        self.Failure_Type = None


def US15_Test(hParser):
    US15_Problems.clear()

    for i in hParser.families:
        hFamily = hParser.families[i]
        if len(hFamily.children_ids) >= 15:
            NewFailureEntry = cUS15_Failure()
            NewFailureEntry.hFamily = hFamily
            NewFailureEntry.Failure_Type = EUS15_FAILURE.US15_FAIL_GT_EQ_15

            US15_Problems[len(US15_Problems)] = NewFailureEntry


def US15_DisplayResults():
    print("")
    print("US15 test failures:")

    pt = PrettyTable()
    pt.field_names = [
        "Family ID",
        "Child Count",
        "Data failure type",
    ]
    for i in US15_Problems:
        pt.add_row(
            [
                US15_Problems[i].hFamily.id,
                len(US15_Problems[i].hFamily.children_ids),
                str(US15_Problems[i].Failure_Type),
            ]
        )

    pt.sortby = "Family ID"

    print(pt.get_string())
    return pt.get_string()


def Execute(hParser):
    US15_Test(hParser)
    return US15_DisplayResults()

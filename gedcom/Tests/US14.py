"""
        US: Multiple births <= 5
        Story Description: No more than five siblings should be born at the same time
"""

from datetime import datetime
from gedcom import individual
from prettytable import PrettyTable;
from enum import Enum

SECONDS_IN_YEAR = 365.25 * 24 * 60 * 60;
DATE_FORMAT = "%Y-%m-%d";

US14_Problems = []
class EUS14_FAILURE(Enum):
    # Individuals
    US14_FAIL_SIBLINGS_BIRTH_GT_5 = 0

class cUS14_Failure:
    hSibling = None
    tSibling = None
    Failure_Type = None;

    def __init__(self):
        self.hSibling = None
        self.tSibling = None
        self.Failure_Type = None;

def US14_Test(hParser):
    US14_Problems.clear();

    count = 0

    for family in hParser.families.values():
        siblings = []

        for sib_id in family.children_ids:
            siblings.append(hParser.individuals[sib_id])

        for i in range(0, len(siblings) - 1):
            for j in range(i + 1, len(siblings) - 1):
                sibling = siblings[i]
                sibling2 = siblings[j]

                sibBirthday = sibling.birth_date
                sibBirthday2 = sibling2.birth_date

                if sibBirthday == sibBirthday2:
                    count = count + 1
                    if count > 5:
                        NewFailureEntry = cUS14_Failure()
                        NewFailureEntry.hSibling = sibling
                        NewFailureEntry.tSibling = sibling2
                        NewFailureEntry.Failure_Type = (
                            EUS14_FAILURE.US14_FAIL_SIBLINGS_BIRTH_GT_5
                        )

                        US14_Problems.append(NewFailureEntry)


def US14_DisplayResults(hParser):
    result = 0

    print ("");
    print ("US14 test failures:");

    pt = PrettyTable();
    pt.field_names = [
        "Sibling A and B Names",
        "Sibling A and B Birthdays",
        "Multiple births > 5",
        "Data failure type"
    ];

    for i in US14_Problems:

        siblingADOB = i.hSibling.birth_date
        siblingBDOB = i.tSibling.birth_date

        siblingAID = i.hSibling.id
        siblingBID = i.tSibling.id

        while siblingAID != siblingBID:
            if siblingADOB == siblingBDOB:
                result += 1
                if US14_Problems.count((siblingADOB, siblingBDOB)) > 5:
                    return result
            break

        pt.add_row(
            [
                (i.hSibling.name, i.tSibling.name),
                (datetime.strftime(i.hSibling.birth_date, DATE_FORMAT), datetime.strftime(i.tSibling.birth_date, DATE_FORMAT)),
                result,
                str(i.Failure_Type)
            ]
        );

    print (pt.get_string());
    return pt.get_string();
    

def Execute(hParser):
    US14_Test(hParser);
    return US14_DisplayResults(hParser);
"""
    US30: List living married
    US30 - Story Description: List all living married peple in a GEDCOM file
    Expected anomaly output: Return all dead married people in a GEDCOM file.
"""

from datetime import datetime
from gedcom import individual, family
from prettytable import PrettyTable;
from enum import Enum

SECONDS_IN_YEAR = 365.25 * 24 * 60 * 60;
DATE_FORMAT = "%Y-%m-%d";

US30_Problems = []

class EUS30_FAILURE(Enum):
    # Individuals
    US30_FAIL_DEAD_MARRIED_PEOPLE = 0

class cUS30_Failure:
    hFamily = None
    hIndividual = None
    Failure_Type = None;

    def __init__(self):
        self.hFamily = None
        self.hIndividual = None
        self.Failure_Type = None;

def US30_Test(hParser):
    US30_Problems.clear();

    for family in hParser.families.values():
        hFamily = family
        for individual in hParser.individuals.values():
            hIndividual = individual
            if (hFamily.married == True and hIndividual.death == True):
                NewFailureEntry = cUS30_Failure()
                NewFailureEntry.hFamily = hFamily
                NewFailureEntry.hIndividual = hIndividual
                NewFailureEntry.Failure_Type = (
                    EUS30_FAILURE.US30_FAIL_DEAD_MARRIED_PEOPLE
                )

                US30_Problems.append(NewFailureEntry)


def US30_DisplayResults(hParser):

    print ("");
    print ("US30 test failures:");

    pt = PrettyTable();
    pt.field_names = [
        "Dead Married People",
        "Data failure type"
    ];

    for i in US30_Problems:

        dead_married_people = (i.hIndividual.name if (i.hFamily.married == True and i.hIndividual.death == True) else 1)
        
        pt.add_row(
            [
                dead_married_people,
                str(i.Failure_Type)
            ]
        );

    print (pt.get_string());
    return pt.get_string();

def Execute(hParser):
    US30_Test(hParser);
    return US30_DisplayResults(hParser);
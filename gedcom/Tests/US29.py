"""
    US29: List deceased
    US29 - Story Description: List all deceased individuals in a GEDCOM file
    Expected anomaly output: Return all living individuals in a GEDCOM file.
"""

from datetime import datetime
from gedcom import individual, family
from prettytable import PrettyTable;
from enum import Enum

SECONDS_IN_YEAR = 365.25 * 24 * 60 * 60;
DATE_FORMAT = "%Y-%m-%d";

US29_Problems = []

class EUS29_FAILURE(Enum):
    # Individuals
    US29_FAIL_LIVING_INDIVIDUALS = 0

class cUS29_Failure:
    hIndividual = None
    Failure_Type = None;

    def __init__(self):
        self.hIndividual = None
        self.Failure_Type = None;

def US29_Test(hParser):
    US29_Problems.clear();

    for individual in hParser.individuals.values():
        hIndividual = individual
        if (hIndividual.birth == True and hIndividual.death == False):
            NewFailureEntry = cUS29_Failure()
            NewFailureEntry.hIndividual = hIndividual
            NewFailureEntry.Failure_Type = (
                EUS29_FAILURE.US29_FAIL_LIVING_INDIVIDUALS
            )

            US29_Problems.append(NewFailureEntry)


def US29_DisplayResults(hParser):

    print ("");
    print ("US29 test failures:");

    pt = PrettyTable();
    pt.field_names = [
        "Living Individuals",
        "Data failure type"
    ];

    for i in US29_Problems:

        living_individuals = (i.hIndividual.name if i.hIndividual.birth == True and i.hIndividual.death == False else 1)
        
        pt.add_row(
            [
                living_individuals,
                str(i.Failure_Type)
            ]
        );

    print (pt.get_string());
    return pt.get_string();

def Execute(hParser):
    US29_Test(hParser);
    return US29_DisplayResults(hParser);
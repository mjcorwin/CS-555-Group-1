"""
    US21: Correct gender for role
    US21 - Story Description: Husband in family should be male and wife in family should be female
    Expected anomaly output: Return incorrect gender for role; Husband in family should return femaile and wife in family should return male
"""

from datetime import datetime
from gedcom import individual, family
from prettytable import PrettyTable;
from enum import Enum

SECONDS_IN_YEAR = 365.25 * 24 * 60 * 60;
DATE_FORMAT = "%Y-%m-%d";

US21_Problems = []


class EUS21_FAILURE(Enum):
    # Individuals
    US21_FAIL_INVALID_GENDER_ROLES = 0

class cUS21_Failure:
    hFamily = None
    hIndividual = None
    Failure_Type = None;

    def __init__(self):
        self.hFamily = None
        self.hIndividual = None
        self.Failure_Type = None;

def US21_Test(hParser):
    US21_Problems.clear();

    for family in hParser.families.values():
        hFamily = family
        for individual in hParser.individuals.values():
            hIndividual = individual
            if (hIndividual.id == hFamily.husband_id and hIndividual.sex != 'M' or (hIndividual.id == hFamily.wife_id and hIndividual.sex != 'F')):
                    NewFailureEntry = cUS21_Failure()
                    NewFailureEntry.hFamily = hFamily
                    NewFailureEntry.hIndividual = hIndividual
                    NewFailureEntry.Failure_Type = (
                        EUS21_FAILURE.US21_FAIL_INVALID_GENDER_ROLES
                    )

                    US21_Problems.append(NewFailureEntry)


def US21_DisplayResults(hParser):

    print ("");
    print ("US21 test failures:");

    pt = PrettyTable();
    pt.field_names = [
        "Wife ID",
        "Husband ID",
        "Incorrect Gender Role",
        "Data failure type"
    ];

    for i in US21_Problems:


        wife = i.hFamily.wife_id
        husband = i.hFamily.husband_id

        IncorrectGender = (wife if i.hIndividual.sex != 'F' else husband if i.hIndividual.sex != 'M' else 1)

        pt.add_row(
            [
                wife,
                husband,
                IncorrectGender,
                str(i.Failure_Type)
            ]
        );

    print (pt.get_string());
    return pt.get_string();
    

def Execute(hParser):
    US21_Test(hParser);
    return US21_DisplayResults(hParser);
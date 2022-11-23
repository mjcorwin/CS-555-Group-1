from datetime import datetime;
from gedcom import individual;
from gedcom import family
from prettytable import PrettyTable

from enum import Enum

#Include person's current age when listing individuals

#Failure - REspond if persons age is not included

US27_Problems = []

class EUS27_FAILURE(Enum):
    # Individuals
    US27_FAIL_NO_AGE = 0

class cUS27_Failure:
    hIndividual = None
    Failure_Type = None;

    def __init__(self):
        self.hIndividual = None
        self.Failure_Type = None;

def US27_Test(hParser):
    US27_Problems.clear();
    for individual in hParser.individuals.values():
        hIndividual = individual
        if hIndividual.birth_date == None or hIndividual.birth == False:
            NewFailureEntry = cUS27_Failure()
            NewFailureEntry.hIndividual = hIndividual
            NewFailureEntry.Failure_Type = (
                EUS27_FAILURE.US27_FAIL_NO_AGE
            )

            US27_Problems.append(NewFailureEntry)
    
def US27_DisplayResults(hParser):

    print ("");
    print ("US27 test failures:");

    pt = PrettyTable();
    pt.field_names = [
        "Living Individuals",
        "Data failure type"
    ];

    for i in US27_Problems:
        
        pt.add_row(
            [
                US27_Problems[i].hIndividual.name,
                str(US27_Problems[i].Failure_Type)
            ]
        );

    print (pt.get_string());
    return pt.get_string();

def Execute(hParser):
    US27_Test(hParser);
    return US27_DisplayResults(hParser);

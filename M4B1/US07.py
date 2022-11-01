from unittest import TestCase;
from datetime import datetime;
from datetime import date;
from gedcom import individual;
from prettytable import PrettyTable;
from enum import Enum;

#US: Less then 150 years old

DATE_FORMAT = "%Y-%m-%d";

global US07_Problems;
class EUS07_FAILURE(Enum):
    US07_FAIL_GT_150 = 0,
    US07_FAIL_NO_BIRTH = 1

class cUS07_Failure:
    hIndividual = None;
    Failure_Type = None;

    def __init__(self):
        self.hIndividual = None;
        self.Failure_Type = None;

def US07_Test(hParser):
    global US07_Problems;
    US07_Problems = {};
    US07_Problems.clear();

    for i in hParser.individuals:
        hIndividual = hParser.individuals[i]
        if (hIndividual.birth == True and hIndividual.death == False):
            #print (str((date.today() - hIndividual.birth_date).days))
            #150 years * 365 = 54750 days + 37 leap year days [[150/4 rounded down]]
            if((date.today() - hIndividual.birth_date).days >= 54787):
                NewFailureEntry = cUS07_Failure();
                NewFailureEntry.hIndividual = hIndividual
                NewFailureEntry.Failure_Type = EUS07_FAILURE.US07_FAIL_GT_150;

                US07_Problems[len(US07_Problems)] = NewFailureEntry;
        elif (hIndividual.birth == True and hIndividual.death == True):
            #print (str(hIndividual.death_date.year - hIndividual.birth_date.year))
            if((hIndividual.death_date - hIndividual.birth_date).days >= 54787):
                NewFailureEntry = cUS07_Failure();
                NewFailureEntry.hIndividual = hIndividual
                NewFailureEntry.Failure_Type = EUS07_FAILURE.US07_FAIL_GT_150;

                US07_Problems[len(US07_Problems)] = NewFailureEntry;
        else:
            NewFailureEntry = cUS07_Failure();
            NewFailureEntry.hIndividual = hIndividual;
            NewFailureEntry.Failure_Type = EUS07_FAILURE.US07_FAIL_NO_BIRTH;

            US07_Problems[len(US07_Problems)] = NewFailureEntry;

def US07_DisplayResults():
    global US07_Problems;
    print ("");
    print ("US07 test failures:");

    pt = PrettyTable();
    pt.field_names = [
        "ID",
        "Name",
        "Birthday",
        "Data failure type"
    ];

    for i in US07_Problems:
        pt.add_row(
            [
                US07_Problems[i].hIndividual.id,
                US07_Problems[i].hIndividual.name,
                datetime.strftime(US07_Problems[i].hIndividual.birth_date, DATE_FORMAT) if US07_Problems[i].hIndividual.birth_date else "",
                str(US07_Problems[i].Failure_Type)
            ]
        );

    pt.sortby = "ID"
    print(pt.get_string());
    return pt.get_string();

def Execute(hParser):
    US07_Test(hParser);
    return US07_DisplayResults();

def ExecuteTests(hParser):
    US07_Test(hParser)
    return US07_Problems
    
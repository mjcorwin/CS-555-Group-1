from datetime import datetime
from gedcom import individual
from prettytable import PrettyTable;
from enum import Enum

SECONDS_IN_YEAR = 365.25 * 24 * 60 * 60;
DATE_FORMAT = "%Y-%m-%d";

global US05_Problems;
global US05_Problems2;
class EUS05_FAILURE(Enum):
    # Families
    US05_FAIL_MARRIAGE_LT_DEATH = 0,
    US05_FAIL_NO_MARRIAGE = 1,
    US05_FAIL_NO_MARRIAGE_NO_DEATH = 2

    # Individuals
    US05_FAIL_BIRTH_GT_DEATH = 0,
    US05_FAIL_NO_BIRTH = 1,
    US05_FAIL_NO_BIRTH_NO_DEATH = 2

class cUS05_Failure:
    hIndividual = None;
    hFamily = None
    Failure_Type = None;

    def __init__(self):
        self.hIndividual = None;
        self.hFamily = None;
        self.Failure_Type = None;

def US05_Test(hParser):
    global US05_Problems;
    global US05_Problems2;

    US05_Problems = {}
    US05_Problems.clear()

    US05_Problems2 = {}
    US05_Problems2.clear()


    for i in hParser.families:
        hFamily = hParser.families[i]

        for j in hParser.individuals:
            hIndividual = hParser.individuals[j]

            if (hFamily.married == True):
                if (hIndividual.death == True):
                    if ( (hFamily.married_date - hIndividual.death_date).days > 0):
                        NewFailureEntry = cUS05_Failure();
                        NewFailureEntry.hIndividual = hIndividual;
                        NewFailureEntry.Failure_Type = EUS05_FAILURE.US05_FAIL_MARRIAGE_LT_DEATH;

                        US05_Problems[len(US05_Problems)] = NewFailureEntry;
                        US05_Problems2[len(US05_Problems2)] = NewFailureEntry;

            else:
                if (hFamily.divorced == True):
                    NewFailureEntry = cUS05_Failure();
                    NewFailureEntry.hFamily = hFamily;
                    NewFailureEntry.Failure_Type = EUS05_FAILURE.US05_FAIL_BIRTH_GT_DEATH;


        else:
            NewFailureEntry = cUS05_Failure();
            NewFailureEntry.hFamily = hFamily;
            NewFailureEntry.Failure_Type = EUS05_FAILURE.US05_FAIL_NO_MARRIAGE_NO_DEATH;

            US05_Problems[len(US05_Problems)] = NewFailureEntry;


    for i in hParser.individuals:
        hIndividual = hParser.individuals[i]

        if (hIndividual.birth == True):
            if(hIndividual.death == True):
                if ( (hIndividual.birth_date - hIndividual.death_date).days > 0):
                    NewFailureEntry = cUS05_Failure();
                    NewFailureEntry.hIndividual = hIndividual;
                    NewFailureEntry.Failure_Type = EUS05_FAILURE.US05_FAIL_BIRTH_GT_DEATH;

                    US05_Problems2[len(US05_Problems2)] = NewFailureEntry;

        else:
            NewFailureEntry = cUS05_Failure();
            NewFailureEntry.hIndividual = hIndividual;
            NewFailureEntry.Failure_Type = EUS05_FAILURE.US05_FAIL_NO_BIRTH_NO_DEATH;

            US05_Problems2[len(US05_Problems2)] = NewFailureEntry;



def US05_DisplayResults():
    global US05_Problems;
    global US05_Problems2;

    print ("");
    print ("US05 test failures:");

    pt = PrettyTable();
    pt.field_names = [
        "ID",
        "INDVIDUAL ID",
        "Marriage Date",
        "Date of death",
        "Data failure type"
    ];

    for i in US05_Problems and US05_Problems2:
        pt.add_row(
            [
                US05_Problems[i].hFamily.id,
                US05_Problems2[i].hIndividual.id,
                datetime.strftime(US05_Problems[i].hFamily.married_date, DATE_FORMAT) if US05_Problems[i].hFamily.married_date else "",
                datetime.strftime(US05_Problems2[i].hIndividual.death_date, DATE_FORMAT) if US05_Problems2[i].hIndividual.death_date else "",
                str(US05_Problems2[i].Failure_Type)
            ]
        );

    pt.sortby = "ID"

    print (pt.get_string());
    return pt.get_string();

def Execute(hParser):
    US05_Test(hParser);
    return US05_DisplayResults();



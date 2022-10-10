from datetime import datetime
from gedcom import individual
from prettytable import PrettyTable;
from enum import Enum

SECONDS_IN_YEAR = 365.25 * 24 * 60 * 60;
DATE_FORMAT = "%Y-%m-%d";

global US06_Problems;
global US06_Problems2;
class EUS06_FAILURE(Enum):
    US06_FAIL_DIVORCE_GT_EQ_DEATH = 0,
    US06_FAIL_NO_DIVORCE = 1,
    US06_FAIL_NO_DIVORCE_NO_DEATH = 2

class cUS06_Failure:
    hIndividual = None;
    hFamily = None
    Failure_Type = None;

    def __init__(self):
        self.hIndividual = None;
        self.hFamily = None;
        self.Failure_Type = None;

def US06_Test(hParser):
    global US06_Problems;
    global US06_Problems2;


    US06_Problems = {}
    US06_Problems.clear()

    US06_Problems2 = {}
    US06_Problems2.clear()


    for i in hParser.individuals:
        hIndividual = hParser.individuals[i]

        for j in hParser.families:
            hFamily = hParser.families[j]

            if (hFamily.divorced == True):
                if(hIndividual.death == True):
                    if ( (hFamily.divorced_date - hIndividual.death_date).days > 0):
                        NewFailureEntry = cUS06_Failure();
                        NewFailureEntry.hFamily = hFamily;
                        NewFailureEntry.Failure_Type = EUS06_FAILURE.US06_FAIL_DIVORCE_GT_EQ_DEATH;

                        US06_Problems[len(US06_Problems)] = NewFailureEntry;

            else:
            # No birth...
                if (hFamily.married == True):
                    NewFailureEntry = cUS06_Failure();
                    NewFailureEntry.hFamily = hFamily;
                    NewFailureEntry.Failure_Type = EUS06_FAILURE.US06_FAIL_NO_DIVORCE;

                    US06_Problems[len(US06_Problems)] = NewFailureEntry;

        else:
            NewFailureEntry = cUS06_Failure();
            NewFailureEntry.hFamily = hFamily;
            NewFailureEntry.Failure_Type = EUS06_FAILURE.US06_FAIL_NO_DIVORCE_NO_DEATH;

            US06_Problems[len(US06_Problems)] = NewFailureEntry;

    for i in hParser.individuals:
        hIndividual = hParser.individuals[i]

        if (hIndividual.birth == True):
            if(hIndividual.death == True):
                if ( (hIndividual.birth_date - hIndividual.death_date).days > 0):
                    NewFailureEntry = cUS06_Failure();
                    NewFailureEntry.hIndividual = hIndividual;
                    NewFailureEntry.Failure_Type = EUS06_FAILURE.US06_FAIL_DIVORCE_GT_EQ_DEATH;

                    US06_Problems2[len(US06_Problems2)] = NewFailureEntry;

        else:
        # No Birth
            if (hIndividual.death == True):
                NewFailureEntry = cUS06_Failure();
                NewFailureEntry.hIndividual = hIndividual;
                NewFailureEntry.Failure_Type = EUS06_FAILURE.US06_FAIL_NO_DIVORCE;

                US06_Problems2[len(US06_Problems2)] = NewFailureEntry;

    else:
        NewFailureEntry = cUS06_Failure();
        NewFailureEntry.hIndividual = hIndividual;
        NewFailureEntry.Failure_Type = EUS06_FAILURE.US06_FAIL_NO_DIVORCE_NO_DEATH;

        US06_Problems2[len(US06_Problems2)] = NewFailureEntry;



def US06_DisplayResults():
    global US06_Problems;

    print ("");
    print ("US06 test failures:");

    pt = PrettyTable();
    pt.field_names = [
        "ID",
        "INDIVIDUAL ID",
        "Date of Divorce",
        "Date of death",
        "Data failure type"
    ];

    for i in US06_Problems and US06_Problems2:
        pt.add_row(
            [
                US06_Problems[i].hFamily.id,
                US06_Problems2[i].hIndividual.id,
                datetime.strftime(US06_Problems[i].hFamily.divorced_date, DATE_FORMAT) if US06_Problems[i].hFamily.divorced_date else "",
                datetime.strftime(US06_Problems2[i].hIndividual.death_date, DATE_FORMAT) if US06_Problems2[i].hIndividual.death_date else "",
                str(US06_Problems2[i].Failure_Type)
            ]
        );

    pt.sortby = "ID"

    print (pt.get_string());
    return pt.get_string();

def Execute(hParser):
    US06_Test(hParser);
    return US06_DisplayResults();
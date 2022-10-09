from datetime import datetime
from gedcom import individual;
from prettytable import PrettyTable;

from enum import Enum;

SECONDS_IN_YEAR = 365.25 * 24 * 60 * 60;
DATE_FORMAT = "%Y-%m-%d";

global US03_Problems;
class EUS03_FAILURE(Enum):
    US03_FAIL_BIRTH_GT_DEATH = 0,
    US03_FAIL_NO_BIRTH = 1,
    US03_FAIL_NO_BIRTH_NO_DEATH = 2

class cUS03_Failure:
    hIndividual = None;
    Failure_Type = None;

    def __init__(self):
        self.hIndividual = None;
        self.Failure_Type = None;

def US03_Test(hParser):
    global US03_Problems;

    US03_Problems = {};
    US03_Problems.clear();

    for i in hParser.individuals:
        hIndividual = hParser.individuals[i];

        if (hIndividual.birth == True):
            if (hIndividual.death == True):
                #print (str((hIndividual.birth_date - hIndividual.death_date).days) + " birth date > death date!");
                if ( (hIndividual.birth_date - hIndividual.death_date).days > 0):
                    NewFailureEntry = cUS03_Failure();
                    NewFailureEntry.hIndividual = hIndividual;
                    NewFailureEntry.Failure_Type = EUS03_FAILURE.US03_FAIL_BIRTH_GT_DEATH;

                    US03_Problems[len(US03_Problems)] = NewFailureEntry;
        else:
            # No birth...
            if (hIndividual.death == True):
                #print (str("Date of death present with no birth date!"));
                NewFailureEntry = cUS03_Failure();
                NewFailureEntry.hIndividual = hIndividual;
                NewFailureEntry.Failure_Type = EUS03_FAILURE.US03_FAIL_NO_BIRTH;

                US03_Problems[len(US03_Problems)] = NewFailureEntry;
            else:
                #print ("Neither birth date nor death date is present!")
                NewFailureEntry = cUS03_Failure();
                NewFailureEntry.hIndividual = hIndividual;
                NewFailureEntry.Failure_Type = EUS03_FAILURE.US03_FAIL_NO_BIRTH_NO_DEATH;

                US03_Problems[len(US03_Problems)] = NewFailureEntry;

def US03_DisplayResults():
    global US03_Problems;

    print ("");
    print ("US03 test failures:");

    pt = PrettyTable();
    pt.field_names = [
        "ID",
        "Name",
        "Birthday",
        "Date of death",
        "Data failure type"
    ];

    for i in US03_Problems:
        pt.add_row(
            [
                US03_Problems[i].hIndividual.id,
                US03_Problems[i].hIndividual.name,
                datetime.strftime(US03_Problems[i].hIndividual.birth_date, DATE_FORMAT) if US03_Problems[i].hIndividual.birth_date else "",
                datetime.strftime(US03_Problems[i].hIndividual.death_date, DATE_FORMAT) if US03_Problems[i].hIndividual.death_date else "",
                str(US03_Problems[i].Failure_Type)
            ]
        );

    pt.sortby = "ID"

    print (pt.get_string());
    return pt.get_string();

def Execute(hParser):
    US03_Test(hParser);
    return US03_DisplayResults();
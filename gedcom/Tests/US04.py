from datetime import datetime
from gedcom import family;
from prettytable import PrettyTable;

from enum import Enum;

SECONDS_IN_YEAR = 365.25 * 24 * 60 * 60;
DATE_FORMAT = "%Y-%m-%d";

global US04_Problems;
class EUS04_FAILURE(Enum):
    US04_FAIL_MARRIED_GT_DIVORCED = 0,
    US04_FAIL_NO_MARRIED = 1,
    US04_FAIL_NO_MARRIED_NO_DIVORCED = 2

class cUS04_Failure:
    hFamily = None;
    Failure_Type = None;

    def __init__(self):
        self.hFamily = None;
        self.Failure_Type = None;

def US04_Test(hParser):
    global US04_Problems;

    US04_Problems = {};
    US04_Problems.clear();

    for i in hParser.families:
        hFamily = hParser.families[i];

        if (hFamily.married == True):
            if (hFamily.divorced == True):
                #print (str((hFamily.married_date - hFamily.divorced_date).days) + " married_date date > divorced_date date!");
                if ( (hFamily.married_date - hFamily.divorced_date).days > 0):
                    NewFailureEntry = cUS04_Failure();
                    NewFailureEntry.hFamily = hFamily;
                    NewFailureEntry.Failure_Type = EUS04_FAILURE.US04_FAIL_MARRIED_GT_DIVORCED;

                    US04_Problems[len(US04_Problems)] = NewFailureEntry;
        else:
            # No married date...
            if (hFamily.divorced == True):
                #print (str("Date of divorced present with no marriage date!"));
                NewFailureEntry = cUS04_Failure();
                NewFailureEntry.hFamily = hFamily;
                NewFailureEntry.Failure_Type = EUS04_FAILURE.US04_FAIL_NO_MARRIED;

                US04_Problems[len(US04_Problems)] = NewFailureEntry;
            else:
                #print ("Neither marriage nor divorced date is present!")
                NewFailureEntry = cUS04_Failure();
                NewFailureEntry.hFamily = hFamily;
                NewFailureEntry.Failure_Type = EUS04_FAILURE.US04_FAIL_NO_MARRIED_NO_DIVORCED;

                US04_Problems[len(US04_Problems)] = NewFailureEntry;

def US04_DisplayResults():
    global US04_Problems;

    print ("");
    print ("US04 test failures:");

    pt = PrettyTable();
    pt.field_names = [
        "ID",
        "Marriage date",
        "Divorced date",
        "Data failure type"
    ];

    for i in US04_Problems:
        pt.add_row(
            [
                US04_Problems[i].hFamily.id,
                datetime.strftime(US04_Problems[i].hFamily.married_date, DATE_FORMAT) if US04_Problems[i].hFamily.married_date else "",
                datetime.strftime(US04_Problems[i].hFamily.divorced_date, DATE_FORMAT) if US04_Problems[i].hFamily.divorced_date else "",
                str(US04_Problems[i].Failure_Type)
            ]
        );

    pt.sortby = "ID"

    print (pt.get_string());
    return pt.get_string();

def Execute(hParser):
    US04_Test(hParser);
    return US04_DisplayResults();
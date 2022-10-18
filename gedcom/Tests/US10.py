#US 10
# Marriage should be at least 14 years after birth of both spouses (parents must be at least 14 years old)
# Reqs - 
# # Wife & Husband age must be > 14 
# Marriage date - birth date > 14 for husband and wife
# no birth date
# no marriage date
# marriage date cannot be in future

from datetime import datetime;
from datetime import date;
from gedcom import individual;
from prettytable import PrettyTable;
from enum import Enum;

#US: Less then 150 years old

DATE_FORMAT = "%Y-%m-%d";

global US10_Problems;
class EUS10_FAILURE(Enum):
    US10_FAIL_NO_WIFHUB = 0,
    US10_FAIL_NO_MARRIAGE = 1,
    US10_FAIL_FUT_MARRIAGE = 2,
    US10_FAIL_HUSB_AGE = 3,
    US10_FAIL_WIFE_AGE = 4

class cUS10_Failure:
    hIndividual = None;
    Failure_Type = None;

    def __init__(self):
        self.hIndividual = None;
        self.Failure_Type = None;

def US10_Test(hParser):
    global US10_Problems;
    US10_Problems = {};
    US10_Problems.clear();

    for i in hParser.families:
        hFamily = hParser.families[i]

        if (hFamily.married == True):
            husb = None;
            wife = None;
            #Code optimization from pair programming! yippee
            husb= hParser.individuals[hParser.families[i].husband_id]
            wife = hParser.individuals[hParser.families[i].wife_id]
            if (wife == None or husb == None or husb == wife):
                NewFailureEntry = cUS10_Failure();
                NewFailureEntry.hFamily = hFamily;
                NewFailureEntry.Failure_Type = EUS10_FAILURE.US10_FAIL_NO_WIFHUB;
                US10_Problems[len(US10_Problems)] = NewFailureEntry;
            #if no marriage date
            elif hFamily.married_date == None:
                NewFailureEntry = cUS10_Failure();
                NewFailureEntry.hFamily = hFamily;
                NewFailureEntry.Failure_Type = EUS10_FAILURE.US10_FAIL_NO_MARRIAGE
                US10_Problems[len(US10_Problems)] = NewFailureEntry;
            #if wedding date is in future
            elif (hFamily.married_date - date.today()).days > 0:
                NewFailureEntry = cUS10_Failure();
                NewFailureEntry.hFamily = hFamily;
                NewFailureEntry.Failure_Type = EUS10_FAILURE.US10_FAIL_FUT_MARRIAGE
                US10_Problems[len(US10_Problems)] = NewFailureEntry;
            #if husband is married when less than 14
            elif (hFamily.married_date - husb.birth_date).days < 5113:
                NewFailureEntry = cUS10_Failure();
                NewFailureEntry.hFamily = hFamily;
                NewFailureEntry.Failure_Type = EUS10_FAILURE.US10_FAIL_HUSB_AGE
                US10_Problems[len(US10_Problems)] = NewFailureEntry;
            #if wife is married when less than 14
            elif (hFamily.married_date - wife.birth_date).days < 5113:
                NewFailureEntry = cUS10_Failure();
                NewFailureEntry.hFamily = hFamily;
                NewFailureEntry.Failure_Type = EUS10_FAILURE.US10_FAIL_WIFE_AGE
                US10_Problems[len(US10_Problems)] = NewFailureEntry;


def US10_DisplayResults():
    global US10_Problems;

    print ("");
    print ("US10 test failures:");

    pt = PrettyTable();
    pt.field_names = [
        "Family ID",
        "Marriage Date",
        "Husband ID",
        "Wife ID",
        "Data failure type"
    ];
    for i in US10_Problems:
        pt.add_row(
            [
                US10_Problems[i].hFamily.id,
                datetime.strftime(US10_Problems[i].hFamily.married_date, DATE_FORMAT) if US10_Problems[i].hFamily.married_date else "",
                US10_Problems[i].hFamily.husband_id,
                US10_Problems[i].hFamily.wife_id,
                str(US10_Problems[i].Failure_Type)
            ]
        );

    pt.sortby = "Family ID"

    print (pt.get_string());
    return pt.get_string();

def Execute(hParser):
    US10_Test(hParser);
    return US10_DisplayResults();
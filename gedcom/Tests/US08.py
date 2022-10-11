#TODO
from datetime import datetime;
from datetime import date;
from gedcom import individual;
from prettytable import PrettyTable;
from enum import Enum;

DATE_FORMAT = "%Y-%m-%d";

#  US08: Children should be born after marriage of parents 
# (and not more than 9 months after their divorce)

global US08_Problems;
class EUS08_FAILURE(Enum):
    US08_FAIL_BIRTH_BF_MARR = 0, #Child found that was born before marriage
    US08_FAIL_NO_BIRTH = 1, #Child found that has no birth
    US08_FAIL_AF_DIVR = 2 #Child found that was born beyond 9 months of divorce

class cUS08_Failure:
    hIndividual = None;
    hFamily = None;
    Failure_Type = None;

    def __init__(self):
        self.hIndividual = None;
        self.hFamily = None;
        self.Failure_Type = None;

def US08_Test(hParser):
    global US08_Problems;
    US08_Problems = {};
    US08_Problems.clear();
    
    for i in hParser.families:
        hFamily = hParser.families[i]

        if (hFamily.married == True):
            for cID in hFamily.children_ids:
                child = None;
                for i in hParser.individuals:
                    if cID == hParser.individuals[i].id:
                        child = hParser.individuals[i]
                if (child.birth == False):
                    NewFailureEntry = cUS08_Failure();
                    NewFailureEntry.hFamily = hFamily;
                    NewFailureEntry.hIndividual = child;
                    NewFailureEntry.Failure_Type = EUS08_FAILURE.US08_FAIL_NO_BIRTH;
                elif (child.birth_date - hFamily.married_date).days < 0:
                    NewFailureEntry = cUS08_Failure();
                    NewFailureEntry.hFamily = hFamily;
                    NewFailureEntry.hIndividual = child;
                    NewFailureEntry.Failure_Type = EUS08_FAILURE.US08_FAIL_BIRTH_BF_MARR;

                    US08_Problems[len(US08_Problems)] = NewFailureEntry;
                
                elif (hFamily.divorced == True):
                    if (child.birth_date - hFamily.divorced_date).days > 273:
                        NewFailureEntry = cUS08_Failure();
                        NewFailureEntry.hFamily = hFamily;
                        NewFailureEntry.hIndividual = child;
                        NewFailureEntry.Failure_Type = EUS08_FAILURE.US08_FAIL_AF_DIVR;

                        US08_Problems[len(US08_Problems)] = NewFailureEntry;



def US08_DisplayResults():
    global US08_Problems;

    print ("");
    print ("US08 test failures:");

    pt = PrettyTable();
    pt.field_names = [
        "Family ID",
        "Marriage Date",
        "Divorce Date",
        "Child ID",
        "Child Birth Date",
        "Data failure type"
    ];
    for i in US08_Problems:
        pt.add_row(
            [
                US08_Problems[i].hFamily.id,
                datetime.strftime(US08_Problems[i].hFamily.married_date, DATE_FORMAT) if US08_Problems[i].hFamily.married_date else "",
                datetime.strftime(US08_Problems[i].hFamily.divorced_date, DATE_FORMAT) if US08_Problems[i].hFamily.divorced_date else "",
                US08_Problems[i].hIndividual.name,
                datetime.strftime(US08_Problems[i].hIndividual.birth_date, DATE_FORMAT) if US08_Problems[i].hIndividual.birth_date else "",
                str(US08_Problems[i].Failure_Type)
            ]
        );

    pt.sortby = "Family ID"

    print (pt.get_string());
    return pt.get_string();

def Execute(hParser):
    US08_Test(hParser);
    return US08_DisplayResults();
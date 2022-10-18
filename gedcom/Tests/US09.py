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
    US09_FAIL_DEAD_MOM = 0, #Child found that was born after death of mother
    US09_FAIL_NO_BIRTH = 1, #Child found that has no birth
    US09_FAIL_DEAD_DAD = 2 #Child found that was born no more than 9 months after death of father

class cUS09_Failure:
    hIndividual = None;
    hFamily = None;
    Failure_Type = None;

    def __init__(self):
        self.hIndividual = None;
        self.hFamily = None;
        self.Failure_Type = None;

def US09_Test(hParser):
    global US09_Problems;
    US09_Problems = {};
    US09_Problems.clear();
    
    for i in hParser.families:
        hFamily = hParser.families[i]

        if (hFamily.married == True):
            for cID in hFamily.children_ids:
                child = None;
                for i in hParser.individuals:
                    if cID == hParser.individuals[i].id:
                        child = hParser.individuals[i]
                if (child.birth == False):
                    NewFailureEntry = cUS09_Failure();
                    NewFailureEntry.hFamily = hFamily;
                    NewFailureEntry.hIndividual = child;
                    NewFailureEntry.Failure_Type = EUS09_FAILURE.US09_FAIL_NO_BIRTH;
                #TODO Get Mom ID
                mom = None;
                dad = None;
                for i in hParser.individuals:
                    if hFamily.wife_id == hParser.individuals[i].id:
                        mom = hParser.individuals[i]
                for i in hParser.individuals:
                    if hFamily.husband_id == hParser.individuals[i].id:
                        dad = hParser.individuals[i]
                if (mom == None and dad == None):
                    break;
                elif ((child.birth_date -  mom.death_date).days < 0):
                    NewFailureEntry = 
                if (child.birth_date - hFamily.married_date).days < 0:
                    NewFailureEntry = cUS09_Failure();
                    NewFailureEntry.hFamily = hFamily;
                    NewFailureEntry.hIndividual = child;
                    NewFailureEntry.Failure_Type = EUS09_FAILURE.US09_FAIL_BIRTH_BF_MARR;

                    US09_Problems[len(US09_Problems)] = NewFailureEntry;
                
                elif (hFamily.divorced == True):
                    if (child.birth_date - hFamily.divorced_date).days > 273:
                        NewFailureEntry = cUS09_Failure();
                        NewFailureEntry.hFamily = hFamily;
                        NewFailureEntry.hIndividual = child;
                        NewFailureEntry.Failure_Type = EUS09_FAILURE.US09_FAIL_AF_DIVR;

                        US09_Problems[len(US09_Problems)] = NewFailureEntry;



def US09_DisplayResults():
    global US09_Problems;

    print ("");
    print ("US09 test failures:");

    pt = PrettyTable();
    pt.field_names = [
        "Family ID",
        "Marriage Date",
        "Divorce Date",
        "Child ID",
        "Child Birth Date",
        "Data failure type"
    ];
    for i in US09_Problems:
        pt.add_row(
            [
                US09_Problems[i].hFamily.id,
                datetime.strftime(US09_Problems[i].hFamily.married_date, DATE_FORMAT) if US09_Problems[i].hFamily.married_date else "",
                datetime.strftime(US09_Problems[i].hFamily.divorced_date, DATE_FORMAT) if US09_Problems[i].hFamily.divorced_date else "",
                US09_Problems[i].hIndividual.name,
                datetime.strftime(US09_Problems[i].hIndividual.birth_date, DATE_FORMAT) if US09_Problems[i].hIndividual.birth_date else "",
                str(US09_Problems[i].Failure_Type)
            ]
        );

    pt.sortby = "Family ID"

    print (pt.get_string());
    return pt.get_string();

def Execute(hParser):
    US09_Test(hParser);
    return US09_DisplayResults();
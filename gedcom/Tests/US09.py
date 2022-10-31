#TODO
from datetime import datetime;
from datetime import date;
from gedcom import individual;
from prettytable import PrettyTable;
from enum import Enum;

DATE_FORMAT = "%Y-%m-%d";

#  US08: Children should be born after marriage of parents 
# (and not more than 9 months after their divorce)

global US09_Problems;
class EUS09_FAILURE(Enum):
    US09_FAIL_NO_BIRTH = 0, #Child found that has no birth 
    US09_FAIL_DEAD_MOM = 1, #Child found that was born after death of mother
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
                if not child.birth:
                        NewFailureEntry = cUS09_Failure();
                        NewFailureEntry.hFamily = hFamily;
                        NewFailureEntry.hIndividual = child;
                        NewFailureEntry.Failure_Type = EUS09_FAILURE.US09_FAIL_NO_BIRTH;
                        US09_Problems[len(US09_Problems)] = NewFailureEntry;
                if mom != None and mom.death == True:
                    if ((child.birth_date - mom.death_date).days > 0):
                        NewFailureEntry = cUS09_Failure();
                        NewFailureEntry.hFamily = hFamily;
                        NewFailureEntry.hIndividual = child;
                        NewFailureEntry.Failure_Type = EUS09_FAILURE.US09_FAIL_DEAD_MOM;
                        US09_Problems[len(US09_Problems)] = NewFailureEntry;
                if dad != None and dad.death == True:
                    if ((child.birth_date - dad.death_date).days > 274):
                            NewFailureEntry = cUS09_Failure();
                            NewFailureEntry.hFamily = hFamily;
                            NewFailureEntry.hIndividual = child;
                            NewFailureEntry.Failure_Type = EUS09_FAILURE.US09_FAIL_DEAD_DAD;
                            US09_Problems[len(US09_Problems)] = NewFailureEntry;
                



def US09_DisplayResults():
    

    print ("");
    print ("US09 test failures:");

    pt = PrettyTable();
    pt.field_names = [
        "Family ID",
        "Child ID",
        "Child Birth Date",
        "Dad ID",
        "Mom ID",
        "Data failure type"
    ];
    for i in US09_Problems:
        pt.add_row(
            [
                US09_Problems[i].hFamily.id,
                US09_Problems[i].hIndividual.id,
                datetime.strftime(US09_Problems[i].hIndividual.birth_date, DATE_FORMAT) if US09_Problems[i].hIndividual.birth_date else "",
                US09_Problems[i].hFamily.husband_id,
                US09_Problems[i].hFamily.wife_id,
                str(US09_Problems[i].Failure_Type)
            ]
        );

    pt.sortby = "Family ID"

    print (pt.get_string());
    return pt.get_string();

def Execute(hParser):
    US09_Test(hParser);
    return US09_DisplayResults();

def ExecuteTests(hParser):
    US09_Test(hParser)
    return US09_Problems
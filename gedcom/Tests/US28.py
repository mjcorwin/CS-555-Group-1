from datetime import datetime;
from gedcom import individual;
from gedcom import family
from prettytable import PrettyTable
from datetime import date

from enum import Enum

#Include person's current age when listing individuals

#Failure - REspond if persons age is not included

US28_Problems = []

class EUS28_FAILURE(Enum):
    # Individuals
    US28_FAIL_BAD_ORDER = 0

class cUS28_Failure:
    oldest = None,
    youngest  = None
    Failure_Type = None;

    def __init__(self):
        self.oldest = None;
        self.youngest = None;
        self.Failure_Type = None;

def age(birthdate):
    today = date.today()
    age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))
    return age

def Sort_Tuple(tup):
    # getting length of list of tuples
    lst = len(tup)
    for i in range(0, lst):
        for j in range(0, lst-i-1):
            if (tup[j][1] > tup[j + 1][1]):
                temp = tup[j]
                tup[j]= tup[j + 1]
                tup[j + 1]= temp
    return tup


def US28_Test(hParser):
    US28_Problems.clear();
    young = 99999999;
    old = 0;
    tup_array = []
    for individual in hParser.individuals.values():
        ind_age = None
        if individual.birth_date == None: ind_age = -1
        else: 
            ind_age = age(individual.birth_date)
            if young > ind_age:
                young = ind_age
            if old < ind_age:
                old = ind_age
        tup_array.append((individual.name, ind_age))
    
    sorted_array = Sort_Tuple(tup_array)
    if sorted_array != tup_array:
        NewFailureEntry = cUS28_Failure()
        NewFailureEntry.oldest = old;
        NewFailureEntry.youngest = young;
        NewFailureEntry.Failure_Type = (
            EUS28_FAILURE.US28_FAIL_NO_AGE
        )

        US28_Problems.append(NewFailureEntry)
    
def US28_DisplayResults(hParser):

    print ("");
    print ("US28 test failures:");

    pt = PrettyTable();
    pt.field_names = [
        "Failure Type",
        "Youngest",
        "Oldest"
    ];

    for i in US28_Problems:

        pt.add_row(
            [
                str(i.Failure_Type),
                i.youngest,
                i.oldest
            ]
        );

    print (pt.get_string());
    return pt.get_string();

def Execute(hParser):
    US28_Test(hParser);
    return US28_DisplayResults(hParser);
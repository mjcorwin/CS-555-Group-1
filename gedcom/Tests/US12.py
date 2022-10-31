from datetime import datetime
from gedcom import individual;
from gedcom import family;
from prettytable import PrettyTable;

from enum import Enum;

SECONDS_IN_YEAR = 365.25 * 24 * 60 * 60;
DATE_FORMAT = "%Y-%m-%d";

global US12_Problems;
class EUS12_FAILURE(Enum):
    US12_FAIL_FATHER_TOOOLD = 0,
    US12_FAIL_MOTHER_TOOOLD = 1,
    US12_FAIL_BOTHPARENTS_TOOOLD = 2

class cUS12_Failure:
    hFamily = None;

    Failure_Type = None;

    def __init__(self):
        self.hFamily = {};
        self.Failure_Type = None;

def US12_ex(Individuals, Families):
    global US12_Problems;

    US12_Problems = [];
    US12_Problems.clear();

    for i in Families:
        if (len(Families[i].children_ids) > 0):
            Father = Individuals[Families[i].husband_id];
            Mother = Individuals[Families[i].wife_id];

            US12_Failure = cUS12_Failure();
            
            for j in Families[i].children_ids:
                Child = Individuals[j];

                # Note: This does not take into account leap years! Relativedelta module could be used for that but that's
                #       an external dependency.
                FatherDifference = (Child.birth_date - Father.birth_date).days / 365;
                MotherDifference = (Child.birth_date - Mother.birth_date).days / 365;

                if (FatherDifference > 79):
                    US12_Failure.hFamily = Families[i];
                    US12_Failure.Failure_Type = EUS12_FAILURE.US12_FAIL_FATHER_TOOOLD;

                if (MotherDifference > 59):
                    US12_Failure.hFamily = Families[i];
                    if (US12_Failure.Failure_Type == EUS12_FAILURE.US12_FAIL_FATHER_TOOOLD):
                        US12_Failure.Failure_Type = EUS12_FAILURE.US12_FAIL_BOTHPARENTS_TOOOLD;
                    else:
                        US12_Failure.Failure_Type = EUS12_FAILURE.US12_FAIL_MOTHER_TOOOLD;

            if (US12_Failure.Failure_Type != None):
                US12_Problems.append(US12_Failure);

    return US12_Problems;

def US12(hParser):
    US12_ex(hParser.individuals, hParser.families);


def US12_DisplayResults(hParser):
    global US12_Problems;

    print ("");
    print ("US12 test failures:");

    pt = PrettyTable();
    pt.field_names = [
        "Family ID",
        "Father ID",
        "Father",
        "Mother ID",
        "Mother",
        "Failure type"
    ];

    #for i in US12_Problems:
    for i in range(0, len(US12_Problems)):
        familyID = US12_Problems[i].hFamily.id;
        FatherID = hParser.families[familyID].husband_id;
        MotherID = hParser.families[familyID].wife_id;

        pt.add_row(
            [
                familyID,
                FatherID,
                hParser.individuals[FatherID].name,
                MotherID,
                hParser.individuals[MotherID].name,
                str(US12_Problems[i].Failure_Type)
            ]
        );

    #pt.sortby = "ID"

    print (pt.get_string());
    return pt.get_string();

def Execute(hParser):
    US12(hParser);
    return US12_DisplayResults(hParser);
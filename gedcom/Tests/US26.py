from datetime import datetime;
from gedcom import individual;
from gedcom import family
from prettytable import PrettyTable

from enum import Enum

SECONDS_IN_YEAR = 365.25 * 24 * 60 * 60
DATE_FORMAT = "%Y-%m-%d"


# US26 - Corresponding entries


global hParser;
global US26_Problems;

global TempIndividuals;
global TempFamilies;



class EUS26_FAILURE(Enum):
    US26_FAIL_NO_FAMILY_WITH_CHILDID = 0,
    US26_FAIL_NO_FAMILY_WITH_SPOUSEID = 1


class cUS26_Failure:
    hIndividual = None;
    Failure_Type = None;

    def __init__(self):
        self.hIndividual = None;
        self.Failure_Type = None;


def Get_Individual(Individuals, IndividualID):
    iIdx = 0;
    hRetVal = None;
    bContinueLoop = True;

    if (len(Individuals) < 1):
        bContinueLoop = False;

    while (bContinueLoop == True):
        if ( (Individuals[iIdx]).id == IndividualID):
            hRetVal = Individuals[iIdx];
            bContinueLoop = False;
        else:
            iIdx += 1;
            if (iIdx > len(Individuals) - 1):
                bContinueLoop = False;

    return hRetVal;

def Get_Family(Families, FamilyID):
    iIdx = 0;
    hRetVal = None;
    bContinueLoop = True;

    if (len(Families) < 1):
        bContinueLoop = False;
        iIdx = -1;

    while (bContinueLoop == True):
        if ( (Families[iIdx]).id == FamilyID):
            hRetVal = Families[iIdx];
            bContinueLoop = False;
        else:
            iIdx += 1;
            if (iIdx > len(Families) - 1):
                bContinueLoop = False;

    return hRetVal;

def Get_FamilyMembership(Families, Id):
    hRetVal = [];
    bContinueLoop = True;

    for i in Families:
        if ( (i.husband_id == Id) or (i.wife_id == Id) or (Id in i.children_ids) ):
            hRetVal.append(i);

    return hRetVal;


def US26_ex(Individuals, Families):
    global US26_Problems

    US26_Problems = [];
    US26_Problems.clear();


    TempIndividuals = [];
    TempIndividuals.clear();

    TempFamilies = [];
    TempFamilies.clear();


    iIdx = 0;
    for x in Individuals.items():
        TempIndividuals.append(x[1]);
        iIdx += 1;

    iIdx = 0;
    for x in Families.items():
        TempFamilies.append(x[1]);
        iIdx += 1;


    for i in Individuals.items():
        hIndiv = i[1];

        if (hIndiv.family_child != None):
            # Individual is a child of a family, so get the family that the child is -supposed- to be a child of first
            hFamily = Get_Family(TempFamilies, hIndiv.family_child);
            if ( (hIndiv.id not in hFamily.children_ids) ):
                US26_Failure = cUS26_Failure();

                US26_Failure.hIndividual = hIndiv;
                US26_Failure.Failure_Type = EUS26_FAILURE.US26_FAIL_NO_FAMILY_WITH_CHILDID;

                US26_Problems.append(US26_Failure);

        if (hIndiv.family_spouse != None):
            hFamily = Get_Family(TempFamilies, hIndiv.family_spouse);
            if ( (hIndiv.id != hFamily.husband_id) and (hIndiv.id != hFamily.wife_id) ):
                US26_Failure = cUS26_Failure();

                US26_Failure.hIndividual = hIndiv;
                US26_Failure.Failure_Type = EUS26_FAILURE.US26_FAIL_NO_FAMILY_WITH_SPOUSEID;

                US26_Problems.append(US26_Failure);



def US26(hParser):
    US26_ex(hParser.individuals, hParser.families);

def US26_DisplayResults():
    global US26_Problems;

    print("");
    print("US26 test failures:");

    pt = PrettyTable();
    pt.field_names = ["ID 1", "Name 1", "Failure type"];

    # for i in US26_Problems:
    for i in range(0, len(US26_Problems)):
        pt.add_row(
            [
                US26_Problems[i].hIndividual.id,
                US26_Problems[i].hIndividual.name,
                US26_Problems[i].Failure_Type,
            ]
        );

    print(pt.get_string());
    return pt.get_string();

def Execute(hParser):
    US26(hParser);
    return US26_DisplayResults();

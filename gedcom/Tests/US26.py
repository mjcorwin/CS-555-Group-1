from datetime import datetime;
from gedcom import individual;
from gedcom import family
from prettytable import PrettyTable

from enum import Enum

SECONDS_IN_YEAR = 365.25 * 24 * 60 * 60
DATE_FORMAT = "%Y-%m-%d"


# US17 - No Marriages to descendants


global hParser;
global US17_Problems;

global TempIndividuals;
global TempFamilies;



class EUS17_FAILURE(Enum):
    US17_FAIL_HUSB_MARRTODESC = 0,
    US17_FAIL_WIFE_MARRTODESC = 1


class cUS17_Failure:
    hIndividual = None;
    SpouseIDs = None;
    FamilyID = None;

    Failure_Type = None;

    def __init__(self):
        self.hIndividual = None;
        self.SpouseIDs = [];
        self.FamilyID = "";
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
        if ( (i.husband_id == Id) or (i.wife_id == Id) ):
            hRetVal.append(i);

    return hRetVal;
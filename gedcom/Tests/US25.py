from datetime import datetime;
from gedcom import individual;
from gedcom import family
from prettytable import PrettyTable

from enum import Enum

SECONDS_IN_YEAR = 365.25 * 24 * 60 * 60
DATE_FORMAT = "%Y-%m-%d"


# US25 - Unique first names in families


global hParser;
global US25_Problems;

global TempIndividuals;
global TempFamilies;



class EUS25_FAILURE(Enum):
    # Conditions:
    #   Child first name matches other child first name
    #
    #   Child first name matches father (the HUSB member) first name
    #   Child first name matches mother (the WIFE member) first name
    #
    #   Father (the HUSB member) matches child first name
    #   Father (the HUSB member) matches Mother (the WIFE member) first name
    #
    #   Mother (the WIFE member) matches child first name
    #   Mother (the WIFE member) matches Father (the HUSB member) first name

    US25_FAIL_CHILD_FNAME_MATCHES_CHILD_FNAME = 0,

    US25_FAIL_CHILD_FNAME_MATCHES_FATHER_FNAME = 1,
    US25_FAIL_CHILD_FNAME_MATCHES_MOTHER_FNAME = 2,

    US25_FAIL_FATHER_FNAME_MATCHES_CHILD_FNAME = 3,
    US25_FAIL_FATHER_FNAME_MATCHES_MOTHER_FNAME = 4,

    US25_FAIL_MOTHER_FNAME_MATCHES_CHILD_FNAME = 5,
    US25_FAIL_MOTHER_FNAME_MATCHES_FATHER_FNAME = 6

class EFAMILIALSTATUS(Enum):
    FAMILIALSTATUS_UNKNOWN  = -1,
    FAMILIALSTATUS_NONE     = 0,
    FAMILIALSTATUS_CHILD    = 1,
    FAMILIALSTATUS_FATHER   = 2,
    FAMILIALSTATUS_MOTHER   = 3

class cUS25_Failure:
    hIndividual_1 = None;
    hIndividual_2 = None;

    Individual_1_Status = None;
    Individual_2_Status = None;

    Failure_Type = None;

    def __init__(self):
        self.hIndividual_1 = None;
        self.hIndividual_2 = None;

        self.Individual_1_Status = None;
        self.Individual_2_Status = None;

        self.Failure_Type = "None";


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

# US25 - Unique first names in families
def US25_ex(Individuals, Families):
    global US25_Problems;

    US25_Problems = [];
    US25_Problems.clear();


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


    for i in Families.items():
        hFamily = i[1];
        hFather = Get_Individual(TempIndividuals, hFamily.husband_id);
        Father_FName = hFather.name[0:hFather.name.find(" ")];

        hMother = Get_Individual(TempIndividuals, hFamily.wife_id);
        Mother_FName = hMother.name[0:hMother.name.find(" ")];

        for childID in hFamily.children_ids:
            Child1 = Get_Individual(TempIndividuals, childID);
            Child1_FName = Child1.name[0:Child1.name.find(" ")];

            # Create a 2nd list without the first item (the childID loop)
            ChildrenIDs_NewList = [x for x in hFamily.children_ids if x != childID];

            for childID2 in ChildrenIDs_NewList:
                Child2 = Get_Individual(TempIndividuals, childID2);
                Child2_FName = Child2.name[0:Child2.name.find(" ")];

                if (Child1_FName == Child2_FName):
                    US25_Failure = cUS25_Failure();

                    US25_Failure.hIndividual_1 = Child1;
                    US25_Failure.hIndividual_2 = Child2;

                    US25_Failure.Individual_1_Status = EFAMILIALSTATUS.FAMILIALSTATUS_CHILD;
                    US25_Failure.Individual_2_Status = EFAMILIALSTATUS.FAMILIALSTATUS_CHILD;

                    US25_Failure.Failure_Type = EUS25_FAILURE.US25_FAIL_CHILD_FNAME_MATCHES_CHILD_FNAME;

                    US25_Problems.append(US25_Failure);

            if (Child1_FName == Father_FName):
                US25_Failure = cUS25_Failure();

                US25_Failure.hIndividual_1 = Child1;
                US25_Failure.hIndividual_2 = hFather;

                US25_Failure.Individual_1_Status = EFAMILIALSTATUS.FAMILIALSTATUS_CHILD;
                US25_Failure.Individual_2_Status = EFAMILIALSTATUS.FAMILIALSTATUS_FATHER;

                US25_Failure.Failure_Type = EUS25_FAILURE.US25_FAIL_CHILD_FNAME_MATCHES_FATHER_FNAME;

                US25_Problems.append(US25_Failure);



                US25_Failure = cUS25_Failure();

                US25_Failure.hIndividual_1 = hFather;
                US25_Failure.hIndividual_2 = Child1;

                US25_Failure.Individual_1_Status = EFAMILIALSTATUS.FAMILIALSTATUS_FATHER;
                US25_Failure.Individual_2_Status = EFAMILIALSTATUS.FAMILIALSTATUS_CHILD;

                US25_Failure.Failure_Type = EUS25_FAILURE.US25_FAIL_FATHER_FNAME_MATCHES_CHILD_FNAME;

                US25_Problems.append(US25_Failure);



            if (Child1_FName == Mother_FName):
                US25_Failure = cUS25_Failure();

                US25_Failure.hIndividual_1 = Child1;
                US25_Failure.hIndividual_2 = hMother;

                US25_Failure.Individual_1_Status = EFAMILIALSTATUS.FAMILIALSTATUS_CHILD;
                US25_Failure.Individual_2_Status = EFAMILIALSTATUS.FAMILIALSTATUS_MOTHER;

                US25_Failure.Failure_Type = EUS25_FAILURE.US25_FAIL_CHILD_FNAME_MATCHES_MOTHER_FNAME;

                US25_Problems.append(US25_Failure);



                US25_Failure = cUS25_Failure();

                US25_Failure.hIndividual_1 = hMother;
                US25_Failure.hIndividual_2 = Child1;

                US25_Failure.Individual_1_Status = EFAMILIALSTATUS.FAMILIALSTATUS_MOTHER;
                US25_Failure.Individual_2_Status = EFAMILIALSTATUS.FAMILIALSTATUS_CHILD;

                US25_Failure.Failure_Type = EUS25_FAILURE.US25_FAIL_MOTHER_FNAME_MATCHES_CHILD_FNAME;

                US25_Problems.append(US25_Failure);

        if (Father_FName == Mother_FName):
            US25_Failure = cUS25_Failure();

            US25_Failure.hIndividual_1 = hFather;
            US25_Failure.hIndividual_2 = hMother;

            US25_Failure.Individual_1_Status = EFAMILIALSTATUS.FAMILIALSTATUS_FATHER;
            US25_Failure.Individual_2_Status = EFAMILIALSTATUS.FAMILIALSTATUS_MOTHER;

            US25_Failure.Failure_Type = EUS25_FAILURE.US25_FAIL_FATHER_FNAME_MATCHES_MOTHER_FNAME;

            US25_Problems.append(US25_Failure);



            US25_Failure = cUS25_Failure();

            US25_Failure.hIndividual_1 = hMother;
            US25_Failure.hIndividual_2 = hFather;

            US25_Failure.Individual_1_Status = EFAMILIALSTATUS.FAMILIALSTATUS_MOTHER;
            US25_Failure.Individual_2_Status = EFAMILIALSTATUS.FAMILIALSTATUS_FATHER;

            US25_Failure.Failure_Type = EUS25_FAILURE.US25_FAIL_MOTHER_FNAME_MATCHES_FATHER_FNAME;

            US25_Problems.append(US25_Failure);



def US25(hParser):
    US25_ex(hParser.individuals, hParser.families);


def US25_DisplayResults():
    global US25_Problems;

    print("");
    print("US25 test failures:");

    pt = PrettyTable();
    pt.field_names = ["ID 1", "Name 1", "Familial status 1", "ID 2", "Name 2", "Familial status 2", "Failure type"];

    # for i in US25_Problems:
    for i in range(0, len(US25_Problems)):
        pt.add_row(
            [
                US25_Problems[i].hIndividual_1.id,
                US25_Problems[i].hIndividual_1.name,
                US25_Problems[i].Individual_1_Status,
                US25_Problems[i].hIndividual_2.id,
                US25_Problems[i].hIndividual_2.name,
                US25_Problems[i].Individual_2_Status,
                US25_Problems[i].Failure_Type,
            ]
        );

    print(pt.get_string());
    return pt.get_string();

def Execute(hParser):
    US25(hParser);
    return US25_DisplayResults();
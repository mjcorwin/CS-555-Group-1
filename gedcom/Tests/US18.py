from datetime import datetime
from gedcom import individual;
from gedcom import family;
from prettytable import PrettyTable;

from enum import Enum;

SECONDS_IN_YEAR = 365.25 * 24 * 60 * 60;
DATE_FORMAT = "%Y-%m-%d";


# US18 - No sibling marriages


global hParser;
global US18_Problems;

global TempIndividuals;
global TempFamilies;



class EUS18_FAILURE(Enum):
    US18_FAIL_SIBLING_MARRIAGE = 0



class cUS18_Failure:
    SpouseIDs = None;
    FamilyID = None;


    Failure_Type = None;

    def __init__(self):
        self.hFamily = {};
        self.SpouseIDs = [];
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

def Get_FamilyMembershipByParent(Families, Id):
    hRetVal = [];
    bContinueLoop = True;

    for i in Families:
        if ( (i.husband_id == Id) or (i.wife_id == Id) ):
            hRetVal.append(i);

    return hRetVal;


def US18_ex(Individuals, Families):
    global US18_Problems;

    global TempIndividuals;
    global TempFamilies;


    US18_Problems = [];
    US18_Problems.clear();

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


    for i in range(0, len(TempFamilies)):
        if (len(TempFamilies[i].children_ids) > 1):
            for j in range(0, len(TempFamilies[i].children_ids)):
                Child1 = Get_Individual(TempIndividuals, TempFamilies[i].children_ids[j]);
                Child1FamilyMemberships = Get_FamilyMembershipByParent(TempFamilies, Child1.id);

                for j2 in range(0, len(Child1FamilyMemberships)):
                    for k in range(j + 1, len(TempFamilies[i].children_ids)):
                        Child2 = Get_Individual(TempIndividuals, TempFamilies[i].children_ids[k]);
                        Child2FamilyMemberships = Get_FamilyMembershipByParent(TempFamilies, Child2.id);

                        hFamily = Get_Family(TempFamilies, Child1FamilyMemberships[j2].id);
                        for k2 in range(0, len(Child2FamilyMemberships)):
                            hFamily2 = Get_Family(TempFamilies, Child2FamilyMemberships[k2].id);
                            if (hFamily.id == hFamily2.id):
                                US18_Fault = cUS18_Failure();
                                US18_Fault.Failure_Type = EUS18_FAILURE.US18_FAIL_SIBLING_MARRIAGE;
                                US18_Fault.FamilyID = hFamily.id;
                                US18_Fault.SpouseIDs.append(Get_Individual(TempIndividuals, Child1.id));
                                US18_Fault.SpouseIDs.append(Get_Individual(TempIndividuals, Child2.id));
                                US18_Problems.append(US18_Fault);

    return US18_Problems;


def US18(hParser):
    US18_ex(hParser.individuals, hParser.families);


def US18_DisplayResults(hParser):
    global US18_Problems;

    print("");
    print("US18 test failures:");

    pt = PrettyTable();
    pt.field_names = ["Family ID", "Spouses", "Failure type"];

    # for i in US18_Problems:
    for i in range(0, len(US18_Problems)):
        Spouses = "";
        for j in range(0, len(US18_Problems[i].SpouseIDs)):
            Spouses = Spouses + (US18_Problems[i].SpouseIDs[j].name) + " (" + US18_Problems[i].SpouseIDs[j].id + "), ";

        Spouses = Spouses[:-2];

        pt.add_row(
            [
                US18_Problems[i].FamilyID,
                Spouses,
                str(US18_Problems[i].Failure_Type),
            ]
        );

    # pt.sortby = "ID"

    print(pt.get_string());
    return pt.get_string();


def Execute(hParser):
    US18(hParser);
    return US18_DisplayResults(hParser);
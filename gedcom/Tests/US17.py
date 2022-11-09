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

def Check_Husband(Husband, CheckFamilies):
    global US17_Problems;

    global TempIndividuals;
    #global TempFamilies;

    # Used to add a breakpoint just prior to the for loop, upon entering a recursive call to this function
    dbgBreakpoint = True;

    # First, grab a husband from a family    
    for j in CheckFamilies:
        if (len(j.children_ids) > 0):

            # Next, iterate over each child
            for k in j.children_ids:
                Child = Get_Individual(TempIndividuals, k);

                #FamiliyMembership = Get_FamilyMembership(Families, hChildren_IDs[k]);
                FamilyMembership = Get_FamilyMembership(TempFamilies, Child.id);
                if (len(FamilyMembership) > 0):

                    # Keep propigating the same Husband object to the next recursive call!
                    FamilyEntered = Check_Wife(Husband, FamilyMembership);

                    #if ( (FamilyEntered.husband_id == Husband.id) and (FamilyEntered.wife_id == Child.id) ):
                    if ( (FamilyEntered.wife_id == Child.id) and (j.husband_id == Husband.id) ):
                        US17_Failure_HUSBAND = cUS17_Failure();
                        US17_Failure_HUSBAND.Failure_Type = EUS17_FAILURE.US17_FAIL_HUSBAND_MARRTODESC;
                        US17_Failure_HUSBAND.SpouseIDs.append(Get_Individual(TempIndividuals, Husband.id));
                        US17_Failure_HUSBAND.SpouseIDs.append(Get_Individual(TempIndividuals, Child.id));
                        US17_Failure_HUSBAND.FamilyID = FamilyEntered.id;
                        US17_Problems.append(US17_Failure_HUSBAND);
                #else:
            return j;
        else:
            #if ( (j.wife_id == Wife.id) and (j.husband_id == k.id) ):
            #    US17_Failure_WIFE = cUS17_Failure();
            #    US17_Failure_WIFE.Failure_Type = EUS17_FAILURE.US17_FAIL_WIFE_MARRTODESC;
            #    US17_Problems.append(US17_Failure_WIFE);
            # We return back the family we're in so that upon the next line after the previous call to Check_Wife gets
            # hit, we can capture the family that was entered to do the check for wife and child marriage
            return j; # ???


def Check_Wife(Wife, CheckFamilies):
    global US17_Problems;

    global TempIndividuals;
    #global TempFamilies;

    # Used to add a breakpoint just prior to the for loop, upon entering a recursive call to this function
    dbgBreakpoint = True;

    # First, grab a wife from a family    
    for j in CheckFamilies:
        if (len(j.children_ids) > 0):

            # Next, iterate over each child
            for k in j.children_ids:
                Child = Get_Individual(TempIndividuals, k);

                #FamiliyMembership = Get_FamilyMembership(Families, hChildren_IDs[k]);
                FamilyMembership = Get_FamilyMembership(TempFamilies, Child.id);
                if (len(FamilyMembership) > 0):

                    # Keep propigating the same Wife object to the next recursive call!
                    FamilyEntered = Check_Wife(Wife, FamilyMembership);

                    #if ( (FamilyEntered.wife_id == Wife.id) and (FamilyEntered.husband_id == Child.id) ):
                    if ( (FamilyEntered.husband_id == Child.id) and (j.wife_id == Wife.id) ):
                        US17_Failure_WIFE = cUS17_Failure();
                        US17_Failure_WIFE.Failure_Type = EUS17_FAILURE.US17_FAIL_WIFE_MARRTODESC;
                        US17_Failure_WIFE.SpouseIDs.append(Get_Individual(TempIndividuals, Wife.id));
                        US17_Failure_WIFE.SpouseIDs.append(Get_Individual(TempIndividuals, Child.id));
                        US17_Failure_WIFE.FamilyID = FamilyEntered.id;
                        US17_Problems.append(US17_Failure_WIFE);
                #else:
            return j;
        else:
            #if ( (j.wife_id == Wife.id) and (j.husband_id == k.id) ):
            #    US17_Failure_WIFE = cUS17_Failure();
            #    US17_Failure_WIFE.Failure_Type = EUS17_FAILURE.US17_FAIL_WIFE_MARRTODESC;
            #    US17_Problems.append(US17_Failure_WIFE);
            # We return back the family we're in so that upon the next line after the previous call to Check_Wife gets
            # hit, we can capture the family that was entered to do the check for wife and child marriage
            return j; # ???

def Remove_Duplicates():
    iIdx = 0;

    bContinueLoop = True;
    if (len(US17_Problems) <= 0):
        bContinueLoop = False;

    bEntryDeleted = False;
    while (bContinueLoop == True):
        FamilyID = US17_Problems[iIdx].FamilyID;

        iIdx2 = iIdx + 1;
        bContinueInnerLoop = True;
        bEntryDeleted = False;
        while (bContinueInnerLoop == True):
            if (US17_Problems[iIdx2].FamilyID == FamilyID):
                del US17_Problems[iIdx2];
                bEntryDeleted = True;
                iIdx = 0;
            iIdx2 += 1;
            if (iIdx2 >= len(US17_Problems)):
                bContinueInnerLoop = False;

        if (bEntryDeleted == False):
            iIdx += 1;

        # -1 here because the inner loop (iIdx2) starts at the index one after the outer (iIdx), thus
        # there needs to be a +1 from iIdx if the inner loop is to run
        if (iIdx >= len(US17_Problems) - 1):
            bContinueLoop = False;            


def US17_ex(Individuals, Families):
    global TempIndividuals;
    global TempFamilies;

    global US17_Problems;

    US17_Problems = [];
    US17_Problems.clear();

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

    Check_Husband
    # First, grab a husband from a family    
    for j in Families.items():
        #Husband = Get_Individual(Individuals, j[1].husband_id);
        #HusbandFamilyMembership = Get_FamilyMembership(Families, Husband.id);
        Husband = Get_Individual(TempIndividuals, j[1].husband_id);
        HusbandFamilyMembership = Get_FamilyMembership(TempFamilies, Husband.id);

    # First, grab a wife from a family    
    for j in Families.items():
        #Wife = Get_Individual(Individuals, j[1].wife_id);
        #WifeFamilyMembership = Get_FamilyMembership(Families, Wife.id);
        Wife = Get_Individual(TempIndividuals, j[1].wife_id);
        WifeFamilyMembership = Get_FamilyMembership(TempFamilies, Wife.id);

        '''
        for k in WifeFamilyMembership:
            #hFamily = Get_Family(Families, k.id);
            hFamily = Get_Family(TempFamilies, k.id);

            # Next, iterate over each child
            #for l in j[1].children_ids:
            for l in hFamily.children_ids:
                #Child = Get_Individual(Individuals, l);
                Child = Get_Individual(TempIndividuals, l);

                #FamilyMembership = Get_FamilyMembership(Families, Child.id);
                FamilyMembership = Get_FamilyMembership(TempFamilies, Child.id);
                if (len(FamilyMembership) > 0):

                    FamilyEntered = Check_Wife(Wife, FamilyMembership);
                    if ( (FamilyEntered.wife_id == Wife.id) and (FamilyEntered.husband_id == Child.id) ):
                        US17_Failure_WIFE = cUS17_Failure();
                        US17_Failure_WIFE.Failure_Type = EUS17_FAILURE.US17_FAIL_WIFE_MARRTODESC;
                        US17_Failure_WIFE.SpouseIDs.append(Get_Individual(TempIndividuals, Wife.id));
                        US17_Failure_WIFE.SpouseIDs.append(Get_Individual(TempIndividuals, Child.id));
                        US17_Failure_WIFE.FamilyID = FamilyEntered.id;
                        US17_Problems.append(US17_Failure_WIFE);
        '''

        # Initially, the families to check is ALL of the families
        Check_Wife(Wife, TempFamilies);

    Remove_Duplicates();

    return US17_Problems;


def US17(Parser):
    global hParser;
    hParser = Parser;
    US17_ex(hParser.individuals, hParser.families);


def US17_DisplayResults():
    global US17_Problems;

    print("");
    print("US17 test failures:");

    pt = PrettyTable();
    pt.field_names = ["Family ID", "Spouses", "Failure type"];

    # for i in US17_Problems:
    for i in range(0, len(US17_Problems)):
        Spouses = "";
        for j in range(0, len(US17_Problems[i].SpouseIDs)):
            Spouses = Spouses + (US17_Problems[i].SpouseIDs[j].name) + " (" + US17_Problems[i].SpouseIDs[j].id + "), ";

        Spouses = Spouses[:-2];

        pt.add_row(
            [
                US17_Problems[i].FamilyID,
                Spouses,
                str(US17_Problems[i].Failure_Type),
            ]
        );

    # pt.sortby = "ID"

    print(pt.get_string());
    return pt.get_string();


def Execute(hParser):
    US17(hParser);
    return US17_DisplayResults();

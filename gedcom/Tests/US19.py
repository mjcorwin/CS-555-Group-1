from datetime import datetime
from gedcom import individual;
from gedcom import family;
from prettytable import PrettyTable;

from enum import Enum;

SECONDS_IN_YEAR = 365.25 * 24 * 60 * 60;
DATE_FORMAT = "%Y-%m-%d";


# US19 - No cousin marriages

global hParser;
global US19_Problems;

class EUS19_FAILURE(Enum):
    US19_FAIL_1stCOUSINS_MARRIAGE = 0



class cUS19_Failure:
    HusbID = None;
    WifeID = None;
    FamilyID = None;

    Failure_Type = None;

    def __init__(self):
        self.hFamily = {};
        self.SpouseIDs = [];
        self.Failure_Type = None;

global bug;
bug = True

def bugp(text):
    if not bug: return
    print(text)
    

#get husband and wife pairing
def US19_Test(hParser):
    global US19_Problems
    US19_Problems = {};
    US19_Problems.clear();
    
    for i in hParser.families:
            hFamily = hParser.families[i]

            if (hFamily.married == True):
                husb = None;
                wife = None;
                #Code optimization from pair programming! yippee
                husb = hParser.individuals[hParser.families[i].husband_id]
                wife = hParser.individuals[hParser.families[i].wife_id]

                husb_dad = None;
                hd_id = None;
                husb_mom = None;
                hm_id = None;
                wife_mom = None;
                wm_id = None;
                wife_dad = None;
                wd_id = None;

                #get parents
                for j in hParser.families:
                    if husb in hParser.families[j].children_ids:
                        husb_dad = hParser.families[j].husband_id;
                        husb_mom = hParser.families[j].wife_id;
                    if wife in hParser.families[j].children_ids:
                        wife_dad = hParser.families[j].husband_id;
                        wife_mom = hParser.families[j].wife_id;
                
                for j in hParser.families:
                    if husb_dad in hParser.families[j].children_ids:
                        hd_id = hParser.families[j].id
                        bugp("HD = " + hd_id)
                    if husb_mom in hParser.families[j].children_ids:
                        hm_id = hParser.families[j].id
                        bugp("HM = " + hm_id)
                    if wife_dad in hParser.families[j].children_ids:
                        wd_id = hParser.families[j].id
                        bugp("WD = " + wd_id)
                    if wife_mom in hParser.families[j].children_ids:
                        wm_id = hParser.families[j].id
                        bugp("WM = " + wm_id)
                
                fam_ids = [hd_id, hm_id, wd_id, wm_id];

                if fam_ids.count(hd_id) > 1:
                    NewFailureEntry = cUS19_Failure();
                    NewFailureEntry.HusbID = husb
                    NewFailureEntry.WifeID = wife
                    NewFailureEntry.FamilyID = hd_id;
                    US19_Problems[len(US19_Problems)] = NewFailureEntry
                if fam_ids.count(hm_id) > 1:
                    NewFailureEntry = cUS19_Failure();
                    NewFailureEntry.HusbID = husb
                    NewFailureEntry.WifeID = wife
                    NewFailureEntry.FamilyID = hm_id;
                    US19_Problems[len(US19_Problems)] = NewFailureEntry
                if fam_ids.count(wd_id) > 1:
                    NewFailureEntry = cUS19_Failure();
                    NewFailureEntry.HusbID = husb
                    NewFailureEntry.WifeID = wife
                    NewFailureEntry.FamilyID = wd_id;
                    US19_Problems[len(US19_Problems)] = NewFailureEntry
                if fam_ids.count(wm_id) > 1:
                    NewFailureEntry = cUS19_Failure();
                    NewFailureEntry.HusbID = husb
                    NewFailureEntry.WifeID = wife
                    NewFailureEntry.FamilyID = wm_id;
                    US19_Problems[len(US19_Problems)] = NewFailureEntry

    return US19_Problems

def US19_DisplayResults():
    global US19_Problems;
    print ("");
    print ("US19 test failures:");

    pt = PrettyTable();
    pt.field_names = [
        "Parents Family ID",
        "Husband ID",
        "Wife ID"
    ];

    for i in US19_Problems:
        pt.add_row(
            [
                US19_Problems[i].HusbID,
                US19_Problems[i].WifeID,
                US19_Problems[i].FamilyID
            ]
        );
    
    pt.sortby = "Parents Family ID"

    print(pt.get_string());
    return pt.get_string();

def Execute(hParser):
    US19_Test(hParser);
    return US19_DisplayResults();

            #For a couple, get their parents family information. If parents are part of the same family, fail


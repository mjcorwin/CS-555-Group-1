from datetime import datetime
from gedcom import individual;
from gedcom import family;
from prettytable import PrettyTable;

from enum import Enum;

SECONDS_IN_YEAR = 365.25 * 24 * 60 * 60;
DATE_FORMAT = "%Y-%m-%d";


# US20 - No marrying uncles or aunts

global hParser;
global US20_Problems;

class EUS20_FAILURE(Enum):
    US20_FAIL_1stCOUSINS_MARRIAGE = 0



class cUS20_Failure:
    HusbID = None;
    WifeID = None;
    FamilyID = None;
    BadSpouse = None;

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
def US20_Test(hParser):
    global US20_Problems
    US20_Problems = {};
    US20_Problems.clear();
    
    for i in hParser.families:
            hFamily = hParser.families[i]

            if (hFamily.married == True):
                husb = None;
                wife = None;
                #Code optimization from pair programming! yippee
                for i in hParser.individuals:
                    if hFamily.wife_id == hParser.individuals[i].id:
                        wife = hParser.individuals[i]
                for i in hParser.individuals:
                    if hFamily.husband_id == hParser.individuals[i].id:
                        husb = hParser.individuals[i]
                if (husb == None and wife == None):
                    break;

                husb_dad = None;
                hd_id = None;
                husb_mom = None;
                hm_id = None;
                hFam = None;

                wife_mom = None;
                wm_id = None;
                wife_dad = None;
                wd_id = None;
                wFam = None;

                #get parents
                for j in hParser.families:
                    if husb.id in hParser.families[j].children_ids:
                        husb_dad = hParser.families[j].husband_id;
                        husb_mom = hParser.families[j].wife_id;
                        hFam = hParser.families[j].id

                    if wife.id in hParser.families[j].children_ids:
                        wife_dad = hParser.families[j].husband_id;
                        wife_mom = hParser.families[j].wife_id;
                        wFam = hParser.families[j].id
                


                for j in hParser.families:
                    if husb_dad in hParser.families[j].children_ids:
                        hd_id = hParser.families[j].id
                    if husb_mom in hParser.families[j].children_ids:
                        hm_id = hParser.families[j].id
            
                    if wife_dad in hParser.families[j].children_ids:
                        wd_id = hParser.families[j].id
                       
                    if wife_mom in hParser.families[j].children_ids:
                        wm_id = hParser.families[j].id
                
                fam_ids = [hd_id, hm_id, wd_id, wm_id];

                if hFam in fam_ids and hFam is not None:
                    NewFailureEntry = cUS20_Failure();
                    NewFailureEntry.HusbID = husb.id
                    NewFailureEntry.WifeID = wife.id
                    NewFailureEntry.FamilyID = hFamily.id
                    NewFailureEntry.BadSpouse = "Uncle"
                    US20_Problems[len(US20_Problems)] = NewFailureEntry
                elif wFam in fam_ids and wFam is not None:
                    NewFailureEntry = cUS20_Failure();
                    NewFailureEntry.HusbID = husb.id
                    NewFailureEntry.WifeID = wife.id
                    NewFailureEntry.FamilyID = hFamily.id
                    NewFailureEntry.BadSpouse = "Aunt"
                    US20_Problems[len(US20_Problems)] = NewFailureEntry

    return US20_Problems

def US20_DisplayResults():
    global US20_Problems;
    print ("");
    print ("US20 test failures:");

    pt = PrettyTable();
    pt.field_names = [
        "Family ID",
        "Husband ID",
        "Wife ID",
        "Bad Spouse Role"
    ];

    for i in US20_Problems:
        pt.add_row(
            [
                US20_Problems[i].FamilyID,
                US20_Problems[i].HusbID,
                US20_Problems[i].WifeID,
                US20_Problems[i].BadSpouse
                
            ]
        );
    

    print(pt.get_string());
    return pt.get_string();

def Execute(hParser):
    US20_Test(hParser);
    return US20_DisplayResults();

            #For a couple, get their parents family information. If parents are part of the same family, fail


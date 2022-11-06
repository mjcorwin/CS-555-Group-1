"""
    US22: Unique IDs
    US22 - Story Description: All individual IDs should be unique and all family IDs should be unique
    Expected anomaly output: Return duplicate individual IDs along with duplicate family IDs.
"""
from datetime import datetime
from collections import defaultdict
from gedcom import individual, family
from prettytable import PrettyTable;
from enum import Enum

SECONDS_IN_YEAR = 365.25 * 24 * 60 * 60;
DATE_FORMAT = "%Y-%m-%d";

US22_Problems = []

class EUS22_FAILURE(Enum):
    # Individuals
    US22_FAIL_NON_UNIQUE_IDs = 0

class cUS22_Failure:
    hFamily = None
    hIndividual = None
    kv = None
    Failure_Type = None;

    def __init__(self, kv=None):
        self.hFamily = None
        self.kv = kv
        self.hIndividual = None
        self.Failure_Type = None;
    


def get_common_individual_ids(hParser):
    unique_lst = []
    duplicate_lst = []
    for family in hParser.families:
        hFamily = hParser.families[family]
        while hFamily:
            hFamily_id = hFamily.id
            hFamily_children_ids = hFamily.children_ids
            if hFamily_id not in unique_lst and hFamily_children_ids not in unique_lst:
                unique_lst.append(hFamily_id)
                unique_lst.append(hFamily_children_ids)
                break
            elif hFamily_id not in duplicate_lst and hFamily_children_ids not in duplicate_lst:
                duplicate_lst.append(hFamily_id)
                duplicate_lst.append(hFamily_children_ids)
                break
        duplicate_individual_ids = [common for common in unique_lst if common in duplicate_lst]
    return duplicate_individual_ids


def get_common_family_ids(hParser):
    unique_lst = []
    duplicate_lst = []
    for family in hParser.families:
        hFamily = hParser.families[family]
        while hFamily:
            hFamily_id = hFamily.id
            if hFamily_id not in unique_lst:
                unique_lst.append(hFamily_id)
                break
            if hFamily_id not in duplicate_lst:
                duplicate_lst.append(hFamily_id)
                break
    duplicate_lst.extend(unique_lst)
    duplicate_individual_ids = [common for common in unique_lst if common in duplicate_lst]
    return duplicate_individual_ids

def US22_Test(hParser):
    US22_Problems.clear();

    hIndividual = get_common_individual_ids(hParser)
    hFamily = get_common_family_ids(hParser)

    NewFailureEntry = cUS22_Failure()
    NewFailureEntry.hIndividual = hIndividual
    NewFailureEntry.hFamily = hFamily
    NewFailureEntry.Failure_Type = (
EUS22_FAILURE.US22_FAIL_NON_UNIQUE_IDs
    )

    US22_Problems.append(NewFailureEntry)

def US22_DisplayResults(hParser):

    print ("");
    print ("US22 test failures:");

    pt = PrettyTable();
    pt.field_names = [
        "Common Individual IDs",
        "Common Family IDs",
        "Data failure type"
    ];

    for i in US22_Problems:
        common_individual_ids = get_common_individual_ids(hParser)
        common_family_ids = get_common_family_ids(hParser)

        pt.add_row(
            [
                common_individual_ids,
                common_family_ids,
                str(i.Failure_Type)
            ]
        );

    print (pt.get_string());
    return pt.get_string();
    

def Execute(hParser):
    US22_Test(hParser);
    return US22_DisplayResults(hParser);
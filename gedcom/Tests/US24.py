from enum import Enum
from prettytable import PrettyTable
from itertools import product

US24_Problems = []


class EUS24_FAILURE(Enum):
    US24_MORE_THAN_ONE_FAMILY_SAME_SPOUSES_AND_MARRIAGE_DATE = 0


class cUS24_Failure:
    def __init__(self):
        self.hFamily_IDs = set()
        self.husband_name = None
        self.wife_name = None
        self.married_date = None
        self.failure_Type = None

    def failed(self):
        return True if self.failure_Type else False


def US24_Test(hParser):
    US24_Problems.clear()

    print("")
    print("US24 test failures:")

    marriage_date_map = {}
    error_map = {}

    for f in hParser.families.values():
        if f.married_date not in marriage_date_map:
            marriage_date_map[f.married_date] = set()

        marriage_date_map[f.married_date].add(f)

    for families in marriage_date_map.values():
        families = list(families)
        size = len(families)
        error = cUS24_Failure

        for i in range(0, size - 1):
            for j in range(i + 1, size):
                f1 = families[i]
                f2 = families[j]

                if f1.id == f2.id:
                    continue

                # We already know date is the same so need to check spouse names
                f1_husband_name = hParser.individuals[f1.husband_id].name
                f2_husband_name = hParser.individuals[f2.husband_id].name

                f1_wife_name = hParser.individuals[f1.wife_id].name
                f2_wife_name = hParser.individuals[f2.wife_id].name

                if f1_husband_name == f2_husband_name and f1_wife_name == f2_wife_name:
                    error_map_key = f1_husband_name + f1_wife_name

                    if error_map_key not in error_map:
                        error_map[error_map_key] = cUS24_Failure()
                    error = error_map[error_map_key]

                    error.hFamily_IDs.add(f1.id)
                    error.hFamily_IDs.add(f2.id)
                    error.husband_name = f1_husband_name
                    error.wife_name = f1_wife_name
                    error.married_date = f1.married_date
                    error.failure_Type = (
                        EUS24_FAILURE.US24_MORE_THAN_ONE_FAMILY_SAME_SPOUSES_AND_MARRIAGE_DATE
                    )
    for error in error_map.values():
        US24_Problems.append(error)


def US24_DisplayResults():
    pt = PrettyTable()
    pt.field_names = [
        "IDs",
        "Husband Name",
        "Wife Name",
        "Marriage Date",
        "Data Failure Type",
    ]

    for p in US24_Problems:
        family_ids = list(p.hFamily_IDs)
        husband_name = p.husband_name
        wife_name = p.wife_name
        date = p.married_date

        pt.add_row(
            [",".join(family_ids), husband_name, wife_name, date, str(p.failure_Type)]
        )

    print(pt.get_string())
    return pt.get_string()


def Execute(hParser):
    US24_Test(hParser)
    return US24_DisplayResults()

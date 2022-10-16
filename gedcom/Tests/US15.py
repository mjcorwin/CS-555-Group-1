from enum import Enum
from prettytable import PrettyTable

US15_Problems = []


class EUS15_FAILURE(Enum):
    US15_FAIL_TOO_MANY_SIBLINGS = 0


class cUS15_Failure:
    def __init__(self):
        self.hFamily = None
        self.failure_Type = None

    def failed(self):
        return True if self.failure_Type else False


def US15_Test(hParser):
    US15_Problems.clear()

    print("")
    print("US15 test failures:")

    for f in hParser.families.values():
        error = cUS15_Failure()

        if len(f.children_ids) > 15:
            error.hFamily = f
            error.failure_Type = EUS15_FAILURE.US15_FAIL_TOO_MANY_SIBLINGS
            US15_Problems.append(error)


def US15_DisplayResults():
    pt = PrettyTable()
    pt.field_names = ["ID", "Number of Siblings", "Data Failure Type"]

    for p in US15_Problems:
        pt.add_row([p.hFamily.id, len(p.hFamily.children_ids), str(p.failure_Type)])

    print(pt.get_string())
    return pt.get_string()


def Execute(hParser):
    US15_Test(hParser)
    return US15_DisplayResults()

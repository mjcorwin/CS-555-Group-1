from enum import Enum
from prettytable import PrettyTable

US16_Problems = []


class EUS16_FAILURE(Enum):
    US16_MALE_FAMILY_NOT_SAME_LAST_NAME = 0


class cUS16_Failure:
    def __init__(self):
        self.hFamily = None
        self.hNames = []
        self.failure_Type = None


def US16_Test(hParser):
    US16_Problems.clear()

    print("")
    print("US16 test failures:")

    for f in hParser.families.values():
        error = cUS16_Failure()

        last_name = None

        # SMELL: Duplicated logic which is also mildly complex
        for child_id in f.children_ids:
            child = hParser.individuals[child_id]
            if not last_name:
                last_name = child.last_name()
            elif last_name != child.last_name():
                error.hFamily = f
                error.failure_Type = EUS16_FAILURE.US16_MALE_FAMILY_NOT_SAME_LAST_NAME
                error.hNames.append(child.last_name())

        if f.husband_id:
            husband = hParser.individuals[f.husband_id]
            if not last_name:
                last_name = husband.last_name()
            elif last_name != husband.last_name():
                error.hFamily = f
                error.failure_Type = EUS16_FAILURE.US16_MALE_FAMILY_NOT_SAME_LAST_NAME
                # SMELL: Duplicated code actually led to a bug!
                error.hNames.append(child.last_name())

        # SMELL: Bad method, not obvious what this is checking
        if error.failure_Type:
            US16_Problems.append(error)


def US16_DisplayResults():
    pt = PrettyTable()
    pt.field_names = ["ID", "Male Family Member Last Names", "Data Failure Type"]

    for p in US16_Problems:
        pt.add_row([p.hFamily.id, ",".join(p.hNames), str(p.failure_Type)])

    print(pt.get_string())
    return pt.get_string()


def Execute(hParser):
    US16_Test(hParser)
    return US16_DisplayResults()

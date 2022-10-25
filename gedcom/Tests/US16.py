from enum import Enum
from prettytable import PrettyTable

US16_Problems = []


class EUS16_FAILURE(Enum):
    US16_MALE_FAMILY_NOT_SAME_LAST_NAME = 0


class cUS16_Failure:
    def __init__(self):
        self.hFamily = None
        self.hNames = set()
        self.failure_Type = None

    def failed(self):
        return self.failure_Type != None


def get_individuals(individuals_dict, ids=[]):
    individuals = []

    for id in ids:
        individuals.append(individuals_dict[id])

    return individuals


def US16_Test(hParser):
    US16_Problems.clear()

    print("")
    print("US16 test failures:")

    for f in hParser.families.values():
        error = cUS16_Failure()

        last_name = None

        individual_ids = f.children_ids
        if f.husband_id:
            individual_ids.append(f.husband_id)

        individuals = get_individuals(hParser.individuals, individual_ids)

        for individual in individuals:
            if not last_name:
                last_name = individual.last_name()
            elif last_name != individual.last_name():
                error.hFamily = f
                error.failure_Type = EUS16_FAILURE.US16_MALE_FAMILY_NOT_SAME_LAST_NAME

            error.hNames.add(individual.last_name())

        if error.failed():
            US16_Problems.append(error)


def US16_DisplayResults():
    pt = PrettyTable()
    pt.field_names = ["ID", "Male Family Member Last Names", "Data Failure Type"]

    for p in US16_Problems:
        pt.add_row([p.hFamily.id, ", ".join(p.hNames), str(p.failure_Type)])

    print(pt.get_string())
    return pt.get_string()


def Execute(hParser):
    US16_Test(hParser)
    return US16_DisplayResults()

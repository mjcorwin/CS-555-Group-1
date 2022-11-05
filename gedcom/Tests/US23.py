from enum import Enum
from prettytable import PrettyTable

US23_Problems = []


class EUS23_FAILURE(Enum):
    US23_MORE_THAN_ONE_INDIVIDUAL_SAME_NAME_AND_BIRTH_DATE = 0


class cUS23_Failure:
    def __init__(self):
        self.hIndividuals = set()
        self.failure_Type = None

    def failed(self):
        return True if self.failure_Type else False


def US23_Test(hParser):
    US23_Problems.clear()

    print("")
    print("US23 test failures:")

    birth_date_map = {}
    error_map = {}

    for i in hParser.individuals.values():
        if (
            i.name in birth_date_map
            and birth_date_map[i.name].birth_date == i.birth_date
        ):
            if i.name not in error_map:
                error_map[i.name] = cUS23_Failure()

            error = error_map[i.name]
            error.hIndividuals.add(i)
            error.hIndividuals.add(birth_date_map[i.name])
            error.failure_Type = (
                EUS23_FAILURE.US23_MORE_THAN_ONE_INDIVIDUAL_SAME_NAME_AND_BIRTH_DATE
            )
        else:
            birth_date_map[i.name] = i

    for error in error_map.values():
        US23_Problems.append(error)


def US23_DisplayResults():
    pt = PrettyTable()
    pt.field_names = ["IDs", "Individual Name", "Birth Dates", "Data Failure Type"]

    for p in US23_Problems:
        individual = list(p.hIndividuals)[0]

        name = individual.name
        date = individual.birth_date
        ids = [i.id for i in p.hIndividuals]

        pt.add_row([",".join(ids), name, date, str(p.failure_Type)])

    print(pt.get_string())
    return pt.get_string()


def Execute(hParser):
    US23_Test(hParser)
    return US23_DisplayResults()

from datetime import datetime

from prettytable import PrettyTable

MULTIPLE_BIRTHS = []

DATE_FORMAT = "%Y-%m-%d"


def dict_key(individual):

    if individual.family_child and individual.birth_date:
        date_str = datetime.strftime(individual.birth_date, DATE_FORMAT)
        return individual.family_child + date_str

    return None


def US32_Test(hParser):
    MULTIPLE_BIRTHS.clear()

    famc_date_dict = {}

    for individual in hParser.individuals.values():
        key = dict_key(individual)
        if not key:
            continue

        if key not in famc_date_dict:
            famc_date_dict[key] = set()
        famc_date_dict[key].add(individual)

    for individuals in famc_date_dict.values():
        if len(individuals) >= 2:
            MULTIPLE_BIRTHS.append(individuals)


def US32_DisplayResults():
    pt = PrettyTable()
    pt.field_names = ["Family ID", "Birthday", "Names"]

    for individuals in MULTIPLE_BIRTHS:
        individuals = list(individuals)
        individual = individuals[0]
        family_id = individual.family_child
        birth_date = individual.birth_date
        names = [i.name for i in individuals]
        names.sort()

        pt.add_row([family_id, birth_date, ",".join(names)])

    print(pt.get_string())
    return pt.get_string()


def Execute(hParser):
    US32_Test(hParser)
    return US32_DisplayResults()

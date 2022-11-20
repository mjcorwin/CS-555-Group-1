from prettytable import PrettyTable

OVER_30_NOT_MARRIED = []


def US31_Test(hParser):
    OVER_30_NOT_MARRIED.clear()

    for individual in hParser.individuals.values():
        if individual.age() > 30 and individual.family_spouse == None:
            OVER_30_NOT_MARRIED.append(individual)

    for family in hParser.families.values():
        if not family.divorced_date:
            continue

        to_remove = []
        for idx, individual in enumerate(OVER_30_NOT_MARRIED):
            id = individual.id

            if id == family.husband_id or id == family.wife_id:
                to_remove.append[idx]

        for idx in to_remove:
            OVER_30_NOT_MARRIED.pop(idx)

    return OVER_30_NOT_MARRIED


def US31_DisplayResults():
    pt = PrettyTable()
    pt.field_names = ["ID", "Name"]

    OVER_30_NOT_MARRIED.sort(key=lambda i: i.id)

    for individual in OVER_30_NOT_MARRIED:
        pt.add_row([individual.id, individual.name])

    print(pt.get_string())
    return pt.get_string()


def Execute(hParser):
    US31_Test(hParser)
    return US31_DisplayResults()

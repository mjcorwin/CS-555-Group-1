from prettytable import PrettyTable

from enum import Enum


global US13_Problems


class EUS13_FAILURE(Enum):
    US13_FAIL_BIRTHDAYS_GT_2_DAYS_LT_8_MONTHS = 0


class cUS13_Failure:
    hChild_A = None
    hChild_B = None
    Failure_Type = None

    def __init__(self):
        self.hChild_A = None
        self.hChild_B = None
        self.Failure_Type = None


def US13_Test(hParser):
    global US13_Problems

    US13_Problems = []
    US13_Problems.clear()

    for family in hParser.families.values():
        children = []

        for child_id in family.children_ids:
            children.append(hParser.individuals[child_id])

        # [1,2,3,4,5]
        # [1,2,3,4,5]

        # diff(1.bday, 2.bday)
        # if within range, error

        for i in range(0, len(children) - 1):
            for j in range(i + 1, len(children) - 1):
                child_a = children[i]
                child_b = children[j]

                # def diff_month(d1, d2):
                # return (d1.year - d2.year) * 12 + d1.month - d2.month

                date1 = child_a.birth_date
                date2 = child_b.birth_date

                delta1 = (date1 - date2).days
                delta2 = (date1.year - date2.year) * 12 + date1.month - date2.month
                if delta1 >= 2 and delta2 <= 8:
                    error = cUS13_Failure()
                    error.hChild_A = child_a
                    error.hChild_B = child_b
                    error.Failure_Type = (
                        EUS13_FAILURE.US13_FAIL_BIRTHDAYS_GT_2_DAYS_LT_8_MONTHS
                    )

                    US13_Problems.append(error)


def US13_DisplayResults(hParser):
    global US13_Problems

    print("")
    print("US13 test failures:")

    pt = PrettyTable()
    pt.field_names = [
        "Child A ID",
        "Child A Birthday",
        "Child B ID",
        "Child B Birthday",
        "Birthday Difference (Days)",
        "Failure type",
    ]

    for p in US13_Problems:
        pt.add_row(
            [
                p.hChild_A.id,
                p.hChild_A.birth_date,
                p.hChild_B.id,
                p.hChild_B.birth_date,
                (p.hChild_A.birth_date - p.hChild_B.birth_date).days,
                str(p.Failure_Type),
            ]
        )

    print(pt.get_string())
    return pt.get_string()


def Execute(hParser):
    US13_Test(hParser)
    return US13_DisplayResults(hParser)

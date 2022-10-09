from datetime import datetime
from .family import Family
from .individual import Individual


def validate(individuals, families):
    all_errors = []

    for function in VALIDATION_LIST:
        errors = function(individuals, families)
        if errors:
            all_errors.extend(errors)

    return all_errors


def US01(individuals, families):
    errors = []
    today = datetime.now().date()

    for record in individuals.values():
        if record.birth_date and record.birth_date > today:
            errors.append(
                f"ERROR: INDIVIDUAL: US01: {record.id}: Birthday {record.birth_date} occurs in the future"
            )

        if record.death_date and record.death_date > today:
            errors.append(
                f"ERROR: INDIVIDUAL: US01: {record.id}: Death {record.birth_date} occurs in the future"
            )

    for record in families.values():
        if record.married_date and record.married_date > today:
            errors.append(
                f"ERROR: FAMILY: US01: {record.id}: Marriage {record.married_date} occurs in the future"
            )

        if record.divorced_date and record.divorced_date > today:
            errors.append(
                f"ERROR: FAMILY: US01: {record.id}: Marriage {record.divorced_date} occurs in the future"
            )

    return errors


VALIDATION_LIST = [US01]

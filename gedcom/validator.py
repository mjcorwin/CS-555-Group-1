from datetime import datetime


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


def US02(individuals, families):
    errors = []

    for f in families.values():
        married_date = f.married_date
        if not married_date:
            continue

        husband = individuals.get(f.husband_id)
        wife = individuals.get(f.wife_id)

        if husband and husband.birth_date and husband.birth_date > married_date:
            errors.append(
                f"ERROR: INDIVIDUAL: US02: {husband.id}: Birthday {husband.birth_date} occurs after Marriage {married_date}"
            )

        if wife and wife.birth_date and wife.birth_date > married_date:
            errors.append(
                f"ERROR: INDIVIDUAL: US02: {wife.id}: Birthday {wife.birth_date} occurs after Marriage {married_date}"
            )

    return errors


VALIDATION_LIST = [US01, US02]

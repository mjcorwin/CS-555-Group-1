from gedcom import validator


class TestUS02:
    def test_empty_family(self, family):
        errors = validator.US02({}, {family.id: family})
        assert len(errors) == 0

    def test_family_with_only_marriage_date(self, family, today):
        family.married_date = today

        errors = validator.US02({}, {family.id: family})
        assert len(errors) == 0

    def test_husband_birth_date_greater_than_married_date(
        self, family_with_husband_and_wife, today, previous_date
    ):
        (family, husband, wife) = family_with_husband_and_wife
        husband.birth_date = today
        family.married_date = previous_date

        individuals = {husband.id: husband, wife.id: wife}

        errors = validator.US02(individuals, {family.id: family})
        assert len(errors) == 1

    def test_wife_birth_date_greater_than_married_date(
        self, family_with_husband_and_wife, today, previous_date
    ):
        (family, husband, wife) = family_with_husband_and_wife
        wife.birth_date = today
        family.married_date = previous_date

        individuals = {husband.id: husband, wife.id: wife}

        errors = validator.US02(individuals, {family.id: family})
        assert len(errors) == 1

    def test_husband_and_wife_birth_date_greater_than_married_date(
        self, family_with_husband_and_wife, today, previous_date
    ):
        (family, husband, wife) = family_with_husband_and_wife
        wife.birth_date = today
        husband.birth_date = today
        family.married_date = previous_date

        individuals = {husband.id: husband, wife.id: wife}

        errors = validator.US02(individuals, {family.id: family})
        assert len(errors) == 2

    def test_husband_birth_date_equalt_to_married_date(
        self, family_with_husband_and_wife, today
    ):
        (family, husband, wife) = family_with_husband_and_wife
        husband.birth_date = today
        family.married_date = today

        individuals = {husband.id: husband, wife.id: wife}

        errors = validator.US02(individuals, {family.id: family})
        assert len(errors) == 0

    def test_wife_birth_date_equalt_to_married_date(
        self, family_with_husband_and_wife, today
    ):
        (family, husband, wife) = family_with_husband_and_wife
        wife.birth_date = today
        family.married_date = today

        individuals = {husband.id: husband, wife.id: wife}

        errors = validator.US02(individuals, {family.id: family})
        assert len(errors) == 0

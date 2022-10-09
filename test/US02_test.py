import random
from datetime import datetime, timedelta

import pytest
from gedcom import validator
from gedcom.family import Family
from gedcom.individual import Individual


@pytest.fixture
def previous_date():
    return datetime.now().date() + timedelta(days=-random.randint(0, 10000))


@pytest.fixture
def today():
    return datetime.now().date()


@pytest.fixture
def make_individual():
    def make_individual():
        return Individual("I" + str(random.randint(0, 10000)))

    return make_individual


@pytest.fixture
def husband(make_individual):
    husband = make_individual()
    husband.sex = "M"

    return husband


@pytest.fixture
def wife(make_individual):
    wife = make_individual()
    wife.sex = "F"

    return wife


@pytest.fixture
def family():
    return Family("F" + str(random.randint(0, 10000)))


@pytest.fixture
def family_with_husband_and_wife(family, husband, wife):
    family.husband_id = husband.id
    family.wife_id = wife.id
    family.married = True

    return (family, husband, wife)


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

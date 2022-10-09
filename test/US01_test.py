import random
from datetime import datetime, timedelta

import pytest
from gedcom import validator
from gedcom.family import Family
from gedcom.individual import Individual


@pytest.fixture
def future_date():
    return datetime.now().date() + timedelta(days=random.randint(0, 10000))


@pytest.fixture
def previous_date():
    return datetime.now().date() + timedelta(days=-random.randint(0, 10000))


@pytest.fixture
def today():
    return datetime.now().date()


@pytest.fixture
def individual():
    return Individual("I" + str(random.randint(0, 10000)))


@pytest.fixture
def family():
    return Family("F" + str(random.randint(0, 10000)))


# TODO: Without date
# TODO: >, <, = for all dates
class TestUS01:
    def test_individual_without_dates(self, individual):
        errors = validator.US01({individual.id: individual}, {})
        assert len(errors) == 0

    def test_family_without_dates(self, family):
        errors = validator.US01({}, {family.id: family})
        assert len(errors) == 0

    def test_individual_birth_date_less_than_today(self, individual, previous_date):
        individual.birth_date = previous_date
        errors = validator.US01({individual.id: individual}, {})
        assert len(errors) == 0

    def test_individual_birth_date_greater_than_today(self, individual, future_date):
        individual.birth_date = future_date
        errors = validator.US01({individual.id: individual}, {})
        assert len(errors) == 1

    def test_birth_date_equal_to_today(self, individual, today):
        individual.birth_date = today
        errors = validator.US01({individual.id: individual}, {})
        assert len(errors) == 0

    def test_individual_death_date_less_than_today(self, individual, previous_date):
        individual.death_date = previous_date
        errors = validator.US01({individual.id: individual}, {})
        assert len(errors) == 0

    def test_individual_death_date_greater_than_today(self, individual, future_date):
        individual.death_date = future_date
        errors = validator.US01({individual.id: individual}, {})
        assert len(errors) == 1

    def test_death_date_equal_to_today(self, individual, today):
        individual.death_date = today
        errors = validator.US01({individual.id: individual}, {})
        assert len(errors) == 0

    def test_family_married_date_less_than_today(self, family, previous_date):
        family.married_date = previous_date
        errors = validator.US01({}, {family.id: family})
        assert len(errors) == 0

    def test_family_married_date_greater_than_today(self, family, future_date):
        family.married_date = future_date
        errors = validator.US01({}, {family.id: family})
        assert len(errors) == 1

    def test_family_married_date_equal_to_today(self, family, today):
        family.married_date = today
        errors = validator.US01({}, {family.id: family})
        assert len(errors) == 0

    def test_family_divorced_date_less_than_today(self, family, previous_date):
        family.divorced_date = previous_date
        errors = validator.US01({}, {family.id: family})
        assert len(errors) == 0

    def test_family_divorced_date_greater_than_today(self, family, future_date):
        family.divorced_date = future_date
        errors = validator.US01({}, {family.id: family})
        assert len(errors) == 1

    def test_family_divorced_date_equal_to_today(self, family, today):
        family.divorced_date = today
        errors = validator.US01({}, {family.id: family})
        assert len(errors) == 0

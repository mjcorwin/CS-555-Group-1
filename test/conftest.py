import random
from datetime import datetime, timedelta

import pytest
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


@pytest.fixture
def make_individual():
    def make_individual():
        return Individual("I" + str(random.randint(0, 10000)))

    return make_individual


@pytest.fixture
def make_male_individual_with_last_name():
    def make_individual(last_name):
        i = Individual("I" + str(random.randint(0, 10000)))
        i.name = f" /{last_name}/"
        i.sex = "M"
        return i

    return make_individual

@pytest.fixture
def make_family_with_same_last_names():
    def make_sibling_last_name(last_name):
        i = Individual("I" + str(random.randint(0, 10000)))
        i.name = f" /{last_name}"
        return i
    return make_sibling_last_name

@pytest.fixture
def make_family_with_birth_dates():
    def make_sibling_birth_dates(birth_dates):
        i = Individual("I" + str(random.randint(0, 10000)))
        i.birth = f" /{birth_dates}"
        return i
    return make_sibling_birth_dates


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
def family_with_husband_and_wife(family, husband, wife):
    family.husband_id = husband.id
    family.wife_id = wife.id
    family.married = True

    return (family, husband, wife)


@pytest.fixture
def add_siblings_to_family():
    def add_siblings(family, num_siblings):
        for _ in range(num_siblings):
            family.children_ids.append("I" + str(random.randint(0, 10000)))

    return add_siblings
# fewer than 15 siblings in a family
import random

import pytest
from gedcom.family import Family
from gedcom.parser import Parser
from gedcom.Tests.US15 import *


@pytest.fixture
def family():
    return Family("F" + str(random.randint(0, 10000)))


@pytest.fixture
def add_siblings_to_family():
    def add_siblings(family, num_siblings):
        for _ in range(num_siblings):
            family.children_ids.append("I" + str(random.randint(0, 10000)))

    return add_siblings


class TestUS15:
    def test_family_with_no_siblings(self, family, add_siblings_to_family):
        add_siblings_to_family(family, 0)
        parser = Parser(None)
        parser.families = {family.id: family}

        US15_Test(parser)
        assert len(US15_Problems) == 0

    def test_family_with_10_siblings(self, family, add_siblings_to_family):
        add_siblings_to_family(family, 10)
        parser = Parser(None)
        parser.families = {family.id: family}

        US15_Test(parser)
        assert len(US15_Problems) == 0

    def test_family_with_15_siblings(self, family, add_siblings_to_family):
        add_siblings_to_family(family, 15)
        parser = Parser(None)
        parser.families = {family.id: family}

        US15_Test(parser)
        assert len(US15_Problems) == 0

    def test_family_with_20_siblings(self, family, add_siblings_to_family):
        add_siblings_to_family(family, 20)
        parser = Parser(None)
        parser.families = {family.id: family}

        US15_Test(parser)
        assert len(US15_Problems) == 1

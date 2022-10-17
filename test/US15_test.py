import random

import pytest
from gedcom.family import Family
from gedcom.parser import Parser
from gedcom.Tests.US15 import *


@pytest.fixture
def family():
    return Family("F" + str(random.randint(0, 10000)))


@pytest.fixture
def parser():
    return Parser(None)


class TestUS15:
    def test_family_with_0_children(self, family):
        parser.families = {family.id: family}

        US15_Test(parser)
        assert len(US15_Problems.keys()) == 0

    def test_family_with_10_children(self, family):
        family.children_ids = ["I"] * 10
        parser.families = {family.id: family}

        US15_Test(parser)
        assert len(US15_Problems.keys()) == 0

    def test_family_with_14_children(self, family):
        family.children_ids = ["I"] * 14
        parser.families = {family.id: family}

        US15_Test(parser)
        assert len(US15_Problems.keys()) == 0

    def test_family_with_15_children(self, family):
        family.children_ids = ["I"] * 15
        parser.families = {family.id: family}

        US15_Test(parser)
        assert len(US15_Problems.keys()) == 1

    def test_family_with_16_children(self, family):
        family.children_ids = ["I"] * 16
        parser.families = {family.id: family}

        US15_Test(parser)
        assert len(US15_Problems.keys()) == 1

    def test_family_with_100_children(self, family):
        family.children_ids = ["I"] * 100
        parser.families = {family.id: family}

        US15_Test(parser)
        assert len(US15_Problems.keys()) == 1

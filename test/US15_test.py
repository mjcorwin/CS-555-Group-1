from gedcom.parser import Parser
from gedcom.Tests.US15 import *


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
        assert len(US15_Problems) == 1

    def test_family_with_20_siblings(self, family, add_siblings_to_family):
        add_siblings_to_family(family, 20)
        parser = Parser(None)
        parser.families = {family.id: family}

        US15_Test(parser)
        assert len(US15_Problems) == 1

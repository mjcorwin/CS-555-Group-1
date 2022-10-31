from gedcom.parser import Parser
from gedcom.Tests.US21 import *

class TestUS21:
    def test_empty_family(self, family):
        parser = Parser(None)
        parser.families = {family.id: family}

        US21_Test(parser)
        assert len(US21_Problems) == 0

    def test_valid_family(self, family):
        parser = Parser(None)
        parser.families = {
            family.id: family,
            family.husband_id: "I100000",
            family.wife_id: "I1000001",
            family.married: True
        }

        US21_Test(parser)
        assert len(US21_Problems) == 0


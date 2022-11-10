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

    def test_invalid_family(self, individual, family):
        parser = Parser(None)

        family_husband_id = "I100000"
        family_wife_id = "I1000001"

        individual_ids = [family_husband_id, family_wife_id]

        female_sex = "F"
        male_sex = "M"

        parser.families = {
            family.id: family,
            family.husband_id: family_husband_id,
            family.wife_id: family_wife_id,
            family.married: True
        }

        parser.families = {
            individual.id: individual,
            individual.id: individual_ids,
            individual.sex: [female_sex, male_sex]
        }

        US21_Test(parser)
        assert len(US21_Problems) == 0


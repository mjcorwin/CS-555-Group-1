from gedcom.parser import Parser
from gedcom.Tests.US16 import *


class TestUS16:
    def test_empty_family(self, family):
        parser = Parser(None)
        parser.families = {family.id: family}

        US16_Test(parser)
        assert len(US16_Problems) == 0

    def test_family_with_only_husband(
        self, family, make_male_individual_with_last_name
    ):
        husband = make_male_individual_with_last_name("Clark")
        family.husband_id = husband.id

        parser = Parser(None)
        parser.families = {family.id: family}
        parser.individuals = {husband.id: husband}

        US16_Test(parser)
        assert len(US16_Problems) == 0

    def test_family_with_only_one_child(
        self, family, make_male_individual_with_last_name
    ):
        child = make_male_individual_with_last_name("Clark")
        family.children_ids.append(child.id)

        parser = Parser(None)
        parser.families = {family.id: family}
        parser.individuals = {child.id: child}

        US16_Test(parser)
        assert len(US16_Problems) == 0

    def test_family_with_male_children_with_different_last_names(
        self, family, make_male_individual_with_last_name
    ):
        individuals = {}

        for i in range(2):
            individual = make_male_individual_with_last_name(f"Clark{i}")
            family.children_ids.append(individual.id)
            individuals[individual.id] = individual

        parser = Parser(None)
        parser.families = {family.id: family}
        parser.individuals = individuals

        US16_Test(parser)
        assert len(US16_Problems) == 1
        assert len(US16_Problems[0].hNames) == 2

    def test_family_with_husband_and_male_child_with_different_last_names(
        self, family, make_male_individual_with_last_name
    ):
        child = make_male_individual_with_last_name("Clark")
        husband = make_male_individual_with_last_name("Bark")

        family.children_ids.append(child.id)
        family.husband_id = husband.id

        parser = Parser(None)
        parser.families = {family.id: family}
        parser.individuals = {husband.id: husband, child.id: child}

        US16_Test(parser)
        assert len(US16_Problems) == 1
        assert len(US16_Problems[0].hNames) == 2

from gedcom.parser import Parser
from gedcom.Tests.US31 import *

from dateutil.relativedelta import relativedelta


class TestUS31:
    def test_no_individuals(self):
        parser = Parser(None)
        parser.individuals = {}
        parser.families = {}

        US31_Test(parser)
        assert len(OVER_30_NOT_MARRIED) == 0

    def test_individual_under_30_not_married(self, individual, today):
        individual.birth_date = today

        parser = Parser(None)
        parser.individuals = {individual.id: individual}
        parser.families = {}

        US31_Test(parser)
        assert len(OVER_30_NOT_MARRIED) == 0

    def test_individual_over_30_not_married(self, individual, today):
        individual.birth_date = today - relativedelta(years=31)

        parser = Parser(None)
        parser.individuals = {individual.id: individual}
        parser.families = {}

        US31_Test(parser)
        assert len(OVER_30_NOT_MARRIED) == 1

    def test_individual_over_30_married(self, today, individual, family):
        individual.birth_date = today - relativedelta(years=31)
        individual.family_spouse = family.id
        family.husband_id = individual.id

        parser = Parser(None)
        parser.individuals = {individual.id: individual}
        parser.families = {family.id: family}

        US31_Test(parser)
        assert len(OVER_30_NOT_MARRIED) == 0

    def test_two_individuals_with_one_over_30_not_married(
        self, make_individual, today, family
    ):
        i1 = make_individual()
        i1.birth_date = today
        i1.family_id = "FID"

        i2 = make_individual()
        i2.birth_date = today - relativedelta(years=31)

        parser = Parser(None)
        parser.individuals = {i1.id: i1, i2.id: i2}

        US31_Test(parser)
        assert len(OVER_30_NOT_MARRIED) == 1

    def test_individual_over_30_divorced(self, today, individual, family):
        individual.birth_date = today - relativedelta(years=31)
        family.husband_id = individual.id
        family.divorce_date = today

        parser = Parser(None)
        parser.individuals = {individual.id: individual}
        parser.families = {family.id: family}

        US31_Test(parser)
        assert len(OVER_30_NOT_MARRIED) == 1

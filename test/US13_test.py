from gedcom.parser import Parser
from gedcom.Tests.US13 import *

class TestUS13:
    def test_empty_siblings(self, individual):
        parser = Parser(None)
        parser.individuals = {individual.id: individual}

        US13_Test(parser)
        assert len(US13_Problems) == 0

    # Bad Smells #2-3: (refactor): avoid repetition by utilizing existing pytest fixtures
    def test_sibling_birth_dates_2_days(self, individual, make_family_with_birth_dates):
        make_family_with_birth_dates(["1990-01-01", "1990-01-03"])
        parser = Parser(None)
        parser.individuals = {individual.birth: individual}

        US13_Test(parser)
        assert len(US13_Problems) == 0

    def test_sibling_birth_dates_3_days(self, individual, make_family_with_birth_dates):
        make_family_with_birth_dates(["1990-01-01", "1990-01-04"])
        parser = Parser(None)

        parser.individuals = {
            individual.birth: individual
        }

        US13_Test(parser)
        assert len(US13_Problems) == 0

    
    def test_sibling_birth_dates_8_months(self, individual, make_family_with_birth_dates):
        make_family_with_birth_dates(["1990-01-01", "1990-09-01"])
        parser = Parser(None)

        parser.individuals = {
            individual.birth: individual
        }

        US13_Test(parser)
        assert len(US13_Problems) == 0

    def test_sibling_birth_dates_7_months(self, individual, make_family_with_birth_dates):
        make_family_with_birth_dates(["1990-01-01", "1990-08-01"])
        parser = Parser(None)

        parser.individuals = {
            individual.birth: individual
        }

        US13_Test(parser)
        assert len(US13_Problems) == 0

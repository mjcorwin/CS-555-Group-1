from gedcom.parser import Parser
from gedcom.Tests.US29 import *

class TestUS29:
    def test_empty_birth_date(self, individual, make_individual_with_birth_dates):
        parser = Parser(None)
        ex_birth_date = make_individual_with_birth_dates([""], "")
        parser.individuals = {
            individual.birth: ex_birth_date
        }
        
        US29_Test(parser)
        assert len(US29_Problems) == 0

    def test_single_birth_date(self, individual, make_individual_with_birth_dates):
        parser = Parser(None)
        ex_birth_date = make_individual_with_birth_dates("1990-01-07", "2001-01-10")
        parser.individuals = {
            individual.birth: ex_birth_date
        }
        
        US29_Test(parser)
        assert len(US29_Problems) == 0

    def test_multiple_birth_dates(self, individual, make_individual_with_birth_dates):
        parser = Parser(None)
        ex_birth_dates = make_individual_with_birth_dates(["1990-01-07", "1991-01-10"], "2001-01-10")
        parser.individuals = {
            individual.birth: ex_birth_dates
        }
        
        US29_Test(parser)
        assert len(US29_Problems) == 0
        



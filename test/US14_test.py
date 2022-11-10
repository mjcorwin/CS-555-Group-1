from gedcom.parser import Parser
from gedcom.Tests.US14 import *

class TestUS14:
    def test_empty_siblings(self, individual):
        parser = Parser(None)
        parser.individuals = {individual.id: individual}
        US14_Test(parser)
        assert len(US14_Problems) == 0

    
    def test_two_siblings(self, individual, make_family_with_birth_dates):
        parser = Parser(None)
        wesley_birthdate = make_family_with_birth_dates(("1990-01-01", "1990-01-01"))
        
        parser.individuals = {
            individual.birth: wesley_birthdate 
        }

        US14_Test(parser)
        assert len(US14_Problems) == 0

    def test_five_siblings(self, individual, make_family_with_birth_dates):
        parser = Parser(None)
        wesley_birthdate = make_family_with_birth_dates(("1990-01-01", "1990-01-01", "1990-01-01", "1990-01-01", "1990-01-01"))

        parser.individuals = {
            individual.birth: wesley_birthdate 
        }

        US14_Test(parser)
        assert len(US14_Problems) == 0
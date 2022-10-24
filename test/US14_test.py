from gedcom.parser import Parser
from gedcom.Tests.US14 import *

class TestUS14:
    def test_empty_siblings(self, individual):
        parser = Parser(None)
        parser.individuals = {individual.id: individual}
        US14_Test(parser)
        assert len(US14_Problems) == 0

    
    def test_two_siblings(self, individual, make_family_with_same_last_names, make_family_with_birth_dates):
        parser = Parser(None)
        wesley_surname = make_family_with_same_last_names(("Wesley, Wesley"))
        wesley_birthdate = make_family_with_birth_dates("1990-01-01")

        individual.id = wesley_surname.id
        
        parser.individuals = {
            individual.name: wesley_surname,
            individual.birth: wesley_birthdate 
        }

        US14_Test(parser)
        assert len(US14_Problems) == 0

    def test_five_siblings(self, individual, make_family_with_same_last_names, make_family_with_birth_dates):
        parser = Parser(None)
        wesley_surname = make_family_with_same_last_names(("Wesley, Wesley, Wesley, Wesley, Wesley"))
        wesley_birthdate = make_family_with_birth_dates("1990-01-01")

        individual.id = wesley_surname.id
        
        parser.individuals = {
            individual.name: wesley_surname,
            individual.birth: wesley_birthdate 
        }

        US14_Test(parser)
        assert len(US14_Problems) == 0
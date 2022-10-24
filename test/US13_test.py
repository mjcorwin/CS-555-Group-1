from gedcom.parser import Parser
from gedcom.Tests.US13 import *

class TestUS13:
    def test_empty_siblings(self, individual):
        parser = Parser(None)
        parser.individuals = {individual.id: individual}

        US13_Test(parser)
        assert len(US13_Problems) == 0

    def test_sibling_birth_dates_2_days(self, individual, make_family_with_same_last_names, make_family_with_birth_dates):
        parser = Parser(None)
        smith_surname = make_family_with_same_last_names("Smith")
        smith_birthdate = make_family_with_birth_dates(("1990-01-01", "1990-01-03"))

        individual.id = smith_surname.id

        parser.individuals = {
            individual.name: smith_surname,
            individual.birth: smith_birthdate,
        }

        US13_Test(parser)
        assert len(US13_Problems) == 0

    def test_sibling_birth_dates_3_days(self, individual, make_family_with_same_last_names, make_family_with_birth_dates):
        parser = Parser(None)
        jackson_surname = make_family_with_same_last_names("Jackson")
        jackson_birthdate = make_family_with_birth_dates(("1990-01-01", "1990-01-04"))

        individual.id = jackson_surname.id

        parser.individuals = {
            individual.name: jackson_surname,
            individual.birth: jackson_birthdate
        }

        US13_Test(parser)
        assert len(US13_Problems) == 0

        
        
    

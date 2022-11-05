from gedcom.parser import Parser
from gedcom.Tests.US24 import *


class TestUS24:
    def test_two_familes_same_names_different_marriage_date(
        self, make_individual, make_family, random_name, today, future_date
    ):
        husband_1 = make_individual()
        husband_1.name = random_name

        wife_1 = make_individual()
        wife_1.name = random_name

        husband_2 = make_individual()
        husband_2.name = random_name

        wife_2 = make_individual()
        wife_2.name = random_name

        individuals = {
            husband_1.id: husband_1,
            husband_2.id: husband_2,
            wife_1.id: wife_1,
            wife_2.id: wife_2,
        }

        f1 = make_family()
        f2 = make_family()

        f1.husband_id = husband_1.id
        f1.wife_id = wife_1.id
        f1.married_date = today

        f2.husband_id = husband_2.id
        f2.wife_id = wife_2.id
        f2.married_date = future_date

        families = {f1.id: f1, f2.id: f2}

        parser = Parser(None)
        parser.individuals = individuals
        parser.families = families

        US24_Test(parser)
        assert len(US24_Problems) == 0

    def test_two_families_different_spouse_names_same_marriage_date(
        self, make_individual, make_family, make_random_name, today
    ):
        husband_1 = make_individual()
        husband_1.name = make_random_name()

        wife_1 = make_individual()
        wife_1.name = make_random_name()

        husband_2 = make_individual()
        husband_2.name = make_random_name()

        wife_2 = make_individual()
        wife_2.name = make_random_name()

        individuals = {
            husband_1.id: husband_1,
            husband_2.id: husband_2,
            wife_1.id: wife_1,
            wife_2.id: wife_2,
        }

        f1 = make_family()
        f2 = make_family()

        f1.husband_id = husband_1.id
        f1.wife_id = wife_1.id
        f1.married_date = today

        f2.husband_id = husband_2.id
        f2.wife_id = wife_2.id
        f2.married_date = today

        families = {f1.id: f1, f2.id: f2}

        parser = Parser(None)
        parser.individuals = individuals
        parser.families = families

        US24_Test(parser)
        assert len(US24_Problems) == 0

    def test_two_families_same_spouse_names_same_marriage_date(
        self, make_individual, make_family, random_name, today
    ):
        husband_1 = make_individual()
        husband_1.name = random_name

        wife_1 = make_individual()
        wife_1.name = random_name

        husband_2 = make_individual()
        husband_2.name = random_name

        wife_2 = make_individual()
        wife_2.name = random_name

        individuals = {
            husband_1.id: husband_1,
            husband_2.id: husband_2,
            wife_1.id: wife_1,
            wife_2.id: wife_2,
        }

        f1 = make_family()
        f2 = make_family()

        f1.husband_id = husband_1.id
        f1.wife_id = wife_1.id
        f1.married_date = today

        f2.husband_id = husband_2.id
        f2.wife_id = wife_2.id
        f2.married_date = today

        families = {f1.id: f1, f2.id: f2}

        parser = Parser(None)
        parser.individuals = individuals
        parser.families = families

        US24_Test(parser)
        assert len(US24_Problems) == 1

    def test_three_families_same_spouse_names_same_marriage_date(
        self, make_individual, make_family, random_name, today
    ):
        husband_1 = make_individual()
        husband_1.name = random_name

        wife_1 = make_individual()
        wife_1.name = random_name

        husband_2 = make_individual()
        husband_2.name = random_name

        wife_2 = make_individual()
        wife_2.name = random_name

        husband_3 = make_individual()
        husband_3.name = random_name

        wife_3 = make_individual()
        wife_3.name = random_name

        individuals = {
            husband_1.id: husband_1,
            husband_2.id: husband_2,
            husband_3.id: husband_3,
            wife_1.id: wife_1,
            wife_2.id: wife_2,
            wife_3.id: wife_3,
        }

        f1 = make_family()
        f2 = make_family()
        f3 = make_family()

        f1.husband_id = husband_1.id
        f1.wife_id = wife_1.id
        f1.married_date = today

        f2.husband_id = husband_2.id
        f2.wife_id = wife_2.id
        f2.married_date = today

        f3.husband_id = husband_3.id
        f3.wife_id = wife_3.id
        f3.married_date = today

        families = {f1.id: f1, f2.id: f2, f3.id: f3}

        parser = Parser(None)
        parser.individuals = individuals
        parser.families = families

        US24_Test(parser)
        assert len(US24_Problems) == 1
        assert len(US24_Problems[0].hFamily_IDs) == 3

    def test_three_families_two_with_same_spouse_names_same_marriage_date(
        self, make_individual, make_family, random_name, make_random_name, today
    ):
        husband_1 = make_individual()
        husband_1.name = random_name

        wife_1 = make_individual()
        wife_1.name = random_name

        husband_2 = make_individual()
        husband_2.name = random_name

        wife_2 = make_individual()
        wife_2.name = random_name

        husband_3 = make_individual()
        husband_3.name = make_random_name()

        wife_3 = make_individual()
        wife_3.name = make_random_name()

        individuals = {
            husband_1.id: husband_1,
            husband_2.id: husband_2,
            husband_3.id: husband_3,
            wife_1.id: wife_1,
            wife_2.id: wife_2,
            wife_3.id: wife_3,
        }

        f1 = make_family()
        f2 = make_family()
        f3 = make_family()

        f1.husband_id = husband_1.id
        f1.wife_id = wife_1.id
        f1.married_date = today

        f2.husband_id = husband_2.id
        f2.wife_id = wife_2.id
        f2.married_date = today

        f3.husband_id = husband_3.id
        f3.wife_id = wife_3.id
        f3.married_date = today

        families = {f1.id: f1, f2.id: f2, f3.id: f3}

        parser = Parser(None)
        parser.individuals = individuals
        parser.families = families

        US24_Test(parser)
        assert len(US24_Problems) == 1
        assert len(US24_Problems[0].hFamily_IDs) == 2

    def test_two_sets_of_two_families_same_spouse_names_same_marriage_date(
        self, make_individual, make_family, make_random_name, today, future_date
    ):
        name_1 = make_random_name()
        name_2 = make_random_name()

        husband_1 = make_individual()
        husband_1.name = name_1

        wife_1 = make_individual()
        wife_1.name = name_1

        husband_2 = make_individual()
        husband_2.name = name_1

        wife_2 = make_individual()
        wife_2.name = name_1

        husband_3 = make_individual()
        husband_3.name = name_2

        wife_3 = make_individual()
        wife_3.name = name_2

        husband_4 = make_individual()
        husband_4.name = name_2

        wife_4 = make_individual()
        wife_4.name = name_2

        individuals = {
            husband_1.id: husband_1,
            husband_2.id: husband_2,
            husband_3.id: husband_3,
            husband_4.id: husband_4,
            wife_1.id: wife_1,
            wife_2.id: wife_2,
            wife_3.id: wife_3,
            wife_4.id: wife_4,
        }

        f1 = make_family()
        f2 = make_family()
        f3 = make_family()
        f4 = make_family()

        f1.husband_id = husband_1.id
        f1.wife_id = wife_1.id
        f1.married_date = today

        f2.husband_id = husband_2.id
        f2.wife_id = wife_2.id
        f2.married_date = today

        f3.husband_id = husband_3.id
        f3.wife_id = wife_3.id
        f3.married_date = future_date

        f4.husband_id = husband_4.id
        f4.wife_id = wife_4.id
        f4.married_date = future_date

        families = {f1.id: f1, f2.id: f2, f3.id: f3, f4.id: f4}

        parser = Parser(None)
        parser.individuals = individuals
        parser.families = families

        US24_Test(parser)
        assert len(US24_Problems) == 2
        assert len(US24_Problems[0].hFamily_IDs) == 2
        assert len(US24_Problems[1].hFamily_IDs) == 2

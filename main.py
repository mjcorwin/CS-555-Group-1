from os import path

from gedcom import printer, validator
from gedcom.parser import Parser

from gedcom import Tests

#INPUT_FILE_PATH = path.join(path.dirname(path.realpath(__file__)), "input3.gedcom")
INPUT_FILE_PATH = path.join(path.dirname(path.realpath(__file__)), "US25.ged");
OUTPUT_FILE_PATH = path.join(path.dirname(path.realpath(__file__)), "results.txt")


def main():
    with open(INPUT_FILE_PATH) as infile:
        parser = Parser(infile)
        parser.parse()

    with open(OUTPUT_FILE_PATH, "w") as outfile:
        validations = "\n".join(validator.validate(parser.individuals, parser.families))

        marriage_before_death = Tests.gedcom.Tests.US05.Execute(parser)

        divorce_before_death = Tests.gedcom.Tests.US06.Execute(parser)

        individuals_table = printer.print_individuals(parser.individuals.values())
        family_table = printer.print_families(
            parser.families.values(), parser.individuals
        )

        '''
            LT_150 = Tests.gedcom.Tests.US07.Execute(parser)

            BIR_BF_MARR_AF_DIV = Tests.gedcom.Tests.US08.Execute(parser)
            # US09 - Can't be born after parents death
            US09 = Tests.gedcom.Tests.US09.Execute(parser)

            # US10 - No marrying before 14 for husb or wife
            US10 = Tests.gedcom.Tests.US10.Execute(parser)

            # US11 - No bigamy
            NO_BIGAMY = Tests.gedcom.Tests.US11.Execute(parser)

            # US12 - Parents not too old
            PARENTS_NOT_TOO_OLD = Tests.gedcom.Tests.US12.Execute(parser)

            # US13 - SIBLINGS SPACING
            US13 = Tests.gedcom.Tests.US13.Execute(parser)

            # US14 - MULTIPLE BIRTHS <= 5
            US14 = Tests.gedcom.Tests.US14.Execute(parser)

            # US15 - More than 15 siblings
            TOO_MANY_SIBLINGS = Tests.gedcom.Tests.US15.Execute(parser)

            # US16 - More than 15 siblings
            MALE_FAMILY_MEMBERS_DIFFERENT_LAST_NAME = Tests.gedcom.Tests.US16.Execute(
                parser
            )

            # US17 - Not married to descendants
            NOT_MARRIED_TO_DESCENDANTS = Tests.gedcom.Tests.US17.Execute(parser)

            # US18 - Siblings should not marry
            SIBLINGS_NOT_MARRIED = Tests.gedcom.Tests.US18.Execute(parser)

            # US23 - Individuals with same name and birthdate
            SAME_NAME_SAME_BIRTH_DATE = Tests.gedcom.Tests.US23.Execute(parser)

            # US24 - Families with same spouse names and marriage date
            SAME_SPOUSE_NAMES_SAME_MARRIED_DATE = Tests.gedcom.Tests.US24.Execute(parser)

            # US21 - Correct Gender for Role
            US21 = Tests.gedcom.Tests.US21.Execute(parser)

            # US22 - Unique IDs
            US22 = Tests.gedcom.Tests.US22.Execute(parser)
        '''

        # US25 - Unique first names in families
        US25 = Tests.gedcom.Tests.US25.Execute(parser);


        '''
            # US31 - List individuals over 30 and not married
            US31 = Tests.gedcom.Tests.US31.Execute(parser)

            # US32 - List multiple births
            US32 = Tests.gedcom.Tests.US32.Execute(parser)


            #US29 - List deceased
            US29 = Tests.gedcom.Tests.US29.Execute(parser)

            #US30 - List living married
            US30 = Tests.gedcom.Tests.US30.Execute(parser)

            print("INDIVIDUALS")
            print(individuals_table)
            print("FAMILIES")
            print(family_table)
            print("VALIDATIONS")
            print(validations)
            print("MARRIAGE BEFORE DEATH")
            print(marriage_before_death)
            print("DIVORCE BEFORE DEATH")
            print(divorce_before_death)

            print("LESS THAN 150 YEARS OLD")
            print(LT_150)

            print("Born before marriage or after divorce")
            print(BIR_BF_MARR_AF_DIV)

            print("Born after parents death")
            print(US09)

            print("No marrying before 14")
            print(US10)

            print("Same name same birthdate")
            print(SAME_NAME_SAME_BIRTH_DATE)

            print("Same spouse names same marriage date")
            print(SAME_SPOUSE_NAMES_SAME_MARRIED_DATE)

            print("US13: Siblings Spacing")
            print(US13)

            print("US14: Multiple births <= 5")
            print(US14)

            print("US21: Correct gender for role")
            print(US21)

            print("US22: Unique IDs")
            print(US22)

            print("US31: List individuals over 30 and not married")
            print(US31)

            print("US32: List multiple births")
            print(US32)

            print("US29: List deceased")
            print(US29)

            print("US30: List living married")
            print(US30)

            outfile.write("INDIVIDUALS\n")
            outfile.write(individuals_table)
            outfile.write("\nFAMILIES\n")
            outfile.write(family_table)

            outfile.write("\nVALIDATIONS\n")
            outfile.write(validations)
            outfile.write("\n")
            outfile.write("\nMARRIAGE BEFORE DEATH\n")
            outfile.write(marriage_before_death)
            outfile.write("\nDIVORCE BEFORE DEATH\n")
            outfile.write(divorce_before_death)

            outfile.write("\n\nLESS THAN 150 YEARS OLD\n")
            outfile.write(LT_150)

            outfile.write("\n\nBorn before marriage or after divorce\n")
            outfile.write(BIR_BF_MARR_AF_DIV)

            outfile.write("\n\nBorn after death of parent(s)\n")
            outfile.write(US09)

            outfile.write("\n\nMarried before either spouse is 14\n")
            outfile.write(US10)

            outfile.write("\n\nNO BIGAMY\n")
            outfile.write(NO_BIGAMY)

            outfile.write("\n\nPARENTS NOT TOO OLD\n")
            outfile.write(PARENTS_NOT_TOO_OLD)

            outfile.write("\n\nPARENTS NOT TOO OLD\n")
            outfile.write(PARENTS_NOT_TOO_OLD)

            outfile.write("\n\nUS13: SIBLINGS SPACING\n")
            outfile.write(US13)

            outfile.write("\n\nUS14: Multiple Births > 5\n")
            outfile.write(US14)

            outfile.write("\n\nTOO MANY SIBLINGS\n")
            outfile.write(TOO_MANY_SIBLINGS)

            # US17 - Not married to descendants
            outfile.write("\nNOT MARRIED TO DESCENDANTS\n")
            outfile.write(NOT_MARRIED_TO_DESCENDANTS)

            # US18 - Siblings should not marry
            outfile.write("\nSIBLINGS NOT MARRIED\n")
            outfile.write(SIBLINGS_NOT_MARRIED)

            outfile.write("\n\nMALE FAMILY MEMBER DIFFERENT LAST NAMES\n")
            outfile.write(MALE_FAMILY_MEMBERS_DIFFERENT_LAST_NAME)

            outfile.write("\n\nSAME NAME SAME BIRTHDATE\n")
            outfile.write(SAME_NAME_SAME_BIRTH_DATE)

            outfile.write("\n\nSAME SPOUSE NAMES SAME MARRIAGE DATE\n")
            outfile.write(SAME_SPOUSE_NAMES_SAME_MARRIED_DATE)

            outfile.write("\n\n\nUS21: Correct Gender for Role\n")
            outfile.write(US21)

            outfile.write("\n\nUS22: Unique IDs\n")
            outfile.write(US22)
        '''

        outfile.write("\n\nUS25: Unique first names in families\n")
        outfile.write(US25);


        '''
            outfile.write("\nUS31: List individuals over 30 and not married\n")
            outfile.write(US31)

            outfile.write("\nUS32: List multiple births\n")
            outfile.write(US32)

            outfile.write("\n\nUS29: List deceased\n")
            outfile.write(US29)

            outfile.write("\n\nUS30: List living married\n")
            outfile.write(US30)
        '''

    Run_Tests(parser)


def Run_Tests(hParser):
    '''
        Tests.US03.Execute(hParser)
        Tests.US04.Execute(hParser)
        Tests.US05.Execute(hParser)
        Tests.US06.Execute(hParser)
        Tests.US07.Execute(hParser)
        Tests.US08.Execute(hParser)
        Tests.US09.Execute(hParser)
        Tests.US10.Execute(hParser)
        Tests.US11.Execute(hParser)
        Tests.US12.Execute(hParser)
        Tests.US13.Execute(hParser)
        Tests.US14.Execute(hParser)
        Tests.US15.Execute(hParser)
        Tests.US16.Execute(hParser)
        Tests.US17.Execute(hParser)
        Tests.US18.Execute(hParser)
        Tests.US23.Execute(hParser)
        Tests.US24.Execute(hParser)
    '''

    Tests.US25.Execute(hParser);


    '''
        Tests.US21.Execute(hParser)
        Tests.US22.Execute(hParser)
        Tests.US31.Execute(hParser)
        Tests.US32.Execute(hParser)
        Tests.US29.Execute(hParser)
        Tests.US30.Execute(hParser)
    '''


if __name__ == "__main__":
    main()

from os import path
from unittest import TestCase

from gedcom import printer, validator
from gedcom.parser import Parser

from gedcom import Tests

INPUT_FILE_PATH = path.join(path.dirname(path.realpath(__file__)), "input.gedcom")
OUTPUT_FILE_PATH = path.join(path.dirname(path.realpath(__file__)), "results.txt")


def main():
    with open(INPUT_FILE_PATH) as infile:
        parser = Parser(infile)
        parser.parse()

    with open(OUTPUT_FILE_PATH, "w") as outfile:
        validations = "\n".join(validator.validate(parser.individuals, parser.families))

        #marriage_before_death = Tests.gedcom.Tests.US05.Execute(parser)

        #divorce_before_death = Tests.gedcom.Tests.US06.Execute(parser)


    Run_UnitTests(parser)
    #Run_Tests(parser)



def Run_Tests(hParser):
    Tests.US03.Execute(hParser);
    Tests.US04.Execute(hParser);
    Tests.US05.Execute(hParser);
    Tests.US06.Execute(hParser);
    Tests.US07.Execute(hParser);
    Tests.US08.Execute(hParser);

def Run_UnitTests(hParser):
    assert Tests.US07.ExecuteTests(hParser) == True


if __name__ == "__main__":
    main()

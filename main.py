from os import path

from gedcom import printer
from gedcom.parser import Parser

from gedcom import Tests;

INPUT_FILE_PATH = path.join(path.dirname(path.realpath(__file__)), "input.gedcom")
OUTPUT_FILE_PATH = path.join(path.dirname(path.realpath(__file__)), "results.txt")


def main():
    with open(INPUT_FILE_PATH) as infile:
        parser = Parser(infile)
        parser.parse()

    with open(OUTPUT_FILE_PATH, "w") as outfile:

        individuals_table = printer.print_individuals(parser.individuals.values())
        family_table = printer.print_families(
            parser.families.values(), parser.individuals
        )

        print("INDIVIDUALS")
        print(individuals_table)
        print("FAMILIES")
        print(family_table)

        outfile.write("INDIVIDUALS\n")
        outfile.write(individuals_table)
        outfile.write("\nFAMILIES\n")
        outfile.write(family_table)

    Run_Tests(parser);

def Run_Tests(hParser):
    Tests.US03.Execute(hParser);
    Tests.US04.Execute(hParser);

if __name__ == "__main__":
    main()

import atexit
import os
import sys

import persistence
from repository import rep


def main(inputfilename):
    rep.__init__()
    rep.create_tables()
    with open(inputfilename) as inputfile:
        content = inputfile.read()
        lines = content.split("\n")
        for line in lines:
            splitLine = line.split(', ')
            if splitLine[0] == 'C':
                coffee_stand = persistence.Coffee_stand(splitLine[1], splitLine[2], splitLine[3])
                rep.coffee_stands.insert(coffee_stand)
            elif splitLine[0] == 'S':
                supplier = persistence.Supplier(splitLine[1], splitLine[2], splitLine[3])
                rep.suppliers.insert(supplier)
            elif splitLine[0] == 'E':
                employee = persistence.Employee(splitLine[1], splitLine[2], splitLine[3], splitLine[4])
                rep.employees.insert(employee)
            elif splitLine[0] == 'P':
                product = persistence.Product(splitLine[1], splitLine[2], splitLine[3],0)
                rep.products.insert(product)


if __name__ == '__main__':
    main(sys.argv[1])

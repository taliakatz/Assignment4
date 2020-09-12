import sys
import persistence
import printdb
from repository import rep


def main(inputfilename):
    with open(inputfilename) as inputfile:
        for line in inputfile:
            splitLine = line.split(", ")
            # s = splitLine[3].strip('/n')
            # splitLine[3] = s
            product_id = splitLine[0]
            sale_or_supply = splitLine[1]
            employee_or_supplier_id = splitLine[2]
            date = splitLine[3]
            if int(sale_or_supply) > 0:
                product = rep.products.find(product_id)
                if product is None:
                    rep.products.insert(product)
                else:
                    quantity = product.quantity + int(sale_or_supply)
                    rep.products.update(quantity, product_id)
                    activity = persistence.Activitie(product_id, sale_or_supply, employee_or_supplier_id, date)
                    rep.activities.insert(activity)
            else:
                product = rep.products.find(product_id)
                quantity = product.quantity + int(sale_or_supply)
                if quantity >= 0:
                    rep.products.update(quantity, product_id)
                    activity = persistence.Activitie(product_id, sale_or_supply, employee_or_supplier_id, date)
                    rep.activities.insert(activity)


if __name__ == '__main__':
    main(sys.argv[1])
    printdb.main()

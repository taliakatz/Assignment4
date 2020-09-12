from repository import rep

def main():
    print("Activities")
    all = rep.activities.find_all()
    for Activitie in all:
        print(Activitie)
    print("Coffee stands")
    all = rep.coffee_stands.find_all()
    for Coffee_stand in all:
        print(Coffee_stand)
    print("Employees")
    all = rep.employees.find_all()
    for Employee in all:
        print(Employee)
    print("Products")
    all = rep.products.find_all()
    for Product in all:
        print(Product)
    print("Suppliers")
    all = rep.suppliers.find_all()
    for Supplier in all:
        print(Supplier)
    print("")
    print("Employees report")
    all = rep.get_employees_reports()
    for Employees_report in all:
        print('{} {} {} {}'.format(Employees_report.name,Employees_report.salary,Employees_report.working_location,Employees_report.total))
    print("")
    print("Activities")
    all = rep.get_activities_report()
    for activities_report in all:
        print(activities_report)




if __name__ == '__main__':
    main()
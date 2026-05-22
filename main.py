# STEP 0

# SQL Library and Pandas Library
import sqlite3
import pandas as pd

# Connect to the database
conn = sqlite3.connect('data.sqlite')

pd.read_sql("""select * from sqlite_master""", conn)

# STEP 1
# Replace None with your code
df_boston = pd.read_sql("""select 
                            firstName, 
                            lastName
                        from employees
                        join offices using(officeCode)
                        where city='Boston';""", conn)

print(df_boston)
print("----------------BORDER-------------------")

# STEP 2
# Replace None with your code
df_zero_emp = pd.read_sql("""select count(employeeNumber) as num_employees
                             from employees
                             join offices using(officeCode)
                             group by city
                             having count(employeeNumber)==0;""", conn)

print(df_zero_emp)
print("----------------BORDER-------------------")

# STEP 3
# Replace None with your code
df_employee = pd.read_sql("""select 
                        e.firstName,e.lastName,
                        o.city,o.state
                        from employees as e
                        left join offices as o using(officeCode)
                        order by e.firstName, e.lastName;""", conn)

print(df_employee)
print("----------------BORDER-------------------")

# STEP 4
# Replace None with your code
df_contacts = pd.read_sql("""select 
                        c.contactFirstName,c.contactLastName,c.phone, c.salesRepEmployeeNumber
                        from customers as c
                        left join orders as o on c.customerNumber=o.customerNumber
                        where o.customerNumber is null 
                        order by c.contactLastName asc;""", conn)

print(df_contacts)
print("----------------BORDER-------------------")

# STEP 5
# Replace None with your code
df_payment = pd.read_sql("""select 
                        c.contactFirstName,c.contactLastName,p.amount, p.paymentDate
                        from customers as c
                        join payments as p on c.customerNumber=p.customerNumber
                        order by cast(p.amount as float) desc;""", conn)

print(df_payment)
print("----------------BORDER-------------------")

# STEP 6
# Replace None with your code
df_credit = pd.read_sql("""select 
                        e.employeeNumber, e.firstName, e.lastName,
                        count(c.customerNumber) as num_of_customers
                        from employees as e
                        join customers as c on e.employeeNumber=c.salesRepEmployeeNumber
                        group by e.employeeNumber,e.firstName,e.lastName
                        having avg(c.creditLimit)>90000
                        order by num_of_customers desc
                        limit 4;""", conn) 

print(df_credit)
print("----------------BORDER-------------------")


# STEP 7
# Replace None with your code
df_product_sold = pd.read_sql("""select 
                              p.productName,
                              count(o.orderNumber) as numorders,
                              sum(o.quantityOrdered) as totalunits
                              from products as p
                              join orderdetails as o on p.productCode=o.productCode
                              group by p.productName
                              order by totalunits desc
                        ;""", conn) 

print(df_product_sold)
print("----------------BORDER-------------------")

# STEP 8
# Replace None with your code
df_total_customers = pd.read_sql("""select 
                              p.productName,p.productCode,
                              count(distinct c.customerNumber) as numpurchasers
                              from products as p
                              join orderdetails as od on p.productCode=od.productCode
                              join orders as o on od.orderNumber=o.orderNumber
                              join customers as c on o.customerNumber=c.customerNumber
                              group by p.productName,p.productCode
                              order by numpurchasers desc;""", conn) 

print(df_total_customers)
print("----------------BORDER-------------------")

# STEP 9
# Replace None with your code
df_customers = pd.read_sql("""select 
                           o.officeCode,o.city,
                           count(distinct c.customerNumber) as n_customers
                           from offices as o
                           join employees as e on o.officeCode=e.officeCode
                           join customers as c on e.employeeNumber=c.salesRepEmployeeNumber
                           group by o.officeCode, o.city;""", conn) 

print(df_customers)
print("----------------BORDER-------------------")


# STEP 10
# Replace None with your code
df_under_20 = pd.read_sql("""
                          with low_volume_products as (
                            select p.productCode
                            from products p
                            join orderdetails od on p.productCode = od.productCode
                            join orders ord on od.orderNumber = ord.orderNumber
                            join customers c on ord.customerNumber = c.customerNumber
                            group by p.productCode
                            HAVING COUNT(DISTINCT c.customerNumber) <= 19
                            )
                        select DISTINCT e.employeeNumber, e.firstName, e.lastName,
                                        o.city, e.officeCode
                        from employees as e
                        join offices as o on e.officeCode = o.officeCode
                        join customers as c on e.employeeNumber = c.salesRepEmployeeNumber
                        join orders as ord on c.customerNumber = ord.customerNumber
                        join orderdetails as od on ord.orderNumber = od.orderNumber
                        where od.productCode IN (select productCode from low_volume_products)
                        order by e.lastName asc
                        """,conn)
print(df_under_20)
print("----------------BORDER-------------------")
conn.close()
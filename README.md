
# Datanota AMBER - DATA360
## stock investment recommendation

Version: MVP 

algorithm: simple weighted average

<br>

![local](./assets/amber_apphome.png)

<br>

## database:
        an Excel file is the data source

<br>

![local](./assets/db_schema_amber.png)

<br>

## buy: 
        given a dollar amount (default value is $1000)
            1. to calculate quantity per stock (considering current price)
            2. to calculate percentage change in weighted average price if invested
            3. to sort from smallest to largest

<br>

![local](./assets/amber_buy.png)

<br>

## sell: 
        given a dollar amount (default value is $1000)
            1. find the oldest transaction
            2. list the oldest unit_price and quantity
            3. calculate percentage change in weighted average after selling the oldest entry

<br>

![local](./assets/amber_sell.png)

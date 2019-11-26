csv2sql
========
[![Support Python Version](https://img.shields.io/badge/Python-3-brightgreen.svg?style=for-the-badge)](https://www.python.org/)


csv file to sql.
---

## [Introduction]()

```text
usage: csv2sql.py [-h] -t TABLE [-d {mysql,oracle}] [-s SEPARATOR] [-e]
                  [-m ORDER_MAPPING]
                  csv_file

Convert a csv file to a sql insert statement for the specified table

positional arguments:
  csv_file              The CSV file to be read

optional arguments:
  -h, --help            show this help message and exit
  -t TABLE, --table TABLE
                        The name of the database table
  -d {mysql,oracle}, --db {mysql,oracle}
                        Database type
  -s SEPARATOR, --separator SEPARATOR
                        The separator used in the CSV
  -e, --exclude_first_line
                        Exclude the first line of csv file
  -m ORDER_MAPPING, --order_mapping ORDER_MAPPING
                        Order Mapping of csv file field and database table
                        field

```

## [Usage]()

if your csv file like this:
```text
name,age,gender
lisa,18,0
mike,20,1
...
```

and you just want to insert the first two columns of data into the database, then your `order_mapping` is `{"name": 0, "age": 1}`.

so, your command is:

```text
python3 csv2sql.py YourCsvFile.csv -t YourTableName -e -m '{"name": 0, "age": 1}'
```
> Generate sql according to mysql syntax by default. if your database is oracle, then add arg `-d oracle`.
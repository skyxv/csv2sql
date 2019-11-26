import argparse
import csv
import json
from datetime import datetime


def parse_arguments():
    parser = argparse.ArgumentParser(description="Convert a csv file to a sql insert statement for the specified table")
    parser.add_argument('csv_file', type=argparse.FileType('r'), help='The CSV file to be read')
    parser.add_argument('-t', '--table', help='The name of the database table', required=True)
    parser.add_argument('-d', '--db', default='mysql', choices=["mysql", "oracle"], help='Database type')
    parser.add_argument('-s', '--separator', default=',', help='The separator used in the CSV')
    parser.add_argument("-e", "--exclude_first_line", help="Exclude the first line of csv file",
                        action="store_true")
    parser.add_argument("-m", "--order_mapping", type=json.loads, help="Order Mapping of csv file field and database table field")

    return parser.parse_args()


class SqlGenerator:
    """
    Convert a csv file to a sql insert statement for the specified table, and write it to `.sql` file.
    """

    def __init__(self, csv_file, table_name, db_type, separator, exclude_first_line, order_mapping):
        """
        :param csv_file: the CSV file to be read.
        :param table_name: the name of the database table.
        :param db_type: database type.
        :param separator: the separator used in the CSV.
        :param exclude_first_line: exclude the first line of csv file.
        :param order_mapping: order mapping of csv file field and database table field.
        """
        self.csv_file = csv_file
        self.table_name = table_name
        self.db_type = db_type
        self.separator = separator
        self.exclude_first_line = exclude_first_line
        self.order_mapping = order_mapping

        self.om_keys_str = ",".join(order_mapping.keys())
        self.mysql_insert_sql = "INSERT INTO {}({}) VALUES\n".format(self.table_name, self.om_keys_str)
        self.orcl_insert_sql = "INSERT ALL \n"

    def is_mysql_db(self):
        return self.db_type == "mysql"

    def get_sql(self, reader):
        for row in reader:
            row_str = ""
            for index in self.order_mapping.values():
                row_str += "'" + row[index] + "',"
            row_str = row_str.strip(',')
            if self.is_mysql_db():
                self.mysql_insert_sql += "(" + row_str + "),\n"
            else:
                self.orcl_insert_sql += "INTO {} ({})\nVALUES ({})\n".format(self.table_name, self.om_keys_str, row_str)
        if self.is_mysql_db():
            return self.mysql_insert_sql[:-2]  # removed `,\n`
        else:
            return self.orcl_insert_sql + "select 1 from dual;\n" + "COMMIT;"

    @property
    def time_string(self):
        now = datetime.now()
        return "{}{}{}{}{}{}".format(now.year, now.month, now.day, now.hour, now.minute, now.second)

    def write_sql_to_file(self, sql):
        with open("./{}.sql".format(self.time_string), 'w') as f:
            f.write(sql)

    def run(self):
        with self.csv_file as f:
            reader = csv.reader(f, delimiter=self.separator, quoting=csv.QUOTE_ALL)
            if self.exclude_first_line:
                next(f)
            self.write_sql_to_file(self.get_sql(reader))


def main():
    args = parse_arguments()
    sql_generator = SqlGenerator(args.csv_file, args.table, args.db, args.separator,
                                 args.exclude_first_line, args.order_mapping)

    sql_generator.run()


if __name__ == "__main__":
    main()

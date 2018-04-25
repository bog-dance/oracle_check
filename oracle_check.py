#!/usr/bin/python3

# oracle_check
# v1.0
#
# Maintainer: Bogdan Tsikhanovskyi (bogdan.tsikhanovskyi@gettyimages.com)
#
# Check for oracle databases.


import cx_Oracle
import argparse

db_user = "monitoring"
db_password = "password"
connection_strings = {
    "dbname1": "(DESCRIPTION=(LOAD_BALANCE=OFF)(FAILOVER=ON)(ADDRESS=(PROTOCOL=TCP)(HOST=hostname1.com)(PORT=1521))(ADDRESS=(PROTOCOL=TCP)(HOST=hostname2.com)(PORT=1521))(CONNECT_DATA=(service_name=name)))",
    "dbname2": "(DESCRIPTION=(LOAD_BALANCE=OFF)(FAILOVER=ON)(ADDRESS=(PROTOCOL=TCP)(HOST=hostname3.com)(PORT=1521))(ADDRESS=(PROTOCOL=TCP)(HOST=hostname4.com)(PORT=1521))(CONNECT_DATA=(service_name=name)))",

}
sql_statement = "select CHECK_NAME, PRIORITY, MESSAGE_TEXT from NAGIOS.VW_DB_HEALTH_CHECKS"


def main():
    dbname = arg_parser()
    db_conn_string = define_connstring(dbname)
    cursor = db_connect(db_user, db_password, db_conn_string)
    check_result = sql_exec(cursor, sql_statement)
    status, exit_code = get_status(check_result)
    output = format_output(status, exit_code, check_result, db_conn_string)
    print(output)
    exit(exit_code)


def arg_parser():
    parser = argparse.ArgumentParser(description='Oracle DB checker')
    parser.add_argument('--dbname', help='to specify of destination host')
    args = parser.parse_args()
    dbname = args.dbname
    return dbname


def define_connstring(dbname):
    if dbname in connection_strings:
        conn_string = connection_strings[dbname]
    else:
        print('There is no such connection string! Available connection strings: {}'.format(connection_strings.keys()))
        exit(1)
    return conn_string


def db_connect(db_user, db_password, db_conn_string):
    try:
        connection = cx_Oracle.connect(db_user, db_password, db_conn_string)
        cursor = connection.cursor()
    except Exception as conn_exception:
        status_message = 'Conn string: {}\nCan\'t connect to oracle db\n{}'.format(db_conn_string, conn_exception)
        print(status_message)
        exit(2)
    return cursor


def sql_exec(cursor, sql_statement):
    cursor.execute(sql_statement)
    data = cursor.fetchall()
    return data


def get_status(check_result):
    status = None
    if not check_result:
        status = "OK"
        exit_code = 0
    else:
        statuses = []
        for check in check_result:
            statuses.append(check[1])
        if "CRITICAL" in statuses:
            status = "CRITICAL"
            exit_code = 2
        elif ("WARNING" in statuses) and ("CRITICAL" not in statuses):
            status = "WARNING"
            exit_code = 1
        elif ("WARNING" not in statuses) and ("CRITICAL" not in statuses):
            status = "OK"
            exit_code = 0
    return status, exit_code


def format_output(status, exit_code, check_result, db_conn_string):
    check_result_str = []
    for check in check_result:
        check_result_str.append(' <li>{}</li>'.format(' '.join(check)))
    check_result_str = '\n'.join(check_result_str)
    status_message = '<h3>General status: <b>{}</b></h3>\n <b>Conn. string:</b> {}\n<ul>\n<b>Statuses of particular checks:</b>\n{}\n</ul>'.format(status, db_conn_string, check_result_str)
    return status_message


if __name__ == "__main__":
    main()

import csv
import os
from argparse import ArgumentParser
from datetime import datetime
from operator import itemgetter
from pathlib import Path

parser = ArgumentParser()
parser.add_argument("-i", "--input", dest="input_file",
    default='/tmp/activity.csv',
    help="CSV input file with transactions (default: %(default)s)")
parser.add_argument("-o", "--output", dest="output_file",
    default='/tmp/activity-processed.csv',
    help="Output location of reformatted CSV (default: %(default)s)")
args = parser.parse_args()

expenses = []
found_format = None


def convert_input(row):
    if (found_format == 'post_desc_amt_cat'):
        if float(row[3]) > 0:
            return {
                "transaction_date": datetime.strptime(row[0], '%m/%d/%Y').strftime('%Y-%m-%d'),
                "description": row[2],
                "amount": row[3],
                "category": row[4],
                }
    elif (found_format == 'long_commas'):
        if float(row[7]) > 0:
            return {
                "transaction_date": datetime.strptime(row[0], '%m/%d/%Y %a').strftime('%Y-%m-%d'),
                "description": row[2],
                "amount": row[7],
                "category": "",
                }
    elif (found_format == 'name_memo_amt'):
        if row[1] == "DEBIT":
            return {
                "transaction_date": datetime.strptime(row[0], '%m/%d/%Y').strftime('%Y-%m-%d'),
                "description": row[2],
                "amount": row[4],
                "category": "",
                }
    elif (found_format == 'amex'):
        if float(row[2]) > 0:
            return {
                "transaction_date": datetime.strptime(row[0], '%m/%d/%y').strftime('%Y-%m-%d'),
                "description": row[1],
                "amount": row[2],
                "category": "",
                }
    elif (found_format == 'business'):
        if float(row[2]) > 0:
            return {
                "transaction_date": datetime.strptime(row[0].strip(), '%m/%d/%Y').strftime('%Y-%m-%d'),
                "description": row[1],
                "amount": row[2],
                "category": "",
                }
    elif (found_format == 'date_trans'):
        if abs(float(row[4])) > 0:
            return {
                "transaction_date": datetime.strptime(row[0], '%m/%d/%Y').strftime('%Y-%m-%d'),
                "description": row[2],
                "amount": abs(float(row[4])),
                "category": "",
                }
    elif (found_format == 'desc_cat_type'):
        if row[4] == "Sale":
            return {
                "transaction_date": datetime.strptime(row[0], '%m/%d/%Y').strftime('%Y-%m-%d'),
                "description": row[2],
                "amount": row[5],
                "category": row[3],
                }
    elif (found_format == 'status_debit_credit'):
        if row[3] and float(row[3]) > 0:
            return {
                "transaction_date": datetime.strptime(row[1], '%m/%d/%Y').strftime('%Y-%m-%d'),
                "description": row[2],
                "amount": row[3],
                "category": "",
                }
    elif (found_format == 'hsbc'):
        if row[2] and float(row[2]) > 0:
            excess_transaction_detail_start = row[1].find(" REF NO") - 3

            return {
                "transaction_date": datetime.strptime(row[0].strip(), '%m/%d/%Y').strftime('%Y-%m-%d'),
                "description": row[1][0:excess_transaction_detail_start].strip(),
                "amount": row[2],
                "category": "",
                }


def detect_format(first_row):
    input_format = None

    if first_row == "Trans. Date,Post Date,Description,Amount,Category":
        input_format = "post_desc_amt_cat"
    elif first_row == "Transaction Date,Post Date,Description,Category,Type,Amount":
        input_format = "desc_cat_type"
    elif first_row == "Status,Date,Description,Debit,Credit":
        input_format = "status_debit_credit"
    elif first_row == '"Date","Transaction","Name","Memo","Amount"':
        input_format = "date_trans"
    elif first_row == "Date,Description,Amount":
        input_format = "amex"
    elif "REF NO" in first_row and "TRAN CD" in first_row and "SIC CD" in first_row:
        input_format = "hsbc"
    elif ',,,,,,' in first_row:
        input_format = "long_commas"

    return input_format


try:
    with open(args.input_file) as csv_file:
        csv_reader = csv.reader(csv_file)

        first_row = csv_file.readline().strip()
        found_format = detect_format(first_row)

        if found_format == None:
            print("Format not recognised for {}".format(args.input_file))
            exit(1)

        if found_format != 'long_commas':
            next(csv_reader)

        for row in csv_reader:
            row_extract = convert_input(row)

            if row_extract:
                expenses.append(row_extract)

except FileNotFoundError:
    print("Cannot open transactions file: " + args.input_file)


if expenses:
    expenses.sort(key=itemgetter("transaction_date"))

    if Path(args.output_file).is_file():
        os.remove(args.output_file)

    with open(args.output_file, "w") as output_file_location:
        columns = ['transaction_date', 'amount', 'category', 'description']
        csv_out = csv.writer(output_file_location)

        for expense in expenses:
            csv_out.writerow([
                expense["transaction_date"],
                abs(float(expense["amount"])),
                expense["category"],
                expense["description"],
            ])

    if Path(args.output_file).is_file():
        print("CSV transformed into file: {}".format(args.output_file))
    else:
        print("No output file generated")

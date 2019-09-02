import csv
from argparse import ArgumentParser
from datetime import datetime
from operator import itemgetter

parser = ArgumentParser()
parser.add_argument("-i", "--input", dest="input_file",
    default='/tmp/activity.csv',
    help="CSV input file with transactions (default: %(default)s)")
parser.add_argument("-o", "--output", dest="output_file",
    default='/tmp/activity-processed.csv',
    help="Output location of reformatted CSV (default: %(default)s)")
parser.add_argument("-f", "--format", dest="format",
    default='post_desc_amt_cat',
    help="Format of input transactions CSV")
args = parser.parse_args()

expenses = []


def convert_input(row):
    if (args.format == 'post_desc_amt_cat'):
        if float(row[3]) > 0:
            return {
                "transaction_date": datetime.strptime(row[0], '%m/%d/%Y').strftime('%Y-%m-%d'),
                "description": row[2],
                "amount": row[3],
                "category": row[4],
                }
    elif (args.format == 'long_commas'):
        if float(row[7]) > 0:
            return {
                "transaction_date": datetime.strptime(row[0], '%m/%d/%Y %a').strftime('%Y-%m-%d'),
                "description": row[2],
                "amount": row[7],
                "category": "",
                }
    elif (args.format == 'name_memo_amt'):
        if row[1] == "DEBIT":
            return {
                "transaction_date": datetime.strptime(row[0], '%m/%d/%Y').strftime('%Y-%m-%d'),
                "description": row[2],
                "amount": row[4],
                "category": "",
                }
    elif (args.format == 'business'):
        if float(row[2]) > 0:
            return {
                "transaction_date": datetime.strptime(row[0].strip(), '%m/%d/%Y').strftime('%Y-%m-%d'),
                "description": row[1],
                "amount": row[2],
                "category": "",
                }
    elif (args.format == 'desc_cat_type'):
        if row[4] == "Sale":
            return {
                "transaction_date": datetime.strptime(row[0], '%m/%d/%Y').strftime('%Y-%m-%d'),
                "description": row[2],
                "amount": row[5],
                "category": row[3],
                }
    elif (args.format == 'status_debit_credit'):
        if row[3] and float(row[3]) > 0:
            return {
                "transaction_date": datetime.strptime(row[1], '%m/%d/%Y').strftime('%Y-%m-%d'),
                "description": row[2],
                "amount": row[3],
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
    elif ',,,,,,' in first_row:
        input_format = "long_commas"

    return input_format


try:
    with open(args.input_file) as csv_file:
        csv_reader = csv.reader(csv_file)

        has_header = csv.Sniffer().has_header(csv_file.read(1024))
        csv_file.seek(0)

        if has_header:
            next(csv_reader)

        for row in csv_reader:
            row_extract = convert_input(row)
            if row_extract:
                expenses.append(row_extract)

except FileNotFoundError:
    print("Cannot open transactions file: " + args.input_file)

if expenses:
    expenses.sort(key=itemgetter("transaction_date"))

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

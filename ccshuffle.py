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
    default='basic',
    help="Format of input transactions CSV")
args = parser.parse_args()

expenses = []

def convert_input(row):
    if (args.format == 'basic'):
        if float(row[3]) > 0:
            return {
                "transaction_date": datetime.strptime(row[0], '%m/%d/%Y').strftime('%Y-%m-%d'),
                "description": row[2],
                "amount": row[3],
                "category": row[4],
                }
    elif (args.format == 'memo'):
        if row[1] == "DEBIT":
            return {
                "transaction_date": datetime.strptime(row[0], '%m/%d/%Y').strftime('%Y-%m-%d'),
                "description": row[2],
                "amount": abs(float(row[4])),
                "category": "",
                }

try:
    with open(args.input_file) as csv_file:
        csv_reader = csv.reader(csv_file)

        if (args.format == 'basic') or (args.format == 'memo'):
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
            csv_out.writerow([expense["transaction_date"], expense["amount"], expense["category"], expense["description"]])

import csv
from datetime import datetime
from operator import itemgetter

input_file = '/tmp/activity.csv'
output_file = '/tmp/activity-processed.csv'

with open(input_file) as csv_file:
    csv_reader = csv.reader(csv_file)
    has_header = csv.Sniffer().has_header(csv_file.read(1024))
    csv_file.seek(0)
    expenses = []

    if has_header:
        next(csv_reader)

    for row in csv_reader:
        if float(row[3]) > 0:
            expenses.append({
                "transaction_date": datetime.strptime(row[0], '%m/%d/%Y').strftime('%Y-%m-%d'),
                "description": row[2],
                "amount": row[3],
                "category": row[4],
                })

if expenses:
    expenses.sort(key=itemgetter("transaction_date"))

    with open(output_file, "w") as output_file_location:
        columns = ['transaction_date', 'amount', 'category', 'description']
        csv_out = csv.writer(output_file_location)

        for expense in expenses:
            csv_out.writerow([expense["transaction_date"], expense["amount"], expense["category"], expense["description"]])

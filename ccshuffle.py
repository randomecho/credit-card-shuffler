import csv

with open('/tmp/activity.csv') as csv_file:
    csv_reader = csv.reader(csv_file)
    has_header = csv.Sniffer().has_header(csv_file.read(1024))
    csv_file.seek(0)
    expenses = []

    if has_header:
        next(csv_reader)

    for row in csv_reader:
        expenses.append({
            "transaction_date": row[0],
            "description": row[2],
            "amount": row[3],
            "category": row[4]
            })

print(expenses)

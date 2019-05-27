# Credit Card Activity Shuffler

Parses a credit card activity statement into a slightly
different format of columns being in different places.

## Output format of CSV

    transaction-date, amount, category, description/location

## Usage

    python3 ccshuffle.py -i /path/to/credit-card-activity-download.csv

## Formats

There are several different formats to consider, but basically it depends
on the input column format of the CSV.

- "default" - `Trans. Date,Post Date,Description,Amount,Category`
- "memo" - `"Date","Transaction","Name","Memo","Amount"`

Use a name from the list above when sending in the flags to help the script
know how to expect the columns in the input file. For example:

    python3 ccshuffle.py --format memo

## Requirements

- Python 3
- Credit card activity statement exported into CSV format

## License

Released under [BSD 3-Clause](./LICENSE).

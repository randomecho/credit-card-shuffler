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

- "post_desc_amt_cat" - `Trans. Date,Post Date,Description,Amount,Category`
- "long_commas" - `05/20/2019  Mon,,"BUSINESS",,,,,2.10,,,,,,,,`
- "name_memo_amt" - `"Date","Transaction","Name","Memo","Amount"`
- "desc_cat_type" - `Transaction Date,Post Date,Description,Category,Type,Amount`
- "status_debit_credit" - `Status,Date,Description,Debit,Credit`
- "business" - ` 05/11/2019,BUSINESS,"-1.17"`

Use a name from the list above when sending in the flags to help the script
know how to expect the columns in the input file. For example:

    python3 ccshuffle.py --format memo

## Requirements

- Python 3
- Credit card activity statement exported into CSV format

## License

Released under [BSD 3-Clause](./LICENSE).

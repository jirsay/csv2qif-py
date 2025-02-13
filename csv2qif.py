import csv
import argparse
from datetime import datetime


"""_summary_
    Modified CSV to QIF converter
    This is a simple converter that inputs a CSV file with specific fields:
        D - Date - date of the transaction
        T - Amount - amount value of the transaction (positive: income, negative: expense)
        P - Payee - if income, who paid; else, who is paid
        M - Memo - free-form information on the transaction

    MoneyDance has other fields:
        C - if the transaction is Uncleared (blank), Cleared, or Reconciling
        N - the external check or transaction number
        L - the Category; if there are Tags, they follow a "/"
        
    The modifications will let me include the other MoneyDance fields
    """

def print_row(rowNr, date, amount, payee, memo):
    print(
        f"{str(rowNr):<3} | "
        f"{str(date):<8} | "
        f"{str(amount):>10} | "
        f"{payee:<15} | "
        f"{memo:<20}"
    )


def csv2qif(input_file='input.csv', output_file='output.qif'):
    qif_data = ["!Type:Bank"]

    with open(input_file, 'r') as csv_file:
        rows = list(csv.reader(csv_file, delimiter=';'))
        print(f"Number of data rows in the csv file: {len(rows) - 1}")
        rowNr = 1
        print("")
        print_row("Row", "Date", "Amount", "Payee", "Memo")
        print("-"*80)
        for row in rows[1:]:
            print_row(rowNr, row[0], row[1], row[2], row[3])
            rowNr += 1
            date = datetime.strptime(row[0], "%d/%m/%y")
            qif_data.extend([
                f"D{date.strftime('%d/%m/%y')}",
                f"M{row[3]}",
                f"T{row[1]}",
                f"P{row[2]}",
                "^"
            ])

    with open(output_file, 'w') as qif_file:
        qif_file.write('\n'.join(qif_data))
    print("\nQIF file created successfully")


parser = argparse.ArgumentParser()
parser.add_argument('files', nargs='*', default=['input.csv', 'output.qif'])
args = parser.parse_args()

if len(args.files) == 1:
    csv2qif(input_file=args.files[0])
else:
    csv2qif(*args.files)

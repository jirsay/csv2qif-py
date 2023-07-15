import csv
import argparse
from datetime import datetime


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

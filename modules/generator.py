import os
import csv
import datetime

MONTH_LETTER_MAP = {
    1: 'A', 2: 'B', 3: 'C', 4: 'D',
    5: 'E', 6: 'F', 7: 'G', 8: 'H',
    9: 'I', 10: 'J', 11: 'K', 12: 'L'
}


def generate_pack_serial(csv_filename, capacity_code):
    now = datetime.datetime.now()
    year = str(now.year)[-2:]
    month_letter = MONTH_LETTER_MAP.get(now.month, 'X')
    prefix = f"{year}{month_letter}{capacity_code}"

    sequence = 1

    if os.path.exists(csv_filename):
        with open(csv_filename, mode='r', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if row.get("PackSerial", "").startswith(prefix):
                    sequence += 1

    return f"{prefix}{sequence:03d}"

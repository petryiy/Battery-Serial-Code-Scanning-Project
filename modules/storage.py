import os
import csv
import datetime


def create_data_record(pack_serial, bms_serial, cell_serials_list):
    record = {
        "PackSerial": pack_serial,
        "BMSSerial": bms_serial,
        "CellSerials": ",".join(cell_serials_list),
        "Timestamp": datetime.datetime.now().isoformat()
    }
    return record


def save_record_to_csv(record, filename):
    file_exists = os.path.exists(filename)
    with open(filename, mode='a', newline='') as csvfile:
        fieldnames = ["PackSerial", "BMSSerial", "CellSerials", "Timestamp"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()
        writer.writerow(record)
    print(f"data saved to CSV: {filename}")

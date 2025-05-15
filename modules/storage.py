import os
import csv


# function to save the record data to csv files given record and filename
def save_record_to_csv(record, filename):
    file_exists = os.path.exists(filename)
    with open(filename, mode='a', newline='') as csvfile:
        fieldnames = ["pack_serial", "bms_serial", "timestamp"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()
        writer.writerow({
            "pack_serial": record["pack_serial"],
            "bms_serial": record["bms_serial"],
            "timestamp": record["timestamp"]
        })
    print(f"Data saved to CSV: {filename}")

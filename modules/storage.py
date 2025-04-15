import os
import csv


# function to save the record data to csv files given record and filename
def save_record_to_csv(record, filename):
    file_exists = os.path.exists(filename)
    with open(filename, mode='a', newline='') as csvfile:
        fieldnames = ["PackSerial", "BMSSerial", "Timestamp"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()
        writer.writerow({
            "PackSerial": record["PackSerial"],
            "BMSSerial": record["BMSSerial"],
            "Timestamp": record["Timestamp"]
        })
    print(f"data saved to CSV: {filename}")

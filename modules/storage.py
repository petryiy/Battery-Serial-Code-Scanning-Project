import os
import csv


# function to save the record data to csv files given record and filename
def save_record_to_csv(record, filename):
    os.makedirs(os.path.dirname(filename), exist_ok=True)

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
    print(f"Data saved to CSV: {filename}")

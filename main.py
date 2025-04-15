import os
import csv

from modules.generator import generate_pack_serial
from modules.passport import create_digital_certificate, create_data_record
from modules.storage import save_record_to_csv

CSV_FILENAME = "data/battery_pack_data.csv"


def get_manual_input(prompt_message):
    return input(prompt_message).strip()


def main():
    print("=== Battery Pack Project ===")

    # read csv information from given path
    cell_csv_path = get_manual_input("Enter the path of the csv containing 16 cell serials: ")
    if not os.path.exists(cell_csv_path):
        print("Can't find the file")
        return

    cell_serials = []

    # include the required information
    with open(cell_csv_path, mode='r', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            serial = row.get("original_qr_content", "")
            date = row.get("production_date", "")
            city = row.get("production_city", "")
            if serial:
                cell_serials.append({
                    "serial": serial,
                    "production_date": date,
                    "production_city": city
                })

    if not cell_serials:
        print("Can't read any cell serial ")
        return

    # assume capacity_code is 14 in this case
    capacity_code = "14"
    pack_serial = generate_pack_serial(CSV_FILENAME, capacity_code)
    print(f"The generated Pack Serial is: {pack_serial}")

    # read the input BMS serial
    bms_serial = ''
    while not bms_serial:
        bms_serial = get_manual_input("Please enter the BMS Serial: ")

    # create the record
    record = create_data_record(pack_serial, bms_serial, cell_serials)
    save_record_to_csv(record, CSV_FILENAME)

    # generate the certificate
    certificate_identifier = create_digital_certificate(record)
    print(f"(simulation) sending '{certificate_identifier}' to IoT")


if __name__ == "__main__":
    main()

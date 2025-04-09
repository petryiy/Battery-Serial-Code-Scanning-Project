import os
import csv

from modules.generator import generate_pack_serial
from modules.passport import create_digital_certificate
from modules.storage import create_data_record, save_record_to_csv

CSV_FILENAME = "data/battery_pack_data.csv"


def get_manual_input(prompt_message):
    return input(prompt_message).strip()


def main():
    print("=== Battery Pack Project ===")

    cell_csv_path = get_manual_input("Enter the path of the csv containing 16 cell serials: ")
    if not os.path.exists(cell_csv_path):
        print("can't find the file")
        return

    cell_serials = []
    capacity_wh_list = []

    with open(cell_csv_path, mode='r', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            serial = row.get("original_qr_content")
            if serial:
                cell_serials.append(serial)
            try:
                capacity_wh = float(row.get("energy_wh", 0))
                capacity_wh_list.append(capacity_wh)
            except ValueError:
                continue

    if not cell_serials:
        print("can't read any cell serial ")
        return

    total_energy = sum(capacity_wh_list)
    capacity_code = "14" if total_energy >= 14000 else "05"
    print(f"the estimated capacity is approximately {total_energy:.0f} Wh, the capacity code is: {capacity_code}")

    pack_serial = generate_pack_serial(CSV_FILENAME, capacity_code)
    print(f"the generated Pack Serial is: {pack_serial}")

    bms_serial = ''
    while not bms_serial:
        bms_serial = get_manual_input("Please enter the BMS Serial: ")

    record = create_data_record(pack_serial, bms_serial, cell_serials)
    save_record_to_csv(record, CSV_FILENAME)

    certificate_identifier = create_digital_certificate(record)
    print(f"(simulation) sending '{certificate_identifier}' to IoT")


if __name__ == "__main__":
    main()

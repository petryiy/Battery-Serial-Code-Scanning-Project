import os
import csv
import streamlit as st

from modules.generator import generate_pack_serial
from modules.passport import create_digital_certificate, create_data_record
from modules.storage import save_record_to_csv

CSV_FILENAME = "data/battery_pack_data.csv"


st.set_page_config(page_title="Battery Passport Generator", layout="centered")


def main():
    st.title("🔋 Battery Passport Generator")
    st.write("Upload a CSV file containing **16 cell serials** to generate a battery passport.")

    uploaded_file = st.file_uploader("Upload your CSV file here", type=["csv"])

    bms_serial = st.text_input("Enter BMS Serial")

    if uploaded_file and bms_serial:
        cell_serials = []
        reader = csv.DictReader(uploaded_file.read().decode("utf-8").splitlines())
        for row in reader:
            serial = row.get("original_qr_content", "")
            date = row.get("production_date", "")
            city = row.get("production_city", "")
            manufacturers = row.get("manufacturers", "")
            model_codes = row.get("model_codes", "")
            if serial:
                cell_serials.append({
                    "serial": serial,
                    "production_date": date,
                    "production_city": city,
                    "manufacturers": manufacturers,
                    "model_codes": model_codes
                })

        if not cell_serials:
            st.error("❌ No valid cell serials found in the CSV file.")
            return

        capacity_code = "14"  # now fixed as per CEO
        pack_serial = generate_pack_serial(CSV_FILENAME, capacity_code)

        record = create_data_record(pack_serial, bms_serial, cell_serials)
        save_record_to_csv(record, CSV_FILENAME)

        cert_identifier, pdf_path = create_digital_certificate(record)

        st.success("🎉 Battery passport generated successfully!")
        with open(pdf_path, "rb") as f:
            st.download_button("📄 Download Battery Passport (PDF)", f, file_name=os.path.basename(pdf_path))

        st.caption(f"Simulated: Sent to IoT Device with ID `{cert_identifier}`")

    elif uploaded_file and not bms_serial:
        st.warning("⚠️ Please enter the BMS Serial to continue.")


if __name__ == "__main__":
    main()

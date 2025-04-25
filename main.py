import os
import csv
import streamlit as st

from modules.generator import generate_pack_serial
from modules.passport import create_digital_certificate, create_data_record
from modules.storage import save_record_to_csv

CSV_FILENAME = "data/battery_pack_data.csv"


st.set_page_config(page_title="Battery Passport Generator", layout="centered")


def main():
    if "submitted" not in st.session_state:
        st.session_state.submitted = False
    if "pack_serial" not in st.session_state:
        st.session_state.pack_serial = None
    if "record" not in st.session_state:
        st.session_state.record = None
    if "pdf_path" not in st.session_state:
        st.session_state.pdf_path = None

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

        if st.button("Generate Battery Passport") and not st.session_state.submitted:
            # generate pack serial
            capacity_code = "14"
            pack_serial = generate_pack_serial(CSV_FILENAME, capacity_code)
            st.session_state.pack_serial = pack_serial
            # save record
            record = create_data_record(pack_serial, bms_serial, cell_serials)
            save_record_to_csv(record, CSV_FILENAME)
            # generate certificate
            cert_identifier, pdf_path = create_digital_certificate(record)

            # save state
            st.session_state.record = record
            st.session_state.pdf_path = pdf_path
            st.session_state.submitted = True

            st.success(f"🎉 Battery passport for pack {pack_serial} generated successfully!")

        if st.session_state.submitted and st.session_state.pdf_path:
            with open(st.session_state.pdf_path, "rb") as f:
                st.download_button(
                    label="📄 Download PDF Passport",
                    data=f.read(),
                    file_name=os.path.basename(st.session_state.pdf_path),
                    mime="application/pdf"
                )

    elif uploaded_file and not bms_serial:
        st.warning("⚠️ Please enter the BMS Serial to continue.")

    # admin window
    st.markdown("---")
    st.header("🔒 Admin Access")

    if "admin_authenticated" not in st.session_state:
        st.session_state.admin_authenticated = False

    # enter password
    admin_password = st.text_input("Enter admin password", type="password")

    # password authorize
    if st.button("Login as Admin"):
        if admin_password == "vaulta_is_best":
            st.session_state.admin_authenticated = True
            st.success("Admin access granted.")
        else:
            st.error("Incorrect password.")

    # download csv
    if st.session_state.admin_authenticated:
        st.subheader("📥 Download all battery passport records")
        if os.path.exists(CSV_FILENAME):
            with open(CSV_FILENAME, "rb") as f:
                st.download_button(
                    label="⬇️ Download CSV File",
                    data=f,
                    file_name=os.path.basename(CSV_FILENAME),
                    mime="text/csv"
                )
        else:
            st.warning("No CSV record file found.")


if __name__ == "__main__":
    main()

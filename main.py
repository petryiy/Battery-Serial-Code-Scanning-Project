import csv
from flask import Flask, request, render_template, send_file
import os
from modules.generator import generate_pack_serial
from modules.passport import create_digital_certificate, create_data_record
from modules.storage import save_record_to_csv, init_db

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
CSV_FILENAME = 'data/battery_pack_data.csv'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs('certificates', exist_ok=True)
os.makedirs('data', exist_ok=True)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        file = request.files["file"]
        bms_serial = request.form.get("bms_serial")

        if file and bms_serial:
            filepath = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(filepath)

            with open(filepath, mode='r', newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                cell_serials = []
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
                return render_template("index.html", download_link=None, error="Invalid CSV content")

            capacity_code = "14"
            pack_serial = generate_pack_serial(bms_serial, capacity_code)

            record = create_data_record(pack_serial, bms_serial, cell_serials)

            save_record_to_csv(record, CSV_FILENAME)
            cert_id, pdf_path = create_digital_certificate(record)

            return render_template("index.html", download_link=pdf_path)

    return render_template("index.html", download_link=None)


@app.route("/download/<path:filename>")
def download_file(filename):
    return send_file(filename, as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True)

import os
import json
import datetime
import qrcode
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter


def create_pdf_certificate(record, pdf_filename):
    qr = qrcode.QRCode(box_size=4, border=2)
    qr.add_data(record["PackSerial"])
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color="black", back_color="white")
    temp_qr_filename = "temp_qr.png"
    qr_img.save(temp_qr_filename)

    c = canvas.Canvas(pdf_filename, pagesize=letter)
    width, height = letter
    c.setFont("Helvetica-Bold", 16)
    c.drawString(72, height - 72, "Battery Passport")
    c.setFont("Helvetica", 12)
    c.drawString(72, height - 100, f"Pack Serial: {record['PackSerial']}")
    c.drawString(72, height - 120, f"BMS Serial: {record['BMSSerial']}")
    c.drawString(72, height - 140, "Cell Serials:")
    y_position = height - 160
    cell_serials = record["CellSerials"].split(',')
    for serial in cell_serials:
        c.drawString(92, y_position, serial)
        y_position -= 15
    c.drawString(72, y_position - 10, f"Timestamp: {record['Timestamp']}")
    c.drawImage(temp_qr_filename, 72, y_position - 120, width=100, height=100)
    c.drawString(72, y_position - 140, "Scan for Pack Serial details.")
    c.save()

    if os.path.exists(temp_qr_filename):
        os.remove(temp_qr_filename)

    print(f"PDF created successfully: {pdf_filename}")


def create_digital_certificate(record):
    cert_identifier = "CERT_" + record["PackSerial"]
    json_filename = f"certificates/battery_passport_{record['PackSerial']}.json"
    with open(json_filename, 'w') as json_file:
        json.dump(record, json_file, indent=4)
    print(f"JSON certificate created: {json_filename}")

    pdf_filename = f"certificates/battery_passport_{record['PackSerial']}.pdf"
    create_pdf_certificate(record, pdf_filename)
    return cert_identifier

from flask import Flask, send_file, jsonify, make_response, current_app, session, request
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from api.v1.views import app_views
from models import storage
from models.user import User
from models.business import Business
from models.permit import Permit
from models.category import Category
from datetime import datetime, timedelta
from num2words import num2words
import os
from flask_mail import Message
from dotenv import load_dotenv
from os import getenv
import qrcode

load_dotenv()


@app_views.route('/generatepermit/<business_id>', methods=['GET'], strict_slashes=False)
def generate_pdf(business_id):
    # Create a PDF file
    business = storage.get_obj_by_id(Business, business_id)
    owner = storage.get_obj_by_id(User, business.owner)
    category = storage.get_obj_by_id(Category, business.category)
    permit = storage.get_permit_by_business_id(business.id)

    if business.verified is True:
        pdf_filename = f"/tmp/permits/{business_id}.pdf"
        qrcode_path = generate_qr_code(business_id, permit.permit_number,
                                       (datetime.now() + timedelta(days=365)).strftime("%d-%b-%Y"))
        width, height = A4

        c = canvas.Canvas(pdf_filename, pagesize=A4)

        image_path = "/home/ubuntu/ePermit-KLF/web_flask/static/images/klf.jpeg"

        # Logo
        c.drawImage(image_path, 100, -50, width=50, height=50)
        c.drawImage(qrcode_path, 410, -900, width=100, height=100)

        # Header and title
        c.setFont("Helvetica-Bold", 14)
        c.drawString(200, height - 50, "SINGLE BUSINESS PERMIT")
        c.setFont("Helvetica", 12)
        c.drawString(700, height - 50, str(datetime.now().year))
        c.drawString(400, height - 50, permit.permit_number)

        # Permit Information
        c.setFont("Helvetica-Bold", 10)
        c.drawString(30, height - 80, "COUNTY GOVERNMENT OF KILIFI")
        c.drawString(30, height - 100, business.sub_county)
        c.drawString(30, height - 120, "GRANTS THIS")
        c.drawString(30, height - 140, "SINGLE BUSINESS PERMIT")
        c.drawString(30, height - 160, "TO")

        # Business Details Table
        data = [
            ["Business ID No", business.id],
            ["Business Name", business.business_name],
            ["Certificate of Registration No/ID No", business.Certificate_of_Registration_No],
            ["Pin No.", business.KRA_pin],
            ["VAT No.", business.vat_no]
        ]

        table = Table(data, colWidths=[200, 300])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))

        table.wrapOn(c, width, height)
        table.drawOn(c, 30, height - 300)

        # Business Activity
        c.setFont("Helvetica", 10)
        c.drawString(30, height - 330, "To engage in the activity/business/profession or occupation of:")
        c.drawString(30, height - 350, "Business Activity Code & Description:")
        c.drawString(250, height - 350, category.category_name)
        c.drawString(30, height - 370, "Detailed Activity Description")
        c.drawString(250, height - 370, business.detailed_description)

        # Fee
        c.drawString(30, height - 410, "Having paid a single Business Permit Fee of:")
        c.drawString(250, height - 410, "Kshs")
        c.drawString(300, height - 410, str(category.fee))
        c.drawString(30, height - 430, f"Kshs (In Words): {num2words(category.fee)} Only")

        # Address Details Table
        address_data = [
            ["P.O BOX No:", business.po_box],
            ["Telephone No:", business.business_telephone],
            ["Telephone No.2:", business.business_telephone_two],
            ["Physical Adress:", business.physical_address],
            ["Plot No:", business.plot_no],
            ["Ward:", business.ward]
        ]

        address_table = Table(address_data, colWidths=[200, 300])
        address_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))

        address_table.wrapOn(c, width, height)
        address_table.drawOn(c, 30, height - 600)

        # Date and Validity
        c.drawString(30, height - 630, "Date of Issue")
        c.drawString(150, height - 630, str(permit.created_at))
        c.drawString(30, height - 650, "Validity Period")
        c.drawString(150, height - 650, (datetime.now() + timedelta(days=365)).strftime("%d-%b-%Y"))

        # Officer Information
        c.drawString(30, height - 690, "This is a system generated Permit")
        c.drawString(250, height - 690, "ePermit")
        c.drawString(30, height - 710, "ePermit System Manage")
        c.drawString(30, height - 730, f"COUNTY GOVERNMENT OF KILIFI - {business.sub_county}")

        # Notice
        c.drawString(30, height - 770, "NOTICE: Please note that issuance of this license/permit does not exempt the holder from compliance with other COUNTY")
        c.drawString(30, height - 790, "GOVERNMENT OF KILIFI Legislations and any other written Law.")

        # Signature Line
        c.drawString(400, height - 790, "Signature and Stamp")
        c.line(400, height - 795, 500, height - 795)

        # Signature Placeholder
        c.drawString(30, height - 830, "No. 36005")
        c.drawString(400, height - 830, "Epermit System")
        c.drawString(400, height - 850, "Sub-County Revenue Officer")
        c.drawString(400, height - 870, "for Chief Officer Finance & Economic Planning")

        c.save()
        recipient_email = owner.email
        subject = "Your Business Permit"
        body = "Please find attached your business permit."

        msg = Message(subject,
                  sender=getenv('MAIL_USERNAME'),
                  recipients=[recipient_email])
        msg.body = body
        with open(pdf_filename, 'rb') as fp:
            msg.attach(pdf_filename, "application/pdf", fp.read())
        current_app.extensions['mail'].send(msg)
        return jsonify({"status": "Email sent"}), 200
    else:
        return jsonify({"error": "Business is not verified"}), 400


@app_views.route('/download_permit/<business_id>', methods=['GET'],
                 strict_slashes=False)
def downlaod_pdf(business_id):
    """ Returns pdf file permit """
    pdf_filename = f"{business_id}.pdf"
    if os.path.exists(pdf_filename):
        return send_file(pdf_filename, as_attachment=True)
    else:
        return jsonify({"error": "File not found"}), 404




def generate_qr_code(business_id, permit_number, expiry_date):
    data = f"Business ID: {business_id}\nPermit Number: {permit_number}\nExpiry Date: {expiry_date}"
    # Create QR code instance
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )

    # Add data to QR code
    qr.add_data(data)
    qr.make(fit=True)

    # Create an image from the QR code
    img = qr.make_image(fill_color="black", back_color="white")

    file_path = '/tmp/qrcode/'
    # Save the image to a file
    img.save(file_path)
    return file_path
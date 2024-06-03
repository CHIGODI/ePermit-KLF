#!/usr/bin/env python3
import os
import qrcode
from datetime import datetime, timedelta
from io import BytesIO

from flask import abort, current_app, jsonify, send_file
from flask_mail import Message
from num2words import num2words
from PIL import Image
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas
from reportlab.platypus import Table, TableStyle

from api.v1.views import app_views
from models import storage
from models.business import Business
from models.category import Category
from models.user import User
from dotenv import load_dotenv
from os import getenv

load_dotenv()


def generate_qr_code(business_id, permit_number, expiry_date):
    """Generates QR code encoded with permit details """
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

    # Save the image to a bytes buffer
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)
    return buffer



@app_views.route('/generatepermit/<business_id>', methods=['GET'], strict_slashes=False)
def generate_pdf(business_id):
    business = storage.get_obj_by_id(Business, business_id)
    if not business:
        abort(404)

    owner = storage.get_obj_by_id(User, business.owner)
    category = storage.get_obj_by_id(Category, business.category)
    permit = storage.get_permit_by_business_id(business.id)

    if not permit or not permit.check_validity():
        return jsonify({"error": "Expired permit or not found"}), 400

    # Create an in-memory bytes buffer
    pdf_buffer = BytesIO()

    # image_path = "/home/ubuntu/ePermit-KLF/web_flask/static/images/klf.jpeg"
    image_path = "/home/chigow/ePermit-KLF/web_flask/static/images/klf.jpeg"
    qrcode_buffer = generate_qr_code(business_id, permit.permit_number,
                                    (datetime.now() + timedelta(days=365)).strftime("%d-%b-%Y"))
    width, height = A4

    # Define the gradient colors to colour the canvas
    start_color = (255 / 255, 255 / 255, 254 / 255)
    end_color = (255 / 255, 255 / 255, 253 / 255)


    # initialising an empty canvas (empty white page with name)
    c = canvas.Canvas(pdf_buffer, pagesize=A4)

    # Draw a rectangle with gradient fill covering the entire canvas
    c.setFillColorRGB(*start_color)
    c.rect(0, 0, width, height, fill=True)
    c.setFillColorRGB(*end_color)
    c.rect(0, 0, width, height, fill=True)


    # Check if the image path is correct and the image exists
    if not os.path.exists(image_path):
        abort(404, description=f"Image not found at {image_path}")


    # return fill colour to black
    c.setFillColorRGB(0, 0, 0)

    # Load the image
    image = Image.open(image_path)

    # Convert the image to grayscale
    image_bw = image.convert("L")

    # Save the grayscale image to a BytesIO buffer
    buffer_logo = BytesIO()
    image_bw.save(buffer_logo, format="PNG")
    buffer_logo.seek(0)

    #LOGO kilifi court of arms
    c.drawImage(image_path,  80, height - 80, width=60, height=60)
    c.drawImage(ImageReader(buffer_logo), 90, height - 160, width=30, height=30)

    # QR Code
    c.setFont("Helvetica-Bold", 5)
    c.drawString(460, height - 198, "Scan QR CODE to verify")
    c.drawImage(ImageReader(qrcode_buffer), 450, height - 190, width=100, height=100)

    # Header and title
    c.setFont("Helvetica-Bold", 16)
    c.drawString(150, height - 50, "SINGLE BUSINESS PERMIT")
    c.setFont("Helvetica", 12)
    c.drawString(535, height - 60, str(datetime.now().year))
    c.setFont("Helvetica-Bold", 9)
    c.drawString(440, height - 80, f'Permit No: {permit.permit_number}')

    # Permit Information
    c.setFont("Helvetica-Bold", 12)
    c.drawString(190, height - 90, "COUNTY GOVERNMENT OF KILIFI")
    c.drawString(200, height - 110, f'{business.sub_county.upper()} SUBCOUNTY')
    c.drawString(235, height - 130, "GRANTS THIS")
    c.drawString(210, height - 150, "SINGLE BUSINESS PERMIT")
    c.drawString(270, height - 170, "TO")

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
    c.setFont("Helvetica-Bold", 10)
    c.drawString(100, height - 330, "To engage in the activity/business/profession or occupation of:")
    c.setFont("Helvetica", 10)
    c.drawString(30, height - 350, "Business Activity Code & Description:")
    c.setFont("Helvetica-Bold", 10)
    c.drawString(30, height - 370, f'{category.activity_code}; {category.category_name}')
    c.setFont("Helvetica", 10)
    c.drawString(250, height - 350, "Detailed Activity Description")
    c.setFont("Helvetica-Bold", 10)
    c.drawString(250, height - 350, business.detailed_description)

    # Fee
    c.setFont("Helvetica-Bold", 10)
    c.drawString(180, height - 410, "Having paid a single Business Permit Fee of:")
    c.drawString(250, height - 430, f"Kshs {str(category.fee)}")
    c.drawString(30, height - 450, f"Kshs (In Words): {num2words(category.fee).capitalize()} Only")

    # Address Details Table
    c.setFont("Helvetica", 10)
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
    c.drawString(30, height - 650, "Validity Period")
    c.drawString(270, height - 650, "Date of Issue")
    c.drawString(270, height - 670, str(permit.created_at))
    c.drawString(450, height - 650, "Date of Expiry")
    c.drawString(450, height - 670, (datetime.now() + timedelta(days=365)).strftime("%d-%b-%Y"))

    # Officer Information
    c.setFont("Helvetica-Bold", 10)
    c.drawString(30, height - 690, "This is a system generated Permit")
    c.drawString(95, height - 710, "ePermit")
    c.drawString(30, height - 750, f"COUNTY GOVERNMENT OF KILIFI - {business.sub_county}")

    # Notice
    c.setFont("Helvetica", 10)
    c.drawString(30, height - 770,
                 "NOTICE: Please note that issuance of this license/permit does not exempt the holder from compliance with other COUNTY")
    c.drawString(30, height - 790,
                 "GOVERNMENT OF KILIFI Legislations and any other written Law.")

    # Signature Placeholder
    c.setFont("Helvetica-Bold", 10)
    c.setFillColorRGB(1, 0, 0)
    c.drawString(30, height - 810, "No. 36005")
    c.setFillColorRGB(0, 0, 0)
    c.setFont("Helvetica", 10)
    c.drawString(400, height - 850, "Sub-County Revenue Officer")
    c.drawString(400, height - 870, "for Chief Officer Finance & Economic Planning")

    c.save()
    recipient_email = owner.email
    subject = "Your Business Permit"
    body = "Please find attached your business permit."

    # send email to client with attachement permit
    msg = Message(subject,
                sender=getenv('MAIL_USERNAME'),
                recipients=[recipient_email])
    msg.body = body

    # Attach PDF from in-memory buffer
    pdf_buffer.seek(0)
    msg.attach(f"{business_id}.pdf", "application/pdf", pdf_buffer.read())
    current_app.extensions['mail'].send(msg)

    # Return the PDF as a downloadable file
    pdf_buffer.seek(0)
    return send_file(pdf_buffer, as_attachment=True,
                     download_name=f"{business_id}.pdf",
                     mimetype='application/pdf')
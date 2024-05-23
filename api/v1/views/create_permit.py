from flask import Flask, send_file
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from api.v1.views import app_views
from models import storage
from models.user import User
from models.business import Business
from models.permit import Permit
from datetime import datetime, timedelta

@app_views.route('/permits/<busines_id>')
def generate_pdf(business_id):
    # Create a PDF file
    business = storage.get_obj_by_id(Business, business_id)

    if business.verified is True:
        pdf_filename = f"{business.name}_permit.pdf"
        doc = SimpleDocTemplate(pdf_filename, pagesize=A4)
        elements = []
        width, height = A4

        # Header and title
        c = canvas.Canvas(pdf_filename, pagesize=A4)
        c.setFont("Helvetica-Bold", 14)
        c.drawString(200, height - 50, "SINGLE BUSINESS PERMIT")
        c.setFont("Helvetica", 12)
        c.drawString(500, height - 50, str(datetime.now().year))

        # Permit Information
        c.setFont("Helvetica-Bold", 10)
        c.drawString(30, height - 80, "COUNTY GOVERNMENT OF KILIFI")
        c.drawString(30, height - 100, business.sub_county)
        c.drawString(30, height - 120, "GRANTS THIS")
        c.drawString(30, height - 140, "SINGLE BUSINESS PERMIT")
        c.drawString(30, height - 160, "TO")

        # Business Details Table
        data = [
            ["Business ID No", "666798"],
            ["Business Name", business.name],
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
        c.drawString(250, height - 350, business.activity_code_description)
        c.drawString(30, height - 370, "Detailed Activity Description")
        c.drawString(250, height - 370, business.activity_description)

        # Fee
        c.drawString(30, height - 410, "Having paid a single Business Permit Fee of:")
        c.drawString(250, height - 410, "Kshs")
        c.drawString(300, height - 410, "5,000.00")
        c.drawString(30, height - 430, "Kshs (In Words): Five Thousand Only")

        # Address Details Table
        address_data = [
            ["P.O BOX No:", "N/A"],
            ["Telephone No:", "0708051357"],
            ["Telephone No.2:", "N/A"],
            ["Business Location:", "MAZERAS-RAILWAYS"],
            ["Plot No:", "Rabai"],
            ["Building:", "Rabai/Kisurutini"]
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
        c.drawString(150, height - 630, permit.created_at)
        c.drawString(30, height - 650, "Validity Period")
        c.drawString(150, height - 650, (datetime.now() + timedelta(days=365)).strftime("%d-%b-%Y"))

        # Officer Information
        c.drawString(30, height - 690, "Name of the Officer issuing this Permit")
        c.drawString(250, height - 690, user.name)
        c.drawString(30, height - 710, "Revenue Licensing Officer")
        c.drawString(30, height - 730, "COUNTY GOVERNMENT OF KILIFI - RABAI SUB COUNTY")

        # Notice
        c.drawString(30, height - 770, "NOTICE: Please note that issuance of this license/permit does not exempt the holder from compliance with other COUNTY")
        c.drawString(30, height - 790, "GOVERNMENT OF KILIFI Legislations and any other written Law.")

        # Signature Line
        c.drawString(400, height - 790, "Signature and Stamp")
        c.line(400, height - 795, 500, height - 795)

        # Signature Placeholder
        c.drawString(30, height - 830, "No. 36005")
        c.drawString(400, height - 830, "FS. KILIFI KIMERA")
        c.drawString(400, height - 850, "Sub-County Revenue Officer")
        c.drawString(400, height - 870, "for Chief Officer Finance & Economic Planning")

        c.save()

        return send_file(pdf_filename, as_attachment=True)
    else:
        return jsonify({''})

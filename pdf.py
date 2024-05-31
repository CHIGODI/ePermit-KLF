#!/usr/bin/env python3
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from datetime import datetime, timedelta
from num2words import num2words

def generate_test_pdf():
    business = {
        'id': '12345',
        'business_name': 'Test Business',
        'Certificate_of_Registration_No': 'CERT123',
        'KRA_pin': 'PIN123',
        'vat_no': 'VAT123',
        'sub_county': 'Kilifi North',
        'verified': True,
        'po_box': '123-456',
        'business_telephone': '0123456789',
        'business_telephone_two': '0987654321',
        'physical_address': '123 Business St.',
        'plot_no': 'PLOT123',
        'ward': 'Ward 1',
        'detailed_description': 'A detailed description of the business activity.'
    }

    category = {
        'category_name': 'Retail Trade',
        'fee': 6500.0
    }

    permit = {
        'created_at': datetime.now().strftime("%d-%b-%Y")
    }

    pdf_filename = f"{business['business_name']}_permit.pdf"
    doc = SimpleDocTemplate(pdf_filename, pagesize=A4)
    elements = []
    width, height = A4

    # Styles
    styles = getSampleStyleSheet()
    styleN = styles['Normal']
    styleH = styles['Heading1']

    # Header and title
    elements.append(Paragraph("SINGLE BUSINESS PERMIT", styleH))
    elements.append(Paragraph(str(datetime.now().year), styleN))
    elements.append(Spacer(1, 12))

    # Permit Information
    elements.append(Paragraph("COUNTY GOVERNMENT OF KILIFI", styleN))
    elements.append(Paragraph(business['sub_county'], styleN))
    elements.append(Paragraph("GRANTS THIS", styleN))
    elements.append(Paragraph("SINGLE BUSINESS PERMIT", styleN))
    elements.append(Paragraph("TO", styleN))
    elements.append(Spacer(1, 12))

    # Business Details Table
    data = [
        ["Business ID No", business['id']],
        ["Business Name", business['business_name']],
        ["Certificate of Registration No/ID No", business['Certificate_of_Registration_No']],
        ["Pin No.", business['KRA_pin']],
        ["VAT No.", business['vat_no']]
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
    elements.append(table)
    elements.append(Spacer(1, 12))

    # Business Activity
    elements.append(Paragraph("To engage in the activity/business/profession or occupation of:", styleN))
    elements.append(Paragraph("Business Activity Code & Description:", styleN))
    elements.append(Paragraph(category['category_name'], styleN))
    elements.append(Paragraph("Detailed Activity Description", styleN))
    elements.append(Paragraph(business['detailed_description'], styleN))
    elements.append(Spacer(1, 12))

    # Fee
    elements.append(Paragraph("Having paid a single Business Permit Fee of:", styleN))
    elements.append(Paragraph("Kshs", styleN))
    elements.append(Paragraph(str(category['fee']), styleN))
    elements.append(Paragraph(f"Kshs (In Words): {num2words(category['fee'])} Only", styleN))
    elements.append(Spacer(1, 12))

    # Address Details Table
    address_data = [
        ["P.O BOX No:", business['po_box']],
        ["Telephone No:", business['business_telephone']],
        ["Telephone No.2:", business['business_telephone_two']],
        ["Physical Address:", business['physical_address']],
        ["Plot No:", business['plot_no']],
        ["Ward:", business['ward']]
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
    elements.append(address_table)
    elements.append(Spacer(1, 12))

    # Date and Validity
    elements.append(Paragraph("Date of Issue", styleN))
    elements.append(Paragraph(permit['created_at'], styleN))
    elements.append(Paragraph("Validity Period", styleN))
    elements.append(Paragraph((datetime.now() + timedelta(days=365)).strftime("%d-%b-%Y"), styleN))
    elements.append(Spacer(1, 12))

    # Officer Information
    elements.append(Paragraph("This is a system generated Permit", styleN))
    elements.append(Paragraph("ePermit", styleN))
    elements.append(Paragraph("ePermit System Manager", styleN))
    elements.append(Paragraph(f"COUNTY GOVERNMENT OF KILIFI - {business['sub_county']}", styleN))
    elements.append(Spacer(1, 12))

    # Notice
    elements.append(Paragraph("NOTICE: Please note that issuance of this license/permit does not exempt the holder from compliance with other COUNTY", styleN))
    elements.append(Paragraph("GOVERNMENT OF KILIFI Legislations and any other written Law.", styleN))
    elements.append(Spacer(1, 12))

    # Signature Line
    elements.append(Paragraph("Signature and Stamp", styleN))
    elements.append(Spacer(1, 24))

    # Signature Placeholder
    elements.append(Paragraph("No. 36005", styleN))
    elements.append(Paragraph("Epermit System", styleN))
    elements.append(Paragraph("Sub-County Revenue Officer", styleN))
    elements.append(Paragraph("for Chief Officer Finance & Economic Planning", styleN))

    # Build the document
    doc.build(elements)

    print(f"PDF generated: {pdf_filename}")

if __name__ == "__main__":
    generate_test_pdf()

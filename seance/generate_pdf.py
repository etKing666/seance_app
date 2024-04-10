from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4


def generate_pdf(recommendations, diagram_path):
    # Create a PDF with ReportLab
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="your_recommendations.pdf"'

    p = canvas.Canvas(response, pagesize=A4)
    p.drawString(100, 750, "Recommendations Report")

    # Example of adding text dynamically
    y_position = 730
    for recommendation in recommendations:
        p.drawString(100, y_position, recommendation)
        y_position -= 20

    # Example of adding an image (diagram)
    p.drawImage(diagram_path, 100, 500, width=400, height=200)  # Adjust dimensions as needed

    p.showPage()
    p.save()
    return response
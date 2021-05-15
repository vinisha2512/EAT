from reportlab.lib.pagesizes import letter, A4
from reportlab.pdfgen import canvas
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics


def hello(contact, mail, name, pname, price, seller, customer, id1):
    pdfmetrics.registerFont(TTFont('DejaVu', 'DejaVuSans.ttf'))
    pdfmetrics.registerFont(TTFont('DejaVuSans', 'DejaVuSans-Bold.ttf'))
    c = canvas.Canvas('invoice.pdf', pagesize=letter)
    width, height = letter
    c.setFont("DejaVu", 15)

    c.drawCentredString(300, 750, "Order No. "+id1)

    c.rect(60, 520, 480, 190, stroke=1, fill=0)

    c.line(300, 520, 300, 710)

    c.line(60, 610, 300, 610)

    c.setFont("DejaVuSans", 12)
    c.drawString(70, 690, "Seller")

    c.setFont("DejaVu", 10)
    c.drawString(70, 675, seller[2][1]+" "+seller[3][1])
    c.setFont("DejaVu", 8)
    c.drawString(70, 665, "Thadomal Shahani Engineering College")
    c.drawString(70, 655, seller[5][1]+" - "+seller[0][1])
    c.drawString(70, 635, contact)
    c.drawString(70, 625, seller[1][1])

    c.setFont("DejaVuSans", 9)
    c.drawString(70, 590, "Payment Information")
    c.setFont("DejaVu", 9)
    c.drawString(70, 575, "yet to be done")

    c.line(300, 640, 540, 640)

    c.setFont("DejaVuSans", 12)
    c.drawString(310, 620, "Customer")

    c.setFont("DejaVu", 10)
    c.drawString(310, 605, customer[2][1]+" "+customer[3][1])
    c.setFont("DejaVu", 8)
    c.drawString(310, 595, "Thadomal Shahani Engineering College")
    c.drawString(310, 585, customer[5][1]+" - "+customer[0][1])
    c.drawString(310, 565, customer[4][1])
    c.drawString(310, 555, customer[1][1])

    c.rect(60, 390, 480, 100, stroke=1, fill=0)

    c.setFont("DejaVuSans", 7)
    c.drawString(65, 478, "List of items")
    c.line(60, 470, 540, 470)
    c.drawString(65, 458, "Description")
    c.drawString(350, 458, "Units")
    c.drawString(410, 458, "Price")
    c.drawString(470, 458, "Total Price")

    rs = "RS " + price
    c.line(60, 450, 540, 450)
    c.setFont("DejaVu", 7)
    c.drawString(65, 432, pname)
    c.drawString(352, 432, "1")
    c.drawString(412, 432, rs)
    c.drawString(475, 432, rs)
    c.setLineWidth(1.2)

    trs = "Total: "+rs
    c.line(60, 420, 540, 420)
    c.setFont("DejaVuSans", 11)
    c.drawString(420, 402, trs)
    c.showPage()
    c.save()
    return 1
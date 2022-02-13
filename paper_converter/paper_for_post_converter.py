from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.units import inch
from reportlab.platypus import Paragraph, SimpleDocTemplate, Table, TableStyle
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen.canvas import Canvas
import pandas as pd

table = pd.read_csv('papers_table.csv')

# Creating full name part
name_column = table['Name']
patronymic_column = table['Patronymic']
fio_column = name_column + ' ' + patronymic_column
    
# Creating address part
address_column = table['Address']
city_column = table['City']
full_address_column = address_column + ', ' + city_column
index_column = table['Index']
columns = [fio_column, full_address_column, index_column]
quantity_of_customers = len(fio_column)

ready_for_print_orders = []

i = 0
while i < quantity_of_customers:
    fullname = columns[0][i]
    address = columns[1][i]
    full_info = [fullname, address, index_column[i]]
    ready_for_print_orders.append(full_info)
    i += 1

# Creating PDF part

pdfmetrics.registerFont(TTFont('TNR', 'Roboto-Regular.ttf'))
style = getSampleStyleSheet()
styleTest = ParagraphStyle('main_style',
                            fontName="TNR",
                            fontSize=10,
                            parent=style['Heading2'],
                            spaceAfter=14,
                            wordWrap="allowWidows",
                            )

indexes = []
names = []
address = []

for i in range(len(ready_for_print_orders)):
    names.append(ready_for_print_orders[i][0])
    indexes.append(str(ready_for_print_orders[i][2]))
    address.append(ready_for_print_orders[i][1])

little = 50
big = 160

orders_quantity = len(names)
number_of_lists = (orders_quantity // 20)+1
not_enough = number_of_lists*20 - orders_quantity

for i in range(not_enough):
    names.append(' ')
    indexes.append(' ')
    address.append(' ')

for i in range(len(names)):
    names[i] = Paragraph(names[i], styleTest)
    indexes[i] = Paragraph(indexes[i], styleTest)
    address[i] = Paragraph(address[i], styleTest)

komu = Paragraph('Who', styleTest)
kuda = Paragraph('Where', styleTest)
index = Paragraph('Index', styleTest)

i = 0

data = [
                [komu,names[i+0],komu,names[i+1],komu,names[i+2],komu,names[i+3]],
                [kuda,address[i+0],kuda,address[i+1],kuda,address[i+2],kuda,address[i+3]],
                [index,indexes[i+0],index,indexes[i+1],index,indexes[i+2],index,indexes[i+3]],
                [komu,names[i+4],komu,names[i+5],komu,names[i+6],komu,names[i+7]],
                [kuda,address[i+4],kuda,address[i+5],kuda,address[i+6],kuda,address[i+7]],
                [index,indexes[i+4],index,indexes[i+5],index,indexes[i+6],index,indexes[i+7]],
                [komu,names[i+8],komu,names[i+9],komu,names[i+10],komu,names[i+11]],
                [kuda,address[i+8],kuda,address[i+9],kuda,address[i+10],kuda,address[i+11]],
                [index,indexes[i+8],index,indexes[i+9],index,indexes[i+10],index,indexes[i+11]],
                [komu,names[i+12],komu,names[i+13],komu,names[i+14],komu,names[i+15]],
                [kuda,address[i+12],kuda,address[i+13],kuda,address[i+14],kuda,address[i+15]],
                [index,indexes[i+12],index,indexes[i+13],index,indexes[i+14],index,indexes[i+15]],
                [komu,names[i+16],komu,names[i+17],komu,names[i+18],komu,names[i+19]],
                [kuda,address[i+16],kuda,address[i+17],kuda,address[i+18],kuda,address[i+19]],
                [index,indexes[i+16],index,indexes[i+17],index,indexes[i+18],index,indexes[i+19]]
        ]

# Building layout for PDF
t=Table(data, 
            colWidths=[little, big, little, big, little, big, little, big],
            style=[
            ('GRID',(0,0),(-1,-1),0,colors.lightgrey),
            ('BOX',(0,0),(1,2),0,colors.black),
            ('BOX',(2,0),(3,2),0,colors.black),
            ('BOX',(4,0),(5,2),0,colors.black),
            ('BOX',(6,0),(7,2),0,colors.black),
            ('BOX',(0,3),(1,5),0,colors.black),
            ('BOX',(2,3),(3,5),0,colors.black),
            ('BOX',(4,3),(5,5),0,colors.black),
            ('BOX',(6,3),(7,5),0,colors.black),
            ('BOX',(0,6),(1,8),0,colors.black),
            ('BOX',(2,6),(3,8),0,colors.black),
            ('BOX',(4,6),(5,8),0,colors.black),
            ('BOX',(6,6),(7,8),0,colors.black),
            ('BOX',(0,9),(1,11),0,colors.black),
            ('BOX',(2,9),(3,11),0,colors.black),
            ('BOX',(4,9),(5,11),0,colors.black),
            ('BOX',(6,9),(7,11),0,colors.black),
            ('BOX',(0,12),(1,14),0,colors.black),
            ('BOX',(2,12),(3,14),0,colors.black),
            ('BOX',(4,12),(5,14),0,colors.black),
            ('BOX',(6,12),(7,14),0,colors.black)
            ])

# Building PDF
canvas = Canvas("papers.pdf", pagesize=(A4[1],A4[0]))
canvas.setFont('TNR', 32)
t.wrapOn(canvas, 2.9*inch, 1.6*inch)
t.drawOn(canvas, 0, 0)

canvas.save()
#!/usr/bin/python
# -*- coding: utf-8 -*-

import itertools
import datetime
from random import randint
from statistics import mean

from reportlab.pdfgen import canvas
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib import colors
from reportlab.pdfgen.canvas import Canvas
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet


async def grouper(iterable, n):
    args = [iter(iterable)] * n
    return itertools.zip_longest(*args)


async def export_to_pdf(data, name: str):
    canvas = Canvas("canvas.pdf", pagesize=A4)
    pdfmetrics.registerFont(TTFont('timesnrcyrmt', 'timesnrcyrmt.ttf'))
    doc = SimpleDocTemplate(f"{name}.pdf", pagesize=A4)

    elements = []
    style = TableStyle(
        [('LINEABOVE', (0, 0), (-1, 0), 1, colors.black),
         ('LINEABOVE', (0, 1), (-1, -1), 1, colors.black),
         ('LINEBELOW', (0, -1), (-1, -1), 1, colors.black),
         ('FONT', (0, 0), (-1, 1), 'timesnrcyrmt', 12),
         ('FONTNAME', (0, 0), (-1, -1), 'timesnrcyrmt',12),
         ('BOX', (0, 0), (-1, -1), 1, colors.black),
         ('BOX', (0, 0), (0, -1), 1, colors.black),
         ('INNERGRID', (0, 0), (-1, -1), 1, colors.black),
         ],
    )

    t = Table(data)
    t.setStyle(style)
    elements.append(t)
    doc.build(elements)


async def start(lines: list, name: str):
    data = [("Х.E.", "К.И", "Д.И.", "Сахар до", "Сахар после", "Самочувствие",
             "П.П.", "Дата")]

    for i in range(len(lines)):
        count = 0
        for string in lines[i]:
            count += 1
            if string is not None and count <= 3:
                data_arr = string.replace("\"", "").replace("{", "").replace("}", "").split(",")
                data.append((data_arr[0].replace("Хлебные еденицы:", "").replace(" ", "", 1),
                             data_arr[1].replace("Короткий инсулин:", "").replace(" ", "", 1),
                             data_arr[2].replace("Длинный инсулин:", "").replace(" ", "", 1),
                             data_arr[3].replace("Сахар до:", "").replace(" ", "", 1),
                             data_arr[4].replace("Сахар после:", "").replace(" ", "", 1),
                             data_arr[5].replace("Самочувствие:", "").replace(" ", "", 1),
                             await get_meal_name(count),
                             (lines[i][len(lines[i]) - 1]).strftime("%d-%m-%Y")))
        count = 0

    a = 0
    await export_to_pdf(data, name)


async def get_meal_name(count: int):
    if count == 1:
        return "Завтрак"
    if count == 2:
        return "Обед"
    if count == 3:
        return "Ужин"

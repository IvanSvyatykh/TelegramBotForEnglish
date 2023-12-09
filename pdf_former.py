#!/usr/bin/python
# -*- coding: utf-8 -*-

import itertools
from random import randint
from statistics import mean

from reportlab.pdfgen import canvas
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont


async def grouper(iterable, n):
    args = [iter(iterable)] * n
    return itertools.zip_longest(*args)


async def export_to_pdf(data, name: str):
    c = canvas.Canvas(f"{name}.pdf", pagesize=A4)
    w, h = A4
    max_rows_per_page = 45
    # Margin.
    x_offset = 50
    y_offset = 50
    # Space between rows.
    padding = 15

    xlist = [x + x_offset for x in [0, 200, 250, 300, 350, 400, 480]]
    ylist = [h - y_offset - i * padding for i in range(max_rows_per_page + 1)]

    for rows in await grouper(data, max_rows_per_page):
        rows = tuple(filter(bool, rows))
        c.grid(xlist, ylist[:len(rows) + 1])
        for y, row in zip(ylist[:-1], rows):
            for x, cell in zip(xlist, row):
                c.drawString(x + 2, y - padding + 3, str(cell))
        c.showPage()

    c.save()


async def start(lines: list, name: str):
    data = [("Хлебные еденицы", "Короткий инсулин", "Длинный инсулин", "Сахар до", "Сахар после", "Самочувствие",
             "Прием пищи", "Дата")]


    for i in range(len(lines)):
        count = 0
        for string in lines[i]:
            count += 1
            if string is not None and count < 3:
                data_arr = string.replace("\"", "").replace("{", "").replace("}", "").split(",")
                data.append((data_arr[0].replace("Хлебные еденицы:", "").replace(" ", "", 1),
                             data_arr[1].replace("Короткий инсулин:", "").replace(" ", "", 1),
                             data_arr[2].replace("Длинный инсулин:", "").replace(" ", "", 1),
                             data_arr[3].replace("Сахар до:", "").replace(" ", "", 1),
                             data_arr[4].replace("Сахар после:", "").replace(" ", "", 1),
                             data_arr[5].replace("Самочувствие:", "").replace(" ", "", 1),
                             await get_meal_name(count),
                             lines[i][len(lines[i]) - 1]))

    a = 0
    await export_to_pdf(data, name)


async def get_meal_name(count: int):
    if count == 0:
        return "Завтрак"
    if count == 1:
        return "Обед"
    if count == 2:
        return "Ужин"

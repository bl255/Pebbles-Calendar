import webbrowser
from random import seed, randint
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import holidays

from calendar_classes import DrawnCalendar, CutLine
from pebble_classes import PebbleImage

# calendar general settings
YEAR = 2023
SK_MONTH_NAMES = ["Január", "Február", "Marec", "Apríl", "Máj", "Jún",
                  "Júl", "August", "September", "Október", "November", "December"]
ITALIC_DATES = [date for date in holidays.Slovakia(years=YEAR).keys()]
BOLD_DATES = [date for date in holidays.Czechia(years=YEAR).keys()]
SUNDAY_FIRST_EXAMPLE = False

PDF_FILENAME = "example_calendar.pdf"
PDF_PAGESIZE = A4
FINAL_PAGE_HEIGHT = 697

# calendar components positions settings
DAYS_GRAPHICS_WIDTH = 480
DAYS_GRAPHICS_UPPER_LEFT_X = (PDF_PAGESIZE[0] - DAYS_GRAPHICS_WIDTH) / 2
DAYS_GRAPHICS_UPPER_LEFT_Y = PDF_PAGESIZE[1] - 170
MONTH_NAME_CENTER_POINT = (PDF_PAGESIZE[0] / 2, PDF_PAGESIZE[1] - 110)

# calendar image position settings
IMAGE_LOWER_LEFT_X = (PDF_PAGESIZE[0] - 480) / 2
IMAGE_LOWER_LEFT_Y = 110

# setting seed
calendar_seed = randint(0, 9999)
seed(calendar_seed)

# initiating canvas, calendar, image, cut line
cal_canvas = canvas.Canvas(PDF_FILENAME, pagesize=PDF_PAGESIZE)
my_calendar = DrawnCalendar(YEAR, content_width=DAYS_GRAPHICS_WIDTH, month_names=SK_MONTH_NAMES,
                            bold_dates=BOLD_DATES, italic_dates=ITALIC_DATES, sunday_first=SUNDAY_FIRST_EXAMPLE)
my_image = PebbleImage((IMAGE_LOWER_LEFT_X, IMAGE_LOWER_LEFT_Y))
cut_line = CutLine(PDF_PAGESIZE[0])

# drawing calendar
cut_line.draw(cal_canvas, PDF_PAGESIZE[1] - FINAL_PAGE_HEIGHT)
for image_stage, month in enumerate(my_calendar.months, 1):
    cal_canvas.showPage()
    my_image.draw_at_stage(cal_canvas, image_stage)
    cal_canvas.showPage()
    month.draw(cal_canvas, (DAYS_GRAPHICS_UPPER_LEFT_X, DAYS_GRAPHICS_UPPER_LEFT_Y),
               MONTH_NAME_CENTER_POINT, f"{month.month_name} {YEAR}")

cal_canvas.showPage()
cut_line.draw(cal_canvas, FINAL_PAGE_HEIGHT)

cal_canvas.save()

# writing report
with open("report.txt", mode="w") as report_file:
    report_file.write(f"seed: {calendar_seed}\n\n")
    report_file.write("bold dates:\n")
    if BOLD_DATES:
        report_file.write("\n".join((str(b_date) for b_date in BOLD_DATES)))
    report_file.write("\n\nitalic dates:\n")
    if ITALIC_DATES:
        report_file.write("\n".join((str(i_date) for i_date in ITALIC_DATES)))

# opening the file
webbrowser.open(PDF_FILENAME)

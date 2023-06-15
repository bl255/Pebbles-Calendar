from reportlab.lib.pagesizes import A4
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from pathlib import Path
import calendar

SUNDAY_FIRST = False
FONTS_FOLDER = "fonts/Lato"
MONTH_NAME_FONT = "Lato-Regular", 40
DAY_FONTS_NAMES = {"default": "Lato-Light",
                   "italic": "Lato-LightItalic",
                   "bold": "Lato-Bold",
                   "bolditalic": "Lato-BoldItalic"}

MONTH_NAMES = ("January", "February", "March", "April", "May", "June",
               "July", "August", "September", "October", "November", "December")

DAY_LINE_WIDTHS = {"weekend": 1.2, "regular_day": 0.6}
DAY_FONT_SIZES = {"different_month": 12, "current_month": 16}

DAY_GAP_SQUARE_RATIO = 0.12
DAY_SQUARE_ROUNDING_RATIO = 0.15
DAY_TEXT_MARGIN_RATIO = 0.1

CUTLINE_LINE_WIDTH = 0.3
CUTLINE_DASH = 9, 9
CUTLINE_COLOR = 0, 0, 0, 0.5

# registering fonts
for item in Path(FONTS_FOLDER).iterdir():
    if item.is_file() and item.suffix == ".ttf":
        fontname = item.stem
        pdfmetrics.registerFont(TTFont(fontname, str(item)))


def font_ascent(font_tuple):
    """Calculates the ascent of a font, i.e., the distance from the baseline to the highest point of a character.

    Args:
        font_tuple (tuple): A tuple where the first element is the font name (str) and the second element is the
        font size (int).

    Returns:
        float: The ascent of the font, calculated as the ratio of the font's highest point to the font size.
    """
    font = pdfmetrics.getFont(font_tuple[0])
    return font.face.ascent / 1000 * font_tuple[1]


class Day:
    """Representation of a calendar day, including drawing attributes.

    Args:
        date (datetime.date): The date this Day instance represents.
        month_num (int): The number of the month this Day instance belongs to.
        bold_dates (list): A list of datetime objects that should be displayed in bold.
        italic_dates (list): A list of datetime objects that should be displayed in italics.
        square_size (float): The size of the square representing this day on the calendar.
        rounding_ratio (float, optional): The ratio used for rounding the corners of the square.
            Defaults to DAY_SQUARE_ROUNDING_RATIO.
        text_margin_ratio (float, optional): The ratio used for setting the margin of the text within the square.
            Defaults to DAY_TEXT_MARGIN_RATIO.
        square_line_cmyk_color (tuple, optional): The color of the square in CMYK format. Defaults to (0, 0, 0, 1).
        square_text_cmyk_color (tuple, optional): The color of the square in CMYK format. Defaults to (0, 0, 0, 1).

    Attributes:
        date (datetime): The date object this Day instance represents.
        month_num (int): The month number for the current day.
        day_text (str): The day number as a string.
        square_size (int): The size of the square that represents the day.
        rounding_ratio (float): The ratio used for rounding the corners of the day's square.
        text_margin_ratio (float): The margin ratio for the day's text.
        square_line_cmyk_color (tuple): The color of the square in CMYK format.
        square_text_cmyk_color (tuple): The color of the square in CMYK format.
        line_width (float): The width of the lines in the day's square.
        day_font_name (str): The font used for the day's text.
        day_square_is_drawn (bool): Determines if the day's square is drawn.
        day_center_text (bool): Determines if the day's text is centered.
        day_font_size (int): The font size of the day's text.
    """

    def __init__(self, date, month_num, bold_dates, italic_dates, square_size,
                 rounding_ratio=DAY_SQUARE_ROUNDING_RATIO, text_margin_ratio=DAY_TEXT_MARGIN_RATIO,
                 square_line_cmyk_color=(0, 0, 0, 1), square_text_cmyk_color=(0, 0, 0, 1)):

        self.date = date
        self.month_num = month_num
        self.day_text = str(self.date.day)

        self.square_size = square_size
        self.rounding_ratio = rounding_ratio
        self.text_margin_ratio = text_margin_ratio
        self.square_line_cmyk_color = square_line_cmyk_color
        self.square_text_cmyk_color = square_text_cmyk_color

        self.line_width = None
        self.day_font_name = None
        self.day_square_is_drawn = None
        self.day_center_text = None
        self.day_font_size = None

        self.get_day_line_width(DAY_LINE_WIDTHS)
        self.get_day_font_name(DAY_FONTS_NAMES, bold_dates, italic_dates)
        self.get_day_font_size_position(DAY_FONT_SIZES)

    def get_day_line_width(self, line_widths):
        """Sets the line width for the day. Weekends and regular days have different line widths.

        Args:
            line_widths (dict): A dictionary mapping the type of day ("weekend" or "regular_day") to line widths.
        """
        if self.date.weekday() in [5, 6]:
            self.line_width = line_widths["weekend"]
        else:
            self.line_width = line_widths["regular_day"]

    def get_day_font_name(self, day_font_names, bold_dates, italic_dates):
        """Sets the font name for the day.

        The font can be different depending on whether the day is in bold_dates or italic_dates.

        Args:
            day_font_names (dict): A dictionary mapping the font styles ("bolditalic", "italic", "bold", "default")
                to font names.
            bold_dates (list): A list of dates that should be bolded.
            italic_dates (list): A list of dates that should be italicized.
        """
        if self.date in italic_dates and self.date in bold_dates:
            self.day_font_name = day_font_names["bolditalic"]

        elif self.date in italic_dates:
            self.day_font_name = day_font_names["italic"]

        elif self.date in bold_dates:
            self.day_font_name = day_font_names["bold"]
        else:
            self.day_font_name = day_font_names["default"]

    def get_day_font_size_position(self, day_font_sizes):
        """Sets the font size and position for the day.

        The font size and position can be different depending on whether the day belongs to the current month.

        Args:
            day_font_sizes (dict): A dictionary mapping the month type ("different_month" or "current_month")
            to font sizes.
        """
        if self.date.month != self.month_num:
            self.day_center_text = True
            self.day_square_is_drawn = False
            self.day_font_size = day_font_sizes["different_month"]
        else:
            self.day_center_text = False
            self.day_square_is_drawn = True
            self.day_font_size = day_font_sizes["current_month"]

    def rounded_square(self, canvas, sq_x, sq_y):
        """Draws a rounded square on the canvas at the specified position.

        Args:
            canvas (reportlab.pdfgen.canvas.Canvas): The canvas on which to draw.
            sq_x (int): The x-coordinate for the top left corner of the square.
            sq_y (int): The y-coordinate for the top left corner of the square.
        """
        radius = self.square_size * self.rounding_ratio
        canvas.setLineWidth(self.line_width)
        canvas.setStrokeColorCMYK(*self.square_line_cmyk_color)
        canvas.roundRect(sq_x, sq_y, self.square_size, self.square_size, radius, stroke=1, fill=0)

    def text_in_square(self, canvas, sq_x, sq_y):
        """Places the day's text inside the square.

        Args:
            canvas (reportlab.pdfgen.canvas.Canvas): The canvas on which to place the text.
            sq_x (int): The x-coordinate for the top left corner of the square.
            sq_y (int): The y-coordinate for the top left corner of the square.
        """
        canvas.setFont(self.day_font_name, self.day_font_size)
        text_width = canvas.stringWidth(self.day_text, self.day_font_name, self.day_font_size)
        text_height = font_ascent((self.day_font_name, self.day_font_size))
        if self.day_center_text:
            tx = sq_x + (self.square_size - text_width) / 2
            ty = sq_y + (self.square_size - text_height) / 2
        else:
            tx = sq_x + self.text_margin_ratio * self.square_size
            ty = sq_y + (1 - self.text_margin_ratio) * self.square_size - text_height
        canvas.setFillColorCMYK(*self.square_text_cmyk_color)
        canvas.drawString(tx, ty, self.day_text)

    def draw(self, canvas, sq_x, sq_y):
        """Executes the drawing operations for the day on the canvas.

        Args:
            canvas (reportlab.pdfgen.canvas.Canvas): The canvas on which to draw.
            sq_x (int): The x-coordinate for the top left corner of the square.
            sq_y (int): The y-coordinate for the top left corner of the square.
        """
        self.text_in_square(canvas, sq_x, sq_y)
        if self.day_square_is_drawn:
            self.rounded_square(canvas, sq_x, sq_y)


class Month:
    """Representation of a Month, including drawing attributes. The class includes individual days, which can have
        customized display properties.

    Args:
        number (int): The number of the month (1 for January, 2 for February, etc.).
        month_name (str): The name of the month.
        month_dates_by_weeks (list): A nested list of datetime.date objects for each day of the month by week.
        page_size (tuple): A tuple containing the width and height of the page (width, height).
        max_width (float): The maximum width for the month display.
        bold_dates (list): A list of datetime.date objects that should be displayed in bold.
        italic_dates (list): A list of datetime.date objects that should be displayed in italics.
        sunday_first (bool, optional): A boolean value that, when set to True, will start drawing with Sunday.
            If set to False, will start drawing with Monday. Defaults to SUNDAY_FIRST.
        gap_ratio (float, optional): The ratio of the gap size between the day squares and day square size.
            Defaults to DAY_GAP_SQUARE_RATIO.
        month_name_font (tuple, optional): The font used to display the month's name.
            Defaults to MONTH_NAME_FONT.

    Attributes:
        number (int): The number of the month (1 for January, etc.).
        month_name (str): The name of the month.
        page_width (float): The width of the page on which the month is to be drawn.
        page_height (float): The height of the page on which the month is to be drawn.
        month_name_font (tuple): The font used to display the month's name.
        bold_dates (list): A list of datetime.date objects that should be displayed in bold.
        italic_dates (list): A list of datetime.date objects that should be displayed in italics.
        sunday_first (bool, optional): A boolean value that, when set to True, will start drawing with Sunday.
            If set to False, will start drawing with Monday. Defaults to SUNDAY_FIRST.
        gap_ratio (float): The ratio of gap size between day squares and day square size.
        max_width (float): The maximum width for the month display.
        days_by_weeks (list): A nested list of Day objects representing each day of the month by week.
    """

    def __init__(self, number, month_name, month_dates_by_weeks, page_size, max_width, bold_dates, italic_dates,
                 sunday_first=SUNDAY_FIRST, gap_ratio=DAY_GAP_SQUARE_RATIO, month_name_font=MONTH_NAME_FONT):

        self.number = number
        self.month_name = month_name
        self.page_width, self.page_height = page_size
        self.month_name_font = month_name_font
        self.bold_dates = bold_dates
        self.italic_dates = italic_dates
        self.sunday_first = sunday_first

        self.gap_ratio = gap_ratio
        self.max_width = max_width

        self.days_by_weeks = self.days_by_weeks_func(month_dates_by_weeks)

    @property
    def square_size(self):
        """Calculates the size of the square for the day boxes in the month.

        Returns:
            float: The size of the square for the day boxes.
        """

        return self.max_width / (7 + 6 * self.gap_ratio)

    @property
    def gap_size(self):
        """Calculates the size of the gap between the day boxes in the month.

        Returns:
            float: The size of the gap for the day boxes.
        """

        return (self.max_width - 7 * self.square_size) / 6

    def days_by_weeks_func(self, dates_by_weeks):
        """Converts a list of dates in the month to a list of Day objects.

        Args:
            dates_by_weeks (list): A nested list of datetime.date objects representing each day of the month by week.

        Returns:
            list: A nested list of Day objects representing each day of the month by week.
        """
        all_days = []
        for week in dates_by_weeks:
            new_week = []
            for day in week:
                new_day = Day(day, self.number, self.bold_dates, self.italic_dates, self.square_size)
                new_week.append(new_day)
            all_days.append(new_week)
        return all_days

    def draw_month_days(self, canvas, tl_point):
        """Draws all the days of the month on the canvas.

        Args:
            canvas (reportlab.pdfgen.canvas.Canvas): The canvas on which the month is being drawn.
            tl_point (tuple): A tuple containing the x, y coordinates of the top left point to start drawing from.
        """
        for w_num, week in enumerate(self.days_by_weeks):
            for day in week:
                square_num = day.date.weekday()
                if self.sunday_first:
                    square_num = (square_num + 1) % 7
                x = tl_point[0] + square_num * (self.square_size + self.gap_size)
                y = tl_point[1] - self.square_size - w_num * (self.square_size + self.gap_size)
                day.draw(canvas, x, y)

    def draw_centered_month_name(self, canvas, center_point, text, text_cmyk_color=(0, 0, 0, 1)):
        """Draws the month name.

        Args:
            canvas (reportlab.pdfgen.canvas.Canvas): The canvas on which the month is being drawn.
            center_point (tuple): A tuple containing the x, y coordinates of the center point of the page.
            text (str): The text to be drawn (the month name).
            text_cmyk_color (tuple, optional): The color of the cut line in CMYK color model. Defaults to (0, 0, 0, 1).
        """
        center_x, center_y = center_point
        canvas.setFont(*self.month_name_font)
        canvas.setFillColorCMYK(*text_cmyk_color)
        canvas.drawCentredString(center_x, center_y - font_ascent(self.month_name_font) / 2, text)

    def draw(self, canvas, days_point, center_point, month_name_text):
        """Draws the entire month on the canvas, including the month name and all the days.

        Args:
            canvas (reportlab.pdfgen.canvas.Canvas): The canvas on which the month is being drawn.
            days_point (tuple): A tuple containing the x, y coordinates of the top left point to start
                drawing days from.
            center_point (tuple): A tuple containing the x, y coordinates of the center point of the page.
            month_name_text (str): The text to be drawn (the month name).
        """
        self.draw_centered_month_name(canvas, center_point, month_name_text)
        self.draw_month_days(canvas, days_point)


class DrawnCalendar:
    """A class used to represent a calendar for a specific year.

    Args:
        year (int): The year for the calendar.
        content_width (float): The width of the calendar content on the page.
        cal_pagesize (tuple, optional): A tuple representing the size of the page for the PDF document.
            Defaults to A4 size.
        month_names (list, optional): A list of string names for each month. Defaults to MONTH_NAMES.
        bold_dates (list, optional): A list of datetime.date objects that should be bolded in the calendar.
            Defaults to None.
        italic_dates (list, optional): A list of datetime.date objects that should be italicized in the calendar.
            Defaults to None.
        sunday_first (bool, optional): A boolean value that, when set to True, week will start with Sunday.
            If set to False, week will start with Monday. Defaults to SUNDAY_FIRST.

    Attributes:
        year (int): The year for the calendar.
        month_names (list): A list of string names for each month.
        pagesize (tuple): A tuple representing the size of the page for the PDF document.
        content_width (float): The width of the calendar content on the page.
        bold_dates (list): A list of datetime.date objects that should be bolded in the calendar.
        italic_dates (list): A list of datetime.date objects that should be italicized in the calendar.
        sunday_first (bool, optional): A boolean value that, when set to True, week will start with Sunday.
            If set to False, week will start with Monday. Defaults to SUNDAY_FIRST.
       """

    def __init__(self, year, content_width, cal_pagesize=A4, month_names=MONTH_NAMES, bold_dates=None,
                 italic_dates=None, sunday_first=SUNDAY_FIRST):

        self.year = year
        self.month_names = month_names
        self.pagesize = cal_pagesize
        self.content_width = content_width

        self.bold_dates = bold_dates or []
        self.italic_dates = italic_dates or []
        self.sunday_first = sunday_first
        self.months = self.create_months()

    def create_months(self):
        """Creates Month objects for each month in the year and returns a list of those objects.

        Returns:
            list: A list of Month objects representing each month in the year.
        """
        all_months = []
        cal = calendar.Calendar()
        if self.sunday_first:
            cal.setfirstweekday(calendar.SUNDAY)
        cal_days = cal.yeardatescalendar(self.year)
        for q_num, quarter in enumerate(cal_days):
            for qm_num, month_dates in enumerate(quarter, 1):
                month_num = q_num * 3 + qm_num
                month_obj = Month(month_num, self.month_names[month_num - 1], month_dates, self.pagesize,
                                  self.content_width, self.bold_dates, self.italic_dates, self.sunday_first)
                all_months.append(month_obj)
        return all_months


class CutLine:
    """A class representing a cut line in a canvas.

    Args:
        width (float): The width of the cut line.
        line_width (float, optional): The thickness of the cut line.
            Default value is determined by `CUTLINE_LINE_WIDTH`.
        dash (tuple, optional): The dash pattern of the cut line.
            Default value is determined by `CUTLINE_DASH`.
        line_cmyk_color (tuple, optional): The color of the cut line in CMYK color model.
            Default value is determined by `CUTLINE_COLOR`.

       Attributes:
           width (float): The width of the cut line.
           line_width (float): The thickness of the cut line. Default value is determined by `CUTLINE_LINE_WIDTH`.
           dash (tuple): The dash pattern of the cut line. Default value is determined by `CUTLINE_DASH`.
           line_cmyk_color (tuple): The color of the cut line in CMYK color model.
            Default value is determined by `CUTLINE_COLOR`.
       """

    def __init__(self, width, line_width=CUTLINE_LINE_WIDTH, dash=CUTLINE_DASH, line_cmyk_color=CUTLINE_COLOR):
        self.width = width
        self.line_width = line_width
        self.dash = dash
        self.line_cmyk_color = line_cmyk_color

    def draw(self, canvas, y_position):
        """Draws the cut line on the given canvas at the specified y position.

        Args:
            canvas (object): The canvas object on which the line is to be drawn.
            y_position (float): The y-position at which the line is to be drawn.
        """
        canvas.setStrokeColorCMYK(*self.line_cmyk_color)
        canvas.setLineWidth(self.line_width)
        canvas.setDash(*self.dash)
        canvas.line(0, y_position, self.width, y_position)
        canvas.setDash()

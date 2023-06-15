from math import sin, cos
from random import randint, uniform

RADIUS_X_RANGE = 20, 36
RADIUS_Y_RANGE = 12, 20
K_ADD_RANGE = -0.05, 0.07
RANDOMIZE_POSITION_RANGE = 0.7, 1.3
RANDOM_CMYK_GREY_RANGE = 0.1, 0.9

PEBBLES_PER_SHELF = 3
PEBBLES_ON_SHELF_GAP = 10
NUMBER_OF_SHELVES = 4
SHELVES_VERTICAL_SPACING = 72
SHELF_WIDTH = 264
SHELF_HEIGHT = 2.4

LINES_SPACING = 24
LINES_LINE_WIDTH = 0.6
LINES_DASH = 6, 12

LINES_START_POINT = (0, 0)
LINES_END_POINT = (480, 408)
SHELVES_LOWER_LEFT_POINT = LINES_START_POINT[0] + 36, LINES_START_POINT[1] + 46.8


def add_points_elements(point1, point2):
    """Adds x and y elements of two point tuples.

        Args:
            point1 (tuple): The first point, represented as a tuple of two floats or ints.
            point2 (tuple): The second point, represented as a tuple of two floats or ints.

        Returns:
            tuple: A point represented as a tuple of two elements (x, y).
        """
    return point1[0] + point2[0], point1[1] + point2[1]


class Shelf:
    """Represents a shelf with specific dimensions and color properties.

    Args:
       start_point (tuple): The starting lower left point (x, y) for drawing the shelf.
       shelf_width (float, optional): The width of the shelf.
       shelf_height (float, optional): The height of the shelf.
       cmyk_color (tuple, optional): The color of the shelf in CMYK format.

    Attributes:
       shelf_width (float): The width of the shelf.
       shelf_height (float): The height of the shelf.
       cmyk_color (tuple): The color of the shelf in CMYK format.
       start_x (float): The x-coordinate of the lower left starting point for drawing the shelf.
       start_y (float): The y-coordinate of the lower left starting point for drawing the shelf.
       """

    def __init__(self, start_point, shelf_width=SHELF_WIDTH, shelf_height=SHELF_HEIGHT, cmyk_color=(0, 0, 0, 1)):
        self.shelf_width = shelf_width
        self.shelf_height = shelf_height
        self.cmyk_color = cmyk_color
        self.start_x, self.start_y = start_point

    def draw(self, canvas):
        """Draws the shelf on a specified canvas.

        Args:
            canvas (reportlab.pdfgen.canvas.Canvas): The canvas on which the shelf is to be drawn.
        """
        canvas.setFillColorCMYK(*self.cmyk_color)
        canvas.rect(self.start_x, self.start_y, self.shelf_width, self.shelf_height, fill=1, stroke=0)

    @property
    def upper_left_point(self):
        """Calculates the coordinates of the upper left point of the shelf.

        Returns:
            tuple: A tuple representing the coordinates (x, y) of the upper left point of the shelf.
        """
        return self.start_x, self.start_y + self.shelf_height


class Shelves:
    """Represents a collection of Shelf objects.

    Args:
        bottom_start (tuple): Coordinates of the starting point at the bottom for the first shelf.
        n (int, optional): Number of shelves to be created.
        spacing (int, optional): Vertical spacing between successive shelves.
        *shelf_args: Variable length argument list to be passed to the Shelf class.
        **shelf_kwargs: Arbitrary keyword arguments to be passed to the Shelf class.

    Attributes:
        bottom_start_x (float): The x-coordinate of the starting point for the bottom shelf.
        bottom_start_y (float): The y-coordinate of the starting point for the bottom shelf.
        n (int): Number of shelves to be created.
        spacing (int): Vertical spacing between consecutive shelves.
        all_shelves (list): List of all Shelf objects created.
    """

    def __init__(self, bottom_start, n=NUMBER_OF_SHELVES, spacing=SHELVES_VERTICAL_SPACING,
                 *shelf_args, **shelf_kwargs):
        self.bottom_start_x, self.bottom_start_y = bottom_start
        self.n = n
        self.spacing = spacing
        self.all_shelves = []

        new_y = self.bottom_start_y
        for n in range(n):
            self.all_shelves.append(Shelf((self.bottom_start_x, new_y), *shelf_args, **shelf_kwargs))
            new_y += self.spacing

    def draw(self, canvas):
        """Draws all the shelves on a specified canvas.

        Args:
            canvas (reportlab.pdfgen.canvas.Canvas): The canvas on which the shelves are to be drawn.

        Note:
            The method uses the `draw` method of the `Pebble` instances to draw each pebble.
        """
        for shelf in self.all_shelves:
            shelf.draw(canvas)


class Pebble:
    """Represents a pebble with a set of geometric attributes and color properties.

    Args:
        center_coordinates (tuple, optional): Coordinates for the center of the pebble.
        cmyk_color (tuple, optional): Color of the pebble in CMYK format
        randomize_zero_points_by (tuple, optional): Range to randomize zero points.
        rx_range (tuple, optional): Range for the x radius of the pebble.
        ry_range (tuple, optional): Range for the y radius of the pebble.
        k_add (tuple, optional): Range to add to the k constant.

    Attributes:
        k (float): Approximation constant for ellipse.
        angles (tuple): Tuple of four float values representing angles in radians.
        center_coordinates (tuple): Tuple of two float values representing the center of the pebble.
        k_add (tuple): Tuple of two float values to adjust the k constant.
        rx_range (tuple): Tuple of two int values representing the x radius range of the pebble.
        ry_range (tuple): Tuple of two int values representing the y radius range of the pebble.
        rx (int): X radius of the pebble.
        ry (int): Y radius of the pebble.
        ran_k (float): Randomized k value for the pebble.
        randomize_zero_points_by (tuple): Tuple of two float values to randomize zero points.
        cmyk_color (tuple): Tuple of four float values representing the color of the pebble in cmyk.
        zero_points (list): List of tuples representing the zero points of the pebble."""

    def __init__(self, center_coordinates=(0, 0), cmyk_color=None, randomize_zero_points_by=RANDOMIZE_POSITION_RANGE,
                 rx_range=RADIUS_X_RANGE, ry_range=RADIUS_Y_RANGE, k_add=K_ADD_RANGE):

        self.k = 0.5522847498  # approximation constant for ellipse
        self.angles = 0.0, 1.5707963267948966, 3.141592653589793, 4.71238898038469
        # [(i / 4) * 2 * pi for _ in range(4)]
        self.center_coordinates = center_coordinates
        self.k_add = k_add
        self.rx_range = rx_range
        self.ry_range = ry_range

        self.rx = randint(*self.rx_range)
        self.ry = randint(*self.ry_range)
        self.ran_k = self.k + uniform(*self.k_add)
        self.randomize_zero_points_by = randomize_zero_points_by

        if cmyk_color is None:
            self.cmyk_color = self.random_cmyk_grey()
        else:
            self.cmyk_color = cmyk_color

        self.zero_points = self.get_zero_points()

    def get_zero_points(self):
        """Calculates corner points of the pebble at the center of 0, 0 based on its angles, radius and randomization.

        Returns:
            list: List of four tuples each containing two floats representing the x, y coordinates of the zero points.
        """
        zero_for_rand = []
        for point_ang in self.angles:
            point_x = self.rx * cos(point_ang) * self.random_xy_displace_scale()
            point_y = self.ry * sin(point_ang) * self.random_xy_displace_scale()
            zero_for_rand.append((point_x, point_y))
        return zero_for_rand

    def random_xy_displace_scale(self):
        """Random coefficient of displacement of the x and y coordinates using the pebble's randomization range.

        Returns:
            float: A random float within the randomization range.
        """

        return uniform(*self.randomize_zero_points_by)

    @staticmethod
    def random_cmyk_grey(random_cmyk_grey_range=RANDOM_CMYK_GREY_RANGE):
        """Generates a random CMYK grey color.

        Args:
            random_cmyk_grey_range (tuple, optional): A tuple of two floats defining the range for generating
            a random shade of grey.

        Returns:
            tuple: A tuple of four floats representing a CMYK color.
        """

        shade = uniform(*random_cmyk_grey_range)
        return 0, 0, 0, shade

    @property
    def curve_controls(self):
        """Calculates and returns the control points for drawing the pebble.

        Returns:
            list: List of tuples each containing four floats representing the x and y coordinates of the control points
            for drawing the pebble.
        """
        controls = []
        for i, ang in enumerate(self.angles):
            angle1 = self.angles[i]
            angle2 = self.angles[(i + 1) % len(self.angles)]
            start_x, start_y = self.points[i]
            end_x, end_y = self.points[(i + 1) % len(self.angles)]

            control1_x = start_x + (-sin(angle1) * self.ran_k * self.rx)
            control1_y = start_y + (cos(angle1) * self.ran_k * self.ry)
            control2_x = end_x + (sin(angle2) * self.ran_k * self.rx)
            control2_y = end_y - (cos(angle2) * self.ran_k * self.ry)
            controls.append((control1_x, control1_y, control2_x, control2_y))
        return controls

    @property
    def points(self):
        """Calculates and returns the points for drawing the pebble based on its center coordinates and zero points.

        Returns:
            list: List of tuples each containing two floats representing the x and y coordinates of the points
            for drawing the pebble.
        """
        draw_points = []
        for zero_point in self.zero_points:
            draw_x = self.center_coordinates[0] + zero_point[0]
            draw_y = self.center_coordinates[1] + zero_point[1]
            draw_points.append((draw_x, draw_y))
        return draw_points

    @property
    def center_distances(self):
        """Calculates and returns the distances from the center of the pebble to the zero points.

        Returns:
            list: List of four floats representing the distances from the center of the pebble to the corner points.
        """
        return [
            min([po[0] for po in self.zero_points]),
            min([po[1] for po in self.zero_points]),
            max([po[0] for po in self.zero_points]),
            max([po[1] for po in self.zero_points])
        ]

    @property
    def measures(self):
        """Calculates the measures of the pebble based on its corner points.

        Returns:
            list: List of two floats representing the measures of the pebble.
        """
        return [
            max([po[0] for po in self.zero_points]) - min([po[0] for po in self.zero_points]),
            max([po[1] for po in self.zero_points]) - min([po[1] for po in self.zero_points])
        ]

    def move(self, new_pos):
        """Moves the pebble to a new position by updating its center coordinates.

        Args:
            new_pos (tuple): A tuple of two floats representing the new position for the center of the pebble.
        """
        self.center_coordinates = new_pos

    def draw(self, canvas):
        """Draws the pebble on the given canvas.

        Args:
            canvas (reportlab.pdfgen.canvas.Canvas): An object representing the canvas on which to draw the pebble.
        """
        path = canvas.beginPath()
        canvas.setFillColorCMYK(*self.cmyk_color)
        for i in range(4):
            if i == 0:
                path.moveTo(*self.points[i])
            path.curveTo(*self.curve_controls[i], *self.points[(i + 1) % 4])
        canvas.drawPath(path, fill=1, stroke=0)


class PebbleCollection:
    """Represents a collection of Pebble objects.

    Attributes:
        all_pebbles (list): A list of Pebble instances.
        n (int): The number of pebbles in the collection.

    Args:
        n (int): The number of pebbles to create for the collection.
        *args: Variable length argument list to be passed to the Pebble constructor.
        **kwargs: Arbitrary keyword arguments to be passed to the Pebble constructor.
    """

    def __init__(self, n, *args, **kwargs):
        self.all_pebbles = []
        self.n = n
        for _ in range(n):
            peb = Pebble(*args, **kwargs)
            self.all_pebbles.append(peb)

    def move_to_shelves(self, shelves, pebbles_per_shelf=PEBBLES_PER_SHELF, gap=PEBBLES_ON_SHELF_GAP):
        """Moves pebbles in the collection to a specific position on a shelf.

        Args:
            shelves (object): An object representing the shelves to which to move the pebbles.
            pebbles_per_shelf (int, optional): The number of pebbles to place on each shelf.
            gap (float, optional): The gap to leave between each pebble on a shelf.
        """
        shift = 0
        for peb_num, peb in enumerate(self.all_pebbles):
            shelf = shelves.all_shelves[peb_num // pebbles_per_shelf]
            new_x = shift + shelf.upper_left_point[0] - peb.center_distances[0]
            new_y = shelf.upper_left_point[1] - peb.center_distances[1]
            new_pos = new_x, new_y
            peb.move(new_pos)

            if (peb_num + 1) % pebbles_per_shelf == 0:
                shift = 0
            else:
                shift += gap + peb.measures[0]

    def draw(self, canvas, num_to_draw):
        """Draws a specified number of pebbles from the collection onto a canvas.

        Args:
            canvas (reportlab.pdfgen.canvas.Canvas): The canvas object on which the pebbles will be drawn.
            num_to_draw (int): The number of pebbles to draw from the collection. If this number exceeds the size
                of the collection, all pebbles in the collection will be drawn.

        Note:
            The method uses the `draw` method of the `Pebble` instances to draw each pebble.
        """
        for peb in self.all_pebbles[:num_to_draw]:
            peb.draw(canvas)


class Lines:
    """Represents a set of parallel lines with customizable attributes.

           Args:
               start_point (tuple): The start point coordinates of the lines.
               end_point (tuple): The end point coordinates of the lines.
               spacing (float, optional): The distance between each line.
               vertical (bool, optional): The orientation of the lines. True if vertical, False if horizontal.
               cmyk_color (tuple, optional): Color of the lines in CMYK format
               line_width (float, optional): Width of the lines.
               dash (tuple, optional): Dash pattern for the lines.

           Attributes:
               start_x (float): The x-coordinate of the start point for the lines.
               start_y (float): The y-coordinate of the start point for the lines.
               end_x (float): The x-coordinate of the end point for the lines.
               end_y (float): The y-coordinate of the end point for the lines.
               spacing (float): The distance between each line.
               vertical (bool): The orientation of the lines.
               cmyk_color (tuple): Color of the lines in CMYK format
               line_width (float): Width of the lines.
               dash (tuple): Dash pattern for the lines.
           """

    def __init__(self, start_point, end_point, spacing=LINES_SPACING, vertical=True,
                 cmyk_color=(0, 1, 0, 0), line_width=LINES_LINE_WIDTH, dash=LINES_DASH):

        self.start_x, self.start_y = start_point
        self.end_x, self.end_y = end_point
        self.spacing = spacing
        self.vertical = vertical
        self.cmyk_color = cmyk_color
        self.line_width = line_width
        self.dash = dash

    def draw(self, canvas):
        """Draws the lines on a specified canvas.

        Args:
            canvas (reportlab.pdfgen.canvas.Canvas): The canvas on which the lines are to be drawn.
        """
        canvas.setFillColorCMYK(*self.cmyk_color)
        canvas.setLineWidth(self.line_width)
        canvas.setDash(*self.dash)

        if self.vertical:
            new_x = self.start_x
            while new_x <= self.end_x:
                canvas.line(new_x, self.start_y, new_x, self.end_y)
                new_x += self.spacing
        else:
            new_y = self.start_y
            while new_y <= self.end_y:
                canvas.line(self.start_x, new_y, self.end_x, new_y)
                new_y += self.spacing

        canvas.setDash()


class PebbleImage:
    """Represents an image consisting of pebbles, shelves, and background lines.

    Args:
        lower_left_point (tuple): The lower left coordinates of the image.

    Attributes:
        x (float): The x-coordinate of the lower left point of the image.
        y (float): The y-coordinate of the lower left point of the image.
        image_shelves (Shelves): The shelves in the image.
        image_pebbles (PebbleCollection): The pebbles in the image.
        image_background_lines (Lines): The background lines in the image.
    """
    def __init__(self, lower_left_point):

        self.x, self.y = lower_left_point
        self.image_shelves = Shelves(add_points_elements(lower_left_point, SHELVES_LOWER_LEFT_POINT))
        self.image_pebbles = PebbleCollection(12)
        self.image_background_lines = Lines(add_points_elements(lower_left_point, LINES_START_POINT),
                                            add_points_elements(lower_left_point, LINES_END_POINT))
        self.image_pebbles.move_to_shelves(self.image_shelves)

    @property
    def num_of_stages(self):
        """Calculates the number of stages in the image, which corresponds to the number of pebbles.

        Returns:
            int: The number of stages.
        """
        return len(self.image_pebbles.all_pebbles)

    def draw_at_stage(self, canvas, image_stage):
        """Draws the image at a specific stage.

        Args:
            canvas (reportlab.pdfgen.canvas.Canvas): The canvas on which the image is to be drawn.
            image_stage (int): The specific stage at which to draw the image.
        """
        self.image_background_lines.draw(canvas)
        self.image_shelves.draw(canvas)
        self.image_pebbles.draw(canvas, image_stage)

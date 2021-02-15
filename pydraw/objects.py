"""
Objects in the PyDraw library

(Author: Noah Coetsee)
"""

import turtle;
import tkinter as tk;
import math;

# from pydraw.errors import *;  # util gives us our errors for us :)
from pydraw.util import *;

from pydraw import Screen;
from pydraw import Location;
from pydraw import Color;

PIXEL_RATIO = 20;


class Object:
    """
    A base object containing a location and screen. This ensures coordinates are
    done with the root at the top left corner, and not at the center.
    """

    def __init__(self, screen: Screen, x: float = 0, y: float = 0, location: Location = None):
        verify(screen, Screen, x, (float, int), y, (float, int), location, Location);

        self._screen = screen;
        self._location = location if location is not None else Location(x, y);

        if isinstance(self, Renderable):
            self._ref = turtle.Turtle();
            self._ref.hideturtle();
            self._ref.penup();

    def x(self, x: float = None) -> float:
        if x is not None:
            verify(x, (float, int));
            self.moveto(x, self.y());

        return self._location.x();

    def y(self, y: float = None) -> float:
        if y is not None:
            verify(y, (float, int));
            self.moveto(self.x(), y);

        return self._location.y();

    def location(self) -> Location:
        return self._location;

    def move(self, *args, **kwargs) -> None:
        """
        Can take either a tuple, Location, or two numbers (dx, dy)
        :return: None
        """

        diff = (0, 0);

        # Basically we don't have an empty tuple at the start.
        if len(args) > 0 and (type(args[0]) is float or type(args[0]) is int or type(args[0]) is Location or
                              type(args[0]) is tuple and not len(args[0]) == 0):
            if len(args) == 1 and type(args[0]) is tuple or type(args[0]) is Location:
                diff = (args[0][0], args[0][1]);
            elif len(args) == 2 and [type(arg) is float or type(arg) is int for arg in args]:
                diff = (args[0], args[1]);
            else:
                raise InvalidArgumentError('Object#move() must take either a tuple/location or two numbers (dx, dy)!');

        for (name, value) in kwargs.items():
            if len(kwargs) == 0 or type(value) is not int and type(value) is not float:
                raise InvalidArgumentError('Object#move() must take either a tuple/location '
                                           'or two numbers (dx, dy)!');

            if name.lower() == 'dx':
                diff = (value, diff[1]);
            if name.lower() == 'dy':
                diff = (diff[0], value);

        self._location.move(diff[0], diff[1]);
        self.update();

    def moveto(self, *args, **kwargs) -> None:
        """
        Move to a new location; takes a Location, tuple, or two numbers (x, y)
        :return: None
        """

        location = self._location;

        # Basically we don't have an empty tuple at the start.
        if len(args) > 0 and (type(args[0]) is float or type(args[0]) is int or type(args[0]) is Location or
                              type(args[0]) is tuple and not len(args[0]) == 0):
            if len(args) == 1 and type(args[0]) is tuple or type(args[0]) is Location:
                location = Location(args[0][0], args[0][1]);
            elif len(args) == 2 and [type(arg) is float or type(arg) is int for arg in args]:
                location = Location(args[0], args[1]);

        for (name, value) in kwargs.items():
            if len(kwargs) == 0 or type(value) is not int and type(value) is not float:
                raise InvalidArgumentError('Object#move() must take either a tuple/location '
                                           'or two numbers (dx, dy)!');

            if name.lower() == 'x':
                location = Location(value, location.y());
            if name.lower() == 'y':
                location = Location(location.x(), value);

        self._location.moveto(location.x(), location.y());
        self.update();

    def _get_real_location(self):
        real_x = self.x() + self.width() / 2 - (self._screen.width() / 2);
        real_y = -self.y() + self._screen.height() / 2 - self.height() / 2;

        return real_x, real_y;

    def remove(self):
        self._screen.remove(self);

    def update(self) -> None:
        real_x, real_y = self._get_real_location();

        if isinstance(self, Renderable):
            self._ref.goto(real_x, real_y);


class Renderable(Object):
    """
    A base class storing most useful methods for 2D Renderable objects.
    """

    def __init__(self, screen: Screen, x: float = 0, y: float = 0, width: float = 10, height: float = 10,
                 color: Color = Color('black'),
                 border: Color = None,
                 fill: bool = True,
                 rotation: float = 0,
                 visible: bool = True,
                 location: Location = None):
        super(Renderable, self).__init__(screen, x, y, location);

        verify(color, Color, border, Color, fill, bool, rotation, (float, int), visible, bool, location, Location);

        self._width = width;
        self._height = height;

        self._angle = rotation;  # default angle to zero degrees

        self._ref.shape('square');
        self._ref.shapesize(stretch_wid=height / PIXEL_RATIO, stretch_len=width / PIXEL_RATIO);

        self._color = color;
        self._border = border;
        self._ref.color(color.__value__());

        self._fill = fill;
        self._visible = visible;

        if self._visible:
            self._ref.showturtle();
        else:
            self._ref.hideturtle();
        self.update();

    def width(self, width: float = None) -> float:
        """
        Get or set the width of the object.
        :param width: the width to set to in pixels, if any
        :return: the width of the object
        """

        if width is not None:
            verify(width, (float, int));
            self._width = width;
            self.update();

        return self._width;

    def height(self, height: float = None) -> float:
        """
        Get or set the height of the object
        :param height: the height to set to in pixels, if any
        :return: the height of the object
        """

        if height is not None:
            verify(height, (float, int));
            self._height = height;
            self.update();

        return self._height;

    def center(self) -> Location:
        """
        Returns the location of the center
        :return: Location object representing center of Renderable
        """

        return Location(self.x() + self.width() / 2, self.y() + self.height() / 2);

    def color(self, color: Color = None) -> Color:
        """
        Get or set the color of the object
        :param color: the color to set to, if any
        :return: the color of the object
        """

        if color is not None:
            verify(color, Color);
            self._color = color;
            self.update();

        return self._color;

    def rotation(self, angle: float = None) -> float:
        """
        Get or set the rotation of the object.
        :param angle: the angle to set the rotation to in degrees, if any
        :return: the angle of the object's rotation in degrees
        """

        if angle is not None:
            verify(angle, (float, int));
            self._angle = angle;
            self.update();

        return self._angle;

    def rotate(self, angle_diff: float = 0) -> None:
        """
        Rotate the angle of the object by a difference, in degrees
        :param angle_diff: the angle difference to rotate by
        :return: None
        """

        verify(angle_diff, (float, int));
        self.rotation(self._angle + angle_diff);

    def border(self, color: Color = None, fill: bool = None) -> Color:
        """
        Add or get the border of the object
        :param color: the color to set the border too, set to Color.NONE to remove border
        :param fill: whether or not to fill the polygon.
        :return: The Color of the border
        """

        update = False;

        if color is not None:
            verify(color, Color);
            self._border = color;
            update = True;
        if fill is not None:
            verify(fill, bool);
            self._fill = fill;
            update = True;

        if update:
            self.update();

        return self._border;

    def fill(self, fill: bool = None) -> bool:
        """
        Returns or sets the current fill boolean
        :param fill: a new fill value, whether or not to fill the polygon
        :return: the fill value
        """

        if fill is not None:
            verify(fill, bool);
            self._fill = fill;
            self.update();

        return self._fill;

    def distance(self, obj) -> float:
        """
        Returns the distance between two objs or locations in pixels
        :param obj: the Renderable/location to check distance between
        :return: the distance between this obj and the passed Renderable/Location.
        """

        if type(obj) is not Location and not isinstance(obj, Renderable):
            raise InvalidArgumentError(f'.distance() must be passed a Renderable or a Location! '
                                       f'(Passed: {type(obj)}');

        location = obj if type(obj) is Location else obj.center();

        return math.sqrt((location.x() - self.center().x()) ** 2 + (location.y() - self.center().y()) ** 2);

    def visible(self, visible: bool = None) -> bool:
        """
        Get or set the visibility of the renderable.
        :param visible: the new visibility value, if any
        :return: the visibility value
        """

        if visible is not None:
            verify(visible, bool);
            self._visible = visible;
            self.update();

        return self._visible;

    def front(self) -> None:
        """
        Brings the shape to the front of the Screen
        (Imagine moving forward on the Z axis)
        :return: None
        """

        self._screen.front(self);

    def transform(self, transform: tuple = None) -> tuple:
        """
        Get or set the transform of the Renderable.
        Transforms represent the width, height, and rotation of Renderables.

        You can retrieve a Transform from a Renderable with this method and set the transform the same way.
        :param transform: the transform to set to, if any.
        :return: the transform
        """

        if transform is not None:
            verify(transform, tuple);
            if not len(transform) == 3:
                raise InvalidArgumentError('Ensure you are passing in a Transform from another object or a '
                                           'tuple in the following order: (width, height, rotation)');
            verify(transform[0], (float, int), transform[1], (float, int), transform[2], (float, int));
            self.width(transform[0]);
            self.height(transform[1]);
            self.rotation(transform[2]);

        return self.width(), self.height(), self.rotation();

    def clone(self):
        """
        Clone this renderable!
        :return: a Renderable
        """

        constructor = type(self);

        return constructor(self._screen, self.x(), self.y(), self.width(), self.height(), self.color(), self.border(),
                           self.fill(), self.rotation(), self.visible());

    def vertices(self) -> list:
        """
        Returns the list of vertices for the Renderable.
        (The vertices will be returned clockwise, starting from the top-leftmost point)
        :return: a list of Locations representing the vertices
        """

        return self._get_vertices();

    def contains(self, *args) -> bool:
        """
        Returns whether or not a point is contained within the object.
        :param args: You may pass in either two numbers, a Location, or a tuple containing and x and y point.
        :return: a boolean value representing whether or not the point is within the bounds of the object.
        """

        x, y = 0, 0;
        count = 0;

        if len(args) == 1:
            if type(args[0]) is Location:
                x = args[0].x();
                y = args[0].y();
            elif type(args[0]) is tuple and len(args[0]) == 2:
                x = args[0][0];
                y = args[0][1];
        elif len(args) == 2:
            if type(args[0]) is not float and type(args[0]) is not int \
                    and type(args[1]) is not float and type(args[1]) is not int:
                raise InvalidArgumentError('Passed arguments must be numbers (x, y), '
                                           'or you may pass a location/tuple.');
            x = args[0];
            y = args[1];
        else:
            raise InvalidArgumentError('You must pass in a tuple, Location, or two numbers (x, y)!');

        # If the point isn't remotely near us, we don't need to perform any calculations.
        if not isinstance(self, CustomRenderable) and self._angle == 0:
            if not (self.x() <= x <= (self.x() + self.width()) and self.y() <= y <= (self.y() + self.height())):
                return False;

        # the contains algorithm uses the line-intersects algorithm to determine if a point is within a polygon.
        # we are going to cast a ray from our point to the positive x. (left to right)

        shape = self.vertices();
        point1 = shape[0];
        for i in range(1, len(shape)):
            # A cool trick that gets the next index in an array, or the first index if i is the last index.
            # (since we start at index 1)
            point2 = shape[i % len(shape)];

            # make sure we're in the ballpark on the y axis (actually able to intersect on the x axis)
            if y > min(point1.y(), point2.y()):

                # Same thing as above
                if y <= max(point1.y(), point2.y()):

                    # Make sure our x is at least less than the max x of this line. (since we're travelling right)
                    if x <= max(point1.x(), point2.x()):

                        # If our y's are equal, that means this line is flat on the x, which makes us tricked until now.
                        # (We now realize we were never in the ballpark in the first place.
                        if point1.y() != point2.y():

                            # Now we get a possible intersection point from left to right.
                            intersects_x = (y - point1.y()) * (point2.x() - point1.x()) / \
                                           (point2.y() - point1.y()) + point1.x();

                            # if the line was vertical or we actually intersected it
                            if point1.x() == point2.x() or x <= intersects_x:
                                count += 1;

            # move up the ladder; next vertices and edge
            point1 = point2;

        return not (count % 2 == 0);

    def overlaps(self, renderable) -> bool:
        """
        Returns if this object is overlapping with the passed object.
        :param renderable: another Renderable instance.
        :return: true if they are overlapping, false if not.
        """

        if not isinstance(renderable, Renderable):
            raise TypeError('Passed non-renderable into Renderable#overlaps(), which takes only Renderables!');

        min_ax = self.x();
        max_ax = self.x() + self.width();

        min_bx = renderable.x();
        max_bx = renderable.x() + renderable.width();

        min_ay = self.y();
        max_ay = self.y() + self.height();

        min_by = renderable.y();
        max_by = renderable.y() + renderable.height();

        a_left_b = max_ax < min_bx;
        a_right_b = min_ax > max_bx;
        a_above_b = min_ay > max_by;
        a_below_b = max_ay < min_by;

        # Do a base check to make sure they are even remotely near each other.
        if a_left_b or a_right_b or a_above_b or a_below_b:
            return False;

        # Check if one shape is entirely inside the other shape
        if (min_ax >= min_bx and max_ax <= max_bx) and (min_ay >= min_by and max_ay <= max_by):
            return True;

        if (min_bx >= min_ax and max_bx <= max_ax) and (min_by >= min_ay and max_by <= max_ay):
            return True;

        # Next we are going to use a sweeping line algorithm.
        # Essentially we will process the lines on the x axis, one coordinate at a time (imagine a vertical line scan).
        # Then we will look for their orientations. We will essentially make sure its impossible they do not cross.
        shape1 = self.vertices();

        # noinspection PyProtectedMember
        shape2 = renderable.vertices();

        # Orientation method that will determine if it is a triangle (and in what direction [cc or ccw]) or a line.
        def orientation(point1: Location, point2: Location, point3: Location) -> str:
            """
            Internal method that will determine the orientation of three points. They can be a clockwise triangle,
            counterclockwise triangle, or a co-linear line segment.
            :param point1: the first point of the main line segment
            :param point2: the second point of the main line segment
            :param point3: the third point to check from another line segment
            :return: the orientation of the passed points
            """
            result = (point2.y() - point1.y() * (point3.x() - point2.x())) - \
                     ((point2.x() - point1.x()) * (point3.y() - point2.y()));

            if result > 0:
                return 'clockwise';
            elif result < 0:
                return 'counter-clockwise';
            else:
                return 'co-linear';

        def point_on_segment(point1: Location, point2: Location, point3: Location) -> bool:
            """
            Returns if point3 lies on the segment formed by point1 and point2.
            """

            return max(point1.x(), point3.x()) >= point2.x() >= min(point1.x(), point3.x()) \
                   and max(point1.y(), point3.y()) >= point2.y() >= min(point1.y(), point3.y());

        # Okay to begin actually detecting orientations, we want to loop through some edges. But only ones that are
        # relevant. In order to do this we will first have to turn the list of vertices into a list of edges.
        # Then we will look through the lists of edges and find the ones closest to each other.

        shape1_edges = [];
        shape2_edges = [];

        shape1_point1 = shape1[0];
        for i in range(1, len(shape1)):
            shape1_point2 = shape1[i % len(shape1)];
            shape1_edges.append((shape1_point1, shape1_point2));
            shape1_point1 = shape1_point2;

        shape2_point1 = shape2[0];
        for i in range(1, len(shape2)):
            shape2_point2 = shape2[i % len(shape2)];
            shape2_edges.append((shape2_point1, shape2_point2));
            shape2_point1 = shape2_point2;

        # Now we are going to test the four orientations that the segments form
        for edge1 in shape1_edges:
            for edge2 in shape2_edges:
                orientation1 = orientation(edge1[0], edge1[1], edge2[0]);
                orientation2 = orientation(edge1[0], edge1[1], edge2[1]);
                orientation3 = orientation(edge2[0], edge2[1], edge1[0]);
                orientation4 = orientation(edge2[0], edge2[1], edge1[1]);

                # If orientations 1 and 2 are different as well as 3 and 4 then they intersect!
                if orientation1 != orientation2 and orientation3 != orientation4:
                    return True;

                # There's some special cases we should check where a point from one segment is on the other segment
                if orientation1 == 0 and point_on_segment(edge1[0], edge2[0], edge1[1]):
                    return True;

                if orientation2 == 0 and point_on_segment(edge1[0], edge2[1], edge1[1]):
                    return True;

                if orientation3 == 0 and point_on_segment(edge2[0], edge1[0], edge1[1]):
                    return True;

                if orientation4 == 0 and point_on_segment(edge2[0], edge1[1], edge2[1]):
                    return True;

        # If none of the above conditions were ever met we just return False. Hopefully we are correct xD.
        return False;

    # noinspection PyProtectedMember
    # noinspection PyUnresolvedReferences
    def _get_vertices(self):
        shape_data = self._screen._screen._shapes[self._ref.turtle.shapeIndex]._data;

        shape = self._ref._polytrafo(self._ref._getshapepoly(shape_data));

        real_shape = [];

        # Now we loop through and modify the coordinates so that they fit the coordinates of our system.
        # this is an unnecessary calculation but I'm doing it now to ensure that the algorithm is correct.

        min_distance = 999999;
        top_left_index = 0;
        for i, (x2, y2) in enumerate(shape):
            location = Location(x2 + self._screen.width() / 2, -y2 + self._screen.height() / 2);

            distance = math.sqrt((location.x()) ** 2 + (location.y()) ** 2);
            if distance < min_distance:
                min_distance = distance;
                top_left_index = i;

            real_shape.append(location);

        real_shape = real_shape[top_left_index:] + real_shape[:top_left_index];
        real_shape.reverse();

        return real_shape;

    def update(self) -> None:
        """
        Update the internal reference of the object.
        :return: None
        """

        # noinspection PyBroadException
        try:
            super().update();
            self._ref.shapesize(stretch_wid=self.height() / PIXEL_RATIO, stretch_len=self.width() / PIXEL_RATIO);
            self._ref.setheading(self._angle);

            if self._visible:
                self._ref.showturtle();
            elif not self._visible:
                self._ref.hideturtle();

            if self._fill is True:
                if self._border is not None:
                    self._ref.color(self._border.__value__(), self._color.__value__());
                else:
                    self._ref.color(self._color.__value__());
            elif self._border is not None:
                # Fill must be passed as an empty string
                FILL_CONSTANT = '';
                self._ref.color(FILL_CONSTANT);
                self._ref.color(self._border.__value__(), FILL_CONSTANT);
            else:
                raise NameError('Fill was set to false but no border was passed.');

        except:
            pass;  # debug('Termination likely, but an internal error may have occurred');


class Rectangle(Renderable):
    def __init__(self, screen: Screen, x: float = 0, y: float = 0, width: float = 10, height: float = 10,
                 color: Color = Color('black'),
                 border: Color = None,
                 fill: bool = True,
                 rotation: float = 0,
                 visible: bool = True,
                 location: Location = None):
        super(Rectangle, self).__init__(screen, x, y, width, height, color, border, fill, rotation, visible, location);
        self._ref.shape('square');


class Oval(Renderable):
    def __init__(self, screen: Screen, x: float = 0, y: float = 0, width: float = 10, height: float = 10,
                 color: Color = Color('black'),
                 border: Color = None,
                 fill: bool = True,
                 rotation: float = 0,
                 visible: bool = True,
                 location: Location = None):
        self._id = 'circle';
        self._wedges = PIXEL_RATIO;
        super(Oval, self).__init__(screen, x, y, width, height, color, border, fill, rotation, visible, location);
        self._ref.shape('circle');

    def wedges(self, wedges: int) -> int:
        self._update_vertices(self._generate_vertices(PIXEL_RATIO / 2, wedges=wedges));
        self._wedges = wedges;
        self.update();

        return self._wedges;

    @staticmethod
    def _generate_vertices(radius, angle_diff: float = 18, wedges: int = None):
        relative_vertices = []

        if wedges is not None:
            angle_diff = 360 / wedges;

        for x in range(0, 360, int(angle_diff)):
            radians = math.radians(x);
            x = radius * math.cos(radians);
            y = radius * math.sin(radians);
            relative_vertices.append((x, y));

        return relative_vertices;

    def _update_vertices(self, shape_vertices):
        import uuid;
        self._id = str(uuid.uuid4());

        shape = turtle.Shape('polygon', shape_vertices);

        # noinspection PyProtectedMember
        self._screen._screen.register_shape(self._id, shape);
        self._ref.shape(self._id);

    def update(self):
        if self._wedges == PIXEL_RATIO:
            if self.width() > 200 or self.height() > 200:
                radius = ((self.width() + self.height()) / 2) / 2;
                angle = (radius * 9) / 300;
                shape_vertices = self._generate_vertices(PIXEL_RATIO / 2, angle);
                self._update_vertices(shape_vertices);

        super().update();


class Triangle(Renderable):
    def __init__(self, screen: Screen, x: float = 0, y: float = 0, width: float = 10, height: float = 10,
                 color: Color = Color('black'),
                 border: Color = None,
                 fill: bool = True,
                 rotation: float = 0,
                 visible: bool = True,
                 location: Location = None):
        super(Triangle, self).__init__(screen, x, y, width, height, color, border, fill, rotation, visible, location);
        self._ref.shape('triangle');


class Polygon(Renderable):
    def __init__(self, screen: Screen, num_sides: int, x: float = 0, y: float = 0,
                 width: float = 10, height: float = 10,
                 color: Color = Color('black'),
                 border: Color = None,
                 fill: bool = True,
                 rotation: float = 0,
                 visible: bool = True,
                 location: Location = None):
        super(Polygon, self).__init__(screen, x, y, width, height, color, border, fill, rotation, visible, location);

        # We need to generate a list of points relative to the center of the polygon
        # the angle between any two vertices in a regular polygon is 2pi / n (where n is num_sides)

        # The "radius" of an imaginary circle that surrounds the shape. Turtle expects the radius of its pixel modifier.
        radius = PIXEL_RATIO / 2;
        shape_points = [];
        for i in range(num_sides):
            shape_points.append((radius * math.cos(2 * math.pi * i / num_sides),
                                 radius * math.sin(2 * math.pi * i / num_sides)));

        import uuid;
        self._id = uuid.uuid4();

        shape = turtle.Shape('polygon', shape_points);

        # noinspection PyProtectedMember
        self._screen._screen.register_shape(str(self._id), shape);
        self._ref.shape(str(self._id));


class CustomRenderable(Renderable):
    """
    A wrapper class to distintify classes that wrap turtle and those that are built on tkinter.
    """
    pass;


# noinspection PyProtectedMember
class CustomPolygon(CustomRenderable):
    """
    Warning: This class is unfinished and if used improperly can have unintended side effects.
    """

    # The below "# noqa" removes a small inspection by pycharm as it complains we do not call the constructor.
    def __init__(self, screen: Screen, vertices: list,  # noqa
                 color: Color = Color('black'),
                 border: Color = None,
                 fill: bool = True,
                 visible: bool = True,
                 rotation: float = 0):
        self._screen = screen;
        self._color = color;
        self._border = border if border is not None else Color('');
        self._fill = fill;
        self._angle = rotation;
        self._visible = visible;

        if len(vertices) <= 2:
            raise InvalidArgumentError('Must pass at least 3 vertices to CustomPolygon!');

        xmin = vertices[0][0];
        xmax = vertices[0][0];
        ymin = vertices[0][1];
        ymax = vertices[0][1];

        real_vertices = [];
        for vertex in vertices:
            new_vertex = Location(vertex[0], vertex[1]);
            real_vertices.append(new_vertex);

            if new_vertex.x() < xmin:
                xmin = new_vertex.x();
            if new_vertex.x() > xmax:
                xmax = new_vertex.x();

            if new_vertex.y() < ymin:
                ymin = new_vertex.y();
            if new_vertex.y() > ymax:
                ymax = new_vertex.y();

        self._numsides = len(real_vertices);
        self._vertices = real_vertices;
        self._location = Location(xmin, ymin);
        self._width = xmin + (xmax - xmin) / 2;
        self._height = ymin + (ymax - ymin) / 2;

        tk_vertices = [];  # we need to convert to tk's coordinate system.
        for vertex in real_vertices:
            tk_vertices.append((vertex.x() - (self._screen.width() / 2),
                                (vertex.y() - (self._screen.height() / 2))));
            # tk_vertices.append((self.x() - ((self._screen.width() / 2) + 1),
            #                                 (self.y() - (self._screen.height() / 2)) + self.height()));

        state = tk.NORMAL if self._visible else tk.HIDDEN;

        self._ref = self._screen._screen.cv.create_polygon(
            tk_vertices,
            fill=self._screen._colorstr(color),
            outline=self._screen._screen._colorstr(self._border.__value__()),
            state=state
        );

    def width(self, width: float = None) -> float:
        """
        Get the width of the CustomPolygon
        :param width: Unsupported.
        :return: the width of the object
        """

        if width is not None:
            raise UnsupportedError('Modifying the width/height of CustomPolygons is not currently possible');

        return self._width;

    def height(self, height: float = None) -> float:
        """
        Get the height of the Polygon
        :param height: Unsupported.
        :return: the height of the object
        """

        if height is not None:
            raise UnsupportedError('Modifying the width/height of CustomPolygons is not currently possible');

        return self._height;

    def rotate(self, angle_diff: float = 0) -> None:
        verify(angle_diff, (float, int));

        self._angle += angle_diff;
        fake_angle = self._angle - angle_diff;

        if self._angle >= 360:
            self._angle = self._angle - 360;

        self._rotate(self._angle);
        self._rotate(fake_angle);  # TODO: THIS IS A HACK. I HAVE NO CLUE WHY IT WORKS.

    def rotation(self, angle: float = None) -> float:
        if angle is not None:
            verify(angle, (float, int));
            self.rotate(angle - self._angle);

        return self._angle;

    def center(self) -> Location:
        """
        Returns the centroid for the CustomPolygon
        :return: centroid in the form of a Location
        """

        # We gonna create a centroid so we can rotate the points around a realistic center
        # Sorry for those of you that get weird rotations..
        x_list = [];
        y_list = [];
        for vertex in self.vertices():
            x_list.append(vertex.x());
            y_list.append(vertex.y());

        # Create a simple centroid (not full centroid)
        centroid_x = sum(x_list) / len(y_list);
        centroid_y = sum(y_list) / len(x_list);

        return Location(centroid_x, centroid_y);

    def vertices(self) -> list:
        return self._vertices;

    def _rotate(self, angle: float) -> None:
        # We have to update here since we cannot remember previous rotations (update method call won't cut it)!
        vertices = self.vertices();

        # First get some values that we gonna use later
        radians = math.radians(angle);
        cosine = math.cos(radians);
        sine = math.sin(radians);

        # We gonna create a centroid so we can rotate the points around a realistic center
        # Sorry for those of you that get weird rotations..
        x_list = [];
        y_list = [];
        for vertex in vertices:
            x_list.append(vertex.x());
            y_list.append(vertex.y());

        # Create a simple centroid (not full centroid)
        centroid_x = sum(x_list) / len(y_list);
        centroid_y = sum(y_list) / len(x_list);

        new_vertices = []
        for vertex in vertices:
            # We have to create these separately because they're ironically used in each others calculations xD
            old_x = vertex.x() - centroid_x;
            old_y = vertex.y() - centroid_y;

            new_x = old_x * cosine - old_y * sine;
            new_y = old_x * sine + old_y * cosine;
            new_vertices.append(Location(new_x + centroid_x, new_y + centroid_y));

        self._vertices = new_vertices;
        self.update();

    def update(self):
        old_ref = self._ref;

        xmin = self._vertices[0][0];
        xmax = self._vertices[0][0];
        ymin = self._vertices[0][1];
        ymax = self._vertices[0][1];

        for vertex in self._vertices:
            if vertex.x() < xmin:
                xmin = vertex.x();
            if vertex.x() > xmax:
                xmax = vertex.x();

            if vertex.y() < ymin:
                ymin = vertex.y();
            if vertex.y() > ymax:
                ymax = vertex.y();

        self._numsides = len(self._vertices);
        self._location = Location(xmin, ymin);
        self._width = xmin + (xmax - xmin) / 2;
        self._height = ymin + (ymax - ymin) / 2;

        tk_vertices = [];  # we need to convert to tk's coordinate system.
        for vertex in self._vertices:
            tk_vertices.append((vertex.x() - (self._screen.width() / 2),
                                (vertex.y() - (self._screen.height() / 2))));
            # tk_vertices.append((self.x() - ((self._screen.width() / 2) + 1),
            #                                 (self.y() - (self._screen.height() / 2)) + self.height()));

        state = tk.NORMAL if self._visible else tk.HIDDEN;

        self._ref = self._screen._screen.cv.create_polygon(
            tk_vertices,
            fill=self._screen._colorstr(self._color),
            outline=self._screen._screen._colorstr(self._border.__value__()),
            state=state
        );

        self._screen._screen.cv.tag_lower(self._ref, old_ref);
        self._screen._screen.cv.delete(old_ref);


class Image(Renderable):
    """
    Image class. Supports basic formats: PNG, GIF, JPG, PPM, images.

    NOTE: This class supports the basic displaying of images, but also supports much more,
    such as image modification (width, height, color, etc) if you have PIL (Pillow) installed!
    You can install PIL/Pillow by running: `pip install pillow` in a terminal!
    """

    TKINTER_TYPES = ['.png', '.gif', '.ppm'];

    def __init__(self, screen: Screen, image: str, x: float = 0, y: float = 0,
                 width: float = None,
                 height: float = None,
                 color: Color = None,
                 border: Color = None,
                 rotation: float = 0,
                 visible: bool = True,
                 location: Location = None):
        self._image_name = image;

        if image[len(image) - 4:len(image)] in self.TKINTER_TYPES:
            self._image = tk.PhotoImage(name=image, file=image);
        else:
            try:
                from PIL import Image, ImageTk;
                image = Image.open(self._image_name);
                self._image = ImageTk.PhotoImage(image);
            except:
                raise UnsupportedError('As PIL is not installed, only .png, .gif, and .ppm images are supported! '
                                       'Install Pillow via: \'pip install pillow\'.');

        self._width = self._image.width();
        self._height = self._image.height();

        self._mask = 123;

        # We have to monkey patch PIL if we modify the image, but we don't wanna cause a RecursionError (call once)
        self._patched = False;

        shape = turtle.Shape('image', self._image);

        # noinspection PyProtectedMember
        screen._screen.register_shape(self._image_name, shape);

        super().__init__(screen, x, y, self._width, self._height, color=Color(''), border=None,
                         rotation=rotation, visible=visible, location=location);
        self._ref.shape(self._image_name);

        if width is not None:
            self.width(width);
        if height is not None:
            self.height(height);

        if color is not None:
            self.color(color);

        if border is not None:
            self.border(border);

    def width(self, width: float = None) -> float:
        """
        Get or set the width of the image (REQUIRES: PIL or Pillow)
        :param width: the width to set to, if any
        :return: None
        """

        if width is not None:
            verify(width, (float, int));
            self._width = width;
            self.update(True);

        return self._width;

    def height(self, height: float = None) -> float:
        """
        Get or set the height of the image
        :param height: the height to set to, if any
        :return: the height
        """

        if height is not None:
            verify(height, (float, int));
            self._height = height;
            self.update(True);

        return self._height;

    def color(self, color: Color = None, alpha: int = 123) -> Color:
        """
        Retrieves or applies a color-mask to the image
        :param color: the color to mask to, if any
        :param alpha: The alpha level of the mask, defaults to 123 (half of 255)
        :return: the mask-color of the object
        """

        if color is not None:
            verify(color, Color);
            self._color = color;
            self._mask = alpha;
            self.update(True);

        return self._color;

    def rotation(self, angle: float = None) -> float:
        """
        Get or set the rotation of the image.
        :param angle: the angle to set the rotation to in degrees, if any
        :return: the angle of the image's rotation in degrees
        """

        if angle is not None:
            verify(angle, (float, int));
            self._angle = angle;
            self.update(True);

        return self._angle;

    # noinspection PyMethodOverriding
    def rotate(self, angle_diff: float) -> None:
        """
        Rotate the angle of the image by a difference, in degrees
        :param angle_diff: the angle difference to rotate by
        :return: None
        """

        if angle_diff != 0:
            verify(angle_diff, (float, int));
            self._angle += angle_diff;
            self.update(True);

    # noinspection PyMethodOverriding
    def border(self, color: Color = None) -> Color:
        """
        Add or get the border of the image
        :param color: the color to set the border too, set to Color.NONE to remove border
        :return: The Color of the border
        """

        if color is not None:
            verify(color, Color);
            self._border = color;
            self.update(True);

        return self._border;

    def fill(self, fill: bool = None) -> bool:
        """
        Unsupported: This doesn't make sense for images.
        """

        raise UnsupportedError('This method is not supported for Images!');

    def vertices(self) -> list:
        """
        Returns the list of vertices for the Renderable.
        (The vertices will be returned clockwise, starting from the top-leftmost point)
        :return: a list of Locations representing the vertices
        """

        # TODO: Fix this to account for angle

        if self._angle != 0:
            raise UnsupportedError('Calling .overlaps() or .contains() on an image with a rotation'
                                   'is not currently possible with pydraw! This feature should be aded soon,'
                                   'but if you\'d like to voice your support for such a feature, please visit:'
                                   'https://github.com/pydraw/pydraw/issues and submit an issue! :)');

        return [self.location(), Location(self.x() + self.width(), self.y()),
                Location(self.x() + self.width(), self.y() + self.height()),
                Location(self.x(), self.y() + self.height())];

    @staticmethod
    def _monkey_patch_del():
        """
        We monkey patch the del function for PIL so it doesn't do stupid things.
        :return:
        """
        from PIL import ImageTk;

        # monkey patch TKinter from this dumb bug they don't catch in TK.PhotoImage
        old_del = ImageTk.PhotoImage.__del__;

        def new_del(self):
            try:
                old_del(self)
            except (AttributeError, RecursionError):
                pass;  # Yeah, we don't care.
            pass;

        ImageTk.PhotoImage.__del__ = new_del

    def update(self, updated: bool = False):
        if updated:
            try:
                from PIL import Image, ImageTk, ImageOps;

                if not self._patched:
                    self._monkey_patch_del();  # If we do have PIL we need to monkey patch this immediately.
                    self._patched = True;

                image = Image.open(self._image_name);

                if self._color is not None:
                    color_layer = Image.new('RGB', image.size,
                                            (self._color.red(), self._color.green(), self._color.blue()));
                    mask = Image.new('RGBA', image.size, (0, 0, 0, self._mask));
                    image = Image.composite(image, color_layer, mask).convert('RGB');

                if self._border is not None:
                    image = ImageOps.expand(image, border=10, fill=self._border.rgb())

                # Do resizing last so we can make sure the other manipulations work properly
                image = image.resize((self.width(), self.height()), Image.ANTIALIAS);

                if self._angle != 0:
                    image = image.rotate(self._angle, resample=Image.BICUBIC, expand=True);

                self._image = ImageTk.PhotoImage(image=image);
            except (RuntimeError, AttributeError):
                pass;  # We are catching some stupid errors from Tkinter involving images and program exiting.
            except:
                raise UnsupportedError('As PIL is not installed, you cannot modify images! '
                                       'Install Pillow via: \'pip install pillow\'.');

        try:
            shape = turtle.Shape('image', self._image);

            # noinspection PyProtectedMember
            self._screen._screen.register_shape(self._image_name, shape);
            self._ref.shape(self._image_name);
        except tk.TclError:
            pass;
        super().update();


# == NON RENDERABLES == #


class Text(Object):
    _anchor = 'nw';  # sw technically means southwest but it means bottom left anchor. (we change to top left in code)
    _aligns = {'left': tk.LEFT, 'center': tk.CENTER, 'right': tk.RIGHT};

    # noinspection PyProtectedMember
    def __init__(self, screen: Screen, text: str, x: float, y: float, color: Color = Color('black'),
                 font: str = 'Arial', size: int = 16, align: str = 'left', bold: bool = False, italic: bool = False,
                 underline: bool = False, strikethrough: bool = False, rotation: float = 0, visible: bool = True):
        super(Text, self).__init__(screen, x, y);
        self._text = text if text is not None else '';
        self._color = color;
        self._font = font;
        self._size = size;
        self._align = align;
        self._bold = bold;
        self._italic = italic;
        self._underline = underline;
        self._strikethrough = strikethrough;
        self._angle = rotation;
        self._visible = visible;

        verify(screen, Screen, text, str, x, (float, int), y, (float, int), color, Color, font, str, size, int,
               align, str, bold, bool, italic, bool, underline, bool, strikethrough, bool, rotation, (float, int),
               visible, bool);

        # Handle font and decorations
        decorations = '';
        if self.bold():
            decorations += 'bold ';
        if self.italic():
            decorations += 'italic ';
        if self.underline():
            decorations += 'underline ';
        if self.strikethrough():
            decorations += 'overstrike ';

        # we use negative font size to change from point font-size to pixel font-size.
        font_data = (self.font(), -self.size(), decorations);

        state = tk.NORMAL if self._visible else tk.HIDDEN;

        self._ref = self._screen._screen.cv.create_text(self.x() - ((self._screen.width() / 2) + 1),
                                                        (self.y() - (self._screen.height() / 2)),
                                                        text=self.text(),
                                                        anchor=Text._anchor,
                                                        justify=Text._aligns[self.align()],
                                                        fill=self._screen._screen._colorstr(self.color().__value__()),
                                                        font=font_data,
                                                        state=state,
                                                        angle=self._angle);

        x0, y0, x1, y1 = screen._screen.cv.bbox(self._ref);
        self._width = x1 - x0;
        self._height = y1 - y0;

        screen._screen.cv.update();

    def text(self, text: str = None) -> str:
        """
        Get or set the text. Use '\n' to separate lines.
        :param text: text to set to (str), if any
        :return: the text
        """

        if text is not None:
            verify(text, str);
            self._text = text;
            self.update();

        return self._text;

    def width(self) -> float:
        """
        Get the width of the text (cannot be modified)
        :return the width of the text
        """

        return self._width;

    def height(self) -> float:
        """
        Get the height of the text, (cannot be modified, although technically the font-size is the text's height)
        :return: the height of the text.
        """

        return self._height;

    def color(self, color: Color = None) -> Color:
        """
        Get or set the color of the text
        :param color: the color to set to, if any
        :return: the color of the text
        """

        if color is not None:
            verify(color, Color);
            self._color = color;
            self.update();

        return self._color;

    def font(self, font: str = None) -> str:
        """
        Get or set the font of the text
        :param font: the font to set to, if any
        :return: the font of the text
        """

        if font is not None:
            verify(font, str);
            self._font = font;
            self.update();

        return self._font;

    def size(self, size: int = None) -> int:
        """
        Get or set the size of the text
        :param size: the size to set to, if any
        :return: the size of the text
        """

        if size is not None:
            verify(size, int);
            self._size = size;
            self.update();

        return self._size;

    def align(self, align: str = None) -> str:
        """
        Get or set the alignment of the text, if a new value is passed it must be 'left', 'center', or 'right'.
        :param align: the alignment to set to, if any
        :return: the alignment of the text
        """

        if align is not None:
            verify(align, str);
            self._align = align.lower();
            self.update();

        return self._align;

    def bold(self, bold: bool = None) -> bool:
        """
        Get or set the bold status of the text
        :param bold: the bold status to set to, if any
        :return: the bold status of the text
        """

        if bold is not None:
            verify(bold, bool);
            self._bold = bold;
            self.update();

        return self._bold;

    def italic(self, italic: bool = None) -> bool:
        """
        Get or set the italic status of the text
        :param italic: the italic status to set to, if any
        :return: the italic status of the text
        """

        if italic is not None:
            verify(italic, bool);
            self._italic = italic;
            self.update();

        return self._italic;

    def underline(self, underline: bool = None) -> bool:
        """
        Get or set the underline status of the text
        :param underline: the underline status to set to, if any
        :return: the underline status of the text
        """

        if underline is not None:
            verify(underline, bool);
            self._underline = underline;
            self.update();

        return self._underline;

    def strikethrough(self, strikethrough: bool = None) -> bool:
        """
        Get or set the strikethrough status of the text
        :param strikethrough: the strikethrough status to set to, if any
        :return: the strikethrough status of the text
        """

        if strikethrough is not None:
            verify(strikethrough, bool);
            self._strikethrough = strikethrough;
            self.update();

        return self._strikethrough;

    def rotation(self, rotation: float = None) -> float:
        """
        Get or set the rotation of the text
        :param rotation: the strikethrough to set to, if any
        :return: the rotation of the text
        """

        if rotation is not None:
            verify(rotation, (float, int));
            self._angle = rotation;
            self.update();

        return self._angle;

    def rotate(self, angle_diff: float = 0) -> None:
        """
        Rotate the angle of the text by a difference, in degrees
        :param angle_diff: the angle difference to rotate by
        :return: None
        """

        verify(angle_diff, (float, int));
        self.rotation(self._angle + angle_diff);

    def visible(self, visible: bool = None) -> bool:
        """
        Get or set the visibility of the text
        :param visible: the visibility to set to, if any
        :return: the visibility of the text
        """

        if visible is not None:
            verify(visible, bool);
            self._visible = visible;
            self.update();

        return self._visible;

    # noinspection PyProtectedMember
    def update(self) -> None:
        # super().update(); | JUST FOR RENDERABLES - DO NOT USE
        # we are going to delete and re-add text to the screen. You cannot alter a text object.
        old_ref = self._ref;

        # Handle font and decorations
        decorations = '';
        if self.bold():
            decorations += 'bold ';
        if self.italic():
            decorations += 'italic ';
        if self.underline():
            decorations += 'underline ';
        if self.strikethrough():
            decorations += 'overstrike ';

        # we use negative font size to change from point font-size to pixel font-size.
        font_data = (self.font(), -self.size(), decorations);

        state = tk.NORMAL if self._visible else tk.HIDDEN;

        self._ref = self._screen._screen.cv.create_text(self.x() - ((self._screen.width() / 2) + 1),
                                                        (self.y() - (self._screen.height() / 2)),
                                                        text=self.text(),
                                                        anchor=Text._anchor,
                                                        justify=Text._aligns[self.align()],
                                                        fill=self._screen._colorstr(self._color),
                                                        font=font_data,
                                                        state=state,
                                                        angle=self._angle);
        self._screen._screen.cv.tag_lower(self._ref, old_ref);
        self._screen._screen.cv.delete(old_ref);

        if self._visible:
            x0, y0, x1, y1 = self._screen._screen.cv.bbox(self._ref);
            self._width = x1 - x0;
            self._height = y1 - y0;

        self._screen._screen.cv.update();


class Line(Object):
    def __init__(self, screen: Screen, *args, color: Color = Color('black'), thickness: int = 1, dashes=None,
                 visible: bool = True):
        super().__init__(screen);
        self._screen = screen;

        if len(args) == 2 and (type(arg) is tuple or type(arg) is Location for arg in args):
            self._pos1 = Location(args[0][0], args[0][1]);
            self._pos2 = Location(args[1][0], args[1][1]);
        elif len(args) == 4 and (type(arg) is float or type(arg) is int for arg in args):
            self._pos1 = Location(args[0], args[1]);
            self._pos2 = Location(args[2], args[3]);
        else:
            raise TypeError('Incorrect Argumentation: Line requires either two Locations, tuples, or four '
                            'numbers (x1, y1, x2, y2).');

        self._color = color;
        self._thickness = thickness;
        self._dashes = dashes;
        self._visible = visible;

        verify(color, Color, thickness, int, dashes, bool, visible, bool);

        state = tk.NORMAL if self._visible else tk.HIDDEN;

        if dashes is not None and type(dashes) is not tuple:
            self._dashes = (dashes, dashes)

        # noinspection PyProtectedMember
        self._ref = self._screen._screen.cv.create_line(self._pos1.x() - screen.width() / 2,
                                                        self._pos1.y() - screen.height() / 2,
                                                        self._pos2.x() - screen.width() / 2,
                                                        self._pos2.y() - screen.height() / 2,
                                                        fill=self._screen._screen._colorstr(self._color.__value__()),
                                                        width=self._thickness, dash=self._dashes, state=state);

    def pos1(self, *args) -> Location:
        """
        Get or set the position of the first endpoint.
        :param args: Either a location or two numbers (x, y) may be passed here.
        :return: the position of the first endpoint.
        """

        if len(args) != 0:
            if len(args) == 1 and type(args[0]) is Location or type(args[0]) is tuple:
                self._pos1 = Location(args[0][0], args[0][1]);
            elif len(args) == 2 and [(type(arg) is float or type(arg) is int for arg in args)]:
                self._pos1 = Location(args[0], args[1]);
            else:
                raise TypeError('Incorrect Argumentation: Requires either a location, tuple, or two numbers.');

        self.update();
        return self._pos1;

    def pos2(self, *args) -> Location:
        """
        Get or set the position of the second endpoint.
        :param args: Either a location or two numbers (x, y) may be passed here.
        :return: the position of the second endpoint.
        """

        if len(args) != 0:
            if len(args) == 1 and type(args[0]) is Location or type(args[0]) is tuple:
                self._pos2 = Location(args[0][0], args[0][1]);
                self.update();
            elif len(args) == 2 and (type(arg) is float or type(arg) is int for arg in args):
                self._pos2 = Location(args[0], args[1]);
                self.update();
            else:
                raise TypeError('Incorrect Argumentation: Requires either a location, tuple, or two numbers.');

        self.update();
        return self._pos2;

    def move(self, dx: float, dy: float, point: int = 0) -> None:
        """
        Move both endpoints by the same dx and dy
        :param dx: the distance x to move
        :param dy: the distance y to move
        :param point: affect only one of the endpoints; options: (1, 2), default=0
        :return: None
        """

        if point != 0:
            if point == 1:
                self._pos1.move(dx, dy);
            elif point == 2:
                self._pos2.move(dx, dy);
            else:
                raise IndexError('Attempted to change point other than 1 or 2.');
        else:
            self._pos1.move(dx, dy);
            self._pos2.move(dx, dy);

        self.update();

    def moveto(self, *args) -> None:
        """
        Move both of the endpoints to new locations.
        :param args: Either two locations, tuples, or four numbers (x1, y1, x2, y2).
        :return: None
        """

        if len(args) == 2 and (type(arg) is tuple or type(arg) is Location for arg in args):
            self._pos1.moveto(args[0][0], args[0][1]);
            self._pos2.moveto(args[1][0], args[1][1]);
        elif len(args) == 4 and (type(arg) is int or type(arg) is float for arg in args):
            self._pos1.moveto(args[0], args[1]);
            self._pos2.moveto(args[2], args[3]);
        else:
            raise TypeError('Incorrect Argumentation: Requires either two locations, tuples, or four numbers (x1, y1, '
                            'x2, y2)');

        self.update();

    # noinspection PyUnusedLocal
    # TODO: Allow for point specification.
    def lookat(self, *args, **kwargs) -> None:
        """
        Make the line look at the given point by moving the second point.
        :return: None
        """

        point = 2;

        if len(args) >= 1 and (type(args[0]) is tuple or type(args[0]) is Location):
            location = Location(args[0][0], args[0][1]);

            if len(args) > 1 and type(args[1]) is int:
                point = args[1];
        elif len(args) >= 2 and (type(arg) is float or type(arg) is int for arg in args[:2]):
            location = Location(args[0], args[1]);

            if len(args) > 2 and type(args[2]) is int:
                point = args[2];
        else:
            raise InvalidArgumentError('You must pass either two numbers (x, y), or a tuple/Location!');

        if 'point' in kwargs:
            if type(kwargs['point']) is not int:
                raise InvalidArgumentError('Point must be an int.');

            point = kwargs['point'];

        # so now we have a location but we need to shorten it to be the same length of our line right now.
        # slope = (self.pos2().y() - self.pos1().y()) / (self.pos2.x() - self.pos1.x());
        length = self.length();

        ray_length = self._length(self.pos1().x(), location.x(), self.pos1().y(), location.y());

        # hypotenuse = (ray_length - length);  # extraneous length (we need to cut this)

        theta = math.atan2(self.pos1().y() - location.y(), self.pos1().x() - location.x()) \
                - math.atan2(self.pos1().y() - self.pos2().y(), self.pos1().x() - self.pos2().x());

        cosine = math.cos(theta);
        sine = math.sin(theta);

        old_x = self.pos2().x() - self.pos1().x();
        old_y = self.pos2().y() - self.pos1().y();

        new_x = old_x * cosine - old_y * sine;
        new_y = old_x * sine + old_y * cosine;

        new_x += self.pos1().x();
        new_y += self.pos1().y();

        # if point == 1:
        #     self.pos1(location);
        # elif point == 2:
        #     self.pos2(location);
        # else:
        #     raise InvalidArgumentError('Point passed in for change was not a number!');

        self.pos2().moveto(new_x, new_y);
        self.update();

    def location(self) -> tuple:
        """
        Returns the locations of both the endpoints
        :return: the locations of both the endpoints
        """

        return self._pos1, self._pos2;

    def length(self) -> float:
        """
        Get the length of the line
        :return: the length of the line
        """
        return self._length(self.pos1().x(), self.pos2().x(), self.pos1().y(), self.pos2().y());

    @staticmethod
    def _length(x1: float, x2: float, y1: float, y2: float) -> float:
        return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2);

    def color(self, color: Color = None) -> Color:
        """
        Get or set the color of the line
        :param color: the color to set to, if any
        :return: the color of the line
        """

        if color is not None:
            verify(color, Color);
            self._color = color;
            self.update();

        return self._color;

    def thickness(self, thickness: int = None) -> int:
        """
        Get or set the thickness of the line
        :param thickness: the thickness to set to, if any
        :return: the thickness of the line
        """

        if thickness is not None:
            verify(thickness, int);
            self._thickness = thickness;
            self.update();

        return self._thickness;

    def dashes(self, dashes: bool = None) -> bool:
        """
        Retrive or enable/disable the dashes for the line
        :param dashes: the visibility to set to, if any
        :return: the toggle-state of dashes
        """

        if dashes is not None:
            verify(dashes, bool);
            self._dashes = dashes;
            self.update();

        return self._dashes;

    def visible(self, visible: bool = None) -> bool:
        """
        Get or set the visibility of the line
        :param visible: the visibility to set to, if any
        :return: the visibility of the line
        """

        if visible is not None:
            verify(visible, bool);
            self._visible = visible;
            self.update();

        return self._visible;

    # noinspection PyProtectedMember
    def update(self):
        try:
            old_ref = self._ref;

            if self._dashes is not None and type(self._dashes) is not tuple:
                self._dashes = (self._dashes, self._dashes)

            state = tk.NORMAL if self._visible else tk.HIDDEN;
            self._ref = self._screen._screen.cv.create_line(self._pos1.x() - self._screen.width() / 2,
                                                            self._pos1.y() - self._screen.height() / 2,
                                                            self._pos2.x() - self._screen.width() / 2,
                                                            self._pos2.y() - self._screen.height() / 2,
                                                            fill=self._screen._colorstr(self.color()),
                                                            width=self._thickness, dash=self._dashes, state=state);

            self._screen._screen.cv.tag_lower(self._ref, old_ref);
            self._screen._screen.cv.delete(old_ref);

            self._screen._screen.cv.update();
        except tk.TclError:
            pass;  # Just catch TclErrors and throw them out.

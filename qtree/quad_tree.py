"""
Implementation of QuadTree data structure
"""
import numpy as np
import matplotlib.patches as mpatches

class Point:
    def __init__(self, x, y, name=""):
        """
        Point
        x (float): x coordinate of point
        y (float): y coordinate of point
        """
        self.x = x
        self.y = y
        self.name = name # Used for classifying points uniquely
        return


class Rectangle:
    def __init__(self, x, y, w, h):
        """
        Rectangle. Used for defining bounding region of QuadTree
        x (float): x coordinate of center of rectangle
        y (float): y coordinate of center of rectangle
        w (float): half-width of rectangle
        h (float): half-height of rectangle
        """
        self.x = x
        self.y = y
        # (x,y) define the center of the rectangle in Cartesian coordinates
        self.w = w
        self.h = h
        return

    def ContainsPoint(self, pt) -> bool:
        """
        Test if bounding region contains Point pt
        point (Point): Point being tested
        Returns a bool. True if point is within region, False otherwise
        """
        return self.x - self.w < pt.x < self.x + self.w and self.y - self.h < pt.y < self.y + self.h

    def IntersectsRegion(self, region) -> bool:
        """
        Test if the rectangle intersects a given region
        :param region: (Rectangle) Region to test
        :return: Bool
        """
        return not (
            region.x - region.w > self.x + self.w or
            region.x + region.w < self.x - self.w or
            region.y - region.h > self.y + self.h or
            region.y + region.h < self.y - self.h
        )

    def DrawOutline(self, ax) -> None:
        """
        Draw edges of QuadTree for visualization
        ax (plt.subplots()): axis to draw onto
        """
        # Rectangle will act as edge of QuadTree
        edge = mpatches.Rectangle(
            (self.x - self.w, self.y - self.h), self.w*2, self.h*2, lw=1, fill=False, ec="#0CFF00"
        )
        ax.add_patch(edge)
        return


class QuadTree:
    def __init__(self, boundary, capacity=4):
        """
        QuadTree data structure
        boundary (Rectangle): Bounding region of the QuadTree
        capacity (int): Maximum capacity of QuadTree. Default is 4
        """
        self.boundary = boundary # boundary of region
        self.capacity = capacity # Max number of points allowed in region
        self.points = [] # Points within this region
        self.divided = False # Whether or not this QuadTree is divided already
        return

    def _subdivide(self) -> None:
        """
        Subdivide the quad tree
        """
        # some local variables
        x = self.boundary.x
        y = self.boundary.y
        w = self.boundary.w
        h = self.boundary.h

        # Define northeast region of QuadTree
        ne = Rectangle(x + w/2, y + h/2, w/2, h/2)
        self.northeast = QuadTree(ne, self.capacity)
        # Define northwest region of QuadTree
        nw = Rectangle(x - w/2, y + h/2, w/2, h/2)
        self.northwest = QuadTree(nw, self.capacity)
        # Define southeast region of QuadTree
        se = Rectangle(x + w/2, y - h/2, w/2, h/2)
        self.southeast = QuadTree(se, self.capacity)
        # Define southwest region of QuadTree
        sw = Rectangle(x - w/2, y - h/2, w/2, h/2)
        self.southwest = QuadTree(sw, self.capacity)
        # Set bool to true
        self.divided = True
        return

    def InsertPoint(self, point) -> None:
        """
        Insert point into the QuadTree
        If the QuadTree is already at maximum capacity, subdivide the QuadTree
        point (Point): Point being inserted into QuadTree
        """
        # Check if point is within bounding region
        if not self.boundary.ContainsPoint(point):
            return
        else:
            if len(self.points) < self.capacity:
                self.points.append(point)
            else:
                if not self.divided:
                    self._subdivide()
                #
                self.northeast.InsertPoint(point)
                self.northwest.InsertPoint(point)
                self.southeast.InsertPoint(point)
                self.southwest.InsertPoint(point)
            return

    def DrawOutline(self, ax) -> None:
        """
        Draw edges of QuadTree for visualization
        ax (plt.subplots()): axis to draw onto
        """
        # Rectangle will act as edge of QuadTree
        qt_edge = mpatches.Rectangle(
            (self.boundary.x - self.boundary.w, self.boundary.y - self.boundary.h),
            self.boundary.w*2,
            self.boundary.h*2,
            lw=0.2, fill=False, ec="w"
        )
        ax.add_patch(qt_edge)

        # If the QuadTree has divided, draw the edges of the daughter nodes also
        if self.divided:
            self.northeast.DrawOutline(ax)
            self.northwest.DrawOutline(ax)
            self.southeast.DrawOutline(ax)
            self.southwest.DrawOutline(ax)
        return

    def QueryRegion(self, region, found=[]) -> list:
        """
        Find points within a given region
        :param found: (array) List of points found within specified region
        :param region: (Rectangle) Region to query points
        :return:
        """
        # Determine if any points are found in region already
        if not found:
            found = []

        # Determine if region and QuadTree overlap
        if not self.boundary.IntersectsRegion(region):
            return found
        else:
            # Iterate through all points within QuadTree and determine if they are also within region of intersection
            for p in self.points:
                if region.ContainsPoint(p):
                    found.append(p)
            # If the region has subdivided, determine which points are within the regions spawned from this node
            if self.divided:
                self.northeast.QueryRegion(region, found)
                self.northwest.QueryRegion(region, found)
                self.southeast.QueryRegion(region, found)
                self.southwest.QueryRegion(region, found)
            return found


if __name__ == "__main__":
    # Define points in space and QuadTree
    x_axis = np.linspace(0, 10, 100)
    y_axis = np.linspace(0, 10, 100)
    rect = Rectangle(x=0, y=0, w=10, h=10)
    qt = QuadTree(boundary=rect, capacity=4)

    # Inserting points into the QuadTree
    for x, y in zip(x_axis, y_axis):
        qt.InsertPoint(Point(x, y))





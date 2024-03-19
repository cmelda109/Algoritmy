from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
import shapefile

class Draw(QWidget):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # query point and polygon
        self.__q = QPointF(-100, -100)
        self.__pol = QPolygonF()

        self.__polygons = []  # Initialize an empty list to store polygons

        self.__add_vertex = False
        # Indices of polygons to highlight or blink
        self.highlighted_polygon_indices = []  # Initialize as an empty list


    def loadData(self):
        # Get path to file via Dialog window
        filename, _ = QFileDialog.getOpenFileName(self, "Open file", "", "Shapefile (*.shp)")

        # Update no data property and return if dialog window is closed
        if not filename:
            self.__no_data = True
            return
        self.__no_data = False

        # Load objects from the shapefile
        shp = shapefile.Reader(filename)
        self.__features = shp.shapes()

        # Find minimum and maximum coordinates
        x_min, y_min, x_max, y_max = float('inf'), float('inf'), float('-inf'), float('-inf')
        for feature in self.__features:
            for x, y in feature.points:
                x_min = min(x_min, x)
                y_min = min(y_min, y)
                x_max = max(x_max, x)
                y_max = max(y_max, y)
        self.__min_max = [x_min, y_min, x_max, y_max]

    def rescaleData(self, width, height):
        # Construct hidden polygon if no data
        if self.__no_data:
            self.__polygons = [QPolygonF([QPointF(0, 0), QPointF(-10, 0), QPointF(0, -10), QPointF(-10, -10)])]
            return

        # Rescale data and create polygons
        self.__polygons = []
        for feature in self.__features:
            polygon = QPolygonF()
            for x, y in feature.points:
                x_rescaled = int(((x - self.__min_max[0]) / (self.__min_max[2] - self.__min_max[0]) * width))
                y_rescaled = int((height - (y - self.__min_max[1]) / (self.__min_max[3] - self.__min_max[1]) * height))
                polygon.append(QPointF(x_rescaled, y_rescaled))
            self.__polygons.append(polygon)

            
    def mousePressEvent(self, e:QMouseEvent):
        # left mouse button click
        x = e.position().x()
        y = e.position().y()

        # add point to polygon
        if self.__add_vertex:
            # create point
            p = QPointF(x,y)

            # append p to polygon
            self.__pol.append(p)

        # set x,y to point
        else:
            self.__q.setX(x)
            self.__q.setY(y)

        # repaint screen
        self.repaint()
        
    def paintEvent(self, e: QPaintEvent):
        # Create QPainter object
        qp = QPainter(self)
        qp.begin(self)

        # Draw polygons
        for index, polygon in enumerate(self.__polygons):
            if index in self.highlighted_polygon_indices:
                # Change color or make the polygon blink
                qp.setPen(Qt.GlobalColor.red)  # Example color, replace with desired color
                qp.setBrush(Qt.GlobalColor.yellow)  # Example color, replace with desired color
            else:
                # Default color for other polygons
                qp.setPen(Qt.GlobalColor.black)  # Default color
                qp.setBrush(Qt.GlobalColor.white)  # Default color
            
            # Draw polygon
            qp.drawPolygon(polygon)

        # Draw point
        d = 3
        qp.setPen(Qt.GlobalColor.black)  # Color for point
        qp.setBrush(Qt.GlobalColor.black)  # Color for point
        qp.drawEllipse(int(self.__q.x() - d/2), int(self.__q.y() - d/2), d, d)

        # End drawing
        qp.end()



    def setHighlightedPolygons(self, indices):
        self.highlighted_polygon_indices = indices
        self.repaint()



    def getPolygons(self):
        """
        Returns the list of polygons drawn on the canvas.
        """
        return self.__polygons

    def getQ(self):
        #Return analyzed point
        return self.__q
    
    def getPol(self):
        #Return analyzed polygon
        return self.__pol
    
    def clearPol(self):
        #Clear polygon
        self.__polygons = []
        
        #Shift point
        self.__q.setX(-100)
        self.__q.setY(-100)
        
        #Repaint screen
        self.repaint()

from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
import shapefile

class Draw(QWidget):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)        
        self.__q = QPointF(-100, -100)
        self.__pol = QPolygonF()
        
        #Initialize an empty list to store polygons
        self.__polygons = []  

        self.__add_vertex = False
        
        #Indices of polygons to highlight 
        self.highlighted_polygon_indices = []  

    def loadDataAndRescalePolygons(self, width, height):
        #Load data from shapefile
        filename, _ = QFileDialog.getOpenFileName(self, "Open file", "", "Shapefile (*.shp)")            
        shp = shapefile.Reader(filename)
        features = shp.shapes()

        #Extract points
        points = [point for feature in features for point in feature.points]
        if points:
            x_coords, y_coords = zip(*points)
            min_x, min_y, max_x, max_y = min(x_coords), min(y_coords), max(x_coords), max(y_coords)
        else:
            min_x, min_y, max_x, max_y = [float('inf')] * 4

        #Rescale data
        polygons = []
        for feature in features:
            polygon = QPolygonF()
            for x, y in feature.points:
                x_rescaled = int(((x - min_x) / (max_x - min_x)) * width)
                y_rescaled = int((1 - (y - min_y) / (max_y - min_y)) * height)
                polygon.append(QPointF(x_rescaled, y_rescaled))
            polygons.append(polygon)
        
        self.__polygons = polygons
            
    def mousePressEvent(self, e:QMouseEvent):
        #Left mouse button click
        x = e.position().x()
        y = e.position().y()

        #Add point to polygon
        if self.__add_vertex:
            # create point
            p = QPointF(x,y)

            #Append p to polygon
            self.__pol.append(p)

        #Set x,y to point
        else:
            self.__q.setX(x)
            self.__q.setY(y)

        #Repaint screen
        self.repaint()
        
    def paintEvent(self, e: QPaintEvent):
        #Create QPainter object
        qp = QPainter(self)
        qp.begin(self)

        #Draw polygons
        for index in range(len(self.__polygons)):
            polygon = self.__polygons[index]
            if index in self.highlighted_polygon_indices:
                #Change color 
                qp.setPen(Qt.GlobalColor.black)  
                qp.setBrush(Qt.GlobalColor.cyan) 
            else:
                #Default color for other polygons
                qp.setPen(Qt.GlobalColor.black)  
                qp.setBrush(Qt.GlobalColor.white)  
            
            #Draw polygon
            qp.drawPolygon(polygon)

        #Draw point
        d = 8
        qp.setPen(Qt.GlobalColor.red)  
        qp.setBrush(Qt.GlobalColor.red)  
        qp.drawEllipse(int(self.__q.x() - d/2), int(self.__q.y() - d/2), d, d)

        #End drawing
        qp.end()

    def setHighlightedPolygons(self, indices):
        #Set highlighted polygon indices
        self.highlighted_polygon_indices = indices
        self.repaint()
                
    def getPolygons(self): 
        #Returns the list of polygons drawn on the canvas       
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

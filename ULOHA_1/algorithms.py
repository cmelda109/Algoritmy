from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from math import pi,acos,sqrt


#Processing data
class Algorithms:
    
    def __init__(self):
        pass
     
    #Ray Crossing   
    def rayCrossing(self, q:QPointF, pol:QPolygonF):         
        #Inicialize amount of left and right intersections
        kl = 0
        kr = 0
        
        #Amount of vertices
        n = len(pol)                  
        
        #Process all segments
        for i in range(n):
            #Reduce coordinates
            xir = pol[i].x() - q.x()
            yir = pol[i].y() - q.y()
            
            xi1r = pol[(i+1)%n].x() - q.x()
            yi1r = pol[(i+1)%n].y() - q.y()
            
            #Point q has same coordinates as a vertex?
            if (xir, yir) == (0, 0):
                return -1
            
            #Check for horizontal edge
            if yi1r == yir:
                continue
                     
            #Compute intersection
            xm = (xi1r * yir - xir * yi1r) / (yi1r - yir)            

            #Right half-plane
            if (yi1r > 0) != (yir > 0) and xm > 0:
                kr += 1
            
            #Left half-plane
            if (yi1r < 0) != (yir < 0) and xm < 0:
                kl += 1
                     
        #Point q inside polygon
        if kr%2 == 1:
            return 1
        
        #Point q on the edge
        if (kl + kr) % 2 != 0:
            return -1
        
        #Point q outside polygon
        return 0
    
    #Winding Number
    def windingNumber(self, q:QPointF, pol:QPointF):
        #Initialize total angle and tolerance
        total_angle = 0
        eps = 1.0e-10

        #Amount of vertices
        n = len(pol)
        
        #Process all segments
        for i in range(n-1):
            
            #Coordinates of point q are same as a vertex?
            if pol[i] == q:                
                return -1

            #Get the determinant
            det = self.computeDeterminant(q, pol[i], pol[i+1])

            #Get the angle
            angle = self.computeAngle(q, pol[i], pol[i+1])

            #Point q in the left halfplane
            if det > 0:
                total_angle += angle

            #Point q in the right half-plane
            if det < 0:
                total_angle -= angle

            #Point q on the edge           
            if det == 0 and angle > pi - eps:
                return -1

        #Point q inside
        if abs(abs(total_angle) - 2*pi) < eps:
            return 1

        #Point q outside
        return 0
    
    #Auxiliary function that calculates determinant for WN algorithm
    def computeDeterminant(self, q, p1: QPointF, p2: QPointF):        
        #Compute determinant
        det = (q.x() - p1.x()) * (p2.y() - p1.y()) - (p2.x() - p1.x()) * (q.y() - p1.y())

        #Return the determinant
        return det

    #Auxiliary function that calculates angle for WN algorithm
    def computeAngle(self, q, p1: QPointF, p2: QPointF):       
        #Compute vectors and dot product
        scalar = (p1.x() - q.x()) * (p2.x() - q.x()) + (p1.y() - q.y()) * (p2.y() - q.y())
        
        #Compute magnitudes
        length = sqrt((p1.x() - q.x())**2 + (p1.y() - q.y())**2) * sqrt((p2.x() - q.x())**2 + (p2.y() - q.y())**2)
        
        #Avoid division by zero
        if length == 0:
            return 0
        
        #Compute the angle and return its absolute value
        return abs(acos(max(-1, min(1, scalar / length))))


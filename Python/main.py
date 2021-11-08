__author__ = “henan”
__version__ = “2018.12.17”


import rhinoscriptsyntax as rs
import math 
import random as rnd

class cell(object):
    def __init__(self, ID, POS, STATE, ZMAX, A, B):
        self.A = A
        self.B = B
        self.list = []
        self.ID = ID
        self.pos = POS
        self.state = STATE
        self.zmax = ZMAX
        self.list.append(self.state)
        
    def live(self,point01, point02, point03,point04,point05,point06,
        point07,point08,k,surface):
        allState = point01.list[k]+point02.list[k]+point03.
        list[k]+point03.list[k]+point04.    
        list[k]+point05.list[k]+point06.list[k]+point07.
        list[k]+point08.list[k]+self.list[k]
        self.C = k

        vector = surface.UVmove(self)
        if self.list[k] ==1:
            if allState >= 4:
                newState = 0
            elif allState <= 1:
                newState = 0
            else:
                newState = 1
                pt = rs.AddPoint(self.pos)
                newPt = rs.MoveObject(pt, vector)
        else:
            if allState == 3:
                newState = 1
                pt = rs.AddPoint(self.pos)
                newPt = rs.MoveObject(pt, vector)                
            else:
                newState = 0
               
        self.state = newState
        self.list.append(self.state)
        self.pos = (self.pos[0], self.pos[1], self.pos[2]+1)
 
class flowAlongUV(object):
    
    def __init__(self, strSrf, imax, jmax, zmax):
        
        self.strSrf = strSrf
        self.UVpt = {}
        Udomain = rs.SurfaceDomain(self.strSrf, 0)
        Vdomain = rs.SurfaceDomain(self.strSrf, 1)
        intU = imax-1
        intV = zmax-1
        Ustep = (Udomain[1]-Udomain[0])/intU
        Vstep = (Vdomain[1]-Vdomain[0])/intV
        rs.EnableRedraw(False)
        for i in range(intU + 1):
            for k in range(intV + 1):
                
                for j in range(jmax):
                    
                    u = Ustep*i + Udomain[0]
                    v = Vstep*k + Vdomain[0]
                    scale = j+1
                    
                    UVpoint = rs.EvaluateSurface(self.strSrf, u, v)
                    UVnorm = rs.SurfaceNormal(self.strSrf, (u,v))
                    UVnorm = rs.VectorUnitize(UVnorm)
                    UVnorm = rs.VectorScale(UVnorm, scale)
                    self.UVpt[(i,j,k)]=rs.MoveObject(UVpoint,UVnorm)
                   
        rs.EnableRedraw(True)
                
    def UVmove(self, cellular):
        A = cellular.A
        B = cellular.B
        C = cellular.C
        self.vector = rs.VectorCreate(self.UVpt[(A,B,C)], cellular.pos) 
        return self.vector
        
def main():
    
    strSrf = rs.GetObject(‘Select a Surface’, rs.filter.surface)
    imax = rs.GetInteger(‘Enter X Value’, 80)
    jmax = rs.GetInteger(‘Enter Y Value’, 12)
    zmax = rs.GetInteger(‘Enter Z Value’, 50)
    
    surface = flowAlongUV(strSrf, imax, jmax, zmax)
    
    pointPopulation = []
    point = {}
    rs.EnableRedraw(False)
    for i in range(imax):
        for j in range(jmax):
            x = i
            y = j
            z = 0
            pointID = rs.AddPoint(x, y, z)
            pointPos = rs.PointCoordinates(pointID)
            pointState = rnd.random()
            if pointState >0.5:
                secondState = 1
            else:
                secondState = 0
            pointState = secondState
            point[(i,j)] = cell(pointID, pointPos, pointState,zmax,i,j)
            if pointState <= 0.5:
                rs.DeleteObject(pointID)
                
    rs.EnableRedraw(True)
    for k in range(zmax):
        rs.EnableRedraw(False)
        for i in range(imax):
            for j in range(jmax):
                
                if i == 0:
                    iminus1 = imax-1
                if i > 0:
                    iminus1 = i - 1
                
                if i == imax-1:
                    iplus1 = 0
                if i < imax-1:
                    iplus1 = i + 1
                    
                #jplus1 = j+1
                #jminus1 = j-1
                
                if j == 0:
                    jminus1 = jmax-1
                if j > 0:
                    jminus1 = j - 1
                    
                if j == jmax-1:
                    jplus1 = 0
                if j < jmax -1:
                    jplus1 = j + 1 
                    
                #rs.AddTextDot(jplus1, point[(i,j)].pos)
                
                
                point[(i,j)].live(point[(iminus1,jminus1)],point[(iminus1,j)],
                point[(iminus1,jplus1)],point[(i,jplus1)], point[(iplus1,jplus1)],
                point[(iplus1,j)], point[(iplus1,jminus1)], point[(i,jminus1)],k,surface)                    
                    #rs.AddTextDot((i,j), point[(i,j)].pos)
        rs.EnableRedraw(True)
    #rs.EnableRedraw(True)
    
        

main()

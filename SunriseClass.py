import time
import math
import datetime


class Sunrise:

    def __init__(self):
        self.dt = datetime.datetime.now()
        self.day = 1
        self.month = 1
        self.year = 1900

    def sunrise(self,month, year, day):
        self.month = month
        self.year = year
        self.day= day
        global R2D
        R2D = 180/math.pi
        global D2R
        D2R = math.pi/180
        self.day_of_the_year( month, year, day)
        self.longitude_to_hour()
        self.sun()
        return self.dt
    def sun(self):
        M = (0.9856 * rise_time) - 3.289
        L = M + ( 1.916 * math.sin(M* D2R)) + (0.020 * math.sin(2*M*D2R)) + 282.63
        if L < 0:
            L = L+360
        elif L > 360:
            L = L - 360
        RA =R2D* math.atan(0.91764 * math.tan(L*D2R))
        if RA < 0 :
            RA = RA + 360
        elif RA > 360:
            RA = RA - 360
        Lquad = ( math.floor( L/ 90)) * 90
        RAquad = ( math.floor(RA/90)) *90
        RA = RA + (Lquad - RAquad)
        RA = RA/15
        sinDec = 0.39782 * math.sin(L*D2R)
  
        cosDec = math.cos(math.asin(sinDec))
        cosH = ( math.cos(90.83*D2R) - (sinDec * math.sin(latitude*D2R))) / (cosDec * math.cos(latitude*D2R))
        Hrise = 360 -(R2D * math.acos( cosH))
    
        Hrise = Hrise/15

        T = Hrise + RA - ( 0.06571 * rise_time) - 6.622
        UT = T - lngHour
        if UT < 0:
            UT = UT + 24
        elif UT > 24:
            UT = UT - 24
        UT=UT+2   
        UT = (UT*3600)
        UT = time.gmtime(UT)
        self.dt = datetime.datetime(self.year,self.month,self.day, UT.tm_hour, UT.tm_min,0,0,None)
        #self.dt = datetime.datetime(1900,1,1,UT.tm_hour,UT.tm_min,0,0,None)
      #  print(self.dt)
     #   return self.dt
    #print("Sunrise time is %s:%s "%(UT.tm_hour, UT.tm_min))
    
    def longitude_to_hour(self):
        global longitude
        longitude = 31.2357116
        global latitude
        latitude = 30.0444196
        global lngHour
        lngHour = longitude / 15
        global rise_time
        global set_time
        rise_time = N + ( (6 - lngHour) / 24)
        set_time = N + ( (18 - lngHour) / 24)
    
    def day_of_the_year(self, month, year, day):
        N1 = math.floor(275 * month / 9)
        N2 = math.floor( (month+ 9) / 12)
        N3 = ( 1 + math.floor( (year - 4 * math.floor(year/4) + 2 ) / 3))
        global N
        N = N1 - (N2 * N3) + day - 30
        



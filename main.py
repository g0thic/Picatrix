#!/usr/bin/python
import datetime
import SunriseClass
import SunsetClass
import xml.etree.ElementTree as ET
import daytime_thread
import nighttime_thread
import os
import time
import sys



def main():

    global days
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    daytime = None
    nighttime = None
    while True:
        getSunriseSunset()
        calculate_sunrisetime()
        get_next_sunrise()
        calculate_sunsettime()
        day_name = days[datetime.datetime.now().weekday()]
        check_day_night()
        if check_day_night() == 1:
            if daytime is None:
                daytime = daytime_thread.daytime_thread("weekdays.xml", day_name, currentSunrise, currentSunset,
                                                        day_hour_length)
            try:
                if nighttime is not None:
                    nighttime.end_thread()
                    nighttime = None
            except BaseException as e:
                nighttime = None
            if not daytime.is_alive():
                daytime.start()  # daytime.run()

        elif check_day_night() == 0:
            if nighttime is None:
                nighttime = nighttime_thread.nighttime_thread("weekdays.xml", day_name, currentSunset, next_sunrise,
                                                              night_hour_length)
            try:
                if daytime is not None:
                    daytime.end_thread()
                    daytime = None
            except BaseException as e:
                daytime = None
            if not nighttime.is_alive():
                nighttime.start()  # nighttime.run()

        elif check_day_night() == -1:
            try:
                day_name = days[datetime.datetime.now().weekday() - 1]
            except BaseException as e:
                day_name = days[6]
            try:
                if daytime is not None:
                    daytime.end_thread()
                    daytime = None
            except:
                daytime = None
            if nighttime is None:
                nighttime = nighttime_thread.nighttime_thread("weekdays.xml", day_name, currentSunset, next_sunrise,
                                                              night_hour_length)
            if not nighttime.is_alive():
                nighttime.start()



def check_day_night(dt = None):
    global isDaytime
    if dt is None:
        dt = datetime.datetime.now()
    if dt < currentSunset and dt > currentSunrise :
        return 1
    elif dt > currentSunset and dt < next_sunrise:
        return 0
    else:
        return -1



def calculate_sunsettime():
    global night_hour_length
    r = next_sunrise - currentSunset
    r = r/12
    night_hour_length = (datetime.datetime.min + r)


def calculate_sunrisetime():
    global day_hour_length
    r = currentSunset - currentSunrise
    r = r / 12
    day_hour_length = (datetime.datetime.min + r)


def get_next_sunrise(month=None, year=None, day=None):
    global next_sunrise
    sr = SunriseClass.Sunrise()
    if month is None and year is None and day is None:
        dt = datetime.datetime.now()
        dt = dt + datetime.timedelta(days=1)
        day = int(dt.strftime("%d"))
        month = int(dt.strftime("%m"))
        year = int(dt.strftime("%Y"))
        next_sunrise = sr.sunrise(month, year, day)
    else:
        next_sunrise = sr.sunrise(month, year, day)
    del sr


def getSunriseSunset(month=None, year=None, day=None):
    sr = SunriseClass.Sunrise()
    ss = SunsetClass.Sunset()
    global currentSunrise
    global currentSunset
    if month is None and year is None and day is None:
        dt = datetime.datetime.now()
        day = int(dt.strftime("%d"))
        month = int(dt.strftime("%m"))
        year = int(dt.strftime("%Y"))
        currentSunrise = sr.sunrise(month, year, day)
        currentSunset = ss.sunset(month, year, day)
    else:
        currentSunrise = sr.sunrise(month, year, day)
        currentSunset = ss.sunset(month, year, day)
    del sr
    del ss

if __name__ == '__main__':
    try:
        main()
    except BaseException:
        print("...?!")
    finally:
        sys.exit()

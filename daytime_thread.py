import threading
import time
import datetime
import xml.etree.ElementTree as ET
import subprocess
import os
import sys


class daytime_thread(threading.Thread):

    def __init__(self, xml_file_name, day_name, sunrise_time, sunset_time, hour_length):
        threading.Thread.__init__(self)
        self.xml_file_name = xml_file_name
        self.xml_tree = ET.parse("C:\\Picatrix\\"+xml_file_name)
        self.day_name = day_name
        self.sunrise_time = sunrise_time
        self.sunset_time = sunset_time
        self.hour_length = hour_length
        self.timestart = datetime.datetime.now()
        self.timeend = datetime.datetime.now()
        self.planet = ""
        self.shouldStop = False

    def end_thread(self):
        self.shouldStop = True



    def run(self):
        #print("thread started")
        self.set_time()
        print("It's " + self.day_name + ", Daytime starts at [" + self.sunrise_time.strftime(
            "%H:%M") + "] and ends at [" + self.sunset_time.strftime("%H:%M") + "]")

        while not self.shouldStop:
            self.play_audio()
            if datetime.datetime.now().ctime() > self.sunset_time.ctime():
                break
            #print (self.timeend)
            t=0
            try:
                mins = int(datetime.datetime.now().strftime("%M"))
                hours = int(datetime.datetime.now().strftime("%H"))
                t = self.timeend - datetime.timedelta(minutes=mins) - datetime.timedelta(hours=hours)
                print("Time left for next hour: ", t.time().strftime("%H:%M"))
                t = (int(t.strftime("%H")) * 3600) + (int(t.strftime("%M")) * 60)

            except:

                print("Error Daytime_thread time difference error at ", datetime.datetime.now())
                t = 3600
            time.sleep(t+120)


    def play_audio(self):
        path = os.path.dirname(sys.executable)
        # os.startfile("C:\\Program Files (x86)\\Windows Media Player\\wmplayer.exe", operation="C:\\Picatrix\\Audio\\Thursday\\Daytime\\Jupiter\\list.wpl")
        # os.system("C:\Program Files (x86)\Windows Media Player\\wmplayer.exe C:\\Picatrix\\Audio\\Thursday\\Daytime\\Jupiter\\list.wpl")
        # os.system("C:\\Picatrix\\Audio\\Thursday\\Daytime\\Jupiter\\list.wpl")
        self.get_time()
        wmpath = "C:\\Program Files (x86)\\Windows Media Player\\wmplayer.exe"
        audiopath = "C:\\Picatrix\\Audio\\"+self.day_name+"\\Daytime\\"+self.planet['name']+"\\list.wpl"
        global exist
        exist = False
        exist = os.path.isfile(audiopath)

        if exist:
            subprocess.Popen(wmpath+" "+audiopath)
            print("Hour starts at:[", self.timestart.strftime("%H:%M"), "] , Hour end:[", self.timeend.strftime("%H:%M"), "] , Planet:[", self.planet['name'],"]")
        else:
            print("Hour starts at:[", self.timestart.strftime("%H:%M"), "] , Hour end:[", self.timeend.strftime("%H:%M"), "] , Planet:[", self.planet['name'],"]",
                  " --No Audio--")


    def get_time(self):
        root = self.xml_tree.getroot()
        day_name = root.find(self.day_name)
        for daytime_nighttime in day_name:
            if daytime_nighttime.tag == "Daytime":
                time_list = day_name.find(daytime_nighttime.tag, daytime_nighttime.attrib)
                for time_part in time_list:    #12
                    if datetime.datetime.now().hour == 00:
                        #print("00   ",self.timestart.time(), datetime.datetime.now().time(), self.timeend.time())

                        if datetime.datetime.now().time() >= self.timestart.time() or \
                                datetime.datetime.now().time() <= self.timeend.time():
                            if self.timeend.hour == 00 or self.timeend.hour == 00:
                                if self.timeend.time() > self.timestart.time():
                                    break

                    if datetime.datetime.now().time() < self.timeend.time() and\
                            datetime.datetime.now().time() >= self.timestart.time():
                        break
                    self.planet = time_part.attrib
                    start_end_list = daytime_nighttime.find(time_part.tag)

                    for vv in start_end_list:   #2

                        if vv.tag == "TimeStart":
                            fp = int(str.find(vv.text, ":"))
                            hour = int(vv.text[0:fp])
                            min = int(vv.text[fp+1:])
                            year =int(datetime.datetime.now().strftime("%Y"))
                            month = int(datetime.datetime.now().strftime("%m"))
                            day = int(datetime.datetime.now().strftime("%d"))
                            self.timestart = datetime.datetime(year,month, day, hour, min, 0, 0, None)

                        elif vv.tag == "TimeEnd":
                            fp = int(str.find(vv.text, ":"))
                            hour = int(vv.text[0:fp])
                            min = int(vv.text[fp + 1:])
                            year = int(datetime.datetime.now().strftime("%Y"))
                            month = int(datetime.datetime.now().strftime("%m"))
                            day = int(datetime.datetime.now().strftime("%d"))
                            self.timeend = datetime.datetime(year, month, day, hour, min, 0, 0, None)

            #print(self.timestart.time(), self.timeend.time(), self.planet[0])



    def set_time(self):
       # tree = ET.parse('weekdays.xml')
        root = self.xml_tree.getroot()
        day_name = root.find(self.day_name)
        #print(self.day_name)
        timepointer = datetime.datetime.now().time()
        hour_length = (int(self.hour_length.strftime("%H")) * 3600) + (int(self.hour_length.strftime("%M")) * 60) +int(self.hour_length.strftime("%S"))
        for daytime_nighttime in day_name:
            if daytime_nighttime.tag == "Daytime":
                #print(daytime_nighttime.tag)
                time_list = day_name.find(daytime_nighttime.tag, daytime_nighttime.attrib)
                current_start_time = self.sunrise_time
                current_end_time = (current_start_time + datetime.timedelta(seconds=hour_length))
                for time_part in time_list:
                    #print(time_part.tag, time_part.attrib)
                    start_end_list = daytime_nighttime.find(time_part.tag)

                    for vv in start_end_list:
                        if vv.tag == "TimeStart":
                            vv.text = current_start_time.strftime("%H") +":"+ current_start_time.strftime("%M")
                            current_start_time = current_end_time
                        elif vv.tag == "TimeEnd":
                            vv.text = current_end_time.strftime("%H") +":" +current_end_time.strftime("%M")
                            current_end_time = (current_start_time+datetime.timedelta(seconds=hour_length))

                        #print(vv.tag, vv.text)
        self.xml_tree.write(self.xml_file_name)

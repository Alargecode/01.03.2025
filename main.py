import datetime
import os
from subprocess import call
import sys
import gettext
   # self.ids.previous_page.text = 'Previous Page'
   # self.ids.save.text = 'Save'
os.environ['KIVY_GL_BACKEND'] = 'gl'
from math import cos, pow, radians, sin, tan
import threading
from time import sleep
import RPi.GPIO as gpio
import signal
from kivy.config import Config
import statistics 
import time

gpio.cleanup()
gpio.setwarnings(False)
Config.set('input', 'mouse', 'mouse,multitouch_on_demand')
Config.set('kivy', 'keyboard_mode', 'systemanddock')
import subprocess
from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy_garden.graph import MeshLinePlot
from kivy.uix.popup import Popup
from kivy.uix.floatlayout import FloatLayout

from fpdf_handler import fpdf_handler
from multi import multi
from excel import excel
gpio.setmode(gpio.BCM)
from motor_drivere import motor_driver
from json_dumper import JsonHandler
from takedata import data
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.label import Label
from kivy.uix.image import Image as KivyImage
import shutil
from kivy.uix.filechooser import FileChooserIconView
from PIL import Image

gettext.bindtextdomain('messages', './locales')
gettext.textdomain('messages')


start_switch = 6  # start kısmındaki switch
stop_switch = 5  # stop kısmındaki switch

gpio.setup(start_switch, gpio.IN, pull_up_down=gpio.PUD_UP)
gpio.setup(stop_switch, gpio.IN, pull_up_down=gpio.PUD_UP)

reset_motor_speed = 200
Builder.load_file('cof.kv')

md = motor_driver(1, False)  # bir adet dc bir adet açı(step) motor modu seçildi, soft start kapatıldı
json_handler = JsonHandler()
md.stop_motor()

language = 'English'

global durdu
durdu = 0

global sıfırlama
sıfırlama = 1
global sayma
sayma = 0

class sample:
    name = ""
    width = 0
    height = 0
    age = 0
    testing_weight = 0
    company_name = ""
    operator_name = ""
    force_screen = 0


sample1 = sample()
sample2 = sample()

# üstte kayan metal malzemenin kütlesi (kg)
normal_force = 200
forces = [[0, 0]]*50000

global calib  # kalibrasyon sayısı
sample_time = 0.1

def find_biggest(array):
    biggest = [0.1, 0.1]
    for i in array[:][:]:
        if i[1] > biggest[1]:
            biggest = i
        else:
            pass
    return biggest

def find_dynamic_static_force_advanced():
    array = []
    array2 = []
    array_mean = 0
    array_mean2 = 0
    sample_time = 0.1
    
    for i in range(int(len(forces)*(1/60)), int(len(forces)*(7/10))):
        if (6 < forces[i][0]):
            #Dinamik burada hesaplanır.
            array_mean += forces[i][1]
            array.append(forces[i])
        else:
            #Statik burada hesaplanır.
            array_mean2 += forces[i][1]
            array2.append(forces[i])
    
    _, max_dynamic_force = find_biggest(array)
    mean_dynamic_force = array_mean / (len(array) + 1)
    _, max_static_force = find_biggest(array2)
    mean_static_force = array_mean2 / (len(array2) + 1)
                                     
    return max_static_force, mean_static_force, max_dynamic_force, mean_dynamic_force
 
class ScreenOne(Screen):

    def shutdown(self):
        call("sudo poweroff", shell= True)       

    def btn_text(self):
        sample1.name = self.ids.first_name.text
        try:
            sample1.width = float(self.ids.first_width.text)
        except:
            sample1.width = 0.00

        try:
            sample1.height = float(self.ids.first_height.text)
        except:
            sample1.height = 0.00

        try:
            sample1.age = float(self.ids.first_age.text)
        except:
            sample1.age = 0.00

        sample1.company_name = self.ids.company_name.text
        sample1.operator_name = self.ids.operator_name.text
        sample1.testing_weight = normal_force

        if self.ids.switch.active:
            sample2.name = self.ids.second_name.text
            try:
                sample2.width = float(self.ids.second_width.text)
            except:
                sample2.width = 0.00
            try:
                sample2.height = float(self.ids.second_height.text)
            except:
                sample2.height = 0.00
            try:
                sample2.age = float(self.ids.second_age.text)
            except:
                sample2.age = 0.00

class ScreenTwo(Screen):
    plot = MeshLinePlot(color=[1, 0, 0, 1])
    
    def __init__(self, **args):
        Screen.__init__(self, **args)
        self.is_reset = False

        global normal_force
        global sample_time
        global test_speed
        global test_distance
        global calib
        test_distance, test_speed, normal_force, sample_time, calib = json_handler.import_save()

    def start(self):
        global durdu
        global forces
        global sıfırlama
        global sayma
        global test_speed
        if(durdu == 0):
            #print("sss")
            data.close()
            forces.clear()
            durdu = 1
            sıfırlama = 1
            gpio.setup(stop_switch, gpio.IN, pull_up_down=gpio.PUD_DOWN)
            gpio.setup(start_switch, gpio.IN, pull_up_down=gpio.PUD_DOWN)

            self.time_ = 0
            forces = [[0, 0]]
            self.ids.graph.remove_plot(self.plot)
            self.ids.graph.add_plot(self.plot)
            #print("s s", gpio.input(stop_switch))
            if not gpio.input(stop_switch):
                self.timer_thread = threading.Thread(target=self.timer, args=("task",))
                self.timer_thread.start()
                self.value_thread = threading.Thread(target=self.get_value, args=("task",))
                self.value_thread.start()

                self.ids.dist_current.text = "0"

                self.ids.val.text ="0"

                test_speed_arranged = 27*test_speed
                md.motor_start(test_speed_arranged,0)
                self.max_distance_event()
            else: 
                pass
            
            return True
    
    def timer(self, arg):
        t = threading.current_thread()
        while getattr(t, "do_run", True):
            self.time_ = round(self.time_ + 0.012, 2)
            sleep(0.012)
    
    def get_value(self, arg):
        global forces
        global calib
        global sıfırlama
        global sayma
        global test_speed
        t = threading.current_thread()
        
        
        self.ids.graph.xmax = 1
        self.ids.graph.ymax = 10

        global test_distance 
        
        while getattr(t, "do_run", True):
            # üç değer alınıyor ve bu 3 değer filtre işleminde kullanılıyor.
            val  = ((data.take_data()*calib))
            val2 = ((data.take_data()*calib))
            val3 = ((data.take_data()*calib))
            
            # Median of three kullanılıyor.
            val = statistics.median([val, val2, val3])
            val = round(val,3)
            self.ids.val.text=str(val)
                    
            if (val >= 0 and self.time_ > 1 and sıfırlama) :
                time_calib = self.time_* 1.305
                forces.append([time_calib, val])
                sayma = sayma + 1
                #print(sayma)
            elif (self.time_ <= 1 and sıfırlama) :
                time_calib = self.time_ * 1.395
                forces.append([time_calib, 0])
            else:
                pass
            
            self.ids.dist_current.text = str(round(self.time_*test_speed/45, 1))  
            
            try:
                if forces[-1][0] == 0:
                    self.ids.graph.xmax = 1
                elif forces[-1][0] > self.ids.graph.xmax:
                    self.ids.graph.xmax = forces[-1][0]

                if len(forces) < 3:
                    self.ids.graph.ymax = 1
                elif forces[-1][1] > self.ids.graph.ymax:
                    self.ids.graph.ymax = (forces[-1][1] * 1.1)
            except:
                pass

            self.ids.graph.y_ticks_major = round(self.ids.graph.ymax / 11, -1)
            self.ids.graph.x_ticks_major = round(self.ids.graph.xmax, -1) * 0.1        
            self.plot.points = forces
            
            if(float(self.ids.dist_current.text) > float(test_distance)):
                t.do_run = False
                print("durrraa")
                self.stop()
               
    def stop_event(self, channel):
        self.stop()
        print("Switchlerden sinyal geldi.")
        data.close()
        return True
        
    def stop_event_master_1(self, channel):
        if gpio.input(start_switch):
            self.stop()
            print("Switclerden sinyal geldi master start.")
            return True

    def stop_event_master_2(self, channel):
        if gpio.input(stop_switch):
            self.stop()
            print("Switclerden sinyal geldi master stop.")
            return True

    
    def stop_100(self):
        global durdu
        durdu = 0
        md.stop_motor()

        self.value_thread.join()
        self.timer_thread.join()
        
        self.time_ = 0
        md.stop_motor()
        if self.is_reset:
            self.start()
        
    def stop(self):
        global sıfırlama
        sıfırlama = 0
        global durdu
        durdu = 0
        try:
            self.value_thread.do_run = False
            self.value_thread.join()
        except:
            pass
        try:
            self.timer_thread.do_run = False
            self.timer_thread.join()

        except:
            pass
        self.time_ = 0
        
        try:
            gpio.remove_event_detect(stop_switch)
            gpio.cleanup(stop_switch)
        except:
            pass
        
        try:
            gpio.remove_event_detect(start_switch)
            gpio.cleanup(start_switch)
        except:
            pass
        
        md.stop_motor()
        if self.is_reset:
            self.start()

    def reset(self):
        global forces
        forces.clear()
        self.stop()
        self.is_reset = False 
        signal.signal(signal.SIGALRM, self.reset_)
        signal.setitimer(signal.ITIMER_REAL, 0.1, 0)
        self.reset_(1,1)

    def reset_(self, signum, _):
        self.stop()
        self.is_reset = False              
        self.motor_backward()
        self.min_distance_event()

    def save_graph(self):
        self.ids.graph.export_to_png("/home/pi/Cof-Tabs/graph.png")

    

    def motor_forward(self):
        self.max_distance_event()
        #md.motor_start(1000, 1)

    def motor_backward(self):
        gpio.setup(start_switch, gpio.IN, pull_up_down=gpio.PUD_DOWN)
        if not gpio.input(start_switch):
            self.min_distance_event()
            md.motor_start(10000, 1)
            

    def max_distance_event(self):

        try:
            gpio.setup(stop_switch, gpio.IN, pull_up_down=gpio.PUD_DOWN)
            gpio.add_event_detect(stop_switch, gpio.RISING, callback=self.stop_event_master_2, bouncetime=1)
        except:
            pass

    def min_distance_event(self):
        try:
            gpio.setup(start_switch, gpio.IN, pull_up_down=gpio.PUD_DOWN)
            gpio.add_event_detect(start_switch, gpio.RISING, callback=self.stop_event_master_1, bouncetime=1)
            
        except:
            pass


class P(FloatLayout):
    pass


class ScreenThree(Screen):
    date_today = datetime.date.today()
    date_text = str(date_today)

    def create_results(self):
        max_static_cof, mean_static_cof, max_dynamic_cof, mean_dynamic_cof = self.find_dynamic_static_cof()       
        return max_static_cof, mean_static_cof, max_dynamic_cof, mean_dynamic_cof

    def find_dynamic_static_cof(self):
       
        max_static_force, mean_static_force, max_dynamic_force, mean_dynamic_force = find_dynamic_static_force_advanced()
        
        mean_dynamic_cof = mean_dynamic_force / (normal_force * 9.81)
        mean_dynamic_cof = round(mean_dynamic_cof, 3)
        max_dynamic_cof = max_dynamic_force / (normal_force * 9.81)
        max_dynamic_cof = round(max_dynamic_cof, 3)
        
        mean_static_cof = mean_static_force / (normal_force * 9.81 )
        mean_static_cof = round(mean_static_cof, 3)
        max_static_cof = max_static_force / (normal_force * 9.81 )
        max_static_cof = round(max_static_cof, 3)
    
        return max_static_cof, mean_static_cof, max_dynamic_cof, mean_dynamic_cof

    def update_results(self):
        
        self.max_static, self.mean_static, self.max_dynamic, self.mean_dynamic = self.create_results()
        self.ids.l_max_static.text = str(self.max_static)
        self.ids.l_mean_static.text = str(self.mean_static)
        self.ids.l_max_dynamic.text = str(self.max_dynamic)
        self.ids.l_mean_dynamic.text = str(self.mean_dynamic)
            
        json_handler.dump_all(self.max_static, self.mean_static, self.max_dynamic, self.mean_dynamic, sample1, sample2, ScreenTwo.plot.points)
            
    
    """def createPDF(self):
        global language
        self.pdf = fpdf_handler()
        self.update_results()
        self.pdf.create_pdf(self.max_dynamic, self.mean_dynamic, self.max_static, self.mean_static, sample1, sample2 ,ScreenTwo.plot.points)
        self.show_popup()"""
    
    def createPDF(self):
        global language
        self.pdf = multi()
        self.update_results()

        self.pdf.create_pdf_ones(self.max_dynamic, self.mean_dynamic, self.max_static, self.mean_static, sample1, sample2 ,ScreenTwo.plot.points, language)
        
        self.exc = excel()
        self.exc.create_excel_report(self.max_dynamic, self.mean_dynamic, self.max_static, self.mean_static, sample1, sample2 ,ScreenTwo.plot.points, language)
        
        self.show_popup()
    
    def whole_save(self):
        global language
        self.pdf = multi()
        self.update_results()

        self.pdf.create_pdf(self.max_dynamic, self.mean_dynamic, self.max_static, self.mean_static, sample1, sample2 ,ScreenTwo.plot.points, language)
        
        self.exc = excel()
        self.exc.create_excel_report(self.max_dynamic, self.mean_dynamic, self.max_static, self.mean_static, sample1, sample2 ,ScreenTwo.plot.points, language)
        
        self.show_popup()


    def show_popup(self):
        show = P()
        self.popupWindow = Popup(title="PDF Olusturuldu", content=show, size_hint=(None, None), size=(400, 200))
        self.popupWindow.open()
        

    def open_file_dialog(self):
        file_chooser = FileChooserListView(path='.')
        file_chooser.bind(on_submit=self.on_file_submit)  # on_submit olayını bağla
        popup = Popup(title='Select Image', content=file_chooser, size_hint=(0.9, 0.9))
        popup.open()

    def on_file_submit(self, instance, value, *args):
        selected_file = value[0] if value else None  # Seçilen dosya yollarından ilkini al veya None
        if selected_file:
            self.load_image(None, selected_file)  # load_image işlevini çağır

    def load_image(self, instance, selected_file, *args):
    
        if isinstance(selected_file, bytes):
            selected_file = selected_file.decode('utf-8')  # Dosya yolunu dizeye dönüştür

        if os.path.exists(selected_file):
            self.process_image(selected_file)
        else:
            print("File not found:", selected_file)
    
    def process_image(self, file_path):
        try:
            # Resmi kopyalamak için hedef dizin ve dosya adını belirleyin
            target_directory = '/home/pi/Cof-Tabs/LOGO'
            target_file = os.path.basename(file_path)

            # Dosyayı hedef dizine kopyalayın
            shutil.copy2(file_path, os.path.join(target_directory, target_file))

            # Resmin adresini kaydedeceğiniz metin dosyasının yolunu belirleyin
            text_file = '/home/pi/Cof-Tabs/logo.txt'
            

            # Metin dosyasını açarak resmin adresini yazın
            with open(text_file, 'w') as file:
                print("target file :   ")
                print(target_file)
                file.write(target_directory + '/' + target_file )

            # Burada resmin boyutu excel ve pdf uygun formata dönüştürülüyor.
            with open(text_file, 'r') as file:
                content = file.read()
            img = Image.open(content)
            width, height = img.size
            image_big_size = 0
            image_big_size = width if width > height else height
            image_ratio = image_big_size / 100
            new_width = width / image_ratio
            new_height = height / image_ratio
            img = img.resize((int(new_width), int(new_height)))
            img.save(content)

            print("Image copied successfully.")
        except Exception as e:
            print("Error while copying image:", str(e))


class ScreenFive(Screen):

    def __init__(self, **args):
        Screen.__init__(self, **args)
        self.ids.normal_force.text = str(normal_force)
        self.ids.calib.text = str(calib)
        self.ids.test_speed.text = str(test_speed)
        self.ids.test_distance.text = str(test_distance)
        
    def save(self):
        count = 0

        if self.ids.normal_force_text.text != "":
            try:
                global normal_force
                normal_force = float(self.ids.normal_force_text.text)
                self.ids.normal_force.text = str(normal_force)
                self.ids.error.color = (0, 0, 0, 0)
            except:
                self.ids.error.text = "Error! (Use only numbers) (use . not ,)"
                self.ids.error.color = (0, 0, 0, 1)
            else:
                count = 1

        if self.ids.calib_text.text != "":
            try:
                global calib
                calib = float(self.ids.calib_text.text)
                self.ids.calib.text = str(calib)
                self.ids.error.color = (0, 0, 0, 0)
            except:
                self.ids.error.text = "Error! (Use only numbers) (use . not ,)"
                self.ids.error.color = (0, 0, 0, 1)
            else:
                count = 1
                
        if self.ids.test_speed.text != "":
            try:
                global test_speed
                test_speed = float(self.ids.test_speed_text.text)
                self.ids.test_speed.text = self.ids.test_speed_text.text
                self.ids.error.color = (0, 0, 0, 0)
            except:
                self.ids.error.text = "Error! (Use only numbers) (use . not ,)"
                self.ids.error.color = (0, 0, 0, 1)
            else:
                count = 1
        
        if self.ids.test_distance.text != "":
            try:
                global test_distance
                test_distance = float(self.ids.test_distance_text.text)
                self.ids.test_distance.text = self.ids.test_distance_text.text
                self.ids.error.color = (0, 0, 0, 0)
            except:
                self.ids.error.text = "Error! (Use only numbers) (use . not ,)"
                self.ids.error.color = (0, 0, 0, 1)
            else:
                count = 1

        if self.ids.normal_force_text.text == "" and self.ids.calib_text.text == "" and self.ids.test_speed_text.text :
            self.ids.error.color = (0, 0, 0, 0)
        if count == 1:
            self.ids.error.text = "Saved"
            self.ids.error.color = (0, 1, 0, 1)

    def save_for_good(self):
        self.save()
        global test_distance
        global test_speed
        global normal_force
        global sample_time
        global calib
        json_handler.dump_calib_save(distance=test_distance, speed=test_speed, normal_force=normal_force,sample_time=sample_time, calib=calib)

        test_distance, test_speed, normal_force, sample_time, calib = json_handler.import_save()

    def reset_to_factory(self):
        global test_distance
        global test_speed
        global normal_force
        global sample_time
        global calib

        test_distance = 100
        test_speed = 100
        normal_force = 200
        sample_time = 0.01
        calib = 1 

        self.ids.normal_force.text = str(normal_force)
        self.ids.calib.text = str(calib)
        self.ids.test_speed.text = str(test_speed)
        self.ids.test_distance.text = str(test_distance)
        json_handler.dump_calib_save(distance=test_distance, speed=test_speed, normal_force=normal_force, sample_time=sample_time, calib=calib)
        test_distance, test_speed, normal_force, sample_time, calib = json_handler.import_save()

    def clean_errors(self):
        self.ids.error.color = (0, 0, 0, 0)

    def language_change(self, text):
        language_change_gl(text)


def language_change_gl(text):
    #screen_one = ScreenOne()
    global sc_one
    global sc_two
    global sc_three 
    global sc_five
    global language

    sc_one = screen_manager.get_screen('screen_one')
    sc_two = screen_manager.get_screen('screen_two')
    sc_three = screen_manager.get_screen('screen_three')
    sc_five = screen_manager.get_screen('screen_five')

    def_language(language)

    if text == 'English':
        language = 'English'
        sc_five.ids.previous_page.text = 'Previous Page'
        sc_five.ids.save.text = 'Save'
        sc_five.ids.reset_factory.text = 'Reset\nFactory Settings'
        sc_five.ids.language.text = 'Change Language'
        sc_five.ids.normal_force_text.hint_text = 'Normal Mass(gr)'
        sc_five.ids.calib_text.hint_text = 'Force Calibration'
        sc_five.ids.test_speed_text.hint_text = 'Test Speed (mm/min)'
        sc_five.ids.test_distance_text.hint_text = 'Test Distance (mm)'
        sc_five.ids.normal_force_label.text = 'Normal Mass:'
        sc_five.ids.calib_label.text = 'Force Calibration:'
        sc_five.ids.test_speed_label.text = 'Test Speed:'
        sc_five.ids.test_distance_label.text = 'Test Distance:'
        

        sc_one.ids.second_sample_header.text = 'Sample'
        sc_one.ids.first_sample_header.text = 'Sample'
        sc_one.ids.calibration.text = 'Calibration'
        sc_one.ids.test.text = 'Test'
        sc_one.ids.first_name.hint_text = 'Sample Name'
        sc_one.ids.first_width.hint_text = 'Width (mm)'
        sc_one.ids.first_height.hint_text = 'Height (mm)'
        sc_one.ids.first_age.hint_text = 'Age (Month)'
        sc_one.ids.second_name.hint_text = 'Sample Name'
        sc_one.ids.second_width.hint_text = 'Width (mm)'
        sc_one.ids.second_height.hint_text = 'Height (mm)'
        sc_one.ids.second_age.hint_text = 'Age (Month)'
        sc_one.ids.company_name.hint_text = 'Company Name'
        sc_one.ids.operator_name.hint_text = 'Operator Name'
        sc_one.ids.shutdown.text = 'Shutdown'

        sc_two.ids.graph.xlabel = 'Time (second)'
        sc_two.ids.graph.ylabel = 'Force (mN)'
        sc_two.ids.start.text = 'Start'
        sc_two.ids.reset_pos.text = 'Reset Position'
        sc_two.ids.pre_page.text = 'Previous Page'
        sc_two.ids.btn.text = 'Result'
        sc_two.ids.distance.text = 'Distance'
        sc_two.ids.force.text = 'Force'

        sc_three.ids.calc_res.text = 'Calculate Result'
        sc_three.ids.create_pdf_label.text = 'Create Report'
        sc_three.ids.pre_page.text = 'Previous Page'
        sc_three.ids.calc_res.text = 'Calculate Result'
        sc_three.ids.max_static.text = '[b]Maximum Static Friction Coefficient[/b]'
        sc_three.ids.mean_static.text = 'Mean Static Friction Coefficient'
        sc_three.ids.max_dynamic.text = 'Maximum Dynamic Friction Coefficient'
        sc_three.ids.mean_dynamic.text = '[b]Mean Dynamic Friction Coefficient[/b]'
        sc_three.ids.date.text = 'Date'
        sc_three.ids.take_symbol.text = 'Choose Logo'
        
    elif text == 'Turkish':
        language = 'Turkish'
        sc_five.ids.previous_page.text = 'Önceki Sayfa'
        sc_five.ids.save.text = 'Kaydet'
        sc_five.ids.reset_factory.text = 'Fabrika\n Ayarlarına Döndür'
        sc_five.ids.language.text = 'Dili Değiştir'
        sc_five.ids.normal_force_text.hint_text = 'Normal Kütle(gr)'
        sc_five.ids.calib_text.hint_text = 'Kuvvet Kalibrasyonu'
        sc_five.ids.test_speed_text.hint_text = 'Test Hızı (mm/dk)'
        sc_five.ids.test_distance_text.hint_text = 'Test Mesafesi (mm)'
        sc_five.ids.normal_force_label.text = 'Normal Kütle:'
        sc_five.ids.calib_label.text = 'Kuvvet Kalibrasyonu:'
        sc_five.ids.test_speed_label.text = 'Test Hızı:'
        sc_five.ids.test_distance_label.text = 'Test Mesafesi:'

        sc_one.ids.first_sample_header.text = 'Numune'
        sc_one.ids.second_sample_header.text = 'Numune'
        sc_one.ids.calibration.text = 'Kalibrasyon'
        sc_one.ids.test.text = 'Test'
        sc_one.ids.first_name.hint_text = 'Numune Adı'
        sc_one.ids.first_width.hint_text = 'Numune Genişliği (mm)'
        sc_one.ids.first_height.hint_text = 'Numune Uzunluğu (mm)'
        sc_one.ids.first_age.hint_text = 'Yaş (Ay)'
        sc_one.ids.second_name.hint_text = 'Numune Adı'
        sc_one.ids.second_width.hint_text = 'Numune Genişliği (mm)'
        sc_one.ids.second_height.hint_text = 'Numune Uzunluğu (mm)'
        sc_one.ids.second_age.hint_text = 'Yaş (Ay)'
        sc_one.ids.company_name.hint_text = 'Şirket Adı'
        sc_one.ids.operator_name.hint_text = 'Operatör Adı'
        sc_one.ids.shutdown.text = 'Kapat'

        sc_two.ids.graph.xlabel = 'Zaman (saniye)'
        sc_two.ids.graph.ylabel = 'Kuvvet (mN)'
        sc_two.ids.start.text = 'Başla'
        sc_two.ids.reset_pos.text = 'Pozisyonu Sıfırla'
        sc_two.ids.pre_page.text = 'Önceki Sayfa'
        sc_two.ids.btn.text = 'Sonuçlar'
        sc_two.ids.distance.text = 'Mesafe'
        sc_two.ids.force.text = 'Kuvvet'

        sc_three.ids.calc_res.text = 'Sonuçları Hesapla'
        sc_three.ids.create_pdf_label.text = 'Rapor Oluştur'
        sc_three.ids.pre_page.text = 'Önceki Sayfa'
        sc_three.ids.calc_res.text = 'Sonuçları Hesapla'
        sc_three.ids.max_static.text = '[b]Maksimum Static Sürtünme Katsayısı[/b]'
        sc_three.ids.mean_static.text = 'Ortalama Static Sürtünme Katsayısı'
        sc_three.ids.max_dynamic.text = 'Maksimum Dinamik Sürtünme Katsayısı'
        sc_three.ids.mean_dynamic.text = '[b]Ortalama Dinamik Sürtünme Katsayısı[/b]'
        sc_three.ids.date.text = 'Tarih'
        sc_three.ids.take_symbol.text = 'Logo Seç'   
                
    elif text == 'Russian':
        language = 'Russian'
        sc_five.ids.previous_page.text = 'Предыдущая страница'
        sc_five.ids.save.text = 'Спасать'
        sc_five.ids.reset_factory.text = 'Сброс к\n заводским настройкам'
        sc_five.ids.language.text = 'Изменение языка'
        sc_five.ids.normal_force_text.hint_text = 'Нормальный вес(грамм)'
        sc_five.ids.calib_text.hint_text = 'Калибровка силы'
        sc_five.ids.test_speed_text.hint_text = 'Миллиметр(mm/Секунда)'
        sc_five.ids.test_distance_text.hint_text = 'Миллиметр(mm)'
        sc_five.ids.normal_force_label.text = 'Нормальная сила:'
        sc_five.ids.calib_label.text = 'Калибровка силы:'
        sc_five.ids.test_speed_label.text = 'Скорость теста:'
        sc_five.ids.test_distance_label.text = 'Скорость теста:'

        sc_one.ids.first_sample_header.text = 'Образец'
        sc_one.ids.second_sample_header.text = 'Образец'
        sc_one.ids.calibration.text = 'Калибровка'
        sc_one.ids.test.text = 'Тест'
        sc_one.ids.first_name.hint_text = 'Образец имени'
        sc_one.ids.first_width.hint_text = 'Ширина образца (mm)'
        sc_one.ids.first_height.hint_text = 'Высота образца (mm)'
        sc_one.ids.first_age.hint_text = 'Возраст (Месяц)'
        sc_one.ids.second_name.hint_text = 'Образец имени'
        sc_one.ids.second_width.hint_text = 'Ширина образца (mm)'
        sc_one.ids.second_height.hint_text = 'Высота образца (mm)'
        sc_one.ids.second_age.hint_text = 'Возраст (Месяц)'
        sc_one.ids.company_name.hint_text = 'Название компании'
        sc_one.ids.operator_name.hint_text = 'Имя оператора'
        sc_one.ids.shutdown.text = 'Выключение'

        sc_two.ids.graph.xlabel = 'Время (секунда)'
        sc_two.ids.graph.ylabel = 'Сила (mN)'
        sc_two.ids.start.text = 'Начало'
        sc_two.ids.reset_pos.text = 'Положение сброса'
        sc_two.ids.pre_page.text = 'Предыдущая страница'
        sc_two.ids.btn.text = 'Результаты'
        sc_two.ids.distance.text = 'Расстояние'
        sc_two.ids.force.text = 'Сила'

        sc_three.ids.calc_res.text = 'Рассчитать результаты'
        sc_three.ids.create_pdf_label.text = 'создавать отчеты'
        sc_three.ids.pre_page.text = 'Предыдущая страница'
        sc_three.ids.max_static.text = '[b]Максимальный коэффициент статического трения[/b]'
        sc_three.ids.mean_static.text = 'Средний статический коэффициент трения'
        sc_three.ids.max_dynamic.text = 'Максимальный динамический коэффициент трения'
        sc_three.ids.mean_dynamic.text = '[b]Средний динамический коэффициент трения[/b]'
        sc_three.ids.date.text = 'Дата'
        sc_three.ids.take_symbol.text = 'Выберите логотип'
        
    if text == 'Arabic':
        language = 'Arabic'
        sc_five.ids.previous_page.text = 'الصفحة السابقة'
        sc_five.ids.save.text = 'حفظ'
        sc_five.ids.reset_factory.text = 'إعادة التعيين إلى إعدادات المصنع'
        sc_five.ids.language.text = 'تغيير اللغة'
        sc_five.ids.normal_force_text.text = 'الكتلة الطبيعية(غ)'
        sc_five.ids.calib_text.text = 'معايرة القوة'
        sc_five.ids.test_speed_text.text = 'سرعة الاختبار (مم/د)'
        sc_five.ids.normal_force_label.text = 'الكتلة الطبيعية:'
        sc_five.ids.calib_label.text = 'معايرة القوة:'
        sc_five.ids.test_speed_label.text = 'سرعة الاختبار:'

        sc_one.ids.first_sample_header.text = 'العينة'
        sc_one.ids.second_sample_header.text = 'العينة'
        sc_one.ids.calibration.text = 'معايرة'
        sc_one.ids.test.text = 'الاختبار'
        sc_one.ids.first_name.text = 'اسم العينة'
        sc_one.ids.first_width.text = 'العرض (مم)'
        sc_one.ids.first_height.text = 'الارتفاع (مم)'
        sc_one.ids.first_age.text = 'العمر (شهر)'
        sc_one.ids.second_name.text = 'اسم العينة'
        sc_one.ids.second_width.text = 'العرض (مم)'
        sc_one.ids.second_height.text = 'الارتفاع (مم)'
        sc_one.ids.second_age.text = 'العمر (شهر)'
        sc_one.ids.company_name.text = 'اسم الشركة'
        sc_one.ids.operator_name.text = 'اسم المشغل'
        sc_one.ids.shutdown.text = 'ايقاف التشغيل'

        sc_two.ids.graph.xlabel = 'الزمن (sec)'
        sc_two.ids.graph.ylabel = 'القوة (mN)'
        sc_two.ids.start.text = 'ابدأ'
        sc_two.ids.reset_pos.text = 'المكان السابق'
        sc_two.ids.pre_page.text = 'الصفحة السابقة'
        sc_two.ids.btn.text = 'النتيجة'
        sc_two.ids.distance.text = 'المسافة'
        sc_two.ids.force.text = 'القوة'

        sc_three.ids.calc_res.text = 'احسب النتيجة'
        sc_three.ids.create_pdf_label.text = 'إنشاء التقارير'
        sc_three.ids.pre_page.text = 'الصفحة السابقة'
        sc_three.ids.calc_res.text = 'احسب النتيجة'
        sc_three.ids.max_static.text = 'معامل الاحتكاك الساكن الاقصى'
        sc_three.ids.mean_static.text = 'متوسط معامل الاحتكاك الساكن الاقصى'
        sc_three.ids.max_dynamic.text = 'معامل الاحتكاك الديناميكي الاقصى'
        sc_three.ids.mean_dynamic.text = 'متوسط معامل الاحتكاك الديناميكي الاقصى'
        sc_three.ids.date.text = 'التاريخ'
        sc_three.ids.take_symbol.text = 'اختر شعارًا'

        
def def_language(language):
    text_file = '/home/pi/Cof-Tabs/language.txt'
    # Metin dosyasını açarak resmin adresini yazın
    with open(text_file, 'w') as file:
        file.write(language)


screen_manager = ScreenManager()

screen_manager.add_widget(ScreenOne(name="screen_one"))
screen_manager.add_widget(ScreenTwo(name="screen_two"))
screen_manager.add_widget(ScreenThree(name="screen_three"))
screen_manager.add_widget(ScreenFive(name="screen_five"))

sc_one = screen_manager.get_screen('screen_one')
sc_two = screen_manager.get_screen('screen_two')
sc_three = screen_manager.get_screen('screen_three')
sc_five = screen_manager.get_screen('screen_five')


class AwesomeApp(App):
    def build(self):
        Window.clearcolor = (1, 1, 1, 1)
        Window.size = (800, 480)  # pencere boyutu
        #Window.size = (1920, 1080)
        Window.fullscreen = True
        
        #Burada sistem kapanınca son dilin ne olduğu bilgisi okunuyor ve arayüzün dili değişiyor.
        file_path = '/home/pi/Cof-Tabs/language.txt'
        try:
            with open(file_path, 'r') as file:
                content = file.read()
        except FileNotFoundError:
            print("File not found:", file_path)
        except Exception as e:
            print("Error while reading file:", str(e))
        language_change_gl(content)
        #Buraya kadar.

        return screen_manager


if __name__ == "__main__":
    AwesomeApp().run()

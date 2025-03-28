import datetime
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.enums import TA_CENTER
from reportlab.platypus import Table, TableStyle, Paragraph
from reportlab.pdfgen import canvas
import os
from os import popen
import shutil
import subprocess

# UTF-8 karakter kodlamasını ayarla
pdfmetrics.registerFont(TTFont('Arial', 'arial.ttf', 'UTF-8'))


global pdf

class multi():

    # Rapor başlığı fonksiyonu
    def baslik_yazdir(self, pdf, max_static, mean_static, max_dynamic, mean_dynamic, sample1, sample2, forces, language):
        text_file = '/home/pi/Cof-Tabs/logo.txt'
        with open(text_file, 'r', encoding="utf-8") as file:
            content = file.read()
            #content[-1] = content[-1].strip()

        pdf.drawImage(content, 50,720, mask='auto')
        if sample2.name == "":
            if language == 'Russian':
                pdf.setFont("Arial", 18)
                pdf.drawCentredString(300, 720, "Результаты испытаний коэффициента трения")
                pdf.line(50, 700, 550, 700)
                pdf.line(50, 100, 550, 100)
                date_today = datetime.datetime.today()
                date_and_time = date_today.strftime("%Y_%m_%d__%H_%M_%S")

                # Tarih ve saat bilgilerini ekle
                now = datetime.datetime.now()
                tarih = now.strftime("%d.%m.%Y")
                saat = now.strftime("%H:%M")
                pdf.setFont("Arial", 12)
                pdf.drawRightString(550, 770, "Дата: {}".format(tarih))
                pdf.drawRightString(550, 750, "Время: {}".format(saat))

                # Ad bilgisi yazdır
                pdf.setFont("Arial", 12)
                pdf.drawString(50, 660, "Стандарт:      ISO 8295")
                pdf.drawString(50, 640, "Название компании:   {}".format(sample1.company_name))
                pdf.drawString(50, 620, "Имя оператора:   {}".format(sample1.operator_name))
                pdf.drawString(50, 600, "Нормальный вес(грамм):   {}".format(sample1.testing_weight))
                pdf.drawString(50, 580, "Образец:   {}".format(sample1.name))
                pdf.drawString(50, 560, "Ширина образца (mm):   {}".format(sample1.width))
                pdf.drawString(50, 540, "Высота образца (mm):   {}".format(sample1.height))
                pdf.drawString(50, 520, "Возраст (Месяц):   {}".format(sample1.age))
                pdf.drawString(50, 500, "Тестирование против:   Тот же образец")
                pdf.drawString(50, 480, "Максимальный коэффициент статического трения:   {}".format(max_static))
                pdf.drawString(50, 460, "Средний статический коэффициент трения:   {}".format(mean_static))
                pdf.drawString(50, 440, "Максимальный динамический коэффициент трения:   {}".format(max_dynamic))
                pdf.drawString(50, 420, "Средний динамический коэффициент трения:   {}".format(mean_dynamic))
               
            if language == 'Turkish':
                pdf.setFont("Arial", 18)
                pdf.drawCentredString(300, 720, "COF Test Sonuçları")
                pdf.line(50, 700, 550, 700)
                date_today = datetime.datetime.today()
                date_and_time = date_today.strftime("%Y_%m_%d__%H_%M_%S")

                # Tarih ve saat bilgilerini ekle
                now = datetime.datetime.now()
                tarih = now.strftime("%d.%m.%Y")
                saat = now.strftime("%H:%M")
                pdf.setFont("Arial", 12)
                pdf.drawRightString(550, 770, "Tarih: {}".format(tarih))
                pdf.drawRightString(550, 750, "Zaman: {}".format(saat))

                # Ad bilgisi yazdır
                pdf.setFont("Arial", 12)
                pdf.drawString(50, 660, "Standart:      ISO 8295")
                pdf.drawString(50, 640, "Şirket Adı:   {}".format(sample1.company_name))
                pdf.drawString(50, 620, "Operatör Adı:   {}".format(sample1.operator_name))
                pdf.drawString(50, 600, "Test Ağırlığı(gr):   {}".format(sample1.testing_weight))
                pdf.drawString(50, 580, "Numune Adı:   {}".format(sample1.name))
                pdf.drawString(50, 560, "Numune Genişliği (mm):   {}".format(sample1.width))
                pdf.drawString(50, 540, "Numune Uzunluğu (mm):   {}".format(sample1.height))
                pdf.drawString(50, 520, "Numune Yaşı (ay):   {}".format(sample1.age))
                pdf.drawString(50, 500, "Test Metodu:   Aynı Numune")
                pdf.drawString(50, 480, "Maksimum Statik Sürtünme Katsayısı:   {}".format(max_static))
                pdf.drawString(50, 460, "Ortalama Statik Sürtünme Katsayısı:   {}".format(mean_static))
                pdf.drawString(50, 440, "Maksimum Dinamik Sürtünme Katsayısı:   {}".format(max_dynamic))
                pdf.drawString(50, 420, "Ortalama Dinamik Sürtünme Katsayısı:   {}".format(mean_dynamic))
                        
            if language == 'English':
                pdf.setFont("Arial", 18)
                pdf.drawCentredString(300, 720, "COF Test Results")
                pdf.line(50, 700, 550, 700)
                date_today = datetime.datetime.today()
                date_and_time = date_today.strftime("%Y_%m_%d__%H_%M_%S")

                # Tarih ve saat bilgilerini ekle
                now = datetime.datetime.now()
                tarih = now.strftime("%d.%m.%Y")
                saat = now.strftime("%H:%M")
                pdf.setFont("Arial", 12)
                pdf.drawRightString(550, 770, "Date: {}".format(tarih))
                pdf.drawRightString(550, 750, "Time: {}".format(saat))

                # Ad bilgisi yazdır
                pdf.setFont("Arial", 12)
                pdf.drawString(50, 660, "Standard:      ISO 8295")
                pdf.drawString(50, 640, "Company Name:   {}".format(sample1.company_name))
                pdf.drawString(50, 620, "Operator Name:   {}".format(sample1.operator_name))
                pdf.drawString(50, 600, "Testing Weight(gr):   {}".format(sample1.testing_weight))
                pdf.drawString(50, 580, "Sample Name:   {}".format(sample1.name))
                pdf.drawString(50, 560, "Sample Width (mm):   {}".format(sample1.width))
                pdf.drawString(50, 540, "Sample Height (mm):   {}".format(sample1.height))
                pdf.drawString(50, 520, "Sample Age (months):   {}".format(sample1.age))
                pdf.drawString(50, 500, "Testing Against:   The same sample")
                pdf.drawString(50, 480, "Maximum Static Coefficient of Friction:   {}".format(max_static))
                pdf.drawString(50, 460, "Mean Static Coefficient of Friction:   {}".format(mean_static))
                pdf.drawString(50, 440, "Maximum Dynamic Coefficient of Friction:   {}".format(max_dynamic))
                pdf.drawString(50, 420, "Mean Dynamic Coefficient of Friction:   {}".format(mean_dynamic))
            pdf.drawImage('/home/pi/Cof-Tabs/graph.png',30,120,550,250, mask='auto')
            
        else:
            if language == 'Russian':
                pdf.setFont("Arial", 18)
                pdf.drawCentredString(300, 720, "Результаты испытаний коэффициента трения")
                pdf.line(50, 700, 550, 700)
                date_today = datetime.datetime.today()
                date_and_time = date_today.strftime("%Y_%m_%d__%H_%M_%S")

                # Tarih ve saat bilgilerini ekle
                now = datetime.datetime.now()
                tarih = now.strftime("%d.%m.%Y")
                saat = now.strftime("%H:%M")
                pdf.setFont("Arial", 12)
                pdf.drawRightString(550, 770, "Дата: {}".format(tarih))
                pdf.drawRightString(550, 750, "Время: {}".format(saat))

                # Ad bilgisi yazdır
                pdf.setFont("Arial", 12)
                pdf.drawString(50, 660, "Стандарт:      ISO 8295")
                pdf.drawString(50, 640, "Название компании:   {}".format(sample1.company_name))
                pdf.drawString(50, 620, "Имя оператора:   {}".format(sample1.operator_name))
                pdf.drawString(50, 600, "Нормальный вес(грамм):   {}".format(sample1.testing_weight))
                pdf.drawString(50, 580, "Образец:   {}".format(sample1.name))
                pdf.drawString(50, 560, "Ширина образца (mm):   {}".format(sample1.width))
                pdf.drawString(50, 540, "Высота образца (mm):   {}".format(sample1.height))
                pdf.drawString(50, 520, "Возраст (Месяц):   {}".format(sample1.age))
                pdf.drawString(50, 500, "Тестирование против:   Другой образец")
                pdf.drawString(50, 480, "Имя второго образца:   {}".format(sample2.name))
                pdf.drawString(50, 460, "Ширина второго образца (mm):   {}".format(sample2.width))
                pdf.drawString(50, 440, "Высота второго образца (mm):   {}".format(sample2.height))
                pdf.drawString(50, 420, "Возраст второй пробы (Месяц):   {}".format(sample2.age))
                pdf.drawString(50, 400, "Максимальный коэффициент статического трения:   {}".format(max_static))
                pdf.drawString(50, 380, "Средний статический коэффициент трения:   {}".format(mean_static))
                pdf.drawString(50, 360, "Максимальный динамический коэффициент трения:   {}".format(max_dynamic))
                pdf.drawString(50, 340, "Средний динамический коэффициент трения:   {}".format(mean_dynamic))
            
            if language == 'Turkish':
                pdf.setFont("Arial", 18)
                pdf.drawCentredString(300, 720, "COF Test Sonuçları")
                pdf.line(50, 700, 550, 700)
                date_today = datetime.datetime.today()
                date_and_time = date_today.strftime("%Y_%m_%d__%H_%M_%S")

                # Tarih ve saat bilgilerini ekle
                now = datetime.datetime.now()
                tarih = now.strftime("%d.%m.%Y")
                saat = now.strftime("%H:%M")
                pdf.setFont("Arial", 12)
                pdf.drawRightString(550, 770, "Tarih: {}".format(tarih))
                pdf.drawRightString(550, 750, "Zaman: {}".format(saat))

                # Ad bilgisi yazdır
                pdf.setFont("Arial", 12)
                pdf.drawString(50, 660, "Standart:      ISO 8295")
                pdf.drawString(50, 640, "şirket Adı:   {}".format(sample1.company_name))
                pdf.drawString(50, 620, "Operatör Adı:   {}".format(sample1.operator_name))
                pdf.drawString(50, 600, "Test Ağırlığı(gr):   {}".format(sample1.testing_weight))
                pdf.drawString(50, 580, "Numune Adı:   {}".format(sample1.name))
                pdf.drawString(50, 560, "Numune Genişliği (mm):   {}".format(sample1.width))
                pdf.drawString(50, 540, "Numune Uzunluğu (mm):   {}".format(sample1.height))
                pdf.drawString(50, 520, "Numune Yaşı (ay):   {}".format(sample1.age))
                pdf.drawString(50, 500, "İkinci Numune Adı:   {}".format(sample2.name))
                pdf.drawString(50, 480, "İkinci Numune Genişliği (mm):   {}".format(sample2.width))
                pdf.drawString(50, 460, "İkinci Numune Uzunluğu (mm):   {}".format(sample2.height))
                pdf.drawString(50, 440, "İkinci Numune Yaşı (ay):   {}".format(sample2.age))
                pdf.drawString(50, 420, "Test Metodu:   Farklı Numune")
                pdf.drawString(50, 400, "Maksimum Statik Sürtünme Katsayısı:   {}".format(max_static))
                pdf.drawString(50, 380, "Ortalama Statik Sürtünme Katsayısı:   {}".format(mean_static))
                pdf.drawString(50, 360, "Maksimum Dinamik Sürtünme Katsayısı:   {}".format(max_dynamic))
                pdf.drawString(50, 340, "Ortalama Dinamik Sürtünme Katsayısı:   {}".format(mean_dynamic))
 
            if language == 'English':
                pdf.setFont("Arial", 18)
                pdf.drawCentredString(300, 720, "COF Test Results")
                pdf.line(50, 700, 550, 700)
                date_today = datetime.datetime.today()
                date_and_time = date_today.strftime("%Y_%m_%d__%H_%M_%S")

                # Tarih ve saat bilgilerini ekle
                now = datetime.datetime.now()
                tarih = now.strftime("%d.%m.%Y")
                saat = now.strftime("%H:%M")
                pdf.setFont("Arial", 12)
                pdf.drawRightString(550, 770, "Date: {}".format(tarih))
                pdf.drawRightString(550, 750, "Time: {}".format(saat))

                # Ad bilgisi yazdır
                pdf.setFont("Arial", 12)
                pdf.drawString(50, 660, "Standard:      ISO 8295")
                pdf.drawString(50, 640, "Company Name:   {}".format(sample1.company_name))
                pdf.drawString(50, 620, "Operator Name:   {}".format(sample1.operator_name))
                pdf.drawString(50, 600, "Testing Weight(gr):   {}".format(sample1.testing_weight))
                pdf.drawString(50, 580, "Sample Name:   {}".format(sample1.name))
                pdf.drawString(50, 560, "Sample Width (mm):   {}".format(sample1.width))
                pdf.drawString(50, 540, "Sample Height (mm):   {}".format(sample1.height))
                pdf.drawString(50, 520, "Sample Age (months):   {}".format(sample1.age))
                pdf.drawString(50, 500, "Testing Against:   Different Sample")
                pdf.drawString(50, 480, "Second Sample Name:   {}".format(sample2.name))
                pdf.drawString(50, 460, "Second Sample Width (mm):   {}".format(sample2.width))
                pdf.drawString(50, 440, "Second Sample Height (mm):   {}".format(sample2.height))
                pdf.drawString(50, 420, "Second Sample Age (months):   {}".format(sample2.age))
                pdf.drawString(50, 400, "Maximum Static Coefficient of Friction:   {}".format(max_static))
                pdf.drawString(50, 380, "Mean Static Coefficient of Friction:   {}".format(mean_static))
                pdf.drawString(50, 360, "Maximum Dynamic Coefficient of Friction:   {}".format(max_dynamic))
                pdf.drawString(50, 340, "Mean Dynamic Coefficient of Friction:   {}".format(mean_dynamic))
            pdf.drawImage('/home/pi/Cof-Tabs/graph.png',30,70,550,250, mask='auto')

    def create_pdf_ones(self, max_static, mean_static, max_dynamic, mean_dynamic, sample1, sample2, forces, language):
        # Yeni bir PDF dosyası oluştur
        date_today = datetime.datetime.today()
        date_and_time = date_today.strftime("%Y_%m_%d__%H_%M_%S")
        filename = "/home/pi/Cof-Tabs/rapor/" + date_and_time + ".pdf"
        pdf = canvas.Canvas(filename, pagesize=letter)

        # Sayfa başlığını yazdır
        self.baslik_yazdir(pdf,max_static, mean_static, max_dynamic, mean_dynamic, sample1, sample2, forces, language)

        date_today = datetime.datetime.today()
        date_and_time = date_today.strftime("%Y_%m_%d__%H_%M_%S")
        
        pdf.save()
        
        name_usb = os.listdir("/media/pi")
        print(len(name_usb))
        for x in range(len(name_usb)):
            print(name_usb[x])
            str = ""
            str = str.join(name_usb[x])
            mount_dir = "/media/pi/" + str
            print(mount_dir)
            try:
                subprocess.run(["sudo", "chmod", "-R", "777", mount_dir], check=True)
            except Exception as e:
                print(f"Hata oluştu: {e}")
                
            dir = os.path.join(mount_dir, "COF_Reports")
            try:
                if not os.path.exists(dir):
                    os.mkdir(dir)
            except:
                pass
            mount_dir = mount_dir + "/COF_Reports"

            #Burada sadece o an üretilen dosya kaıyt ediliyor.
            dosya_yolu = "/home/pi/Cof-Tabs/rapor/" + date_and_time + ".pdf"
            
            try: 
                shutil.copy(dosya_yolu, mount_dir)
            except Exception as e:
                print(f"Kopyalama sırasında bir hata: {e}")
            
            #self.copy_folder_contents(dosya_yolu, mount_dir)
    
    def create_pdf(self, max_static, mean_static, max_dynamic, mean_dynamic, sample1, sample2, forces, language):
        # Yeni bir PDF dosyası oluştur
        """date_today = datetime.datetime.today()
        date_and_time = date_today.strftime("%Y_%m_%d__%H_%M_%S")
        filename = "/home/pi/Cof-Tabs/rapor/" + date_and_time + ".pdf"
        pdf = canvas.Canvas(filename, pagesize=letter)

        # Sayfa başlığını yazdır
        self.baslik_yazdir(pdf,max_static, mean_static, max_dynamic, mean_dynamic, sample1, sample2, forces, language)

        date_today = datetime.datetime.today()
        date_and_time = date_today.strftime("%Y_%m_%d__%H_%M_%S")
        
        pdf.save()"""
        
        name_usb = os.listdir("/media/pi")
        print(len(name_usb))
        for x in range(len(name_usb)):
            print(name_usb[x])
            str = ""
            str = str.join(name_usb[x])
            mount_dir = "/media/pi/" + str
            
            try:
                subprocess.run(["sudo", "chmod", "-R", "777", mount_dir], check=True)
            except Exception as e:
                print(f"Hata oluştu: {e}")

            print(mount_dir)
            dir = os.path.join(mount_dir, "COF_Reports")
            try:
                if not os.path.exists(dir):
                    os.mkdir(dir)
            except:
                pass
            mount_dir = mount_dir + "/COF_Reports"

            
            dosya_yolu = "/home/pi/Cof-Tabs/rapor"
    
            self.copy_folder_contents(dosya_yolu, mount_dir)
        """try:
            #shutil.copytree(dosya_yolu, mount_dir)
            #shutil.copy(filename, mount_dir)
            print("Kayıt etti")
            #shutil.copy(filename_json, mount_dir)
        except:
            print("usb kayıt edilmedi")"""
    
    def copy_folder_contents(self, source_folder, target_folder):
        try:
            for item in os.listdir(source_folder):
                source_item = os.path.join(source_folder, item)
                target_item = os.path.join(target_folder, item)
                if os.path.isfile(source_item):
                    shutil.copy(source_item, target_item)
                elif os.path.isdir(source_item):
                    shutil.copytree(source_item, target_item)
            #print("Folder contents copied successfully.")
        except Exception as e:
            print("Error while copying folder contents:", str(e))
    

        

import datetime
import shutil
import os
from os import popen
from fpdf import FPDF
from json_dumper import JsonHandler

json_out = JsonHandler()

class sample:
    name = "Sample Name"
    width = 10
    height = 20
    age = 0


class fpdf_handler(FPDF):
    date = "0"
    time = "0"
    date_today = "0"
    date_and_time = "0"

    def set_time(self):
        self.date_today = datetime.datetime.today()
        self.date = self.date_today.strftime("%d:%m:%Y")
        self.time = self.date_today.strftime("%H:%M:%S")
        self.date_and_time = self.date_today.strftime("%Y_%m_%d__%H_%M_%S")

    def header(self):
        # Set up a logo
        self.image('/home/pi/Cof-Tabs/mini_logo.png', 10, 8, 33)
        self.set_font('Arial', 'I', 15)
        # Add test time
        self.cell(150)
        self.cell(0, 0, 'Date: ' + self.date, ln=1, align="L")
        self.cell(150)
        self.cell(0, 10, 'Time: ' + self.time, ln=1, align="L")
        self.cell(0, 10, "COF Test Results", ln=1, align="C")
        # Line break
        self.ln(5)
        self.set_line_width(1)
        self.line(x1=10, y1=30, x2=200, y2=30)
        # self.ln(10)

    def footer(self):
        self.set_y(-10)
        self.set_font('Arial', 'I', 12)
        self.set_line_width(1)
        self.line(x1=10, y1=285, x2=200, y2=285)
        self.cell(0, 10, "Alarge Laboratory Test Technology - https://www.alarge.com.tr/en/ - info@alarge.com.tr")

    def graph_to_pdf(self, choise):
        if choise == 1:
            self.image('/home/pi/Cof-Tabs/graph.png', x=30, y=160, w=150)
        else:
            self.image('/home/pi/Cof-Tabs/graph.png', x=30, y=190, w=150)

    def create_pdf(self, max_static, mean_static, max_dynamic, mean_dynamic, sample1, sample2, forces, language):
        self.set_time()
        self.add_page()
        self.set_font('Times', '', 12)
        if sample2.name == "":
            self.single_table(sample1, max_static, mean_static, max_dynamic, mean_dynamic, language)
            self.graph_to_pdf(1)
        else:
            self.diff_table(sample1, sample2, max_static, mean_static, max_dynamic, mean_dynamic, language)
            self.graph_to_pdf(2)

        filename = "/home/pi/Cof-Tabs/rapor/" + self.date_and_time + ".pdf"
        name_usb = os.listdir("/media/pi")
        str = ""
        str = str.join(name_usb)
        mount_dir = "/media/pi/" + str
        print(mount_dir)
        dir = os.path.join(mount_dir, "COF_Reports")
        try:
            if not os.path.exists(dir):
                os.mkdir(dir)
        except:
            pass
        mount_dir = mount_dir + "/COF_Reports"
        self.output(filename)
        filename_json = "/home/pi/Cof-Tabs/rapor/COF_Test_" + self.date_and_time + ".json"

        try:
            shutil.copy(filename, mount_dir)
            shutil.copy(filename_json, mount_dir)
        except:
            print("usb kayıt edilmedi")

    def single_table(self, sample, max_dynamic, mean_dynamic, max_static, mean_static, language):
        if language == 'English':
            data = [['Standard: ', "ISO 8295"],
                    ['Company Name: ', str(sample.company_name)],
                    ['Operator Name: ', str(sample.operator_name)],
                    ['Testing Weight(gr): ', str(sample.testing_weight)],
                    ['Sample Name: ', str(sample.name)],
                    ['Sample Width(mm): ', str(sample.width)],
                    ['Sample Height(mm): ', str(sample.height)],
                    ['Sample Age(months): ', str(sample.age)],
                    ['Testing Against: ', 'The same sample'],
                    ['Max Static Coefficient of Friction: ', str(max_static)],
                    ['Mean Static Coefficient of Friction: ', str(mean_static)],
                    ['Max Dynamic Coefficient of Friction: ', str(max_dynamic)],
                    ['Mean Dynamic Coefficient of Friction: ', str(mean_dynamic)]
                    ]
        if language == 'Turkish':
            data = [['Standart: ', "ISO 8295"],
                    ['Şirket Adı: ', str(sample.company_name)],
                    ['Operatör Adı: ', str(sample.operator_name)],
                    ['Test Ağırlığı(gr): ', str(sample.testing_weight)],
                    ['Numune Adı: ', str(sample.name)],
                    ['Numune Genişliği(mm): ', str(sample.width)],
                    ['Numune Yüksekliği(mm): ', str(sample.height)],
                    ['Numune Yaşı(ay): ', str(sample.age)],
                    ['Test Türü: ', 'Aynı Numune'],
                    ['Maksimum Statik Sürtünme Katsayısı: ', str(max_static)],
                    ['Ortalama Statik Sürtünme Katsayısı: ', str(mean_static)],
                    ['Maksimum Dinamik Sürtünme Katsayısı: ', str(max_dynamic)],
                    ['Ortalama Statik Sürtünme Katsayısı: ', str(mean_dynamic)]
                    ]
        spacing = 2
        self.set_font("Arial", size=12)
        col_width = self.w / 2.2
        row_height = self.font_size
        for row in data:
            for item in row:
                self.cell(col_width, row_height * spacing,
                          txt=item, border=0)
            self.ln(row_height * spacing)

    def diff_table(self, sample1, sample2, max_static, mean_static, max_dynamic, mean_dynamic):
        data = [['Standard: ', "ISO 8295"],
                ['Company Name: ', str(sample1.company_name)],
                ['Operator Name: ', str(sample1.operator_name)],
                ['Testing Weight(gr): ', str(sample1.testing_weight)],
                ['Sample Name: ', str(sample1.name)],
                ['Sample Width(mm): ', str(sample1.width)],
                ['Sample Height(mm): ', str(sample1.height)],
                ['Sample Age: ', str(sample1.age)],
                ['Testing Against: ', 'Different Sample'],
                ['Second Sample Name: ', str(sample2.name)],
                ['Second Sample Width(mm): ', str(sample2.width)],
                ['Second Sample Height(mm): ', str(sample2.height)],
                ['Second Sample Age(months): ', str(sample2.age)],
                ['Max Static Coefficient of Friction: ', str(max_dynamic)],
                ['Mean Static Coefficient of Friction: ', str(mean_dynamic)],
                ['Max Dynamic Coefficient of Friction: ', str(max_static)],
                ['Mean Dynamic Coefficient of Friction: ', str(mean_static)]
                ]
        spacing = 2
        self.set_font("Arial", size=12)
        col_width = self.w / 2.2
        row_height = self.font_size
        for row in data:
            for item in row:
                self.cell(col_width, row_height * spacing,
                          txt=item, border=0)
            self.ln(row_height * spacing)



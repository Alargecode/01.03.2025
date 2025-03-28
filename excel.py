from openpyxl import Workbook
from openpyxl.drawing.image import Image as XLImage
import datetime

class excel():

    def create_excel_report(self, max_static, mean_static, max_dynamic, mean_dynamic, sample1, sample2, forces, language):

        # Excel dosyası oluştur
        workbook = Workbook()
        sheet = workbook.active

        # Resmi eklemek istediğiniz hücrenin konumunu belirleyin
        image_cell = 'A1'

        path_adress = '/home/pi/Cof-Tabs/logo.txt'
        with open(path_adress, 'r') as file:
            content = file.read()
        img = XLImage(content)

        sheet.add_image(img, image_cell)
        
        graph_cell = 'A20'
        graph = XLImage("/home/pi/Cof-Tabs/graph.png")
        graph.width = 550  
        graph.height = 250
        sheet.add_image(graph, graph_cell)

        if sample2.name == "":
            if language == 'Russian':
                sheet['C1'] = "Результаты испытаний коэффициента трения"
                sheet['B3'] = "Стандарт:"
                sheet['E3'] = "ISO 8295"
                sheet['B4'] = "Название компании:"
                sheet['E4'] = sample1.company_name
                sheet['B5'] = "Имя оператора:"
                sheet['E5'] = sample1.operator_name
                sheet['B6'] = "Нормальный вес(грамм):"
                sheet['E6'] = sample1.testing_weight
                sheet['B7'] = "Образец:"
                sheet['E7'] = sample1.name
                sheet['B8'] = "Ширина образца (mm):"
                sheet['E8'] = sample1.width
                sheet['B9'] = "Высота образца (mm):"
                sheet['E9'] = sample1.height
                sheet['B10'] = "Возраст (Месяц):"
                sheet['E10'] = sample1.age
                sheet['B11'] = "Тестирование против:"
                sheet['E11'] = "Тот же образец"
                sheet['B12'] = "Максимальный коэффициент статического трения:"
                sheet['E12'] = max_static
                sheet['B13'] = "Средний статический коэффициент трения:"
                sheet['E13'] = mean_static
                sheet['B14'] = "Максимальный динамический коэффициент трения:"
                sheet['E14'] = max_dynamic
                sheet['B15'] = "Средний динамический коэффициент трения:"
                sheet['E15'] = mean_dynamic
            
            if language == 'Turkish':
                sheet['C1'] = "COF Test Sonuçları"
                sheet['B3'] = "Standart:"
                sheet['E3'] = "ISO 8295"
                sheet['B4'] = "Şirket Adı:"
                sheet['E4'] = sample1.company_name
                sheet['B5'] = "Operatör Adı:"
                sheet['E5'] = sample1.operator_name
                sheet['B6'] = "Test Ağırlığı(gr):"
                sheet['E6'] = sample1.testing_weight
                sheet['B7'] = "Numune Adı:"
                sheet['E7'] = sample1.name
                sheet['B8'] = "Numune Genişliği (mm):"
                sheet['E8'] = sample1.width
                sheet['B9'] = "Numune Uzunluğu (mm):"
                sheet['E9'] = sample1.height
                sheet['B10'] = "Numune Yaşı (ay):"
                sheet['E10'] = sample1.age
                sheet['B11'] = "Test Metodu:"
                sheet['E11'] = "Aynı Numune"
                sheet['B12'] = "Maksimum Statik Sürtünme Katsayısı:"
                sheet['E12'] = max_static
                sheet['B13'] = "Ortalama Statik Sürtünme Katsayısı:"
                sheet['E13'] = mean_static
                sheet['B14'] = "Maksimum Dinamik Sürtünme Katsayısı:"
                sheet['E14'] = max_dynamic
                sheet['B15'] = "Ortalama Dinamik Sürtünme Katsayısı:"
                sheet['E15'] = mean_dynamic
            
            if language == 'English':
                sheet['C1'] = "COF Test Results"
                sheet['B3'] = "Standard:"
                sheet['E3'] = "ISO 8295"
                sheet['B4'] = "Company Name:"
                sheet['E4'] = sample1.company_name
                sheet['B5'] = "Operator Name:"
                sheet['E5'] = sample1.operator_name
                sheet['B6'] = "Testing Weight(gr):"
                sheet['E6'] = sample1.testing_weight
                sheet['B7'] = "Sample Name:"
                sheet['E7'] = sample1.name
                sheet['B8'] = "Sample Width (mm):"
                sheet['E8'] = sample1.width
                sheet['B9'] = "Sample Height (mm)"
                sheet['E9'] = sample1.height
                sheet['B10'] = "Sample Age (months)"
                sheet['E10'] = sample1.age
                sheet['B11'] = "Testing Against:"
                sheet['E11'] = "The same sample"
                sheet['B12'] = "Maximum Static Coefficient of Friction:"
                sheet['E12'] = max_static
                sheet['B13'] = "Mean Static Coefficient of Friction:"
                sheet['E13'] = mean_static
                sheet['B14'] = "Maximum Dynamic Coefficient of Friction:"
                sheet['E14'] = max_dynamic
                sheet['B15'] = "Mean Dynamic Coefficient of Friction:"
                sheet['E15'] = mean_dynamic

        else:
            if language == 'Russian':
                sheet['C1'] = "Результаты испытаний коэффициента трения"
                sheet['B3'] = "Стандарт:"
                sheet['E3'] = "ISO 8295"
                sheet['B4'] = "Название компании:"
                sheet['E4'] = sample1.company_name
                sheet['B5'] = "Имя оператора:"
                sheet['E5'] = sample1.operator_name
                sheet['B6'] = "Нормальный вес(грамм):"
                sheet['E6'] = sample1.testing_weight
                sheet['B7'] = "Образец:"
                sheet['E7'] = sample1.name
                sheet['B8'] = "Ширина образца (mm):"
                sheet['E8'] = sample1.width
                sheet['B9'] = "Высота образца (mm):"
                sheet['E9'] = sample1.height
                sheet['B10'] = "Возраст (Месяц):"
                sheet['E10'] = sample1.age
                sheet['B11'] = "Имя второго образца:"
                sheet['E11'] = sample2.name
                sheet['B12'] = "Ширина второго образца (mm):"
                sheet['E12'] = sample2.width
                sheet['B13'] = "Высота второго образца (mm):"
                sheet['E13'] = sample2.height
                sheet['B14'] = "Возраст второй пробы (Месяц):"
                sheet['E14'] = sample2.age
                sheet['B15'] = "Тестирование против:"
                sheet['E15'] = "Тот же образец"
                sheet['B16'] = "Максимальный коэффициент статического трения:"
                sheet['E16'] = max_static
                sheet['B17'] = "Средний статический коэффициент трения:"
                sheet['E17'] = mean_static
                sheet['B18'] = "Максимальный динамический коэффициент трения:"
                sheet['E18'] = max_dynamic
                sheet['B19'] = "Средний динамический коэффициент трения:"
                sheet['E19'] = mean_dynamic
            
            if language == 'Turkish':
                sheet['C1'] = "COF Test Sonuçları"
                sheet['B3'] = "Standart:"
                sheet['E3'] = "ISO 8295"
                sheet['B4'] = "Şirket Adı:"
                sheet['E4'] = sample1.company_name
                sheet['B5'] = "Operatör Adı:"
                sheet['E5'] = sample1.operator_name
                sheet['B6'] = "Test Ağırlığı(gr):"
                sheet['E6'] = sample1.testing_weight
                sheet['B7'] = "Numune Adı:"
                sheet['E7'] = sample1.name
                sheet['B8'] = "Numune Genişliği (mm):"
                sheet['E8'] = sample1.width
                sheet['B9'] = "Numune Uzunluğu (mm):"
                sheet['E9'] = sample1.height
                sheet['B10'] = "Numune Yaşı (ay):"
                sheet['E10'] = sample1.age
                sheet['B11'] = "İkinci Numune Adı:"
                sheet['E11'] = sample2.name
                sheet['B12'] = "İkinci Numune Genişliği (mm):"
                sheet['E12'] = sample2.width
                sheet['B13'] = "İkinci Numune Uzunluğu (mm):"
                sheet['E13'] = sample2.height
                sheet['B14'] = "İkinci Numune Yaşı (ay):"
                sheet['E14'] = sample2.age
                sheet['B15'] = "Test Metodu:"
                sheet['E15'] = "Aynı Numune"
                sheet['B16'] = "Maksimum Statik Sürtünme Katsayısı:"
                sheet['E16'] = max_static
                sheet['B17'] = "Ortalama Statik Sürtünme Katsayısı:"
                sheet['E17'] = mean_static
                sheet['B18'] = "Maksimum Dinamik Sürtünme Katsayısı:"
                sheet['E18'] = max_dynamic
                sheet['B19'] = "Ortalama Dinamik Sürtünme Katsayısı:"
                sheet['E19'] = mean_dynamic
            
            if language == 'English':
                sheet['C1'] = "COF Test Results"
                sheet['B3'] = "Standard:"
                sheet['E3'] = "ISO 8295"
                sheet['B4'] = "Company Name:"
                sheet['E4'] = sample1.company_name
                sheet['B5'] = "Operator Name:"
                sheet['E5'] = sample1.operator_name
                sheet['B6'] = "Testing Weight(gr):"
                sheet['E6'] = sample1.testing_weight
                sheet['B7'] = "Sample Name:"
                sheet['E7'] = sample1.name
                sheet['B8'] = "Sample Width (mm):"
                sheet['E8'] = sample1.width
                sheet['B9'] = "Sample Height (mm)"
                sheet['E9'] = sample1.height
                sheet['B10'] = "Sample Age (months)"
                sheet['E10'] = sample1.age
                sheet['B11'] = "Second Sample Name:"
                sheet['E11'] = sample2.name
                sheet['B12'] = "Second Sample Width (mm):"
                sheet['E12'] = sample2.width
                sheet['B13'] = "Second Sample Height (mm):"
                sheet['E13'] = sample2.height
                sheet['B14'] = "Second Sample Age (months):"
                sheet['E14'] = sample2.age
                sheet['B15'] = "Testing Against:"
                sheet['E15'] = "The same sample"
                sheet['B16'] = "Maximum Static Coefficient of Friction:"
                sheet['E16'] = max_static
                sheet['B17'] = "Mean Static Coefficient of Friction:"
                sheet['E17'] = mean_static
                sheet['B18'] = "Maximum Dynamic Coefficient of Friction:"
                sheet['E18'] = max_dynamic
                sheet['B19'] = "Mean Dynamic Coefficient of Friction:"
                sheet['E19'] = mean_dynamic



        # Excel dosyasını kaydedin
        date_today = datetime.datetime.today()
        date_and_time = date_today.strftime("%Y_%m_%d__%H_%M_%S")
        filename = "/home/pi/Cof-Tabs/excel/" + date_and_time + ".xlsx"
        workbook.save(filename)



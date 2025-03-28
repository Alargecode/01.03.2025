from openpyxl import Workbook
from openpyxl.drawing.image import Image

# Excel dosyası oluştur
workbook = Workbook()
sheet = workbook.active

# Resmi eklemek istediğiniz hücrenin konumunu belirleyin
image_cell = 'A1'

path_adress = '/home/pi/Cof-Tabs/logo.txt'
with open(path_adress, 'r') as file:
    content = file.read()
img = Image(content)


# Resmi ekleyin
img.width = 100  # Resim genişliğini ayarlayın (isteğe bağlı)
img.height = 100  # Resim yüksekliğini ayarlayın (isteğe bağlı)
sheet.add_image(img, image_cell)
sheet['C1'] = "COF Test Sonuçları"
# Excel dosyasını kaydedin
workbook.save('dosya.xlsx')

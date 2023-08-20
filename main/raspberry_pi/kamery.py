import shutil
#from picamera import PiCamera

"""
#obsluga kamery
camera = PiCamera()
camera.capture('/var/www/html/photos/photo.jpg')
"""
#dodawanie zdjecia
src_path = 'kot.jpg'  
dst_path = '/var/www/html/photos/obraz.jpg'  

shutil.copy(src_path, dst_path)

print('zdjecie na serwerze')

#to trzeba dac w petli zeby co np. 1s dodawalo sie nowe zdjecie z picamera

"""
#usuwanie zdjecia
file_path = '/var/www/html/photos/obraz.jpg'  # ścieżka do pliku na serwerze Apache

if shutil.os.path.exists(file_path):
    shutil.os.remove(file_path)
    print('Zdjęcie zostało usunięte.')
else:
    print('Plik nie istnieje.')
    
"""


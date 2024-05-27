#Bu devre için Esp32 nin içine ssd1306 kütüphanesi eklenmelidir#
#Ilgili kütüphaneye "https://randomnerdtutorials.com/micropython-oled-display-esp32-esp8266/" linkinden ulaşabilirsin.#

from machine import Pin, I2C, PWM
import ssd1306
import time
import dht

# DHT22 Sensörü Ayarları
dht_pin = Pin(4)
sensor = dht.DHT22(dht_pin)

# OLED Ekran Ayarları
i2c = I2C(scl=Pin(22), sda=Pin(21))
oled_width = 128
oled_height = 64
oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)

# Servo Motor Ayarları
servo = PWM(Pin(18), freq=50)

def set_servo_angle(angle):
    duty = int((angle / 180) * 1023 / 20 + 51.5)
    servo.duty(duty)

# Röle Ayarları
relay = Pin(15, Pin.OUT)

# LED Ayarları
led = Pin(5, Pin.OUT)

# Buton Ayarları
button = Pin(17, Pin.IN, Pin.PULL_DOWN)

# Servo motoru kontrol eden fonksiyon (röle üzerinden güç sağlanıyor)
def control_servo(state):
    if state:
        relay.value(1)  # Röleyi aç (servo motoru çalıştır)
        set_servo_angle(90)  # Servo motoru 90 dereceye ayarla
    else:
        relay.value(0)  # Röleyi kapat (servo motoru durdur)
        set_servo_angle(0)  # Servo motoru 0 dereceye ayarla

# Ana döngü
while True:
    try:
        sensor.measure()
        temp = sensor.temperature()
        hum = sensor.humidity()
        
        # OLED Ekranda sıcaklık ve nemi göster
        oled.fill(0)
        oled.text('Temp: {:.1f}C'.format(temp), 0, 0)
        oled.text('Humidity: {:.1f}%'.format(hum), 0, 10)
        oled.show()
        
        # Sıcaklık belirli bir seviyenin altına düştüğünde LED'i yak
        if temp < 20:  # Sıcaklık eşiği
            led.value(1)  # LED'i yak
        else:
            led.value(0)  # LED'i söndür
        
        # Butona basıldığında servo motorunu kontrol et
        if button.value() == 1:
            control_servo(True)
            time.sleep(5)  # Servo motoru 5 saniye çalıştır
            control_servo(False)
        
        time.sleep(2)  # Ölçümleri her 2 saniyede bir yap
    except OSError as e:
        print('Sensor Reading Failed')

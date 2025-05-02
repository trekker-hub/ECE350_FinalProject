'''
TARIQ ALDALOU
ECE350 FINAL PROJECT
AUTO WATERING SYSTEM
'''

import time
from datetime import datetime
import board
import adafruit_dht
import RPi.GPIO as GPIO
from RPLCD.i2c import CharLCD   # I²C driver

# ── SETTING UP 
MOISTURE_PIN   = 17
RELAY_PIN      = 27
DHT_PIN        = board.D4
WATER_SECS     = 1
CHECK_INTERVAL = 1
MAX_DHT_RETRY  = 3
LCD_ADDR       = 0x27           
# ──────────────────────────────────────────────────────

# ── BOARD SETTINGS 
GPIO.setmode(GPIO.BCM)
GPIO.setup(MOISTURE_PIN, GPIO.IN)
GPIO.setup(RELAY_PIN, GPIO.OUT, initial=GPIO.LOW)

dht = adafruit_dht.DHT11(DHT_PIN, use_pulseio=False)

lcd = CharLCD(i2c_expander='PCF8574',
              address=LCD_ADDR,
              port=1,
              cols=16, rows=2,
              charmap='A02',
              auto_linebreaks=False)
lcd.backlight_enabled = True

# ──  FUNCTIONS 
def read_climate():
    for _ in range(MAX_DHT_RETRY):
        try:
            return dht.temperature, dht.humidity
        except RuntimeError:
            time.sleep(WATER_SECS)
    return None, None

def soil_is_dry():
    return GPIO.input(MOISTURE_PIN) == GPIO.HIGH  # LOW → dry

def set_pump(on: bool):
    GPIO.output(RELAY_PIN, GPIO.LOW if on else GPIO.HIGH)

def show_on_lcd(temp, hum, dry, pump):
    lcd.home()                         # stay flicker-free
    t = f"{temp:.1f}C" if temp is not None else "N/A"
    h = f"{hum:.1f}%"  if hum  is not None else "N/A"
    lcd.write_string(f"T:{t:<5} H:{h:<4}")   # already 16 chars
    lcd.crlf()

    soil  = "Dry" if dry else "Wet"
    pstat = "ON"  if pump else "OFF"
    line2 = f"Soil:{soil:<3}Pump:{pstat}"   # 15 or 16… pad it
    lcd.write_string(line2.ljust(16))       # <- added .ljust(16)


def console_log(temp, hum, dry, pump):
    print(f"[{datetime.now():%H:%M:%S}] "
          f"T={temp if temp is not None else 'N/A'}C | "
          f" H={hum if hum is not None else 'N/A'}% | "
          f"Soil={'Dry' if dry else 'Wet'} | "
          f"Pump={'ON' if pump else 'OFF'}")

# ── MAIN LOOP 
try:
    while True:
        temperature, humidity = read_climate()
        dry = soil_is_dry()

        pump_state = dry
        set_pump(pump_state)
        show_on_lcd(temperature, humidity, dry, pump_state)
        console_log(temperature, humidity, dry, pump_state)

        time.sleep(WATER_SECS if pump_state else CHECK_INTERVAL)

except KeyboardInterrupt:
    print("\nStopped by user")

finally:
    set_pump(False)
    lcd.clear()
    GPIO.cleanup()

# Smart Plant‑Watering System

Automated houseplants powered by a Raspberry Pi 4.

> **Goal:** Keep your plant perfectly watered by monitoring soil moisture, ambient temperature & humidity, and automatically activating a micro‑water‑pump when needed. Current conditions are shown on a 16×2 LCD and logged for later analysis.

---

## 🛠️ Hardware Bill of Materials

| Qty | Component                           | Purpose                                                                    |
| --- | ----------------------------------- | -------------------------------------------------------------------------- |
| 1   | **Raspberry Pi 4** (any RAM)        | Brains of the system; runs Python controller & provides Wi‑Fi / networking |
| 1   | **Capacitive soil‑moisture sensor** | Reads volumetric water content of soil                                     |
| 1   | **DHT‑11 temp & humidity sensor**   | Tracks ambient climate around the plant                                    |
| 1   | **5 V micro water pump** + tubing   | Delivers water from reservoir to plant                                     |
| 1   | **1‑channel 5 V relay module**      | Switches the pump on/off safely                                            |
| 1   | **16 × 2 I²C LCD display**          | Shows live values & pump status                                            |
| 1   | **LED (green)** + 330 Ω resistor    | Blinks when pump runs                                                      |
| 1   | 220µF electrolytic **capacitor**    | Smooths pump inrush current                                                |
| 1   | 5 V ⎓ **DC power supply** (2 A+)    | Feeds Pi + pump (or use separate rails)                                    |
| —   | Jumper **wires**, breadboard or PCB | Connections                                                                |

> **Optional:** PCF8591 ADC if using an analog moisture probe.

---

## 📐 Wiring Overview

```
DHT‑11       → Pi GPIO 4 (data) + 5 V + GND
Moisture Sns → Pi GPIO 18 (analog via ADC) / or direct digital pin
Relay IN     → Pi GPIO 23
Relay VCC/GND→ 5 V / GND
Pump 5 V     → Relay COM → 5 V supply
Pump GND     → GND (through 470 µF cap across pump leads)
LCD SDA/SCL  → Pi SDA1/SCL1 (GPIO 2/3) 5 V tolerant
LED anode    → Pi GPIO 24 through 330 Ω → LED cathode → GND
```

---

## 🖥️ Software

### Requirements

```bash
sudo apt update && sudo apt install -y python3-pip i2c-tools git
pip3 install RPi.GPIO smbus2 adafruit-circuitpython-dht
```
---

## 🔧 Configuration

```yaml
sampling_interval: 1       # seconds between sensor reads
pump_time: 1               # seconds pump stays on
```

---

## 🛠️ Troubleshooting

| Symptom                      | Check                                                |
| ---------------------------- | ---------------------------------------------------- |
| `i2cdetect` shows no devices | Enable I²C in `raspi-config`; check SDA/SCL pull‑ups |
| Pump never starts            | Verify relay wiring & `GPIO 23`; watch LED           |
| Pi stopps whenever pump work | Add 220µF capacitor to the LCD and pump              |
| LCD gibberish or blank       | Confirm I²C address in `lcd.py` (0x27/0x3F)          |

---

Built to keep Zataar green 💚.

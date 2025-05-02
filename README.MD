# PCF8591 Raspberry Pi Examples

Read analog voltage, temperature, or light‑dependent resistor (LDR) inputs on a Raspberry Pi (or any I²C‑capable SBC) using the Philips PCF8591 8‑bit A/D & D/A converter.

---

## ✨ Features

* **4× 8‑bit ADC channels** – sample multiple analog sensors
* **1× 8‑bit DAC output** – generate an analog test signal
* **Pure‑Python example** – no external libraries beyond `smbus2`
* **Step‑by‑step setup** – enable I²C, detect the board, wire the circuit
* Works on **Pi 4 / Pi 5 / Zero 2 W** and most Linux SBCs

---

## 🛠 Hardware

| Qty | Part                                   | Notes                                               |
| --- | -------------------------------------- | --------------------------------------------------- |
| 1   | PCF8591 breakout module                | Often labelled “Analog‑to‑Digital Converter Module” |
| 1   | Raspberry Pi + micro‑SD + PSU          | Any model with I²C pins (SDA/SCL)                   |
| n   | Analog sensors (pot, LDR, thermistor…) | 0–3.3 V range preferred                             |
| —   | Breadboard & jumper wires              |                                                     |

👉 **Pinout:**

```
PCF8591        Raspberry Pi (BCM)
———           ————————————————
VCC   ↔  3V3   (pin 1)
GND   ↔  GND   (pin 6)
SDA   ↔  SDA1  (GPIO 2, pin 3)
SCL   ↔  SCL1  (GPIO 3, pin 5)
A0‑A2 ↔  GND   (keep at default 0×48 address)
```

---

## 🚀 Quick Start

### 1 · Enable I²C & reboot

```bash
sudo raspi-config  # Interface Options ▶ I2C ▶ Enable
sudo reboot
```

### 2 · Install tools & libraries

```bash
sudo apt update && sudo apt install -y i2c-tools python3-smbus2 git
```

### 3 · Clone this repo

```bash
git clone https://github.com/your‑username/pcf8591‑examples.git
cd pcf8591‑examples
```

### 4 · Detect the board

```bash
sudo i2cdetect -y 1    # look for 0x48–0x4F
```

> Expected output includes **`48`** in the 0x40–0x4F row. If you don’t see it, check power and wiring.

### 5 · Run the demo

```bash
python3 read_analog.py --address 0x48 --channel 0
```

You should see a stream of raw 8‑bit values (0–255) that change as you turn a potentiometer or cover the LDR.

---

## 📄 Repository Layout

```
.
├─ read_analog.py      # main example script
├─ dac_sawtooth.py     # demonstrates the DAC output
├─ images/             # wiring diagrams & screenshots
└─ LICENSE
```

---

## 🤔 How It Works

* The PCF8591 appears on the I²C bus with a 7‑bit address of **0x48** by default.
* To read channel *N*, we write the control byte `0x40 | N` then perform a dummy read followed by the real conversion result.
* The example uses **`smbus2`** for repeated‑start combined write/read, ensuring glitch‑free sampling.

See the inline comments in `read_analog.py` for the gory details.

---

## 🐞 Troubleshooting

| Symptom                      | Fix                                                        |
| ---------------------------- | ---------------------------------------------------------- |
| `i2cdetect` shows all `--`   | Check SDA/SCL wiring, enable I²C in `raspi-config`         |
| `Errno 121 Remote I/O error` | Wrong address, floating A0–A2 pins, or 5 V on the module   |
| Readings stuck at 255 or 0   | Sensor voltage outside 0–3.3 V range, or unconnected input |

---

## 🤝 Contributing

Pull requests are welcome! Please open an issue first if you plan a large change so we can discuss the best approach.

---

## 📜 License

This project is licensed under the MIT License – see `LICENSE` for details.

# 📡 Helios – ESP32 Measurement System

**Helios** is a sensor monitoring system using an ESP32 microcontroller to collect and transmit data on **current, pressure, and temperature**. The data is visualized and logged on a host PC using a **PyQt-based GUI**.

---

## 📁 Project Structure

```
.
├── Monitor.py          # PyQt GUI for real-time graph & logging
├── README.md           # Project description
├── include/            # Header files (PlatformIO default)
├── lib/                # External libraries (PlatformIO)
├── platformio.ini      # ESP32 build configuration (PlatformIO)
├── src/
│   └── main.cpp        # Firmware: Reads sensors and sends CSV via Serial
└── test/               # Unit tests (if any)
```

---

## ⚙️ How It Works

### 1. 📦 ESP32 Firmware (`src/main.cpp`)

* Measures:

  * **Thrust**
  * **Pressure**
  * **Temperature**
* Sends measurements via **Serial** in **CSV format**:

  ```
  timestamp,temperature,pressure,thrust
  ```

### 2. PC Monitoring (`Monitor.py`)

* Built with **PyQt**
* Features:

  - **Real-time graph** of incoming sensor data
  - **Logging** to CSV file
  - **Start/Stop monitoring** controls
  - Automatically parses incoming serial data and updates GUI

---

## 📂 Log Output

When monitoring is active, logs are saved in CSV format in the same structure:

```
timestamp,temperature,pressure,thrust
```

---
import sys
import serial
import threading
import csv
import time
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel
from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg

PORT = 'COM5' #'COM5' 5:esp, 6:holobro
BAUD = 57600
CSV_FILE = 'data_log.csv'

class SerialMonitor(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("UART 실시간 센서 모니터")
        self.resize(800, 800)

        # 데이터 버퍼
        self.time_data = []
        self.temp_data = []
        self.pressure_data = []
        self.thrust_data = []

        # 시리얼 포트 열기
        self.ser = serial.Serial(PORT, BAUD, timeout=0.1)

        # CSV 파일 초기화
        with open(CSV_FILE, mode='w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Time (s)', 'Temperature (C)', 'Pressure (bar)', 'Thrust (N)'])

        # UI 구성
        self.layout = QVBoxLayout()

        # === Plot 1: Temperature ===
        self.temp_label = QLabel("📈 온도 (°C)")
        self.temp_plot = PlotWidget()
        self.temp_curve = self.temp_plot.plot(pen='r')
        self.temp_plot.setLabel('left', 'Temperature (°C)')
        self.temp_plot.setLabel('bottom', 'Time (s)')

        # === Plot 2: Pressure ===
        self.pressure_label = QLabel("📈 압력 (bar)")
        self.pressure_plot = PlotWidget()
        self.pressure_curve = self.pressure_plot.plot(pen='g')
        self.pressure_plot.setLabel('left', 'Pressure (bar)')
        self.pressure_plot.setLabel('bottom', 'Time (s)')

        # === Plot 3: Thrust ===
        self.thrust_label = QLabel("📈 추력 (N)")
        self.thrust_plot = PlotWidget()
        self.thrust_curve = self.thrust_plot.plot(pen='b')
        self.thrust_plot.setLabel('left', 'Thrust (N)')
        self.thrust_plot.setLabel('bottom', 'Time (s)')

        # === Input ===
        self.input_line = QLineEdit()
        self.send_button = QPushButton("Send Command")
        self.send_button.clicked.connect(self.send_command)

        # === Layout 추가 ===
        self.layout.addWidget(self.temp_label)
        self.layout.addWidget(self.temp_plot)
        self.layout.addWidget(self.pressure_label)
        self.layout.addWidget(self.pressure_plot)
        self.layout.addWidget(self.thrust_label)
        self.layout.addWidget(self.thrust_plot)
        self.layout.addWidget(self.input_line)
        self.layout.addWidget(self.send_button)

        self.setLayout(self.layout)

        # 수신 스레드 시작
        self.running = True
        self.thread = threading.Thread(target=self.read_serial)
        self.thread.start()

        # 그래프 업데이트 타이머
        self.timer = pg.QtCore.QTimer()
        self.timer.timeout.connect(self.update_graph)
        self.timer.start(500)

    def send_command(self):
        msg = self.input_line.text().strip()
        if msg:
            if msg == "ignition":
                with open(CSV_FILE, mode='a', newline='') as f_csv:
                    writer = csv.writer(f_csv)
                    writer.writerow(['---', 'ignition', '---'])

            
            self.ser.write((msg).encode('utf-8'))
            self.input_line.clear()

    def read_serial(self):
        while self.running:
            if self.ser.in_waiting > 0:
                try:
                    raw = self.ser.readline().decode('utf-8', errors='ignore').strip()
                    if raw.count(',') == 3:
                        t_str, p_str, f_str, s_str = raw.split(',')
                        t = float(t_str)
                        p = float(p_str)
                        f_ = float(f_str)
                        s = float(s_str)

                        self.temp_data.append(t)
                        self.pressure_data.append(p)
                        self.thrust_data.append(f_)
                        self.time_data.append(s)

                        with open(CSV_FILE, mode='a', newline='') as f_csv:
                            writer = csv.writer(f_csv)
                            writer.writerow([s, t, p, f_])
                    else:
                        print(f"[수신] {raw}")
                except Exception as e:
                    print(f"[에러] {e}")
            time.sleep(0.01)

    def update_graph(self):
        self.temp_curve.setData(self.time_data, self.temp_data)
        self.pressure_curve.setData(self.time_data, self.pressure_data)
        self.thrust_curve.setData(self.time_data, self.thrust_data)

    def closeEvent(self, event):
        self.running = False
        self.thread.join()
        self.ser.close()
        event.accept()

# 실행
if __name__ == "__main__":
    app = QApplication(sys.argv)
    monitor = SerialMonitor()
    monitor.show()
    sys.exit(app.exec_())

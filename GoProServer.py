import os
import sys
import time
import asyncio
import sqlite3
import datetime
import threading
from threading import Timer, Event
import requests
from GoProSever_Frontend import Ui_MainWindow
from pynput.mouse import Listener, Button
from open_gopro import WiredGoPro, constants
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *


class DatabaseThread(QThread):
    db_progress = pyqtSignal(str)
    db_finished = pyqtSignal()
    db_data_loaded = pyqtSignal(list)

    def __init__(self, ui=None):
        super().__init__()
        self.ui = ui
        self.db_path = os.path.abspath("video_solution.db")
        print(f"Database path: {self.db_path}")  # Debugging

    def run(self):
        """ Default run method to create database and load initial data. """
        self.create_db()
        self.load_data()

    def create_db(self):
        try:
            self.db_progress.emit("Creating database...")

            # Check if file exists before opening connection
            if not os.path.exists(self.db_path):
                print(f"Creating new database file: {self.db_path}")
                open(self.db_path, 'w').close()  # Manually create an empty file

            with sqlite3.connect(self.db_path, check_same_thread=False) as conn:
                cursor = conn.cursor()
                cursor.execute("""CREATE TABLE IF NOT EXISTS tags (
                    id INTEGER PRIMARY KEY,
                    code TEXT NOT NULL,
                    time_stamp TEXT NOT NULL,
                    original_file TEXT NOT NULL,
                    associated_file TEXT NOT NULL
                )""")
                conn.commit()

            self.db_progress.emit("Database created successfully.")
        except Exception as e:
            self.db_progress.emit(f"Error creating DB: {e}")
            print(f"Error creating DB: {e}")

    def load_data(self):
        """ Loads the last entry from the database and sends it to the UI. """
        try:
            self.db_progress.emit("Loading data from database...")
            if not os.path.exists(self.db_path):
                self.db_progress.emit("Database file does not exist! Skipping load.")
                return

            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                query = "SELECT * FROM tags ORDER BY id DESC LIMIT 1"
                cursor.execute(query)
                row = cursor.fetchone()

            if row:
                self.db_data_loaded.emit(list(row))
            else:
                self.db_progress.emit("No data found in the database.")

            self.db_finished.emit()
        except Exception as e:
            self.db_progress.emit(f"Error loading data: {e}")

    def insert_or_update_data(self, tag_code, current_time, file_name, associated_name):
        """ Insert a new record into the database. """
        if not tag_code or not current_time or not file_name or not associated_name:
            self.db_progress.emit("Error: Data cannot be empty")
            return

        try:
            self.db_progress.emit("Inserting data into the database...")
            conn = sqlite3.connect(self.db_path, check_same_thread=False)
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO tags (code, time_stamp, original_file, associated_file)
                VALUES (?, ?, ?, ?)
            """, (tag_code, current_time, file_name, associated_name))
            conn.commit()
            conn.close()

            self.db_progress.emit(f"Data inserted: {tag_code}")
            self.load_data()  # Refresh table
        except Exception as e:
            self.db_progress.emit(f"Error inserting data: {e}")
            print(f"Error inserting data: {e}")


class CameraMonitor(QThread):
    """Camera monitoring thread using QThread instead of QRunnable"""
    error = pyqtSignal()
    finished = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.camera_connected = True  # Track state
        self.running = True

    def is_ip_camera_connected(self):
        """Checks if the camera is reachable"""
        try:
            response = requests.get("http://172.24.190.51:8080/gp/gpControl", timeout=2)
            return response.status_code == 200
        except requests.exceptions.RequestException:
            return False

    def check_camera_status(self):
        """Check camera status every 3 seconds"""
        if self.is_ip_camera_connected():
            if not self.camera_connected:
                self.finished.emit()  # Notify UI
                print("Camera reconnected.")
                self.camera_connected = True
        else:
            if self.camera_connected:
                self.error.emit()  # Notify UI
                print("Camera disconnected.")
                self.camera_connected = False

    def run(self):
        """Runs the monitoring thread with QTimer"""
        self.timer = QTimer()
        self.timer.timeout.connect(self.check_camera_status)
        self.timer.start(3000)  # Check every 3 seconds

        loop = QEventLoop()  # Create an event loop
        loop.exec_()


class SensorThread(QThread):
    sensor_triggered = pyqtSignal(str)  #  Signal for UI updates
    sensor_not_triggered = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.listener = None
        self.click_detected = Event()

    def run(self):
        """Runs the mouse listener in a background thread."""
        def on_click(x, y, button, pressed):
            if button == Button.middle and pressed:
                message = f"Sensor triggered at {x}, {y}, with {button}"
                print(message)
                self.sensor_triggered.emit(message)  #  Send to UI
                self.click_detected.set()
                return False  # Stop listener after the first click

        self.listener = Listener(on_click=on_click)
        listener_thread = threading.Thread(target=self.listener.start, daemon=True)
        listener_thread.start()  # Start listener in a separate thread

        if not self.click_detected.wait(timeout=10):  # Timeout handling
            self.sensor_not_triggered.emit("No sensor input within dispatch time.")

        self.listener.stop()  # Stop listener to prevent background threads


class GoProApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()  # Instantiate Ui_MainWindow
        self.init_ui()

        # Gopro
        self.gopro = WiredGoPro()
        self.raw_path = "Raw"
        self.raw_video_path = os.path.join(os.getcwd(), self.raw_path)
        os.makedirs(self.raw_path, exist_ok=True)
        self.download_path = "Downloads"
        self.download_video_path = os.path.join(os.getcwd(), self.download_path)
        os.makedirs(self.download_path, exist_ok=True)
        self.tag = None
        self.model_name = "No Camera"
        self.battery = 0

        # Loop Instantiating
        self.loop = asyncio.new_event_loop()

        # Start asyncio loop in a separate thread
        threading.Thread(target=self.run_event_loop, daemon=True).start()
        asyncio.run_coroutine_threadsafe(self.initialize(), self.loop)

        # Database
        self.db_thread = DatabaseThread()
        self.db_thread.db_progress.connect(self.update_log)
        self.db_thread.db_finished.connect(lambda: self.update_log("Database operation completed: "))
        self.db_thread.db_data_loaded.connect(self.update_table)
        self.db_thread.start()

        # Sensor
        self.sensor_thread = SensorThread()
        self.sensor_thread.sensor_not_triggered.connect(self.update_db_after_no_trigger)
        self.sensor_thread.sensor_triggered.connect(self.update_db_after_trigger)

        # Functions calling
        self.camera_monitor_fn()

        #  Connect buttons
        self.ui.start_pushbutton.clicked.connect(self.tag_scan)
        self.ui.tag_lineEdit.returnPressed.connect(self.tag_scan)

    def camera_monitor_fn(self):
        """Start the camera monitoring thread"""
        self.camera_monitor_worker = CameraMonitor()
        self.camera_monitor_worker.error.connect(self.show_disconnected)
        self.camera_monitor_worker.finished.connect(self.show_connected)
        self.camera_monitor_worker.start()

    def init_ui(self):
        # Static Components
        self.ui.setupUi(self)  # Setup UI components
        self.ui.log_textEdit.setEnabled(True)
        self.ui.tag_lineEdit.setFocus()
        self.setup_table()
        self.ui.log_textEdit.setReadOnly(True)

    async def get_battery(self):
        try:
            info = await asyncio.shield(self.gopro.http_command.get_camera_state())
            battery_percentage = info.data.get(constants.StatusId.INTERNAL_BATTERY_PERCENTAGE)
            QMetaObject.invokeMethod(self, "update_battery", Qt.QueuedConnection)
            print(f"Battery Percentage is: {battery_percentage}")
            return battery_percentage
        except Exception as e:
            print(f"Error while getting battery per : {e}")
            return 0

    async def get_model(self):
        try:
            camera_info = await asyncio.shield(self.gopro.http_command.get_camera_info())
            return camera_info.data.model_name
        except Exception as e:
            print(f"Error while getting model name: {e}")
            return "No Camera"

    async def initialize(self):
        try:
            await self.gopro.open()

            self.model_name = await self.get_model()
            self.battery = await self.get_battery()

            # Update UI
            QMetaObject.invokeMethod(self, 'update_ui', Qt.QueuedConnection)

            # Use lambda to pass data safely
            QMetaObject.invokeMethod(self, 'update_battery', Qt.QueuedConnection)

        except Exception as e:
            print(f"Error while Initializing : {e}")

    def update_log(self, message):
        # Ensure the method is invoked in the main thread
        QTimer.singleShot(0, lambda: self.ui.log_textEdit.append(message))

    def update_table(self, row):
        if row:
            # Ensure you insert a new row
            self.ui.tableWidget.insertRow(0)  # Insert row at the top (index 0)

            # Loop through all columns in the row (assuming 5 items in the row)
            for col, data in enumerate(row):
                item = QTableWidgetItem(str(data))  # Convert data to string for display
                self.ui.tableWidget.setItem(0, col, item)  # Add the item to the correct cell

    def setup_table(self):
        self.ui.tableWidget.setColumnCount(5)  # Ensure correct column count
        # Set column widths
        self.ui.tableWidget.setColumnWidth(0, 50)
        self.ui.tableWidget.setColumnWidth(1, 150)
        self.ui.tableWidget.setColumnWidth(2, 100)
        self.ui.tableWidget.setColumnWidth(3, 100)
        self.ui.tableWidget.setColumnWidth(4, 150)

        # Set header labels
        self.ui.tableWidget.setHorizontalHeaderLabels(["id", "code", "time_stamp", "original_file", "associated_file"])

        # Optional: Auto-resize columns
        self.ui.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

    # Async operation starts
    def tag_scan(self):
        tag_code = self.ui.tag_lineEdit.text()
        print(f"Band scanned {tag_code}")
        self.update_log("Band Scanned")
        self.start_sensor_listener()

    def start_sensor_listener(self):
        self.update_log("Waiting for sensor input...")
        self.sensor_thread.start()

    def update_db_after_no_trigger(self):
        tag_code = self.ui.tag_lineEdit.text()
        self.send_code(tag_code)
        current_time = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        print(f"Updating the DB scanned code : {tag_code}")
        self.ui.tag_lineEdit.clear()
        self.ui.tag_lineEdit.setFocus()
        file_name = "No-Sensor"
        associated_name = f"No-Sensor-{current_time}"

        try:
            self.db_thread.insert_or_update_data(tag_code=tag_code, current_time=current_time, file_name=file_name,
                                                 associated_name=associated_name)
            self.update_log("Updated db with no sensor data")
        except Exception as e:
            print(f"Error While updating db record with no sensor data : {e}")
            self.update_log(f"Error While updating db record with no sensor data : {e}")

    def send_code(self, association_code):
        association_code = str(association_code.replace(".mp4", ""))
        # Define the network path
        network_path = r"\\dufraerialcam01\Users\Imixadmin\Pictures\tag"

        with_code = os.path.join(network_path, association_code + ".txt")
        print(f"with code: {with_code}")

        # Ensure the directory exists
        directory = os.path.dirname(with_code)
        if not os.path.exists(directory):
            print("Error: Directory does not exist.")
        else:
            try:
                # Create and write to the file
                with open(with_code, "w") as f:
                    f.write(association_code)  # Example QR code data
                print(f"{association_code}.txt created successfully!")
            except Exception as e:
                print(f"Error writing file: {e}")

    def update_db_after_trigger(self):
        tag_code = self.ui.tag_lineEdit.text()
        self.send_code(association_code=tag_code)
        current_time = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        print(f"Updating the DB scanned code : {tag_code}")
        self.ui.tag_lineEdit.clear()
        self.ui.tag_lineEdit.setFocus()
        associated_name = f"{tag_code}-{current_time}.mp4"

        # If capture_handler isn't async, use run_in_executor to run it as a separate thread.
        future = asyncio.run_coroutine_threadsafe(self.capture_handler(associated_name), self.loop)
        try:
            file_name = future.result(timeout=10)  # Set a timeout of 10 seconds
        except Exception as e:
            print(f"Error while capturing video: {e}")
            return

        print(f"Video captured {file_name}")
        self.update_log(file_name)

        if not tag_code or not current_time or not file_name or not associated_name:
            print("Data cannot be empty")
            self.update_log("Data cannot be empty")
            return

        try:
            self.db_thread.insert_or_update_data(tag_code=tag_code, current_time=current_time, file_name=file_name,
                                                 associated_name=associated_name)
            # self.start_rendering(tag_code=tag_code)
            print("Data sent to Server")

        except Exception as e:
            print(f"Error while sending data to server : {e}")

    async def capture_handler(self, associated_name):
        print("Capture operation started")
        file_name = await self.capture_video(associated_name)
        print(f"{file_name} Video captured")
        return file_name

    async def capture_video(self, associated_name):
        try:
            assert (await self.gopro.http_command.set_shutter(shutter=constants.Toggle.ENABLE)).ok
            await asyncio.sleep(3)
            assert (await self.gopro.http_command.set_shutter(shutter=constants.Toggle.DISABLE)).ok
            last_media = await self.download_last_media(associated_name)
            self.update_log("Video captured and Downloaded")
            print("Video captured and Downloaded")
            return last_media

        except Exception as e:
            self.update_log(f"Error while capturing video : {e}")
            print(f"Error while capturing video : {e}")

    async def download_last_media(self, associated_name):
        try:
            last_media = await self.gopro.http_command.get_last_captured_media()
            os.makedirs(self.raw_path, exist_ok=True)

            local_file_path = os.path.join(self.raw_path, last_media.data.file)
            converter_input = "conv_input"
            temp = os.path.join(os.getcwd(), converter_input)
            os.makedirs(temp, exist_ok=True)
            converter_input_path = os.path.join(temp, associated_name)
            associated_name_path = os.path.join(temp, associated_name)

            await self.gopro.http_command.download_file(
                camera_file=last_media.data.as_path,
                local_file=local_file_path
            )

            # Debugging print
            print(f"Original filename: {local_file_path}")
            print(f"Renaming to: {associated_name_path}")

            # Ensure the file exists before renaming
            if os.path.exists(local_file_path):
                await asyncio.sleep(2)  # Ensure download completes
                os.rename(local_file_path, associated_name_path)
                self.update_log(f"Media has been downloaded: {associated_name}")
                return last_media.data.file
            else:
                self.update_log(f"File not found after download: {local_file_path}")

        except Exception as e:
            self.update_log(f"Error while downloading: {repr(e)}")

    @pyqtSlot()
    def show_disconnected(self):
        QMessageBox.warning(self, "Camera Disconnected", "The camera has been disconnected")

    @pyqtSlot()
    def show_connected(self):
        QMessageBox.information(self, "Camera Connected", "The camera has been connected back")

    @pyqtSlot()
    def update_ui(self):
        self.ui.camera_label.setText(self.model_name)

    @pyqtSlot()
    def update_battery(self):
        self.ui.Battery.display(str(self.battery))

    def run_event_loop(self):
        if not self.loop.is_running():
            asyncio.set_event_loop(self.loop)
            self.loop.run_forever()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = GoProApp()
    window.show()
    try:
        sys.exit(app.exec_())
    except:
        print("Exiting")

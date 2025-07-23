from PyQt6.QtWidgets import (
    QApplication, QWidget, QTabWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QLineEdit, QPushButton, QComboBox, QMessageBox, QTableWidget, QTableWidgetItem,
    QHeaderView
)
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QFont
import sys
from datetime import datetime

# === Core Classes ===
class Car:
    def __init__(self, car_id, brand, model, car_type, rental_rate):
        self.car_id = car_id
        self.brand = brand
        self.model = model
        self.car_type = car_type
        self.rental_rate = rental_rate
        self.available = True

    def rent(self):
        self.available = False

    def return_car(self):
        self.available = True


class Customer:
    def __init__(self, customer_id, name):
        self.customer_id = customer_id
        self.name = name
        self.rentals = []
        self.rental_history = []

    def rent_car(self, rental):
        self.rentals.append(rental)
        self.rental_history.append(rental)

    def return_car(self, rental):
        if rental in self.rentals:
            self.rentals.remove(rental)


class Rental:
    def __init__(self, rental_id, car, customer, start_date, end_date):
        self.rental_id = rental_id
        self.car = car
        self.customer = customer
        self.start_date = start_date
        self.end_date = end_date

    def calculate_cost(self):
        days = (self.end_date - self.start_date).days
        return days * self.car.rental_rate


# === Main Window ===
class CarRentalApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🚗 Car Rental System - PyQt6")
        self.setGeometry(300, 100, 900, 650)

        self.customers = {}
        self.rentals = []
        self.rental_counter = 1
        self.cars = self.create_cars()

        self.initUI()

    def create_cars(self):
        car_data = [
            ("C001", "Toyota", "Corolla", "Sedan", 5000),
            ("C002", "Toyota", "Land Cruiser", "SUV", 12000),
            ("C003", "Honda", "Civic", "Sedan", 5500),
            ("C004", "BMW", "X5", "Luxury SUV", 15000),
            ("C005", "Suzuki", "Cultus", "Hatchback", 3500),
            ("C006", "Kia", "Sportage", "SUV", 11000),
            ("C007", "Mercedes", "E-Class", "Luxury Sedan", 18000),
            ("C008", "Hyundai", "Tucson", "SUV", 9500),
            ("C009", "Ford", "Focus", "Hatchback", 4000),
            ("C010", "Audi", "A6", "Luxury Sedan", 17000),
            ("C011", "Jeep", "Wrangler", "SUV", 13000),
            ("C012", "Range Rover", "Evoque", "Luxury SUV", 20000),
            ("C013", "Nissan", "X-Trail", "SUV", 9000),
            ("C014", "Lexus", "RX", "Luxury SUV", 19000),
            ("C015", "Hyundai", "Elantra", "Sedan", 4800),
            ("C016", "BMW", "M5", "Sports Sedan", 22000),
            ("C017", "Ford", "Mustang", "Sports Coupe", 25000),
            ("C018", "Audi", "Q7", "SUV", 16000),
            ("C019", "Kia", "Sorento", "SUV", 10500),
            ("C020", "Suzuki", "Alto", "Hatchback", 3000),
            ("C021", "Mercedes", "C-Class", "Luxury Sedan", 16500),
            ("C022", "Toyota", "Camry", "Sedan", 5800),
            ("C023", "Nissan", "Patrol", "SUV", 14000),
            ("C024", "Honda", "Accord", "Sedan", 6000),
            ("C025", "BMW", "M8", "Luxury Coupe", 26000),
        ]
        return [Car(*c) for c in car_data]

    def initUI(self):
        layout = QVBoxLayout()

        self.tabs = QTabWidget()
        layout.addWidget(self.tabs)

        self.tab_rent = QWidget()
        self.tab_return = QWidget()
        self.tab_history = QWidget()

        self.tabs.addTab(self.tab_rent, "🚘 Rent a Car")
        self.tabs.addTab(self.tab_return, "🔁 Return a Car")
        self.tabs.addTab(self.tab_history, "📋 Rental History")

        self.setup_rent_tab()
        self.setup_return_tab()
        self.setup_history_tab()

        self.setLayout(layout)

    def setup_rent_tab(self):
        layout = QVBoxLayout()

        font_label = QFont("Arial", 13)
        font_input = QFont("Arial", 12)

        # Customer Name
        hbox_name = QHBoxLayout()
        label_name = QLabel("Customer Name:")
        label_name.setFont(font_label)
        hbox_name.addWidget(label_name)

        self.input_name = QLineEdit()
        self.input_name.setFont(font_input)
        self.input_name.setPlaceholderText("Enter full name")
        self.input_name.setFixedHeight(35)
        hbox_name.addWidget(self.input_name)
        layout.addLayout(hbox_name)

        # Car Selection
        hbox_car = QHBoxLayout()
        label_car = QLabel("Select Car:")
        label_car.setFont(font_label)
        hbox_car.addWidget(label_car)

        self.combo_car = QComboBox()
        self.combo_car.setFont(font_input)
        self.combo_car.setFixedHeight(35)
        hbox_car.addWidget(self.combo_car)
        layout.addLayout(hbox_car)

        # Start Date
        hbox_start = QHBoxLayout()
        label_start = QLabel("Start Date (YYYY-MM-DD):")
        label_start.setFont(font_label)
        hbox_start.addWidget(label_start)

        self.input_start = QLineEdit()
        self.input_start.setFont(font_input)
        self.input_start.setPlaceholderText("YYYY-MM-DD")
        self.input_start.setFixedHeight(35)
        hbox_start.addWidget(self.input_start)
        layout.addLayout(hbox_start)

        # End Date
        hbox_end = QHBoxLayout()
        label_end = QLabel("End Date (YYYY-MM-DD):")
        label_end.setFont(font_label)
        hbox_end.addWidget(label_end)

        self.input_end = QLineEdit()
        self.input_end.setFont(font_input)
        self.input_end.setPlaceholderText("YYYY-MM-DD")
        self.input_end.setFixedHeight(35)
        hbox_end.addWidget(self.input_end)
        layout.addLayout(hbox_end)

        # Rent Button
        self.btn_rent = QPushButton("Book Now")
        self.btn_rent.setFont(QFont("Arial", 14, weight=QFont.Weight.Bold))
        self.btn_rent.setFixedHeight(45)
        self.btn_rent.setStyleSheet("""
            QPushButton {
                background-color: #28a745; 
                color: white; 
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #218838;
            }
        """)
        self.btn_rent.clicked.connect(self.handle_rent)
        layout.addWidget(self.btn_rent)

        self.tab_rent.setLayout(layout)
        self.refresh_car_list()

    def setup_return_tab(self):
        layout = QVBoxLayout()

        font_label = QFont("Arial", 13)
        font_input = QFont("Arial", 12)

        # Rental ID Input
        hbox_rental_id = QHBoxLayout()
        label_rental_id = QLabel("Rental ID:")
        label_rental_id.setFont(font_label)
        hbox_rental_id.addWidget(label_rental_id)

        self.input_rental_id = QLineEdit()
        self.input_rental_id.setFont(font_input)
        self.input_rental_id.setFixedHeight(35)
        hbox_rental_id.addWidget(self.input_rental_id)

        layout.addLayout(hbox_rental_id)

        # Return Button
        self.btn_return = QPushButton("Return Car")
        self.btn_return.setFont(QFont("Arial", 14, weight=QFont.Weight.Bold))
        self.btn_return.setFixedHeight(45)
        self.btn_return.setStyleSheet("""
            QPushButton {
                background-color: #ffc107; 
                color: black; 
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #e0a800;
            }
        """)
        self.btn_return.clicked.connect(self.handle_return)
        layout.addWidget(self.btn_return)

        self.tab_return.setLayout(layout)

    def setup_history_tab(self):
        layout = QVBoxLayout()

        self.table_history = QTableWidget()
        self.table_history.setColumnCount(6)
        self.table_history.setHorizontalHeaderLabels(["Rental ID", "Customer", "Car", "Start Date", "End Date", "Cost (Rs)"])
        self.table_history.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table_history.verticalHeader().setVisible(False)
        self.table_history.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table_history.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table_history.setFont(QFont("Arial", 11))
        layout.addWidget(self.table_history)

        self.tab_history.setLayout(layout)

        self.refresh_history()

    def refresh_car_list(self):
        self.combo_car.clear()
        for car in self.cars:
            if car.available:
                display = f"{car.brand} {car.model} - {car.car_type} (Rs {car.rental_rate}/day)"
                self.combo_car.addItem(display)

    def refresh_history(self):
        self.table_history.setRowCount(0)
        for rental in self.rentals:
            row_pos = self.table_history.rowCount()
            self.table_history.insertRow(row_pos)
            self.table_history.setItem(row_pos, 0, QTableWidgetItem(rental.rental_id))
            self.table_history.setItem(row_pos, 1, QTableWidgetItem(rental.customer.name))
            self.table_history.setItem(row_pos, 2, QTableWidgetItem(f"{rental.car.brand} {rental.car.model}"))
            self.table_history.setItem(row_pos, 3, QTableWidgetItem(rental.start_date.strftime("%Y-%m-%d")))
            self.table_history.setItem(row_pos, 4, QTableWidgetItem(rental.end_date.strftime("%Y-%m-%d")))
            self.table_history.setItem(row_pos, 5, QTableWidgetItem(str(rental.calculate_cost())))

    def handle_rent(self):
        name = self.input_name.text().strip()
        car_text = self.combo_car.currentText()
        start_str = self.input_start.text().strip()
        end_str = self.input_end.text().strip()

        if not name or not car_text or not start_str or not end_str:
            QMessageBox.warning(self, "Missing Info", "Please fill all fields.")
            return

        try:
            start_date = datetime.strptime(start_str, "%Y-%m-%d")
            end_date = datetime.strptime(end_str, "%Y-%m-%d")
            if end_date <= start_date:
                raise ValueError("End date must be after start date")
        except Exception as e:
            QMessageBox.warning(self, "Invalid Date", "Please enter valid dates in YYYY-MM-DD format.\n" + str(e))
            return

        # Find the selected car
        selected_car = None
        for car in self.cars:
            display = f"{car.brand} {car.model} - {car.car_type} (Rs {car.rental_rate}/day)"
            if display == car_text and car.available:
                selected_car = car
                break

        if not selected_car:
            QMessageBox.warning(self, "Unavailable", "Selected car is not available.")
            self.refresh_car_list()
            return

        # Check or add customer
        customer = self.customers.get(name)
        if not customer:
            customer = Customer(f"CU{len(self.customers)+1:03d}", name)
            self.customers[name] = customer

        # Rent car
        selected_car.rent()
        rental_id = f"R{self.rental_counter:03d}"
        self.rental_counter += 1

        rental = Rental(rental_id, selected_car, customer, start_date, end_date)
        customer.rent_car(rental)
        self.rentals.append(rental)

        QMessageBox.information(self, "Success", f"Car booked!\nRental ID: {rental_id}\nCost: Rs {rental.calculate_cost()}")

        self.clear_rent_fields()
        self.refresh_car_list()
        self.refresh_history()

    def clear_rent_fields(self):
        self.input_name.clear()
        self.input_start.clear()
        self.input_end.clear()
        self.combo_car.setCurrentIndex(-1)

    def handle_return(self):
        rental_id = self.input_rental_id.text().strip()
        if not rental_id:
            QMessageBox.warning(self, "Input Required", "Please enter Rental ID.")
            return

        rental = next((r for r in self.rentals if r.rental_id == rental_id), None)
        if not rental:
            QMessageBox.warning(self, "Not Found", "Rental ID not found.")
            return

        # Return car
        rental.car.return_car()
        rental.customer.return_car(rental)

        QMessageBox.information(self, "Returned", f"Car {rental.car.brand} {rental.car.model} returned.\nTotal cost: Rs {rental.calculate_cost()}")

        self.input_rental_id.clear()
        self.refresh_car_list()
        self.refresh_history()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CarRentalApp()
    window.show()
    sys.exit(app.exec())

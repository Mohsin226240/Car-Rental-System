from datetime import datetime
# Car class
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

# Customer class
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

# Rental class
class Rental:
    def __init__(self, rental_id, car, customer, start_date, end_date):
        self.rental_id = rental_id
        self.car = car
        self.customer = customer
        self.start_date = start_date
        self.end_date = end_date

    def calculate_cost(self):
        rental_days = (self.end_date - self.start_date).days
        return rental_days * self.car.rental_rate

# RentalSystem class
class RentalSystem:
    def __init__(self):
        self.cars = []
        self.customers = []
        self.rentals = []

    def add_car(self, car):
        self.cars.append(car)

    def add_customer(self, customer):
        self.customers.append(customer)

    def show_available_cars_by_type(self, car_type):
        available_cars = [car for car in self.cars if car.available and car.car_type.lower() == car_type.lower()]
        if available_cars:
            print(f"\nAvailable {car_type} Cars:")
            for car in available_cars:
                print(f"{car.car_id}: {car.brand} {car.model} - ${car.rental_rate}/day")
        else:
            print("No available cars of this type.")

    def book_car(self, customer, car_id, start_date, end_date):
        car = next((car for car in self.cars if car.car_id == car_id and car.available), None)
        if car:
            rental_id = f"R{len(self.rentals) + 1}"
            rental = Rental(rental_id, car, customer, start_date, end_date)
            self.rentals.append(rental)
            car.rent()
            customer.rent_car(rental)
            print(f"\nCar '{car.model}' booked successfully!✅")
            print(f"Your Rental ID is: {rental_id}")
            print("Thank you for booking with us!\n")
            return rental_id
        else:
            print("\nInvalid or unavailable Car ID. Please try again.")
            return None

    def return_car(self, rental_id):
        rental = next((rental for rental in self.rentals if rental.rental_id == rental_id), None)
        if rental:
            rental.car.return_car()
            rental.customer.return_car(rental)
            cost = rental.calculate_cost()
            print(f"\nCar returned successfully✅. Total cost: ${cost}")
            return True
        else:
            print("Invalid Rental ID. Please enter a valid ID.")
            return False

    def view_rental_history(self, customer):
        if customer.rental_history:
            print(f"\nRental History for {customer.name}:")
            for rental in customer.rental_history:
                cost = rental.calculate_cost()
                print(f"Rental ID: {rental.rental_id} | Car: {rental.car.brand} {rental.car.model} | "
                      f"From: {rental.start_date.date()} To: {rental.end_date.date()} | Cost: ${cost}")
        else:
            print(f"\nNo rental history found for {customer.name}.")

# ------------------------ MAIN PROGRAM -----------------------------

if __name__ == "__main__":
    system = RentalSystem()

    # Add sample cars
    cars_data = [
        ("C1", "Toyota", "Corolla","Economy", 45 ),
        ("C2", "Toyota", "Camry","Economy", 40 ),
        ("C3", "Honda", "Civic","Economy", 45 ),
        ("C4", "BMW", "M5","Luxury", 100 ),
        ("C5", "Mercedes", "C-Class","Luxury", 105 ),
        ("C6", "Honda", "City","Economy", 38 ),
        ("C7", "BMW", "X5", "SUV", 45 ),
        ("C8", "BMW", "M8","Luxury", 120 ),
        ("C9", "Audi", "A6","Luxury", 110 ),
        ("C10", "Audi", "Q7","SUV", 90 ),
        ("C11", "Kia", "Sportage","SUV", 75 ),
        ("C12", "Ford", "Focus","Economy", 45 ),
        ("C13", "Hyundai", "Santro","Economy", 35 ),
        ("C14", "Hyundai", "Elantra","Economy", 60 ),
        ("C15", "Toyota", "Land Cruiser V8","SUV", 110 ),
        ("C16", "Suzuki", "Cultus","Economy", 38 ),
    ]
    for data in cars_data:
        system.add_car(Car(*data))
    # Welcome Customers
    print("Welcome to Smart Car🚗 Rental System")
    # Register customer
    name = input("Enter your name: ")
    customer_id = len(system.customers) + 1
    customer = Customer(customer_id, name)
    system.add_customer(customer)

    print(f"\nWelcome {name}!")

    # Asking for car type and show available cars
    while True:
        car_type = input("Which type of car do you want to rent? (Economy / Luxury / SUV): ").strip()
        if car_type.lower() in ['economy', 'luxury', 'suv']:
            system.show_available_cars_by_type(car_type)
            break
        else:
            print("Invalid type. Please choose from Economy, Luxury, or SUV.")
    while True:
     car_id = input("\nEnter Car ID to rent: ").strip()
    # Checking if Car ID is valid and available
     valid_car = next((car for car in system.cars if car.car_id == car_id and car.available), None)

     if not valid_car:
        print("Invalid Car ID or Car not available. Please try again.")
        continue 

     start_date_str = input("Enter start date (YYYY-MM-DD): ").strip()
     end_date_str = input("Enter end date (YYYY-MM-DD): ").strip()

     try:
        start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
        end_date = datetime.strptime(end_date_str, "%Y-%m-%d")
     except ValueError:
        print("Invalid date format. Please use YYYY-MM-DD.")
        continue
     rental_id = system.book_car(customer, car_id, start_date, end_date)
     if rental_id:
        break
    want_to_return = input("\nDo you want to return the car now? (yes/no): ").strip().lower()

    if want_to_return == "yes":
     while True:
        rental_input = input("Enter your Rental ID to return the car: ").strip()
        rental = next((rental for rental in system.rentals if rental.rental_id == rental_input), None)
        if rental:
            if system.return_car(rental_input):
                break
        else:
            print("Invalid Rental ID. Please enter a valid ID.")
    else:
     print("\nOkay, you can return the car later.")
    show_history = input("\nWould you like to view your rental history? (yes/no): ").strip().lower()
    if show_history == "yes":
        system.view_rental_history(customer)
    else:
        print("\nThank you for using our car rental service. Goodbye!")
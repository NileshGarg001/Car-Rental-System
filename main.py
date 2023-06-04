import time


class Car:
    def __init__(self, carId, make, model, year, rp):
        self.carId = carId
        self.model = model
        self.make = make
        self.year = year
        self.rental_status = False
        self.rental_price = rp
        self.rented_by = None

    def rent_car(self,customer):
        if not self.rental_status:
            self.rented_by = customer
            print(f"{self.make} {self.model} ({self.year}) has been rented by {customer}.")
        else:
            print("Sorry, the car is currently not available for rent.")

    def return_car(self):
        if self.rental_status:
            self.rental_status = False
            rented_by = self.rented_by
            self.rented_by = None
            print(f"{self.make} {self.model} ({self.year}) has been returned by {rented_by}.")
        else:
            print("The car is already available for rent.")

    def get_rental_details(self):
        if not self.rental_status:
            return f"The {self.make} {self.model} ({self.year}) is available for rent at ${self.rental_price} per hour."
        else:
            return f"The {self.make} {self.model} ({self.year}) is currently rented and not available for rent."

    def __str__(self):
        return f"{self.make} {self.model} ({self.year})"


class Customer:
    def __init__(self,customerId, name, contact):
        self.customer_Id = customerId
        self.name = name
        self.contact = contact
        self.rental_history = []
        self.currently_rented = []
        self.pending_money = 0
        # each item in rental history contains rental car, it's rented time and then its return time or null value

    def rent_a_car(self, car):
        """"This method is to be called when user has already decided which car to rent """
        if not car.rental_status:
            car.rental_status = True
            curr = time.time()
            self.rental_history.append([car, curr, "Not Returned"])
            self.currently_rented.append(car)
        else:
            print("Sorry, the car is currently not available for rent.")

    def __returned__(self,car):
        car.rental_status = False
        curr = time.time()
        try:
            for c in self.rental_history:
                id1 = c[0].carId
                id2 = car.carId
                if id1 == id2 and c[2] == "Not Returned":
                    c[2] = curr
                    cost = int(((c[2] - c[1])/3600)*c[0].rental_price)
                    self.pending_money += cost
                    for a in range(len(self.currently_rented)):
                        if self.currently_rented[a].carId == car.carId :
                            self.currently_rented.pop(a)
                            break
                    break
        except:
            print("Car not previously rented ")

    def get_rental_history(self):
        if len(self.rental_history) == 0:
            print("No rental history")
        else:
            for a in self.rental_history:
                if a[2] == "Not Returned":
                    print(f"Car: {a[0]} Rented On : {a[1]} {a[2]}")
                else:
                    print(f"Car: {a[0]} Rented On : {a[1].ctime()} Returned On {a[2].ctime()}")


class RentalManager:
    def __init__(self):
        self.available_cars = []
        self.rented_cars = []
        self.customers = []

    def add_car(self, car):
        self.available_cars.append(car)
        print(f"{car} has been added to the available cars.")

    def remove_car(self, car):
        if car in self.available_cars:
            self.available_cars.remove(car)
            print(f"{car} has been removed from the available cars.")
        elif car in self.rented_cars:
            print(f"{car} is rented by {car.rented_by} . It cannot be removed")
        else:
            print(f"{car} is not found in the inventory.")

    def display_available_cars(self):
        if self.available_cars:
            print("Available Cars:")
            for car in self.available_cars:
                print(f"- {car}")
        else:
            print("No cars available for rent.")

    def handle_rental_request(self, customerid, carid):
        customer1 = self.find_customer(customerid)
        car = self.find_car(carid)
        if customer1 and car:
            customer.rent_car(car)
            self.rented_cars.append(car)
        else:
            print("Invalid customer ID or car ID.")

    def handle_return(self, carid):
        car = self.find_car(carid)
        if car:
            car.return_car()
            self.rented_cars.remove(car)
        else:
            print("Invalid car ID.")

    def generate_rental_report(self):
        print("Rental Report:")
        for car in self.rented_cars:
            print(f"{car}: Rented by {car.rented_by}")

    def find_customer(self, customerid):
        for customer1 in self.customers:
            if customer1.customer_id == customerid:
                return customer1
        return None

    def find_car(self, carid):
        for car in self.available_cars + self.rented_cars:
            if car.carid == carid:
                return car
        return None

    def add_customer(self, customer1):
        self.customers.append(customer1)
        print(f"{customer1} has been added to the customer list.")


class DataStorage:
    def __init__(self, car_file, customer_file):
        self.car_file = car_file
        self.customer_file = customer_file

    def save_cars(self, cars):
        with open(self.car_file, "w") as file:
            for car in cars:
                file.write(f"{car.car_id},{car.make},{car.model},{car.year},{car.rental_price},{car.is_available}\n")

    def load_cars(self):
        cars = []
        try:
            with open(self.car_file, "r") as file:
                for line in file:
                    car_data = line.strip().split(",")
                    car_id, make, model, year, rental_price, is_available = car_data
                    car = Car(car_id, make, model, year, float(rental_price))
                    car.is_available = bool(is_available)
                    cars.append(car)
        except FileNotFoundError:
            print(f"Car file '{self.car_file}' not found. Starting with an empty inventory.")
        return cars

    def save_customers(self, customers):
        with open(self.customer_file, "w") as file:
            for customer in customers:
                file.write(f"{customer.customer_id},{customer.name},{customer.contact_details}\n")

    def load_customers(self):
        customers = []
        try:
            with open(self.customer_file, "r") as file:
                for line in file:
                    customer_data = line.strip().split(",")
                    customer_id, name, contact_details = customer_data
                    customer = Customer(customer_id, name, contact_details)
                    customers.append(customer)
        except FileNotFoundError:
            print(f"Customer file '{self.customer_file}' not found. Starting with an empty customer list.")
        return customers


def display_menu():
    print("Car Rental System Menu:")
    print("1. Rent a Car")
    print("2. Return a Car")
    print("3. View Available Cars")
    print("4. View Rental History")
    print("5. Exit")


# Initialize the RentalManager
rental_manager = RentalManager()

while True:
    display_menu()
    choice = input("Enter your choice: ")

    if choice == "1":
        customer_id = input("Enter your customer ID: ")
        car_id = input("Enter the car ID you want to rent: ")
        rental_manager.handle_rental_request(customer_id, car_id)

    elif choice == "2":
        car_id = input("Enter the car ID you want to return: ")
        rental_manager.handle_return(car_id)

    elif choice == "3":
        rental_manager.display_available_cars()

    elif choice == "4":
        customer_id = input("Enter your customer ID: ")
        customer = rental_manager.find_customer(customer_id)
        if customer:
            customer.display_rental_history()
        else:
            print("Invalid customer ID.")

    elif choice == "5":
        print("Thank you for using the Car Rental System.")
        break

    else:
        print("Invalid choice. Please try again.")


if __name__ == '__main__':
    display_menu()


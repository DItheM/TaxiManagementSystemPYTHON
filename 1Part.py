import re

# Stored Location list array
location_list = ["Melbourne", "Chadstone", "Clayton", "Brighton", "Fitzroy"]
# Stored Customer list array
customer_list = ["Louis", "Ella"]
# Stored Rate Types
rate_type = {
    "standard": 1.5,
    "peak": 1.8,
    "weekends": 2,
    "holiday": 2.5
}
# variable to store destination list
destination_list = []
# dictionarie to store booking history
booking_history = dict()
# Initialize variables to store current location and name selections
dep_location_name = ""
des_location_name = ""
customer_name = ""
# Initialize variables for the trip price calculation
total_distance = 0
basic_fee = 4.2
distance_fee = 0
discount = 0
total_cost = 0
selected_rate = 0

# Input and Validate Customer Name


def input_customer_name():
    global customer_name
    while True:
        customer_name = input(
            "Enter the name of the customer [e-g. Huong]: \n")
        if not re.match("^[a-zA-Z]+$", customer_name):
            print("Please Enter a Valid Customer Name")
        else:
            break

# Input and Validate Departure Location
# validating using location_list


def input_departure_location():
    global dep_location_name
    while True:
        dep_location_name = input(
            "Enter the departure location [enter a valid location only, e-g. Melbourne]:\n")
        if not dep_location_name in location_list:
            print("Please Enter a Valid Location")
        else:
            break

# Check whether the location is already used or not
# get the destination as a parameter
# check using destination_list
# returns a boolean value


def is_destination_already_exists(destination):
    for x in destination_list:
        if x["destination"] == destination:
            return True
    return False

# Input and Validate destination Location
# check whether Departure is equal to Destination or not
# check valid destination using location_list
# calls is_destination_already_exists() to Check whether the location is already used or not


def input_destination_location():
    global des_location_name
    while True:
        des_location_name = input(
            "Enter the destination location [enter a valid location only, e-g. Chadstone]:\n")
        if dep_location_name == des_location_name:
            print("Departure cannot equal to Destination")
        elif not des_location_name in location_list:
            print("Please Enter a Valid Location")
        elif is_destination_already_exists(des_location_name):
            print("You already entered the destination")
        else:
            break

# Validate and input distance


def input_distance():
    global total_distance
    while True:
        dist = input(
            "Enter the distance (km) [enter a positive number only, e-g. 12.5, 6.8]: \n")
        if not re.match("^[0-9]*\.?[0-9]+$", dist):
            print("Please Enter a Valid Distance")
        else:
            total_distance += float(dist)
            # store destination and distance to include in the reciept
            destination_list.append({
                "destination": des_location_name,
                "distance": dist})
            break

# ask for rate and calculate price


def calculate_price():
    global distance_fee, discount, total_cost, selected_rate
    while True:
        # Convert the list of rate names to a comma-separated string
        rate_string = ", ".join(rate_type.keys())
        dist = input(
            f"Enter the rate type [enter a valid type only, {rate_string}]: \n")
        if dist in rate_type:
            # calculating total cost
            selected_rate = rate_type[dist]
            distance_fee = total_distance * rate_type[dist]
            if customer_name in customer_list:
                discount = distance_fee * 0.1
                total_cost = distance_fee + basic_fee - discount
            else:
                total_cost = distance_fee + basic_fee

            # Add destinations to destinations list using destination_list
            destinations = []
            for x in destination_list:
                destinations.append(x["destination"])

            # data model to insert the trip data to booking_history
            model = {
                "Departure": dep_location_name,
                "Destination": destinations,
                "Total cost": total_cost}

            # insert data to booking_history
            if booking_history.get(customer_name) == None:
                booking_history[customer_name] = [model]
            else:
                data_list = []
                for x in booking_history.get(customer_name):
                    data_list.append(x)
                data_list.append(model)
                booking_history[customer_name] = data_list

            # Add customer name to customer_list
            if not customer_name in customer_list:
                customer_list.append(customer_name)
            break
        else:
            print("Please enter a valid option")

# Input and Validate another Destination Location


def input_another_destination():
    global total_distance
    while True:
        answer = input(
            "Do you want to add another destination [y - Yes, n- No]? : \n")
        if answer == "y":
            input_destination_location()
            input_distance()
        elif answer == "n":
            calculate_price()
            show_reciept()

            # resetting the variable for next iterations
            destination_list.clear()
            total_distance = 0
            break
        else:
            print("Please enter a valid option")

# Display Taxi Receipt


def show_reciept():
    print("---------------------------------------------------------")
    print("Taxi Receipt")
    print("---------------------------------------------------------")
    print(f"Name: {customer_name}")
    print(f"Departure: {dep_location_name}")
    # get all destinations using destination_list
    for x in destination_list:
        dest = x["destination"]
        dist = x["distance"]
        print(f"Destination: {dest}")
        print(f"Distance: {dist} (km)")
    print(f"Rate: {selected_rate} (AUD per km)")
    print(f"Total distance: {total_distance} (km)")
    print("---------------------------------------------------------")
    print(f"Basic fee: {basic_fee} (AUD)")
    print(f"Distance fee: {distance_fee:.2f} (AUD)")
    print(f"Discount: {discount:.2f} (AUD)")
    print("---------------------------------------------------------")
    print(f"Total cost: {total_cost:.2f} (AUD)")
    print("---------------------------------------------------------")


# while loop to show menu over and over
while True:
    # Menu
    print("\nWelcome to the RMIT taxi management system! \n ################################################################## \n You can choose from the following options:")
    print(" 1: Book a trip \n 2: Add/update rate types and prices \n 3: Display existing customers\n 4: Display existing locations \n 5: Display existing rate types\n 6: Add new locations \n 7: Display the most valuable customer \n 8: Display a customer booking history \n 0: Exit the program \n")
    print("################################################################## \n ")
    selection = input("Choose one option:")
    # Selection 1: Make a trip
    if selection == "1":
        input_customer_name()
        input_departure_location()
        input_destination_location()
        input_distance()
        input_another_destination()

    # Selection 2: Add new rates and prices
    if selection == "2":
        print("You selected: Add/update rate types and prices")
        # Input rate types
        new_rate_types_input = input(
            "Enter the new rate types or existing rate types separated by commas: ")
        # split singles to new_rate_types array list
        new_rate_types = [rate.strip()
                          for rate in new_rate_types_input.split(",")]

        while True:
            # Input prices
            new_prices_input = input(
                "Enter the prices for the entered rate types separated by commas: ")
            # split singles to new_prices array list
            new_prices = [price.strip()
                          for price in new_prices_input.split(",")]

            # check entered prices are not negative and 0
            is_valid = True
            for price in new_prices:
                if not (re.match(r"^[0-9]*\.?[0-9]+$", price) and float(price) > 0):
                    is_valid = False
                    break

            if is_valid:
                # Update rate_type dictionary with new rate types and prices
                for rate, price in zip(new_rate_types, new_prices):
                    rate_type[rate] = float(price)
                print("New rate types and prices added successfully!")
                break
            else:
                print("Please enter a valid price/prices")

    # Selection 3: Show existing customers
    if selection == "3":
        print("---------------------------------------------------------")
        print("Existing Customers")
        print("---------------------------------------------------------")
        # show every customer by iterating through customer_list
        i = 1
        for x in customer_list:
            print(f"{i}. {x}")
            i += 1

    # Selection 4: Show existing locations
    if selection == "4":
        print("---------------------------------------------------------")
        print("Existing Locations")
        print("---------------------------------------------------------")
        # show every location by iterating through location_list
        i = 1
        for x in location_list:
            print(f"{i}. {x}")
            i += 1

    # Selection 5: Show rate types
    if selection == "5":
        print("---------------------------------------------------------")
        print("Existing Rate Types")
        print("---------------------------------------------------------")
        i = 1
        data = rate_type.items()  # get rate name and rate as a tuple
        # show every rate by iterating through data
        for x in data:
            print(f"{i}. {x[0]}: {x[1]} (AUD per km)")
            i += 1

    # Selection 6: Add new locations
    if selection == "6":
        print("You selected: Add Locations")
        # Input new locations
        new_locations_input = input(
            "Enter the new locations separated by commas: ")
        # split singles to new_rate_types array list
        new_locations = [location.strip()
                         for location in new_locations_input.split(",")]

        # Update Location list array with new locations
        # skip a location and show a message if it already  exists
        for location in new_locations:
            if location in location_list:
                print(f"** {location} already exists")
            else:
                location_list.append(location)
        print("New locations added successfully exept already exist locations!")

    # Selection 7: Display the most valuable customer
    if selection == "7":
        print("You selected: Display the most valuable customer")
        if not booking_history:
            print("No booking history available.")
        else:
            max_spent = 0
            most_valuable_customers = []

            # calculate total spent for a customer
            for customer, bookings in booking_history.items():
                total_spent = sum(booking["Total cost"]
                                  for booking in bookings)

                # find most valuable customer
                if total_spent > max_spent:
                    max_spent = total_spent
                    most_valuable_customers = [customer]
                elif total_spent == max_spent:
                    most_valuable_customers.append(customer)

            # display most valuable customer or customers
            if most_valuable_customers:
                if len(most_valuable_customers) == 1:
                    customer_name = most_valuable_customers[0]
                    total_spent = max_spent
                    print(
                        f"The most valuable customer is {customer_name} with a total spending of {total_spent:.2f} AUD.")
                else:
                    customers = ', '.join(most_valuable_customers)
                    print(
                        f"The most valuable customers are {customers} with a total spending of {max_spent:.2f} AUD each.")
            else:
                print("No customer has spent any money.")

    # Selection 8: Display booking history
    if selection == "8":
        print("You selected: Display a customer booking history")

        # Input and validate customer name
        if booking_history:
            while True:
                customer_name = input("Enter the name of the customer: ")
                if customer_name in booking_history.keys():
                    break
                else:
                    print("Invalid customer name. Please enter a valid customer name.")

            # Display booking history for the customer
            print("---------------------------------------------------------")
            print(f"Booking history of {customer_name}")
            print("---------------------------------------------------------")
            # get trip data by iterate through booking_history dictionary
            for idx, booking in enumerate(booking_history[customer_name], start=1):
                departure = booking.get("Departure", "N/A")
                destinations = ', '.join(booking.get("Destination", []))
                total_cost = booking.get("Total cost", "N/A")

                print(f"Booking {idx}")
                print(f"Departure: {departure}")
                print(f"Destination: {destinations}")
                print(f"Total cost: {total_cost}")
                print()
        else:
            print("No booking history available.")

    # Selection 0: Exit the program
    if selection == "0":
        print("You exited from the program")
        break

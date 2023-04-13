#! /usr/bin/env python3


# imports
import os
import json
import requests
from textwrap import dedent
from datetime import datetime, timedelta

# address calculator
from geopy.geocoders import Nominatim

# define constants
global TOPPINGS, SIZES


# tuple of toppings w/ prices
# will format as (topping, price)
TOPPINGS = [
    
    ("Onions", 2.34),
    ("Ham", 2.35),
    ("Pineapple", 2.40),
    ("Sausage", 2.47),
    ("Pepperoni", 2.67),
    ("Mushrooms", 3.55), 
    ("Black Olives", 3.56),
    ("Extra Cheese", 3.94),
    ("Green Pepper", 3.98),
    ("Basil", 4.17),
    ("Garlic", 4.69),

]


# end values will be multiplied by a base
# value (eg 2) to mainifest price increases
SIZES = [

    ("Small", 0),
    ("Medium", 1),
    ("Large", 2),
    ("Extra", 3),

]


def clear():
    """
    Clear function.
    """
    os.system("cls" if os.name == "nt" else "clear")


class Address_Handler:
    """
    Handles travel time calculation.
    """


    def __init__(self) -> None:
        pass


    def _get_coords(self, address:str):
        """
        Returns a set of longitude and latitude coordinates from
        a given address.

        ### Parameters

        `address` - The address to convert into coordinates.

        ### Returns

        `(float, float)` - The latitude and longitude coordinates, in that order.

        `(None, None)` - A return value indicating that the requested location was
        not valid or does not exist.
        """

        # create object
        geolocator = Nominatim(user_agent="myapplication")

        # timeout is high since it takes a while to finish the request
        location = geolocator.geocode(address, timeout = 99)

        # this is because the given address either doesn't exist or is
        # in invalid format.
        if location == None:

            # returning 2 values to avoid failure in tuple unpacking
            return None, None
        
        return location.latitude, location.longitude


    def get_time_to_area(self, address_1:str, address_2:str):
        """
        Returns the time between locations, in minutes, by car.

        ### Parameters

        `address_1` - The address to start from.

        `address_2` - The address to go to.

        ### Returns

        `(float, False)` - The time it will take to travel between 
        the two points. The second value is a boolean indicator that
        indicates whether or not this is the default value, which
        means that one of the addresses were invalid.

        `(45, True)` - The default travel time value. Default is 45.
        """

        lat_1, long_1 = self._get_coords(address_1)
        lat_2, long_2 = self._get_coords(address_2)

        # check for failed return
        if None in [lat_1, long_1, lat_2, long_2]:
            
            # default value is 45
            # true returned to indicate default
            return 45, True

        # request the api
        api_request = requests.get(f"http://router.project-osrm.org/route/v1/car/{long_1},{lat_1};{long_2},{lat_2}?overview=false")
        routes = json.loads(api_request.content)
        
        # the request itself will return an object, but the
        # dictionary get will return a nonetype object if 
        # the location is invalid.
        if routes.get("routes") is None:
            return 45, True
        
        # calculate in minutes
        time = round(routes.get("routes")[0]["duration"]/60, 2)

        # given time
        return time, False


class Pizza_Program:
    """
    Main Program. Handles user interface and query program.
    """


    def __init__(self) -> None:

        # other data needed to work
        self.home_address = "11430 68 St NW, Edmonton, AB"
        self.welcome_message = dedent(
        """
        Welcome to the Pizza Ordering Script.
        Please select from the Options below to make your custom Pizza!
        """                              
        )
        
        # delivery time handler
        self.address_handler = Address_Handler()
        
        # cost tracking
        self.default_pizza_cost = 10.99
        self.cost = self.default_pizza_cost
        

    def get_size(self):
        """
        Asks user for the size of pizza they want.

        Returns the size as a string and increases the internal 
        object cost counter.
        """


        print(f"Default Pizza Cost: {self.default_pizza_cost}")


        # based on how the list is presented, the user can input a number
        # we have to transform this number into a string.
        num_to_size = {
            "1": "Small",
            "2": "Medium",
            "3": "Large",
            "4": "Extra"
        }


        # the dictionary is used to ensure the choice given exists
        choose_dict = {}

        # the number is used to order the list
        choose_num = 1
        for i in SIZES:

            # this displays the size choice and cost
            print(f"{choose_num}. Size {i[0]}: + ${i[1]*2:.2f}")

            # this creates an entry in the choosing dictionary, with 
            # the value for the choose_num key being the cost of the size.
            choose_dict[f"{choose_num}"] = round(i[1]*2, 2)

            # This adds the string itself to the dictionary, with
            # the value for the string being the cost of the size.
            choose_dict[i[0].lower()] = round(i[1]*2, 2)

            choose_num += 1

        # this loop ensures that incorrect input can be handled indefinitely.
        while 1:

            # we lower the input because that matches the string keys in the
            # choosing dictionary
            choice = input("Please select a size to begin.\n").lower()

            # check if the size exists
            if choose_dict.get(choice) is None:
                print("Sorry, that input is invalid. Please try again.")
                continue

            # return the size
            else:
            
                self.cost += choose_dict[choice]

                # convert number to string if needed
                if num_to_size.get(choice) is not None:
                    choice = num_to_size[choice]
                
                # capitalize since we lowered the input
                return choice.capitalize()


    def get_toppings(self):
        """
        Queries user for Pizza toppings.

        Returns a list of toppings.
        """

        # this dictionary is used to convert the number to the name of the topping
        num_to_name_dict = {}

        # this dictionary is used to store the names and cost of various toppings
        choose_dict = {}

        # used for ordering lists
        choose_num = 1
        
        # used to determine 
        for i in TOPPINGS:
            print(f"{choose_num}. {i[0]}: + ${i[1]}")
            choose_dict[f"{choose_num}"] = round(i[1], 2)
            choose_dict[i[0].lower()] = round(i[1], 2)
            num_to_name_dict[f"{choose_num}"] = i[0].lower()
            choose_num += 1

        chosen_toppings = []
        print("Please enter your desired toppings.")
        print("Hit CTRL+D (CTRL+Z on Windows) to exit, or type \"exit\" to finish selection.")
        while 1:
            try:
                topping = input().lower()


                # convert to name, if needed
                if num_to_name_dict.get(topping) is not None:
                    topping = num_to_name_dict[topping]


                # since we are checking for CTRL+D anyway, we raise an
                # EOFError in order to trigger processing code
                if topping in ["exit", "done"]:
                    raise EOFError


                # check if topping exists
                if choose_dict.get(topping) is None:
                    print("Topping does not exist.")
                    continue

                
                # prevent duplicates
                if topping in chosen_toppings:
                    print("Topping already chosen. Skipping.")
                    continue

                # increase cost and append toppings
                self.cost += choose_dict[topping]
                chosen_toppings.append(topping)

            except EOFError:

                # processing code

                clear()
                
                
                chosen_toppings = [i.capitalize() for i in chosen_toppings]
                
                for i in chosen_toppings:
                    print(i)
                
                
                print("These are your toppings. Continue? [Y/n]")
                should_continue = input().lower()
                
                if "n" in should_continue:
                    print("Exiting program...")
                    exit()
                
                return chosen_toppings
        

    def main(self):
        """
        Main function of class.
        """

        # introduction
        print("Welcome to Pizza Ordering Script.")
        print(self.welcome_message)


        # get address and driving time to address
        address = input("Please enter your address only (no postal code)\n")
        time, is_default = self.address_handler.get_time_to_area(self.home_address, address)
        
        # add time to make pizza (estimate)
        time += 20


        # display message.
        clear()


        # run scripts to get toppings
        size = self.get_size()
        clear()
        toppings = self.get_toppings()
        clear()


        # output
        print(f"Size: {size}\n")

        print("\nToppings:\n")

        for i in toppings:
            print(i)
        
        print()
        print(f"Cost before tax: {self.cost:.2f}")
        print(f"Tax: {self.cost*0.05:.2f}")
        print (f"Total cost: {self.cost + self.cost*0.05:.2f}\n")

        # allow user to exit script if wanted
        continue_ = input("Continue with order? [Y/n]\n")


        if "n" in continue_.lower():
            exit()

        # time processing
        cur_time = datetime.now()
        time_delta = timedelta(minutes=time)
        delivery_time = cur_time + time_delta
        format = '%I:%M:%S %p'
        time_to = delivery_time.time().strftime(format)

        # alert user if default time is used
        if is_default:
            print("Alert; address could not be found.")
            print("Defaulting to 45 minute delivery time.")

        print(f"Delivery time is {time_to}.")
        print("Have a good day!")


def main():
    """
    Main Function of program.
    """
    pizza_thing = Pizza_Program()
    pizza_thing.main()
    return 0
    


if __name__ == "__main__":
    main()
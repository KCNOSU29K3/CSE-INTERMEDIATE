#! /usr/bin/env python3
"""
Module containing resources for interacting with a digital form of a phonebook.
"""
import os
import ssl
import json
import time
import curses
import string
import random
import smtplib
from tqdm import tqdm
from colorama import Fore
from hashlib import sha256
from getpass import getpass
from .textpad import Textbox
from typing import NoReturn


class NoIDError(Exception):
    """
    Error occurring when no available form of id is able to be found.
    """
    pass


class PhoneBook:
    """
    Phonebook construct for interacting with a digital phonebook.
    """

    def __init__(self) -> None:
        pass


    def set_data_file(self, location:str) -> int:
        """
        Sets the location of the data file. Will create a data file
        if needed.

        ### Parameters

        `location` - The location to create the file. Must end in `.json`.

        ### Returns

        `int` - The return status of the function. If the file does not end 
        in `.json`, the return code will be `-1. Otherwise, it will be 0.
        """

        if not location.endswith(".json"):
            return -1

        # assign internal data
        self.data_location = location

        # create file if it doesn't exist
        if not os.path.exists(self.data_location):
            with open(os.path.abspath(self.data_location), "w") as file:

                # constructing a base
                tmp = {
                    "contacts" : {

                    },
                    "count": 0
                }

                json.dump(tmp, file, indent=4),

        return 0


    def get_all_contact_ids(self):
        """
        Returns a list of all contact ids.
        Requires no parameters.
        """
        with open(self.data_location, "r") as file:
            data:dict = json.load(file)

        available_ids = list(data["contacts"].keys())
        return available_ids


    def get_contact_data(self, contact_id:str) -> dict|int:
        """
        Returns the underlying data from the contact id.

        ### Parameters

        `contact_id` - The Contact ID as given in the JSON file.

        ### Returns

        `dict` - The data stored as a dictionary.

        `int` - Indicates that given contact ID does not exist.
        """

        # load data and return
        with open(self.data_location, "r") as file:
            data = json.load(file)

        # check that ID exists
        if data["contacts"].get(contact_id) is None:
            return -1
        
        return data["contacts"][contact_id]


    def lookup_contact(self, name:str) -> list|None:
        """
        Looks up a contact based on a name. Will return a list
        of possible contacts based on what is returned.

        ### Parameters

        `name` - The name to search up.

        ### Returns

        `list` - Possible Contacts.

        `None` - No Contact found.
        """
        first_name:str = name.split(" ")[0]
        last_name:str = name.split(" ")[-1]
        # removing last_name since it will conflict
        # with the search
        if last_name == first_name:
            last_name = None

        # load file and search
        with open(self.data_location, "r") as file:
            contents:dict = json.load(file)
        
        contacts = list(contents["contacts"].keys())
        possible_contacts:list = []

        for contact in contacts:
            if contents["contacts"][contact]["first_name"] == first_name:
                possible_contacts.append(str(contact))
            
            elif contents["contacts"][contact]["last_name"] == last_name:
                possible_contacts.append(str(contact))

        if len(possible_contacts) == 0:
            return None
        
        else:
            return possible_contacts


    def add_contact(
        self,
        name:str,
        phone:str|int|None,
        email:str|None,
        address:str|None,
        identifiers:list|None
        ) -> int|NoIDError:
        """
        Adds a Contact to the contacts list. At least one form of contact
        id is required.

        ### Parameters

        `name` - The name of the contact.

        `phone` - The phone number of the contact. Optional.

        `email` - The email address of the contact. Optional.

        `address` - The address of the contact. Optional.

        `identifiers` - A list of keyword identifiers used for searching
        contacts. Optional.

        ### Returns

        `int` - The Contact was added successfully.

        ### Raises

        `NoIDError` - The addition request did not contain a valid form of
        contact ID.
        """

        # checking that we have some form of id
        if phone is None and email is None:
            raise NoIDError("No ID Found.")

        # encoding everything to string
        # also handling pure int so its more readable
        if isinstance(phone, int):
            tmp:list = []
            phone = str(phone)
            tmp.append(phone[0:3])
            tmp.append("-")
            tmp.append(phone[3:6])
            tmp.append("-")
            tmp.append(phone[6:])
            phone = "".join(tmp)
            pass

        # dealing with names
        name_list = name.split(" ")
        first_name:str = name_list[0]
        last_name:str = name_list[-1]

        if first_name == last_name:
            last_name:None = None

        # generate a hash for id
        # aggregating data
        data:str = first_name
        hash_id = sha256(data.encode()).hexdigest()


        with open(self.data_location, "r") as file:
            contents = json.load(file)

        # create new key name and increment count
        current_count = contents["count"]
        contact_key_name = f"contact_{current_count+1}"
        contents["count"] += 1


        # instantiate the new object
        contents["contacts"][contact_key_name] = {
            "first_name" : first_name,
            "last_name" : last_name,
            "phone" : phone,
            "email" : email,
            "address" : address,
            "identifiers" : identifiers,
            "hash_id":hash_id
        }

        # dumping data to file
        with open(self.data_location, "w") as file:
            json.dump(contents, file, indent=4)


        return 0


    def remove_contact(self, contact_id:str) -> int:
        """
        Removes a contact from the contact list.

        ### Parameters

        `contact_id` - the name of the contact ID as found
        in the JSON file.

        ### Returns

        `int` - Exit code of this method. -1 if the given ID 
        does not exist, otherwise 0.
        """
        # loading contacts

        with open(self.data_location, "r") as file:
            data:dict = json.load(file)

        if data["contacts"].get(contact_id) is None:
            return -1
        new_instance = {
            "contacts":{

            },
            "count": 0
        }

        contacts_list = list(data["contacts"].keys())
        for contact in contacts_list:
            if contact != contact_id:
                new_instance_keyname = f"contact_{new_instance['count']+1}"
                new_instance["contacts"][new_instance_keyname] = data["contacts"][contact]
                new_instance["count"] += 1

        with open(self.data_location, "w") as file:
            json.dump(new_instance, file, indent=4)
        
        return 0


    def find_contact_lists(self, identifers:list[str]) -> list|None:
        """
        Searches contacts given a list of identifer keywords.

        ### Parameters

        `identifers` - A list containing the keywords to search for.

        ### Returns

        `list` - A list of possible contacts fitting the keyword constraints.

        `None` - No contacts found.
        """
        
        # loading content
        with open(self.data_location, "r") as file:
            contacts:dict = json.load(file)

        targets:list = []

        for _ in contacts["contacts"]:
            for identifier in identifers:
                if contacts["contacts"][_]["identifiers"] is None:
                    continue
                if identifier in contacts["contacts"][_]["identifiers"]:
                    targets.append(_)
        
        if len(targets) == 0:
            return None
        
        else:
            return targets


    def send_email(self, sender_email:str, reciever_emails:str|list[str], subject_header:str, contents:str, sender_password:str) -> int:
        """
        Sends an email to a given reciever.

        ### Parameters

        `sender_email` - The email of the sender as a string.

        `reciever_emails` - The email or emails to send the message to.

        `subject_header` - The subject header of the email.

        `contents` - The contents of the email to send.
        """
        # creating context and opening default port for ssl
        port:int = 465
        
        context = ssl.create_default_context()

        # catching possible authentication error
        try:
            # instantiating connection
            with smtplib.SMTP_SSL("smtp.gmail.com", port, context) as server:
                # login
                server.login(sender_email, sender_password)

                # construct and send
                message = f"""\
                Subject: {subject_header}

                {contents}
                """

                server.sendmail(sender_email, reciever_emails, message)


                return 0
        # auth error
        except smtplib.SMTPAuthenticationError:
            return -1


class Wrapper(PhoneBook):

    def __init__(self) -> None:
        # inherit from class
        super().__init__()
        self.set_data_file(".contacts.json")


    def prettify_contact_dictionary(self, contact_id) -> str:
        """
        Formats data to a more human friendly type.

        ### Parameters

        `contact_id` - the contact id of the contact as seen in the json file.
        Ie: contact_1, etc

        ### Returns
        
        `str` - A formatted string containing the data in the contact.
        """

        # get data
        data = self.get_contact_data(contact_id)

        # list all keys
        key_list:list = list(data.keys())

        # convert null last name to empty str to avoid later autoformatting
        if data["last_name"] == None:
            data["last_name"] = ""

        # autoformat all null keys to prettier "Not Found"
        for key in key_list:
            if data[key] is None:
                data[key] = "Not Found"
        
        # format data
        # spaces are for the Fore colored text.
        formatted_data = (f'Name: { data["first_name"] } {data["last_name"]}\n'
        f' Phone Number: {data["phone"]}\n'
        f' Email Address: {data["email"]}\n'
        f' Street Address: {data["address"]}\n'
        f' Contact ID: {contact_id}'
        )

        return formatted_data


class PySimpleGUI_Interface:
    
    def __init__(self) -> None:
        pass


class CLI(Wrapper, PySimpleGUI_Interface):


    def __init__(self) -> None:
        # inherit
        super().__init__()


    def system_clear(self):
        """
        Alias function to clear the screen.
        Requires no parameters and returns `None`.
        """
        os.system("cls" if os.name == "nt" else "clear")


    def add_contact_dialog(self) -> int:
        """
        The CLI Dialog required to add a contact to the phonebook.
        Requires no parameters. Always returns `0`.
        """
        self.system_clear()

        # get needed parameters
        print(Fore.GREEN, "What is the name of the new contact?")
        name:str = input(" ")
        
        self.system_clear()
        print(Fore.GREEN, "What is the phone number of the new contact? (press enter to leave blank)")
        phone_number:str = input(" ").strip(" ")
        
        # phone number conversion
        if phone_number == "":
            phone_number = None
        if "-" not in phone_number:
            phone_number = int(phone_number)
        
        # email
        self.system_clear()
        print(Fore.GREEN, "What is the email address of the new contact? (press enter to leave blank)")
        email:str = input(" ")
        if email == "":
            email = None
        
        # address
        self.system_clear()
        print(Fore.GREEN, "What is the street address of the new contact? (press enter to leave blank)")
        street_addr:str = input(" ")
        if street_addr == "":
            street_addr = None
        
        # identifiers
        self.system_clear()
        print(Fore.GREEN, "What are some identifying keywords about the new contact?\n Seperate them by spaces.\n (press enter to leave blank)")
        keywords:str = input(" ")
        if keywords == "":
            keywords = None
        else:
            keywords = keywords.split(" ")


        # allow user to confirm data
        self.system_clear()
        print(
            Fore.GREEN, 
            "Please Ensure This Information Is Correct:\n"
            f" Name is: {name}\n"
            f" Phone Number is: {phone_number}\n"
            f" Email Address is: {email}\n"
            f" Street Address is: {street_addr}\n"
            f" identifiying keywords are: {keywords}\n"
            " [Y/N]"
        )
        correct = input(" ")
        if "y" not in correct.lower():
            print(Fore.GREEN, "Cancelled.")
            print(Fore.GREEN, "Press Enter To Continue.")
            input(" ")
            return 0


        self.system_clear()
        for i in tqdm(range(25), "Adding Contact", colour="green"):
            time.sleep(random.random() * 0.1)
        
        try:
            self.add_contact(
                name,
                phone_number,
                email,
                street_addr,
                keywords
            )
        except NoIDError:
            print(Fore.RED, "No Contact Method added. Failed to add Contact.")
            print(Fore.RED, "Press Enter To Continue.")
            input(" ")
            return 0

        print(Fore.GREEN, "Contact Added.")
        print(Fore.GREEN, "Click Enter to Continue.")
        input(" ")
        return 0


    def remove_contact_dialog(self) -> int:
        """
        CLI Dialog for removing a contact from the contacts list.
        Requires no parameters and always returns `0`.
        """
        # clear and list contacts
        self.system_clear()
        print(Fore.GREEN, "Here is a list of all contacts.")
        self.list_all_contacts()
        # ask for contact id
        print(Fore.GREEN, "What is the contact id of the contact you wish to delete?")
        contact_id:str = input(" ")

        self.system_clear()
        
        # confirm.
        print(Fore.GREEN, "Are you sure you want to do this? [Y/N]")
        confirm:str = input(" ")
        
        if "y" not in confirm.lower():
            self.system_clear()
            print(Fore.GREEN, "Cancelled.")
            print(Fore.GREEN, "Press Enter to Continue.")
            input(" ") 
            return 0

        self.system_clear()

        # make it seem like we are doing something
        for i in tqdm(range(25), "Removing Contact", colour="green"):
            time.sleep(random.random() * 0.1)
        
        # remove
        self.remove_contact(contact_id)
        
        # inform and return.
        print(Fore.GREEN, "Contact Removed.")
        print(Fore.GREEN, "Press Enter to Continue.")
        input(" ")
        return 0


    def search_contact_name(self) -> int:
        """
        CLI Dialog for searching contacts based on names.
        Requires no Parameters and always returns `0`.
        """
        self.system_clear()
        # get name
        print(Fore.GREEN, "Please enter the Name you you wish to search for.")
        name:str = input(" ")
        self.system_clear()

        # make it seem like we are searching hard
        for i in tqdm(range(25), "Searching...", colour="green"):
            time.sleep(random.random() * 0.1)

        # do the search
        found:list|None = self.lookup_contact(name)

        # none found
        if found is None:
            print(Fore.GREEN, "Found no Contacts by that name.")
            print(Fore.GREEN, "Press Enter to Continue.")
            input(" ")
            return 0
        
        # how many matches
        print(Fore.GREEN, f"Found {len(found)} possible matches.")
        for possible_contact in found:

            # print + format contacts
            print(Fore.GREEN, "~"*10)
            print(Fore.GREEN, self.prettify_contact_dictionary(possible_contact))

        print(Fore.GREEN, "~"*10)
        
        # allow user to look at them
        print("Press Enter to Continue.")
        input(" ")
        return 0


    def send_email_dialog(self) -> None:
        """
        CLI Dialog needed to send an email.
        Requires no parameters and always returns `None`.
        """

        # Curses email editor.
        # the name of the package is very fitting.
        def email_editor() -> str:
            """
            Minimalist Email Editor for sending an email.
            """
            # try for error catching and returning terminal to defaults
            try:
                # creating a mainwindow for the header message
                mainwindow = curses.initscr()
                
                # coloring window 
                curses.start_color()
                curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLUE)
                mainwindow.bkgd(" ", curses.color_pair(1) | curses.A_BOLD)
                # getting max x/y for centering math
                y, x = mainwindow.getmaxyx()
                
                # telling user what to do
                boot_message:str = "EMAIL MESSAGE SYSTEM BOOTED."
                subtext:str = "Please enter your message here. Enter Ctrl+D to save it."
                mainwindow.addstr(0, (x-len(boot_message))//2, boot_message)
                mainwindow.addstr(1, (x-len(subtext))//2, subtext)

                # refreshing window
                mainwindow.refresh()
                
                # echo off to stop keys entered from appearing twice
                curses.noecho()

                # creating a subwindow for the textbox
                editwin = curses.newwin(y,x, 3,0)
                i:Textbox = Textbox(editwin)
                
                # allow user to edit.
                i.edit()

                # get message.
                message:str = i.gather()

            # finally means it always runs.
            finally:

                # shutdown windows
                curses.endwin()

            # return message
            return message

        
        def email_editor_alpha() -> str:
            """
            A VERY primitive email editor.
            Requires no parameters and returns a string.
            """
            print()
            # inform user of stuff
            print(Fore.GREEN, "Enter your message here.")
            print(Fore.GREEN, "Lines once entered cannot be changed.")
            print(Fore.GREEN, "Hit Ctrl+D to save.")
            lines:list = []
            
            # get input
            while True:
                try:
                    line = input(" ")
                except EOFError:
                    break
                lines.append(line)
                lines.append("\n")

            # return input
            return "".join(lines)

        
        # clear after everything
        self.system_clear()

        # get sender email
        print(Fore.GREEN, "What is your email?")
        sender_email:str = input(" ")

        # get sender password
        self.system_clear()
        print(Fore.GREEN, "What is your email password?")
        sender_password:str = getpass(" ")

        # get recipent emails. The send email function can handle a list of emails.
        self.system_clear()
        print(Fore.GREEN, "What is the recipient email?\n Seperate multiple email addresses with spaces.")
        recipient_emails:list[str] = input(" ").split(" ")

        # get the subject headers.
        self.system_clear()
        print(Fore.GREEN, "What is the subject header?")
        subject_header:str = input(" ")

        # get message
        # using the curses editor because you can edit input after hitting enter.
        self.system_clear()

        # make it look like we're actually doing something
        for i in tqdm(range(25), "Booting Email Editor...", colour="green"):
            time.sleep(random.random() * 0.1)
        
        # boot it
        try:
            subject_content:str = email_editor()
        except:
            self.system_clear()
            print(Fore.RED, "EMAIL BOOT FAILED.")
            print(Fore.RED, "USING ALPHA EMAIL EDITOR...")
            subject_content = email_editor_alpha()
            pass
        # confirm with user
        self.system_clear()
        print(Fore.GREEN, "Are you sure you want to send this email? [Y/N]")
        confirm:str = input(" ")

        if "y" not in confirm:
            # clear and cancel
            self.system_clear()
            print(Fore.GREEN, "Cancelling...")
            print(Fore.GREEN, "Press Enter to Continue.")
            input(" ")
            return
        
        # clear
        self.system_clear()
        # make it look like something is happening.
        for i in tqdm(range(25), "Sending Email", colour="green"):
            time.sleep(random.random() * 0.1)

        # try to send the email. Catch server errors.
        try:
            self.send_email(
                sender_email,
                recipient_emails,
                subject_header,
                subject_content,
                sender_password
                )
            print(Fore.GREEN, "Email Sent.\n Press Enter to Continue.")
            input(" ")
            return
        except Exception as e:
            # informing user of error.
            print(Fore.RED, f"UNCAUGHT EXCEPTION: {e}")
            print(Fore.RED, "EMAIL COULD NOT BE SENT.")
            print(Fore.RED, "Press Enter to Continue.")
            input(" ")
            return


    def search_contact_keywords(self) -> int:
        """
        Searches through available contacts based on set keywords.
        Requires no parameters and always returns `0`.
        """
        # clear system
        self.system_clear()
        
        # get keywords
        print(Fore.GREEN, "Please enter a list of keywords you want to search for, seperated by spaces.")
        keywords:str = input(" ").split(" ")
        
        # clear again
        self.system_clear()

        # search bar to make it look a lot harder than it actually is
        for i in tqdm(range(25), "Searching...", colour="green"):
            time.sleep(random.random() * 0.1)
        
        # search
        found:list|None = self.find_contact_lists(keywords)
        
        # nothing found
        if found is None:
            print(Fore.GREEN, "Found No Matches with those keywords.")
            print(Fore.GREEN, "Press Enter to Continue.")
            input(" ")
            return 0

        # print prettyified contact list.
        print(Fore.GREEN, f"Found {len(found)} possible matches.")
        for possible_contact in found:
            print(Fore.GREEN, "~"*10)
            print(Fore.GREEN, self.prettify_contact_dictionary(possible_contact))
        
        # allow user to look at info
        print("Press Enter to Continue.")
        input(" ")
        return 0


    def list_all_contacts(self) -> None:
        """
        Lists all contact IDs.
        Requires no parameters and always returns `None`.
        """
        # breakline
        print(Fore.GREEN, "~"*10)
        
        # iterate through contacts
        for i in self.get_all_contact_ids():
            # print them + add breakline
            print(Fore.GREEN, self.prettify_contact_dictionary(i))
            print(Fore.GREEN, "~"*10)
        
        # allow user to wait
        print(Fore.GREEN, "Press Enter to Continue.")
        input(" ")


    def boot_menu(self) -> NoReturn:
        """
        Instantiates boot menu and runs main program.
        Requires no parameters and does not return.
        """
        # make it feel cool
        self.system_clear()
        for i in tqdm(range(0, 100), "Booting...", colour="green"):
            # randomizing time
            time.sleep(0.1 * random.random())

        # clear screen
        self.system_clear()

        # present list
        # tmp is for choice indexing
        options_list:list[str] = ["CLI", "PySimpleGUI"]
        tmp:int = 0

        # print the boot message
        print(Fore.GREEN,"Phonebook System Booted.")
        print(Fore.GREEN, "Interface Options:")
        for i in options_list:
            time.sleep(0.5)
            print(Fore.GREEN, f"{i} [{tmp}]")
            tmp += 1

        # ask for input, check to make sure numerical
        time.sleep(0.5)
        print(Fore.GREEN, "Please Select An Interface (number): ")
        interface:str = input(" ")

        tmp:list[str] = [i for i in string.ascii_letters + string.punctuation]
        for i in tmp:
            if i in interface:
                print(Fore.RED, "SYSTEM ERROR: INCORRECT INPUT")
                print(Fore.RED,"IRRECOVERABLE: EXITING")
                exit(-1)

        # match statement to determine which version to launch
        match int(interface):
            case 0:
                self.CLI_main()
            case _:
                print(Fore.RED, "ERROR: NOT IMPLEMENTED")
                print(Fore.RED, "IRRECOVERABLE: EXITING")
                exit (-1)


    def CLI_main(self):
        """
        Runs the CLI Version of the main program.
        """
        # clear
        self.system_clear()
        # make user feel nice
        for i in tqdm(range(50), "Booting CLI...", colour="green"):
            time.sleep(random.random() / 10)

        # giving user list of options

        # loop forever
        while True:

            # clear after every dialog returns
            self.system_clear()

            # provide list of options
            options_list:list[str] = [
                "Add A Contact",
                "Remove A Contact",
                "List All Contacts",
                "Find A Contact With A Name",
                "Find A Contact With A Keyword",
                "Send An Email (Assumes Access to Account)",
                "Exit"
            ]

            # list all options
            tmp:int = 0
            for i in options_list:
                time.sleep(0.2)
                print(Fore.GREEN, f"{i} [{tmp}]")
                tmp += 1

            time.sleep(0.5)
            print(Fore.GREEN, "Please Select An Option (number): ")
            option:str = input(" ")

            # verify input
            tmp:list[str] = [i for i in string.ascii_letters + string.punctuation]
            for i in tmp:
                if i in option:
                    print(Fore.RED, "SYSTEM ERROR: INCORRECT INPUT")
                    print(Fore.RED,"IRRECOVERABLE: EXITING")
                    exit(-1)

            # match statement for cleaner code
            match int(option):
                case 0:
                    # add contact
                    self.add_contact_dialog()
                case 1:
                    # remove contact
                    self.remove_contact_dialog()
                case 2:
                    # list all contacts
                    # because of the way in which the function
                    # works we need to clear it like this.
                    self.system_clear()
                    self.list_all_contacts()
                case 3:
                    # search with names
                    self.search_contact_name()
                case 4:
                    # search with keywords
                    self.search_contact_keywords()
                case 5:
                    # send email dialog
                    self.send_email_dialog()
                case 6:
                    # exiting code
                    self.system_clear()
                    print(Fore.GREEN, "Beginning Exit...")
                    for i in tqdm(range(25), "Saving Program State", colour="green"):
                        time.sleep(random.random() * 0.1)
                    self.system_clear()
                    exit(0)
                case _:
                    # user chose nonexistent option
                    print(Fore.RED, "ERROR: NOT IMPLEMENTED")
                    print(Fore.RED, "IRRECOVERABLE: EXITING")
                    exit(-1)


def init_program():
    """
    Intializes the main program.
    """
    # catching errors
    try:

        i = CLI()
        i.boot_menu()

    # informing user of error, providing them with a solution, and exiting
    except Exception as e:

        print(Fore.RED, "UNCAUGHT EXCEPTION")
        print(Fore.RED, f"EXCEPTION: {e}")
        print(Fore.RED, "inform author at w.garrioch456@gmail.com with the name of the error.")
        print(Fore.RED, "IRRECOVERABLE: EXITING")
        exit(-1)

    # catching keyboard interrupt to avoid traceback
    except KeyboardInterrupt:

        print(Fore.RED, "\n KILL SIGNAL RECIEVED; EXITING")
        exit(0)


if __name__ == "__main__":
    init_program()
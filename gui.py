import tkinter as tk
# I import tkinter and call it tk so I can create the GUI window, labels, buttons, entries, and frames

from tkinter import messagebox
# I import messagebox so I can show pop-up messages like errors, success messages, and warnings

from datetime import datetime, date
# I import datetime and date so I can check if the booking date is written correctly and is in the future


from user import User
# I import the User class because normal users can create accounts, log in, and make bookings

from admin import Administrator
# I import the Administrator class because admins have extra features like managing users and facilities

from access_type import AccessType
# I import AccessType so I can create Standard and Premium access types

from facility import StudyRoom, SportCourt, EventHall
# I import the different facility classes so the system can create study rooms, sport courts, and event halls

from booking import Booking
# I import Booking so the system can create booking objects when a user reserves a facility

from confirmation_record import ConfirmationRecord
# I import ConfirmationRecord so the system can create a receipt/confirmation after booking

from data_manager import DataManager
# I import DataManager so the GUI can save and load users, facilities, bookings, and records


class BookingGUI:
    # This class controls the whole graphical user interface for the Smart Campus Facility Booking System

    def __init__(self):
        # This constructor starts the whole GUI program when I create a BookingGUI object

        self.main_window = tk.Tk()
        # I create the main Tkinter window where all pages and buttons will appear

        self.main_window.title("Smart Campus Facility Booking System")
        # I set the title that appears at the top of the window

        self.main_window.geometry("1050x700")
        # I set the window size to 1050 pixels wide and 700 pixels tall

        self.main_window.resizable(False, False)
        # I stop the user from resizing the window so the layout stays neat

        self.dataManager = DataManager(
            "users.pkl",
            "facilities.pkl",
            "bookings.pkl",
            "confirmation_records.pkl"
        )
        # I create a DataManager object and tell it the file names where the system data will be saved

        self.users = self.dataManager.loadUsers()
        # I load the saved users from the users file

        self.facilities = self.dataManager.loadFacilities()
        # I load the saved facilities from the facilities file

        self.bookings = self.dataManager.loadBookings()
        # I load the saved bookings from the bookings file

        self.confirmationRecords = self.dataManager.loadConfirmationRecords()
        # I load the saved confirmation records from the confirmation records file

        self.currentUser = None
        # At the start, no user is logged in yet, so I set currentUser to None

        self.standardAccess = AccessType("Standard", ["StudyRoom"], False, 1)
        # I create Standard access, where the user can only book StudyRoom and does not have priority

        self.premiumAccess = AccessType("Premium", ["StudyRoom", "SportCourt", "EventHall"], True, 3)
        # I create Premium access, where the user can book all facility types and has priority access

        if len(self.facilities) == 0:
            # I check if there are no facilities saved yet

            self.createSampleFacilities()
            # If the facilities list is empty, I create sample facilities so the system has something to show

        self.showLoginPage()
        # I start the program by showing the login page first

        self.main_window.mainloop()
        # I keep the GUI window open and running so the user can interact with it

    def clearWindow(self):
        # This function clears the current page before showing a new page

        for widget in self.main_window.winfo_children():
            # I go through every widget currently inside the main window

            widget.destroy()
            # I remove each widget so the next page can appear cleanly

    def saveAllData(self):
        # This function saves all important system data at once

        self.dataManager.saveUsers(self.users)
        # I save the updated users list

        self.dataManager.saveFacilities(self.facilities)
        # I save the updated facilities list

        self.dataManager.saveBookings(self.bookings)
        # I save the updated bookings list

        self.dataManager.saveConfirmationRecords(self.confirmationRecords)
        # I save the updated confirmation records list

    def refreshFacilityStatus(self, facility):
        # This function checks the facility slots and updates the facility status

        if len(facility.getAvailableTimeSlots()) == 0:
            # If there are no available time slots left

            facility.setBookingStatus("Fully Booked")
            # I set the facility status to Fully Booked

        else:
            # If there is at least one available time slot

            facility.setBookingStatus("Available")
            # I set the facility status to Available

    def validateFutureDate(self, dateText):
        # This function checks if the date is written correctly and is a future date

        try:
            # I use try because the user might type the date in the wrong format

            bookingDate = datetime.strptime(dateText, "%Y-%m-%d").date()
            # I convert the text into a real date using the required format YYYY-MM-DD

            if bookingDate <= date.today():
                # I check if the chosen booking date is today or in the past

                return False
                # If it is today or past, I return False because booking must be for the future

            return True
            # If the date is valid and in the future, I return True

        except ValueError:
            # If Python cannot convert the text into a date, it means the format is wrong

            return False
            # I return False because the date is not valid

    def createSampleFacilities(self):
        # This function creates sample facilities when the system has no saved facilities yet

        self.facilities.append(
            StudyRoom(1, "Study Room A", "Library", 10, ["10:00", "12:00", "2:00"], "Available", 20.0, 4)
        )
        # I add a study room with an ID, name, location, capacity, slots, status, fee, and number of tables

        self.facilities.append(
            SportCourt(2, "Basketball Court", "Sports Building", 20, ["9:00", "1:00", "5:00"], "Available", 50.0, "Basketball")
        )
        # I add a sport court with its details, including the sport type Basketball

        self.facilities.append(
            EventHall(3, "Main Event Hall", "Block C", 100, ["11:00", "3:00", "6:00"], "Available", 100.0, True)
        )
        # I add an event hall with its details, including that it has an audio system

        self.dataManager.saveFacilities(self.facilities)
        # I save these sample facilities so they stay available next time the program runs

    def showLoginPage(self):
        # This function shows the login page to the user

        self.clearWindow()
        # I clear anything currently on the screen before building the login page

        top_frame = tk.Frame(self.main_window)
        # I create a top frame for the page title

        middle_frame = tk.Frame(self.main_window)
        # I create a middle frame for the email and password input boxes

        bottom_frame = tk.Frame(self.main_window)
        # I create a bottom frame for the login and account buttons

        top_frame.pack(pady=25)
        # I place the top frame in the window and add vertical spacing

        middle_frame.pack(pady=10)
        # I place the middle frame with smaller vertical spacing

        bottom_frame.pack(pady=20)
        # I place the bottom frame with spacing around the buttons

        tk.Label(top_frame, text="Smart Campus Facility Booking System", font=("Arial", 20)).pack()
        # I display the system title at the top of the login page

        tk.Label(middle_frame, text="Email:").grid(row=0, column=0, padx=10, pady=10)
        # I create the Email label and place it in the first row

        emailBox = tk.Entry(middle_frame, width=35)
        # I create an input box where the user can type their email

        emailBox.grid(row=0, column=1, padx=10, pady=10)
        # I place the email input box beside the Email label

        tk.Label(middle_frame, text="Password:").grid(row=1, column=0, padx=10, pady=10)
        # I create the Password label and place it in the second row

        passwordBox = tk.Entry(middle_frame, width=35, show="*")
        # I create the password input box, and show="*" hides the password while typing

        passwordBox.grid(row=1, column=1, padx=10, pady=10)
        # I place the password input box beside the Password label

        def login():
            # This inner function runs when the user clicks the Login button

            email = emailBox.get()
            # I get the email typed by the user

            password = passwordBox.get()
            # I get the password typed by the user

            if email == "" or password == "":
                # I check if the user left either field empty

                messagebox.showerror("Error", "Please enter email and password.")
                # I show an error message asking the user to fill both fields

                return
                # I stop the login process because the input is incomplete

            for user in self.users:
                # I loop through all saved users to find a matching account

                if user.login(email, password):
                    # I call the user's login method to check if the email and password match

                    self.currentUser = user
                    # If login is correct, I store this user as the current logged-in user

                    if isinstance(user, Administrator):
                        # I check if the logged-in user is an Administrator

                        self.showAdminDashboard()
                        # If it is an admin, I show the admin dashboard

                    else:
                        # If the user is not an admin

                        self.showUserDashboard()
                        # I show the normal user dashboard

                    return
                    # I stop the function because login was successful

            messagebox.showerror("Error", "Invalid email or password.")
            # If no matching user was found, I show an error message

        tk.Button(bottom_frame, text="Login", width=22, command=login).grid(row=0, column=0, padx=10, pady=10)
        # I create a Login button that runs the login function when clicked

        tk.Button(bottom_frame, text="Create Account", width=22, command=self.showCreateAccountPage).grid(row=0, column=1, padx=10, pady=10)
        # I create a Create Account button that moves the user to the account creation page

        tk.Button(bottom_frame, text="Create Admin Demo", width=22, command=self.createAdminDemo).grid(row=1, column=0, columnspan=2, pady=10)
        # I create a demo admin button that creates a sample admin account for testing

    def createAdminDemo(self):
        # This function creates a demo admin account if it does not already exist

        for user in self.users:
            # I loop through all saved users

            if user.getEmail() == "admin@zu.ac.ae":
                # I check if the demo admin email already exists

                messagebox.showinfo("Admin Exists", "Admin already exists.\nEmail: admin@zu.ac.ae\nPassword: 123")
                # If it exists, I show the user the admin login details

                return
                # I stop the function so I do not create the admin twice

        admin = Administrator(999, "Admin", "admin@zu.ac.ae", "123", self.premiumAccess)
        # I create a new Administrator object with demo login details and Premium access

        self.users.append(admin)
        # I add the new admin to the users list

        self.dataManager.saveUsers(self.users)
        # I save the updated users list so the admin account stays saved

        messagebox.showinfo("Admin Created", "Admin email: admin@zu.ac.ae\nPassword: 123")
        # I show a message telling the user the admin account was created

    def showCreateAccountPage(self):
        # This function shows the page where a new user can create an account

        self.clearWindow()
        # I clear the login page before showing the create account page

        top_frame = tk.Frame(self.main_window)
        # I create a top frame for the page title

        form_frame = tk.Frame(self.main_window)
        # I create a form frame for name, email, and password input boxes

        button_frame = tk.Frame(self.main_window)
        # I create a button frame for Create and Back buttons

        top_frame.pack(pady=20)
        # I place the title frame on the window

        form_frame.pack(pady=10)
        # I place the form frame below the title

        button_frame.pack(pady=20)
        # I place the button frame below the form

        tk.Label(top_frame, text="Create Account", font=("Arial", 20)).pack()
        # I display the Create Account title

        tk.Label(form_frame, text="Name:").grid(row=0, column=0, padx=10, pady=10)
        # I create the Name label in the form

        nameBox = tk.Entry(form_frame, width=35)
        # I create an input box for the user's name

        nameBox.grid(row=0, column=1, padx=10, pady=10)
        # I place the name input beside the Name label

        tk.Label(form_frame, text="Email:").grid(row=1, column=0, padx=10, pady=10)
        # I create the Email label

        emailBox = tk.Entry(form_frame, width=35)
        # I create an input box for the user's email

        emailBox.grid(row=1, column=1, padx=10, pady=10)
        # I place the email input beside the Email label

        tk.Label(form_frame, text="Password:").grid(row=2, column=0, padx=10, pady=10)
        # I create the Password label

        passwordBox = tk.Entry(form_frame, width=35, show="*")
        # I create a password input box and hide the typed password with stars

        passwordBox.grid(row=2, column=1, padx=10, pady=10)
        # I place the password input beside the Password label

        def createAccount():
            # This inner function runs when the user clicks Create

            name = nameBox.get()
            # I get the name typed by the user

            email = emailBox.get()
            # I get the email typed by the user

            password = passwordBox.get()
            # I get the password typed by the user

            if name == "" or email == "" or password == "":
                # I check if any field is empty

                messagebox.showerror("Error", "Please fill all fields.")
                # I show an error message because all fields are required

                return
                # I stop the function until the user fills everything

            for user in self.users:
                # I check all existing users

                if user.getEmail() == email:
                    # I check if the entered email is already used

                    messagebox.showerror("Error", "This email already exists.")
                    # I show an error because two users should not have the same email

                    return
                    # I stop account creation

            newUser = User(len(self.users) + 1, name, email, password, self.standardAccess)
            # I create a new normal user with a new ID and Standard access by default

            self.users.append(newUser)
            # I add the new user to the users list

            self.dataManager.saveUsers(self.users)
            # I save the updated users list to the file

            messagebox.showinfo("Success", "Account created successfully.")
            # I show a success message after creating the account

            self.showLoginPage()
            # I send the user back to the login page so they can log in

        tk.Button(button_frame, text="Create", width=20, command=createAccount).grid(row=0, column=0, padx=10, pady=10)
        # I create a Create button that runs createAccount when clicked

        tk.Button(button_frame, text="Back", width=20, command=self.showLoginPage).grid(row=0, column=1, padx=10, pady=10)
        # I create a Back button that returns to the login page

    def showUserDashboard(self):
        # This function shows the normal user dashboard after login

        self.clearWindow()
        # I clear the previous page before showing the dashboard

        top_frame = tk.Frame(self.main_window)
        # I create a top frame for welcome text and access type

        button_frame = tk.Frame(self.main_window)
        # I create a button frame for dashboard actions

        top_frame.pack(pady=25)
        # I place the top frame with spacing

        button_frame.pack(pady=20)
        # I place the button frame under it

        tk.Label(top_frame, text="User Dashboard", font=("Arial", 20)).pack()
        # I show the User Dashboard title

        tk.Label(top_frame, text="Welcome " + self.currentUser.getName()).pack(pady=8)
        # I welcome the currently logged-in user by their name

        tk.Label(top_frame, text="Access Type: " + self.currentUser.getAccessType().getTypeName()).pack(pady=5)
        # I show the user's current access type, like Standard or Premium

        tk.Button(button_frame, text="View Facilities", width=30, command=self.showFacilitiesPage).grid(row=0, column=0, padx=10, pady=8)
        # This button takes the user to the facilities page

        tk.Button(button_frame, text="View Booking History", width=30, command=self.showBookingHistory).grid(row=1, column=0, padx=10, pady=8)
        # This button lets the user see their previous bookings

        tk.Button(button_frame, text="Upgrade to Premium", width=30, command=self.upgradeCurrentUser).grid(row=2, column=0, padx=10, pady=8)
        # This button upgrades the current user to Premium access

        tk.Button(button_frame, text="Update Profile", width=30, command=self.showUpdateProfilePage).grid(row=3, column=0, padx=10, pady=8)
        # This button opens the page where the user can update their name, email, and password

        tk.Button(button_frame, text="Logout", width=30, command=self.showLoginPage).grid(row=4, column=0, padx=10, pady=8)
        # This button logs the user out by returning to the login page

    def upgradeCurrentUser(self):
        # This function upgrades the logged-in user to Premium access

        self.currentUser.setAccessType(self.premiumAccess)
        # I change the current user's access type to Premium

        self.dataManager.saveUsers(self.users)
        # I save the users list so the upgrade is not lost

        messagebox.showinfo("Access Upgraded", "Your access type is now Premium.")
        # I show a message to confirm the upgrade

        self.showUserDashboard()
        # I refresh the user dashboard so it shows the new access type

    def showFacilitiesPage(self):
        # This function shows all facilities that the user can view and try to book

        self.clearWindow()
        # I clear the dashboard before showing the facilities page

        top_frame = tk.Frame(self.main_window)
        # I create a top frame for the page title and access type

        facility_frame = tk.Frame(self.main_window)
        # I create a frame where each facility row will be displayed

        button_frame = tk.Frame(self.main_window)
        # I create a frame for the Back button

        top_frame.pack(pady=10)
        # I place the top frame

        facility_frame.pack(pady=10)
        # I place the facility list frame

        button_frame.pack(pady=10)
        # I place the button frame

        tk.Label(top_frame, text="Available Facilities", font=("Arial", 20)).pack()
        # I show the title for the facilities page

        tk.Label(top_frame, text="Your Access Type: " + self.currentUser.getAccessType().getTypeName()).pack(pady=5)
        # I show the user's access type so they know what they are allowed to book

        rowNumber = 0
        # I start rowNumber at 0 so I can place each facility in a new row

        for facility in self.facilities:
            # I loop through every facility saved in the system

            self.refreshFacilityStatus(facility)
            # I update the facility status before displaying it

            facilityText = (
                facility.getName()
                + " | Type: " + facility.getFacilityType()
                + " | Capacity: " + str(facility.getCapacity())
                + " | Status: " + facility.getBookingStatus()
                + " | Slots: " + str(facility.getAvailableTimeSlots())
                + " | Fee: " + str(facility.getFee()) + " AED/hour"
            )
            # I build one text line that shows the facility name, type, capacity, status, slots, and fee

            tk.Label(
                facility_frame,
                text=facilityText,
                width=85,
                anchor="w",
                justify="left",
                wraplength=850
            ).grid(row=rowNumber, column=0, padx=10, pady=8)
            # I display the facility details as a label in the facility frame

            tk.Button(
                facility_frame,
                text="Book",
                width=10,
                command=lambda f=facility: self.showBookingPage(f)
            ).grid(row=rowNumber, column=1, padx=5, pady=8)
            # I create a Book button beside each facility, and lambda makes sure the correct facility is sent

            rowNumber += 1
            # I move to the next row for the next facility

        tk.Button(button_frame, text="Back", width=20, command=self.showUserDashboard).pack()
        # I create a Back button to return to the user dashboard

    def showBookingPage(self, facility):
        # This function shows the form where the user books a selected facility

        self.clearWindow()
        # I clear the facilities page before showing the booking form

        top_frame = tk.Frame(self.main_window)
        # I create a top frame for the title and facility details

        form_frame = tk.Frame(self.main_window)
        # I create a form frame for user inputs

        button_frame = tk.Frame(self.main_window)
        # I create a button frame for Calculate, Confirm, and Back buttons

        top_frame.pack(pady=10)
        # I place the top frame

        form_frame.pack(pady=10)
        # I place the form frame

        button_frame.pack(pady=10)
        # I place the button frame

        tk.Label(top_frame, text="Book Facility", font=("Arial", 20)).pack()
        # I show the booking page title

        tk.Label(top_frame, text=facility.displayDetails(), wraplength=900).pack(pady=5)
        # I display the selected facility details and wrap long text so it fits

        tk.Label(top_frame, text="Available Slots: " + str(facility.getAvailableTimeSlots())).pack(pady=5)
        # I show the available time slots for this facility

        tk.Label(top_frame, text="Date format must be YYYY-MM-DD. Booking must be for a future date.").pack(pady=5)
        # I give the user instructions for the correct date format

        tk.Label(form_frame, text="Date:").grid(row=0, column=0, padx=10, pady=10)
        # I create a Date label

        dateBox = tk.Entry(form_frame, width=35)
        # I create an entry box for the booking date

        dateBox.grid(row=0, column=1, padx=10, pady=10)
        # I place the date input beside the Date label

        tk.Label(form_frame, text="Time Slot:").grid(row=1, column=0, padx=10, pady=10)
        # I create a Time Slot label

        timeBox = tk.Entry(form_frame, width=35)
        # I create an entry box for the user to type a time slot

        timeBox.grid(row=1, column=1, padx=10, pady=10)
        # I place the time slot box beside the label

        tk.Label(form_frame, text="Duration:").grid(row=2, column=0, padx=10, pady=10)
        # I create a Duration label

        durationBox = tk.Entry(form_frame, width=35)
        # I create an entry box for the booking duration

        durationBox.grid(row=2, column=1, padx=10, pady=10)
        # I place the duration box beside the label

        tk.Label(form_frame, text="Participants:").grid(row=3, column=0, padx=10, pady=10)
        # I create a Participants label

        participantsBox = tk.Entry(form_frame, width=35)
        # I create an entry box for the number of participants

        participantsBox.grid(row=3, column=1, padx=10, pady=10)
        # I place the participants box beside the label

        costLabel = tk.Label(form_frame, text="Total Cost: ")
        # I create a label where the calculated cost will appear

        costLabel.grid(row=4, column=0, columnspan=2, padx=10, pady=10)
        # I place the cost label under the form inputs

        def calculateCostOnly():
            # This inner function calculates the price without confirming the booking

            try:
                # I use try because the duration might not be a valid number

                duration = float(durationBox.get())
                # I take the duration from the input box and convert it to a decimal number

                if duration <= 0:
                    # I check that duration is greater than 0

                    messagebox.showerror("Error", "Duration must be greater than 0.")
                    # I show an error if the duration is 0 or negative

                    return
                    # I stop the calculation

                totalCost = facility.calculateFee(duration)
                # I calculate the total cost using the facility fee and duration

                costLabel.config(text="Total Cost: " + str(totalCost) + " AED")
                # I update the cost label to show the calculated total cost

            except ValueError:
                # If duration cannot be converted to a number

                messagebox.showerror("Error", "Duration must be a number.")
                # I show an error message telling the user to enter a number

        def confirmBooking():
            # This inner function confirms the booking after checking all rules

            try:
                # I use try because duration and participants need to be converted into numbers

                bookingDate = dateBox.get()
                # I get the booking date from the date input box

                timeSlot = timeBox.get()
                # I get the selected time slot from the time input box

                duration = float(durationBox.get())
                # I convert the duration into a decimal number

                participants = int(participantsBox.get())
                # I convert the participants into a whole number

                if bookingDate == "" or timeSlot == "":
                    # I check if date or time slot was left empty

                    messagebox.showerror("Error", "Please fill all fields.")
                    # I show an error because the booking needs all details

                    return
                    # I stop the booking process

                if not self.validateFutureDate(bookingDate):
                    # I check if the date format is correct and if the date is in the future

                    messagebox.showerror("Error", "Date must be in YYYY-MM-DD format and must be a future date.")
                    # I show an error if the date is invalid

                    return
                    # I stop the booking process

                if duration <= 0:
                    # I check if the duration is valid

                    messagebox.showerror("Error", "Duration must be greater than 0.")
                    # I show an error if the duration is 0 or negative

                    return
                    # I stop the booking process

                if participants <= 0:
                    # I check if participants is at least 1

                    messagebox.showerror("Error", "Participants must be greater than 0.")
                    # I show an error if the participant number is not valid

                    return
                    # I stop the booking process

                if participants > facility.getCapacity():
                    # I check if the number of participants is more than the facility capacity

                    messagebox.showerror("Error", "Participants exceed facility capacity.")
                    # I show an error if too many people are trying to book

                    return
                    # I stop the booking process

                if timeSlot not in facility.getAvailableTimeSlots():
                    # I check if the selected time slot is available

                    messagebox.showerror("Error", "This time slot is not available.")
                    # I show an error if the slot is already booked or does not exist

                    return
                    # I stop the booking process

                if not self.currentUser.getAccessType().canBook(facility.getFacilityType()):
                    # I check if the current user's access type allows this facility type

                    messagebox.showerror("Error", "Your access type does not allow booking this facility type.")
                    # I show an error if the user does not have permission

                    return
                    # I stop the booking process

                totalCost = facility.calculateFee(duration)
                # After all checks pass, I calculate the final booking cost

                booking = Booking(
                    len(self.bookings) + 1,
                    bookingDate,
                    timeSlot,
                    duration,
                    participants,
                    totalCost,
                    "Confirmed",
                    self.currentUser,
                    facility
                )
                # I create a new Booking object using the booking details

                confirmation = ConfirmationRecord(
                    len(self.confirmationRecords) + 1,
                    booking,
                    facility.getName(),
                    facility.getLocation(),
                    bookingDate,
                    timeSlot,
                    duration,
                    totalCost
                )
                # I create a confirmation record, like a receipt for the confirmed booking

                booking.setConfirmationRecord(confirmation)
                # I connect the confirmation record to the booking

                self.currentUser.addBooking(booking)
                # I add the booking to the current user's booking history

                self.bookings.append(booking)
                # I add the booking to the full system booking list

                self.confirmationRecords.append(confirmation)
                # I add the confirmation record to the full confirmation records list

                facility.updateAvailability(timeSlot, False)
                # I remove the booked time slot from the available slots

                self.refreshFacilityStatus(facility)
                # I update the facility status after the slot is booked

                self.saveAllData()
                # I save users, facilities, bookings, and records after the booking is confirmed

                messagebox.showinfo(
                    "Success",
                    "Booking confirmed.\nTotal cost: " + str(totalCost) + " AED\nConfirmation record created."
                )
                # I show a success pop-up with the total cost and confirmation message

                self.showUserDashboard()
                # After booking, I return the user to the dashboard

            except ValueError:
                # If duration or participants were typed in the wrong format

                messagebox.showerror("Error", "Duration must be a number and participants must be a whole number.")
                # I show an error explaining what type of input is required

        tk.Button(button_frame, text="Calculate Cost", width=20, command=calculateCostOnly).grid(row=0, column=0, padx=10, pady=10)
        # I create a Calculate Cost button that only calculates price

        tk.Button(button_frame, text="Confirm Booking", width=20, command=confirmBooking).grid(row=0, column=1, padx=10, pady=10)
        # I create a Confirm Booking button that validates and saves the booking

        tk.Button(button_frame, text="Back", width=20, command=self.showFacilitiesPage).grid(row=0, column=2, padx=10, pady=10)
        # I create a Back button that returns to the facilities page

    def showBookingHistory(self):
        # This function shows the current user's booking history

        self.clearWindow()
        # I clear the current page before showing booking history

        top_frame = tk.Frame(self.main_window)
        # I create a top frame for the title

        history_frame = tk.Frame(self.main_window)
        # I create a frame to display each booking

        button_frame = tk.Frame(self.main_window)
        # I create a frame for the Back button

        top_frame.pack(pady=10)
        # I place the top frame

        history_frame.pack(pady=10)
        # I place the booking history frame

        button_frame.pack(pady=10)
        # I place the button frame

        tk.Label(top_frame, text="Booking History", font=("Arial", 20)).pack()
        # I show the Booking History page title

        rowNumber = 0
        # I start rowNumber at 0 so every booking can be displayed on a new row

        if len(self.currentUser.getBookingHistory()) == 0:
            # I check if the user has no bookings

            tk.Label(history_frame, text="No bookings found").grid(row=0, column=0, pady=10)
            # If the list is empty, I show a simple message

        else:
            # If the user has bookings

            for booking in self.currentUser.getBookingHistory():
                # I loop through every booking in the current user's history

                bookingText = (
                    "Booking ID: " + str(booking.getBookingId()) + "\n"
                    "Date: " + booking.getBookingDate() + "\n"
                     "Time: " + str(
                    booking.getTimeSlot()) + "\n"
                    "Duration: " + str(booking.getDuration()) + "\n"
                    "Participants: " + str(
                    booking.getNumberOfParticipants()) + "\n"
                    "Facility: " + booking.getFacility().getName() + "\n"
                    "Cost: " + str(
                    booking.getTotalCost()) + " AED\n"
                    "Status: " + booking.getStatus()
                )
                # I build a multi-line text that shows the booking details clearly

                tk.Label(
                    history_frame,
                    text=bookingText,
                    width=55,
                    anchor="w",
                    justify="left",
                    relief="solid",
                    padx=10,
                    pady=8
                ).grid(row=rowNumber, column=0, padx=10, pady=8)
                # I display the booking details inside a bordered label

                tk.Button(
                    history_frame,
                    text="Modify",
                    width=10,
                    command=lambda b=booking: self.showModifyBookingPage(b)
                ).grid(row=rowNumber, column=1, padx=5, pady=8)
                # I create a Modify button for this exact booking

                tk.Button(
                    history_frame,
                    text="Delete",
                    width=10,
                    command=lambda b=booking: self.deleteBooking(b)
                ).grid(row=rowNumber, column=2, padx=5, pady=8)
                # I create a Delete button for this exact booking

                rowNumber += 1
                # I move to the next row for the next booking

        tk.Button(button_frame, text="Back", width=20, command=self.showUserDashboard).pack()
        # I create a Back button to return to the user dashboard

    def showModifyBookingPage(self, booking):
        # This function opens a page where the user can edit an existing booking

        self.clearWindow()
        # I clear the booking history page before showing the modify form

        top_frame = tk.Frame(self.main_window)
        # I create a top frame for the title and current booking details

        form_frame = tk.Frame(self.main_window)
        # I create a form frame for the new booking values

        button_frame = tk.Frame(self.main_window)
        # I create a button frame for saving or going back

        top_frame.pack(pady=10)
        # I place the top frame

        form_frame.pack(pady=10)
        # I place the form frame

        button_frame.pack(pady=10)
        # I place the button frame

        tk.Label(top_frame, text="Modify Booking", font=("Arial", 20)).pack()
        # I show the Modify Booking page title

        tk.Label(top_frame, text="Current Booking: " + booking.displayBookingDetails(), wraplength=900).pack(pady=5)
        # I show the current booking details so the user knows what they are editing

        tk.Label(top_frame, text="Date format must be YYYY-MM-DD and must be a future date.").pack(pady=5)
        # I remind the user about the correct date format

        tk.Label(form_frame, text="New Date:").grid(row=0, column=0, padx=10, pady=10)
        # I create a label for the new date input

        dateBox = tk.Entry(form_frame, width=35)
        # I create an input box for the new booking date

        dateBox.insert(0, booking.getBookingDate())
        # I fill the box with the current booking date as a starting value

        dateBox.grid(row=0, column=1, padx=10, pady=10)
        # I place the date box beside the label

        tk.Label(form_frame, text="New Time Slot:").grid(row=1, column=0, padx=10, pady=10)
        # I create a label for the new time slot input

        timeBox = tk.Entry(form_frame, width=35)
        # I create an input box for the new time slot

        timeBox.insert(0, booking.getTimeSlot())
        # I fill the box with the current time slot

        timeBox.grid(row=1, column=1, padx=10, pady=10)
        # I place the time slot box beside its label

        tk.Label(form_frame, text="New Duration:").grid(row=2, column=0, padx=10, pady=10)
        # I create a label for the new duration input

        durationBox = tk.Entry(form_frame, width=35)
        # I create an input box for the new duration

        durationBox.insert(0, str(booking.getDuration()))
        # I fill the box with the current duration, converting it to text

        durationBox.grid(row=2, column=1, padx=10, pady=10)
        # I place the duration box beside its label

        tk.Label(form_frame, text="Participants:").grid(row=3, column=0, padx=10, pady=10)
        # I create a label for the participant number

        participantsBox = tk.Entry(form_frame, width=35)
        # I create an input box for the new number of participants

        participantsBox.insert(0, str(booking.getNumberOfParticipants()))
        # I fill the box with the current number of participants

        participantsBox.grid(row=3, column=1, padx=10, pady=10)
        # I place the participants box beside the label

        def saveChanges():
            # This function runs when the user clicks Save Changes to modify an existing booking

            try:
                # I use try because some values need to be converted into numbers, and the user might type something wrong

                newDate = dateBox.get()
                # I get the new date that the user typed in the date box

                newTimeSlot = timeBox.get()
                # I get the new time slot that the user typed in the time slot box

                newDuration = float(durationBox.get())
                # I get the new duration and convert it to a decimal number

                newParticipants = int(participantsBox.get())
                # I get the new number of participants and convert it to a whole number

                if newDate == "" or newTimeSlot == "":
                    # I check if the user left the date or time slot empty

                    messagebox.showerror("Error", "Please fill all fields.")
                    # I show an error message because these fields are required

                    return
                    # I stop the function so the booking is not updated with missing information

                if not self.validateFutureDate(newDate):
                    # I check if the new date is written in the correct format and is in the future

                    messagebox.showerror("Error", "Date must be in YYYY-MM-DD format and must be a future date.")
                    # I show an error if the date is wrong or not a future date

                    return
                    # I stop the function because the date is not valid

                if newDuration <= 0 or newParticipants <= 0:
                    # I check that the duration and participants are both greater than 0

                    messagebox.showerror("Error", "Duration and participants must be greater than 0.")
                    # I show an error if the user enters 0 or a negative number

                    return
                    # I stop the function because the booking details are not valid

                facility = booking.getFacility()
                # I get the facility that belongs to this booking

                oldTimeSlot = booking.getTimeSlot()
                # I save the old time slot before changing it

                facility.updateAvailability(oldTimeSlot, True)
                # I temporarily make the old time slot available again, so the system can check the new slot properly

                if newParticipants > facility.getCapacity():
                    # I check if the new number of participants is more than the facility capacity

                    facility.updateAvailability(oldTimeSlot, False)
                    # Since the change is not allowed, I put the old time slot back as booked

                    messagebox.showerror("Error", "Participants exceed facility capacity.")
                    # I show an error message explaining the problem

                    return
                    # I stop the update process

                if newTimeSlot not in facility.getAvailableTimeSlots():
                    # I check if the new time slot is available in the facility list

                    facility.updateAvailability(oldTimeSlot, False)
                    # Since the new slot is not available, I put the old time slot back as booked

                    messagebox.showerror("Error", "This time slot is not available.")
                    # I show an error telling the user the time slot cannot be used

                    return
                    # I stop the update process

                if not self.currentUser.getAccessType().canBook(facility.getFacilityType()):
                    # I check if the user's access type allows them to book this facility type

                    facility.updateAvailability(oldTimeSlot, False)
                    # Since the user is not allowed, I restore the old time slot as booked

                    messagebox.showerror("Error", "Your access type does not allow this facility.")
                    # I show an error message about the access type restriction

                    return
                    # I stop the update process

                newCost = facility.calculateFee(newDuration)
                # I calculate the new total cost based on the new duration

                booking.setBookingDate(newDate)
                # I update the booking date with the new date

                booking.setTimeSlot(newTimeSlot)
                # I update the booking time slot with the new time slot

                booking.setDuration(newDuration)
                # I update the booking duration

                booking.setNumberOfParticipants(newParticipants)
                # I update the number of participants

                booking.setTotalCost(newCost)
                # I update the total cost after recalculating it

                confirmation = booking.getConfirmationRecord()
                # I get the confirmation record connected to this booking

                if confirmation is not None:
                    # I check if this booking already has a confirmation record

                    confirmation.setDate(newDate)
                    # I update the date inside the confirmation record too

                    confirmation.setTimeSlot(newTimeSlot)
                    # I update the time slot inside the confirmation record

                    confirmation.setDuration(newDuration)
                    # I update the duration inside the confirmation record

                    confirmation.setCost(newCost)
                    # I update the cost inside the confirmation record

                facility.updateAvailability(newTimeSlot, False)
                # I mark the new time slot as booked, so no one else can book it

                self.refreshFacilityStatus(facility)
                # I update the facility status after changing the slot availability

                self.saveAllData()
                # I save all updated users, facilities, bookings, and confirmation records

                messagebox.showinfo("Success", "Booking modified successfully.")
                # I show a success message to tell the user the booking was updated

                self.showBookingHistory()
                # I return the user to the booking history page

            except ValueError:
                # If duration or participants were not entered as numbers, Python will come here

                messagebox.showerror("Error", "Duration must be a number and participants must be a whole number.")
                # I show an error explaining the correct input type

        tk.Button(button_frame, text="Save Changes", width=20, command=saveChanges).grid(row=0, column=0, padx=10,
                                                                                         pady=10)
        # I create the Save Changes button, and when clicked it runs saveChanges

        tk.Button(button_frame, text="Back", width=20, command=self.showBookingHistory).grid(row=0, column=1, padx=10,
                                                                                             pady=10)
        # I create the Back button, and when clicked it returns to the booking history page

    def deleteBooking(self, booking):
        # This function deletes a booking from the user history and system records

        facility = booking.getFacility()
        # I get the facility linked to this booking

        timeSlot = booking.getTimeSlot()
        # I get the time slot that was booked

        facility.updateAvailability(timeSlot, True)
        # Since the booking is being deleted, I make that time slot available again

        self.refreshFacilityStatus(facility)
        # I update the facility status after freeing the time slot

        self.currentUser.cancelBooking(booking.getBookingId())
        # I remove the booking from the current user's booking history

        self.bookings = [
            b for b in self.bookings
            if b.getBookingId() != booking.getBookingId()
        ]
        # I rebuild the bookings list and keep only bookings that are not the deleted booking

        self.confirmationRecords = [
            record for record in self.confirmationRecords
            if record.getBooking().getBookingId() != booking.getBookingId()
        ]
        # I also remove the confirmation record that belongs to the deleted booking

        self.saveAllData()
        # I save all updated data after deleting the booking

        messagebox.showinfo("Deleted", "Booking deleted successfully.")
        # I show a message that the booking was deleted

        self.showBookingHistory()
        # I refresh the booking history page

    def showUpdateProfilePage(self):
        # This function shows the page where the user can update their profile

        self.clearWindow()
        # I clear the current screen first

        top_frame = tk.Frame(self.main_window)
        # I create a top frame for the title

        form_frame = tk.Frame(self.main_window)
        # I create a form frame for the input boxes

        button_frame = tk.Frame(self.main_window)
        # I create a button frame for Update and Back buttons

        top_frame.pack(pady=20)
        # I place the top frame with spacing

        form_frame.pack(pady=10)
        # I place the form frame below the title

        button_frame.pack(pady=20)
        # I place the button frame below the form

        tk.Label(top_frame, text="Update Profile", font=("Arial", 20)).pack()
        # I display the page title

        tk.Label(form_frame, text="New Name:").grid(row=0, column=0, padx=10, pady=10)
        # I create a label for the new name field

        nameBox = tk.Entry(form_frame, width=35)
        # I create an input box for the user's name

        nameBox.insert(0, self.currentUser.getName())
        # I fill the input box with the user's current name

        nameBox.grid(row=0, column=1, padx=10, pady=10)
        # I place the name box beside the label

        tk.Label(form_frame, text="New Email:").grid(row=1, column=0, padx=10, pady=10)
        # I create a label for the new email field

        emailBox = tk.Entry(form_frame, width=35)
        # I create an input box for the user's email

        emailBox.insert(0, self.currentUser.getEmail())
        # I fill the input box with the user's current email

        emailBox.grid(row=1, column=1, padx=10, pady=10)
        # I place the email box beside the label

        tk.Label(form_frame, text="New Password:").grid(row=2, column=0, padx=10, pady=10)
        # I create a label for the new password field

        passwordBox = tk.Entry(form_frame, width=35)
        # I create an input box for the user's password

        passwordBox.insert(0, self.currentUser.getPassword())
        # I fill the input box with the user's current password

        passwordBox.grid(row=2, column=1, padx=10, pady=10)

        # I place the password box beside the label

        def updateProfile():
            # This function runs when the user clicks the Update button

            if nameBox.get() == "" or emailBox.get() == "" or passwordBox.get() == "":
                # I check if any profile field is empty

                messagebox.showerror("Error", "Please fill all fields.")
                # I show an error because all profile fields are required

                return
                # I stop the function so empty data is not saved

            self.currentUser.updateProfile(nameBox.get(), emailBox.get(), passwordBox.get())
            # I update the current user's name, email, and password using the values from the input boxes

            self.dataManager.saveUsers(self.users)
            # I save the updated users list

            messagebox.showinfo("Success", "Profile updated.")
            # I show a success message

            self.showUserDashboard()
            # I return the user to the dashboard

        tk.Button(button_frame, text="Update", width=20, command=updateProfile).grid(row=0, column=0, padx=10, pady=10)
        # I create the Update button that saves the profile changes

        tk.Button(button_frame, text="Back", width=20, command=self.showUserDashboard).grid(row=0, column=1, padx=10,
                                                                                            pady=10)
        # I create the Back button that returns to the user dashboard without updating

    def showAdminDashboard(self):
        # This function shows the main dashboard for the administrator

        self.clearWindow()
        # I clear the current page before showing the admin dashboard

        top_frame = tk.Frame(self.main_window)
        # I create a top frame for the page title

        button_frame = tk.Frame(self.main_window)
        # I create a frame for all admin action buttons

        top_frame.pack(pady=20)
        # I place the title frame

        button_frame.pack(pady=20)
        # I place the button frame

        tk.Label(top_frame, text="Admin Dashboard", font=("Arial", 20)).pack()
        # I show the Admin Dashboard title

        tk.Button(button_frame, text="View Daily Bookings", width=35, command=self.showDailyBookingsPage).grid(row=0, column=0, padx=10, pady=7)
        tk.Button(button_frame, text="View Facility Status", width=35, command=self.showAdminFacilityStatus).grid(row=1, column=0, padx=10, pady=7)
        tk.Button(button_frame, text="Update Facility Availability", width=35, command=self.showUpdateFacilityAvailabilityPage).grid(row=2, column=0, padx=10, pady=7)
        tk.Button(button_frame, text="Monitor Facility Usage", width=35, command=self.showFacilityUsagePage).grid(row=3, column=0, padx=10, pady=7)
        tk.Button(button_frame, text="Upgrade User Access", width=35, command=self.showUpgradeUserPage).grid(row=4, column=0, padx=10, pady=7)
        tk.Button(button_frame, text="Manage Users", width=35, command=self.showManageUsersPage).grid(row=5, column=0, padx=10, pady=7)
        tk.Button(button_frame, text="Logout", width=35, command=self.showLoginPage).grid(row=6, column=0, padx=10, pady=7)

    def showDailyBookingsPage(self):
        # This function shows a page where the admin can search bookings by date

        self.clearWindow()
        # I clear the current page before showing the Daily Bookings page

        top_frame = tk.Frame(self.main_window)
        # I create a top frame for the page title

        form_frame = tk.Frame(self.main_window)
        # I create a form frame for the date input

        result_frame = tk.Frame(self.main_window)
        # I create a result frame where booking results will appear

        button_frame = tk.Frame(self.main_window)
        # I create a button frame for the Search and Back buttons

        top_frame.pack(pady=10)
        # I place the top frame with spacing

        form_frame.pack(pady=10)
        # I place the form frame below the title

        result_frame.pack(pady=10)
        # I place the result frame where booking results will appear

        button_frame.pack(pady=10)
        # I place the button frame at the bottom

        tk.Label(top_frame, text="Daily Bookings", font=("Arial", 20)).pack()
        # I display the Daily Bookings page title

        tk.Label(form_frame, text="Enter Date:").grid(row=0, column=0, padx=10, pady=10)
        # I create a label asking the admin to enter a date

        dateBox = tk.Entry(form_frame, width=35)
        # I create an input box where the admin types the date

        dateBox.grid(row=0, column=1, padx=10, pady=10)
        # I place the date input box beside the label

        def searchBookings():
            # This function runs when the admin clicks Search

            for widget in result_frame.winfo_children():
                # I loop through everything currently inside the result frame

                widget.destroy()
                # I remove old search results before showing new ones

            searchDate = dateBox.get()
            # I get the date typed by the admin

            if searchDate == "":
                # I check if the admin left the date empty

                messagebox.showerror("Error", "Please enter a date.")
                # I show an error because a date is required

                return
                # I stop the search process

            dailyBookings = self.currentUser.viewDailyBookings(searchDate, self.bookings)
            # I ask the admin object to return all bookings that match the entered date

            if len(dailyBookings) == 0:
                # I check if no bookings were found for this date

                tk.Label(result_frame, text="No bookings for this date.").pack()
                # I display a message saying there are no bookings

            else:
                # If bookings exist for this date

                for booking in dailyBookings:
                    # I loop through every booking found

                    tk.Label(result_frame, text=booking.displayBookingDetails(), width=90, anchor="w", wraplength=900).pack(pady=5)
                    # I display the booking details in the result frame

        tk.Button(button_frame, text="Search", width=20, command=searchBookings).grid(row=0, column=0, padx=10, pady=10)
        # I create a Search button that runs searchBookings

        tk.Button(button_frame, text="Back", width=20, command=self.showAdminDashboard).grid(row=0, column=1, padx=10, pady=10)
        # I create a Back button that returns to the admin dashboard

    def showAdminFacilityStatus(self):
        # This function shows the admin all facilities and their current status

        self.clearWindow()
        # I clear the current page before showing facility status

        top_frame = tk.Frame(self.main_window)
        # I create a top frame for the page title

        status_frame = tk.Frame(self.main_window)
        # I create a frame where facility information will be displayed

        button_frame = tk.Frame(self.main_window)
        # I create a frame for the Back button

        top_frame.pack(pady=10)
        # I place the top frame

        status_frame.pack(pady=10)
        # I place the status frame

        button_frame.pack(pady=10)
        # I place the button frame

        tk.Label(top_frame, text="Facility Status", font=("Arial", 20)).pack()
        # I display the Facility Status title

        rowNumber = 0
        # I start rowNumber at 0 so each facility appears on a new row

        for facility in self.facilities:
            # I loop through every facility in the system

            self.refreshFacilityStatus(facility)
            # I refresh the facility status before displaying it

            text = (
                "Name: " + facility.getName() + "\n"
                "Type: " + facility.getFacilityType() + "\n"
                "Location: " + facility.getLocation() + "\n"
                "Capacity: " + str(
                facility.getCapacity()) + "\n"
                "Status: " + facility.getBookingStatus() + "\n"
                "Available Slots: " + str(
                facility.getAvailableTimeSlots()) + "\n"
                "Fee: " + str(facility.getFee()) + " AED/hour"
            )
            # I build a full multi-line description of the facility

            tk.Label(
                status_frame,
                text=text,
                width=60,
                anchor="w",
                justify="left",
                relief="solid",
                padx=10,
                pady=8
            ).grid(row=rowNumber, column=0, padx=10, pady=8)
            # I display the facility details inside a bordered label

            rowNumber += 1
            # I move to the next row for the next facility

        self.dataManager.saveFacilities(self.facilities)
        # I save the facilities after refreshing their statuses

        tk.Button(button_frame, text="Back", width=20, command=self.showAdminDashboard).pack()
        # I create a Back button to return to the admin dashboard

    def showUpdateFacilityAvailabilityPage(self):
        # This function allows the admin to manage facility time slots

        self.clearWindow()
        # I clear the current page before showing the availability page

        top_frame = tk.Frame(self.main_window)
        # I create a top frame for the page title

        facility_frame = tk.Frame(self.main_window)
        # I create a frame where facility availability will be displayed

        button_frame = tk.Frame(self.main_window)
        # I create a frame for the Back button

        top_frame.pack(pady=10)
        # I place the title frame

        facility_frame.pack(pady=10)
        # I place the facility frame

        button_frame.pack(pady=10)
        # I place the button frame

        tk.Label(top_frame, text="Update Facility Availability", font=("Arial", 20)).pack()
        # I display the page title

        rowNumber = 0
        # I start row numbering at 0

        for facility in self.facilities:
            # I loop through all facilities

            self.refreshFacilityStatus(facility)
            # I refresh the status before displaying it

            text = (
                facility.getName()
                + " | Status: " + facility.getBookingStatus()
                + " | Slots: " + str(facility.getAvailableTimeSlots())
            )
            # I create a short text showing the facility name, status, and available slots

            tk.Label(
                facility_frame,
                text=text,
                width=85,
                anchor="w",
                justify="left",
                wraplength=850
            ).grid(row=rowNumber, column=0, padx=10, pady=5)
            # I display the facility information

            tk.Button(
                facility_frame,
                text="Edit",
                width=10,
                command=lambda f=facility: self.showEditSingleFacilityAvailability(f)
            ).grid(row=rowNumber, column=1, padx=5, pady=5)
            # I create an Edit button for this exact facility

            rowNumber += 1
            # I move to the next row

        tk.Button(button_frame, text="Back", width=20, command=self.showAdminDashboard).pack()
        # I create a Back button that returns to the admin dashboard

    def showEditSingleFacilityAvailability(self, facility):
        # This function allows the admin to add or remove slots for one facility

        self.clearWindow()
        # I clear the page before showing the edit form

        top_frame = tk.Frame(self.main_window)
        # I create a top frame for the title and current slots

        form_frame = tk.Frame(self.main_window)
        # I create a form frame for entering a slot

        button_frame = tk.Frame(self.main_window)
        # I create a frame for action buttons

        top_frame.pack(pady=10)
        # I place the title frame

        form_frame.pack(pady=10)
        # I place the form frame

        button_frame.pack(pady=10)
        # I place the button frame

        tk.Label(top_frame, text="Edit Availability for " + facility.getName(), font=("Arial", 20)).pack()
        # I display the facility name in the title

        tk.Label(top_frame, text="Current Slots: " + str(facility.getAvailableTimeSlots()), wraplength=900).pack(pady=5)
        # I display the facility’s current available slots

        tk.Label(form_frame, text="Time Slot:").grid(row=0, column=0, padx=10, pady=10)
        # I create a label asking for a time slot

        slotBox = tk.Entry(form_frame, width=35)
        # I create an input box for entering a slot

        slotBox.grid(row=0, column=1, padx=10, pady=10)
        # I place the input box beside the label

        def addSlot():
            # This function adds a new available slot

            slot = slotBox.get()
            # I get the slot typed by the admin

            if slot == "":
                # I check if the admin left the slot empty

                messagebox.showerror("Error", "Please enter a time slot.")
                # I show an error message

                return
                # I stop the function

            facility.updateAvailability(slot, True)
            # I add the slot as available

            self.refreshFacilityStatus(facility)
            # I refresh the facility status

            self.dataManager.saveFacilities(self.facilities)
            # I save the updated facilities

            messagebox.showinfo("Success", "Time slot added.")
            # I show a success message

            self.showUpdateFacilityAvailabilityPage()
            # I return to the availability page

        def removeSlot():
            # This function removes a slot from the facility

            slot = slotBox.get()
            # I get the slot typed by the admin

            if slot == "":
                # I check if the slot field is empty

                messagebox.showerror("Error", "Please enter a time slot.")
                # I show an error message

                return
                # I stop the function

            facility.updateAvailability(slot, False)
            # I remove the slot from availability

            self.refreshFacilityStatus(facility)
            # I refresh the facility status

            self.dataManager.saveFacilities(self.facilities)
            # I save the updated facilities list

            messagebox.showinfo("Success", "Time slot removed.")
            # I show a success message

            self.showUpdateFacilityAvailabilityPage()
            # I return to the availability page

        tk.Button(button_frame, text="Add Slot", width=20, command=addSlot).grid(row=0, column=0, padx=10, pady=10)
        tk.Button(button_frame, text="Remove Slot", width=20, command=removeSlot).grid(row=0, column=1, padx=10, pady=10)
        tk.Button(button_frame, text="Back", width=20, command=self.showUpdateFacilityAvailabilityPage).grid(row=0, column=2, padx=10, pady=10)

    def showFacilityUsagePage(self):
        # This function shows how many times each facility was booked

        self.clearWindow()
        # I clear the current page before showing the usage page

        top_frame = tk.Frame(self.main_window)
        # I create a top frame for the page title

        usage_frame = tk.Frame(self.main_window)
        # I create a frame where the usage results will be shown

        button_frame = tk.Frame(self.main_window)
        # I create a frame for the Back button

        top_frame.pack(pady=10)
        # I place the top frame

        usage_frame.pack(pady=10)
        # I place the usage frame

        button_frame.pack(pady=10)
        # I place the button frame

        tk.Label(top_frame, text="Facility Usage Monitoring", font=("Arial", 20)).pack()
        # I display the title of the page

        rowNumber = 0
        # I start from row 0 so each facility can be shown on a separate row

        for facility in self.facilities:
            # I loop through each facility in the system

            count = 0
            # I start the booking count at 0 for this facility

            for booking in self.bookings:
                # I loop through all bookings in the system

                if booking.getFacility().getFacilityId() == facility.getFacilityId():
                    # I check if this booking belongs to the current facility

                    count += 1
                    # If it matches, I add 1 to the count

            text = facility.getName() + " was booked " + str(count) + " time(s). Capacity: " + str(
                facility.getCapacity())
            # I create a sentence showing how many times the facility was booked and its capacity

            tk.Label(
                usage_frame,
                text=text,
                width=85,
                anchor="w",
                justify="left",
                wraplength=850
            ).grid(row=rowNumber, column=0, padx=10, pady=5)
            # I display the usage information on the page

            rowNumber += 1
            # I move to the next row for the next facility

        tk.Button(button_frame, text="Back", width=20, command=self.showAdminDashboard).pack()
        # I create a Back button to return to the admin dashboard

    def showUpgradeUserPage(self):
        # This function shows all normal users so the admin can upgrade them

        self.clearWindow()
        # I clear the current screen before showing the upgrade page

        top_frame = tk.Frame(self.main_window)
        # I create a top frame for the page title

        user_frame = tk.Frame(self.main_window)
        # I create a frame where users will be listed

        button_frame = tk.Frame(self.main_window)
        # I create a frame for the Back button

        top_frame.pack(pady=10)
        # I place the top frame

        user_frame.pack(pady=10)
        # I place the user list frame

        button_frame.pack(pady=10)
        # I place the button frame

        tk.Label(top_frame, text="Upgrade User Access", font=("Arial", 20)).pack()
        # I display the page title

        rowNumber = 0
        # I start rowNumber at 0 to place each user on a new row

        for user in self.users:
            # I loop through every user in the system

            if not isinstance(user, Administrator):
                # I only show normal users because admins do not need to be upgraded

                userText = user.getName() + " - " + user.getEmail() + " - " + user.getAccessType().getTypeName()
                # I create a text line showing the user's name, email, and current access type

                tk.Label(
                    user_frame,
                    text=userText,
                    width=75,
                    anchor="w",
                    justify="left",
                    wraplength=750
                ).grid(row=rowNumber, column=0, padx=10, pady=5)
                # I display the user's information on the page

                tk.Button(
                    user_frame,
                    text="Upgrade",
                    width=10,
                    command=lambda u=user: self.upgradeUser(u)
                ).grid(row=rowNumber, column=1, padx=5, pady=5)
                # I create an Upgrade button for this specific user

                rowNumber += 1
                # I move to the next row for the next user

        tk.Button(button_frame, text="Back", width=20, command=self.showAdminDashboard).pack()
        # I create a Back button to return to the admin dashboard

    def upgradeUser(self, user):
        # This function upgrades the selected user to Premium access

        user.setAccessType(self.premiumAccess)
        # I change the user's access type to Premium

        self.dataManager.saveUsers(self.users)
        # I save the users list so the upgrade is stored

        messagebox.showinfo("Success", user.getName() + " upgraded to Premium.")
        # I show a success message with the user's name

        self.showUpgradeUserPage()
        # I refresh the upgrade user page

    def showManageUsersPage(self):
        # This function allows the admin to view, add, modify, and delete users

        self.clearWindow()
        # I clear the current page before showing the manage users page

        top_frame = tk.Frame(self.main_window)
        # I create a top frame for the title

        user_frame = tk.Frame(self.main_window)
        # I create a frame where user rows will be displayed

        button_frame = tk.Frame(self.main_window)
        # I create a frame for Add New User and Back buttons

        top_frame.pack(pady=10)
        # I place the top frame

        user_frame.pack(pady=10)
        # I place the user list frame

        button_frame.pack(pady=10)
        # I place the button frame

        tk.Label(top_frame, text="Manage Users", font=("Arial", 20)).pack()
        # I display the Manage Users title

        rowNumber = 0
        # I start at row 0 for displaying users

        for user in self.users:
            # I loop through all users

            if not isinstance(user, Administrator):
                # I only display normal users, not admin accounts

                userText = user.getName() + " | " + user.getEmail() + " | " + user.getAccessType().getTypeName()
                # I create a text line showing the user's name, email, and access type

                tk.Label(
                    user_frame,
                    text=userText,
                    width=70,
                    anchor="w",
                    justify="left",
                    wraplength=700
                ).grid(row=rowNumber, column=0, padx=10, pady=5)
                # I display the user's information in the user frame

                tk.Button(
                    user_frame,
                    text="Modify",
                    width=8,
                    command=lambda u=user: self.showAdminModifyUserPage(u)
                ).grid(row=rowNumber, column=1, padx=5, pady=5)
                # I create a Modify button for this specific user

                tk.Button(
                    user_frame,
                    text="Delete",
                    width=8,
                    command=lambda u=user: self.adminDeleteUser(u)
                ).grid(row=rowNumber, column=2, padx=5, pady=5)
                # I create a Delete button for this specific user

                rowNumber += 1
                # I move to the next row for the next user

        tk.Button(button_frame, text="Add New User", width=20, command=self.showAdminAddUserPage).grid(row=0, column=0,
                                                                                                       padx=10, pady=10)
        # I create an Add New User button so the admin can create a user account

        tk.Button(button_frame, text="Back", width=20, command=self.showAdminDashboard).grid(row=0, column=1, padx=10,
                                                                                             pady=10)
        # I create a Back button to return to the admin dashboard

    def showAdminAddUserPage(self):
        # This function shows a form for the admin to add a new user

        self.clearWindow()
        # I clear the manage users page before showing the add user form

        top_frame = tk.Frame(self.main_window)
        # I create a top frame for the title

        form_frame = tk.Frame(self.main_window)
        # I create a form frame for user information inputs

        button_frame = tk.Frame(self.main_window)
        # I create a button frame for Add User and Back buttons

        top_frame.pack(pady=20)
        # I place the top frame

        form_frame.pack(pady=10)
        # I place the form frame

        button_frame.pack(pady=20)
        # I place the button frame

        tk.Label(top_frame, text="Admin Add User", font=("Arial", 20)).pack()
        # I display the Add User page title

        tk.Label(form_frame, text="Name:").grid(row=0, column=0, padx=10, pady=10)
        # I create a label for the user's name

        nameBox = tk.Entry(form_frame, width=35)
        # I create an input box for the user's name

        nameBox.grid(row=0, column=1, padx=10, pady=10)
        # I place the name input box beside the label

        tk.Label(form_frame, text="Email:").grid(row=1, column=0, padx=10, pady=10)
        # I create a label for the user's email

        emailBox = tk.Entry(form_frame, width=35)
        # I create an input box for the user's email

        emailBox.grid(row=1, column=1, padx=10, pady=10)
        # I place the email input box beside the label

        tk.Label(form_frame, text="Password:").grid(row=2, column=0, padx=10, pady=10)
        # I create a label for the user's password

        passwordBox = tk.Entry(form_frame, width=35)
        # I create an input box for the user's password

        passwordBox.grid(row=2, column=1, padx=10, pady=10)
        # I place the password input box beside the label

        tk.Label(form_frame, text="Access Type:").grid(row=3, column=0, padx=10, pady=10)
        # I create a label for choosing the user's access type

        accessVar = tk.StringVar(value="Standard")
        # I create a variable to store the selected access type, and the default is Standard

        tk.OptionMenu(form_frame, accessVar, "Standard", "Premium").grid(row=3, column=1, padx=10, pady=10)

        # I create a dropdown menu so the admin can choose Standard or Premium

        def addUser():
            # This function runs when the admin clicks Add User

            name = nameBox.get()
            # I get the name typed by the admin

            email = emailBox.get()
            # I get the email typed by the admin

            password = passwordBox.get()
            # I get the password typed by the admin

            if name == "" or email == "" or password == "":
                # I check if any input field is empty

                messagebox.showerror("Error", "Please fill all fields.")
                # I show an error because all fields are required

                return
                # I stop the function so the user is not created with missing data

            for user in self.users:
                # I loop through all existing users

                if user.getEmail() == email:
                    # I check if the email is already used by another user

                    messagebox.showerror("Error", "This email already exists.")
                    # I show an error because emails must be unique

                    return
                    # I stop the function

            if accessVar.get() == "Standard":
                # I check if the selected access type is Standard

                access = self.standardAccess
                # I assign the Standard access object

            else:
                # If it is not Standard, then it must be Premium

                access = self.premiumAccess
                # I assign the Premium access object

            newUser = User(len(self.users) + 1, name, email, password, access)
            # I create a new User object with a new ID and the chosen access type

            self.users.append(newUser)
            # I add the new user to the users list

            self.dataManager.saveUsers(self.users)
            # I save the users list so the new user is stored

            messagebox.showinfo("Success", "User added successfully.")
            # I show a success message

            self.showManageUsersPage()
            # I return to the Manage Users page

        tk.Button(button_frame, text="Add User", width=20, command=addUser).grid(row=0, column=0, padx=10, pady=10)
        # I create the Add User button that runs addUser

        tk.Button(button_frame, text="Back", width=20, command=self.showManageUsersPage).grid(row=0, column=1, padx=10,
                                                                                              pady=10)
        # I create the Back button that returns to the Manage Users page

    def showAdminModifyUserPage(self, user):
        # This function shows a form where the admin can edit a selected user's details

        self.clearWindow()
        # I clear the manage users page before showing the modify user form

        top_frame = tk.Frame(self.main_window)
        # I create a top frame for the title

        form_frame = tk.Frame(self.main_window)
        # I create a form frame for the user's details

        button_frame = tk.Frame(self.main_window)
        # I create a button frame for Save Changes and Back buttons

        top_frame.pack(pady=20)
        # I place the top frame

        form_frame.pack(pady=10)
        # I place the form frame

        button_frame.pack(pady=20)
        # I place the button frame

        tk.Label(top_frame, text="Admin Modify User Details", font=("Arial", 20)).pack()
        # I display the Modify User page title

        tk.Label(form_frame, text="Name:").grid(row=0, column=0, padx=10, pady=10)
        # I create a label for the user's name

        nameBox = tk.Entry(form_frame, width=35)
        # I create an input box for the user's name

        nameBox.insert(0, user.getName())
        # I fill the name box with the user's current name

        nameBox.grid(row=0, column=1, padx=10, pady=10)
        # I place the name input box beside the label

        tk.Label(form_frame, text="Email:").grid(row=1, column=0, padx=10, pady=10)
        # I create a label for the user's email

        emailBox = tk.Entry(form_frame, width=35)
        # I create an input box for the user's email

        emailBox.insert(0, user.getEmail())
        # I fill the email box with the user's current email

        emailBox.grid(row=1, column=1, padx=10, pady=10)
        # I place the email input box beside the label

        tk.Label(form_frame, text="Password:").grid(row=2, column=0, padx=10, pady=10)
        # I create a label for the user's password

        passwordBox = tk.Entry(form_frame, width=35)
        # I create an input box for the user's password

        passwordBox.insert(0, user.getPassword())
        # I fill the password box with the user's current password

        passwordBox.grid(row=2, column=1, padx=10, pady=10)
        # I place the password input box beside the label

        tk.Label(form_frame, text="Access Type:").grid(row=3, column=0, padx=10, pady=10)
        # I create a label for access type

        accessVar = tk.StringVar(value=user.getAccessType().getTypeName())
        # I create a variable that stores the user's current access type

        tk.OptionMenu(form_frame, accessVar, "Standard", "Premium").grid(row=3, column=1, padx=10, pady=10)

        # I create a dropdown menu so the admin can change the access type

        def saveUserChanges():
            # This function runs when the admin clicks Save Changes

            name = nameBox.get()
            # I get the updated name from the name box

            email = emailBox.get()
            # I get the updated email from the email box

            password = passwordBox.get()
            # I get the updated password from the password box

            if name == "" or email == "" or password == "":
                # I check if any field is empty

                messagebox.showerror("Error", "Please fill all fields.")
                # I show an error because all details must be filled

                return
                # I stop the function

            for otherUser in self.users:
                # I loop through all users to check email uniqueness

                if otherUser != user and otherUser.getEmail() == email:
                    # I check if another user already has this email

                    messagebox.showerror("Error", "This email already belongs to another user.")
                    # I show an error because the email is already taken

                    return
                    # I stop the function

            user.setName(name)
            # I update the user's name

            user.setEmail(email)
            # I update the user's email

            user.setPassword(password)
            # I update the user's password

            if accessVar.get() == "Standard":
                # I check if the admin selected Standard

                user.setAccessType(self.standardAccess)
                # I set the user's access type to Standard

            else:
                # If the admin selected Premium

                user.setAccessType(self.premiumAccess)
                # I set the user's access type to Premium

            self.dataManager.saveUsers(self.users)
            # I save the users list after changing the user's details

            messagebox.showinfo("Success", "User details updated successfully.")
            # I show a success message

            self.showManageUsersPage()
            # I return to the Manage Users page

        tk.Button(button_frame, text="Save Changes", width=20, command=saveUserChanges).grid(row=0, column=0, padx=10,
                                                                                             pady=10)
        # I create a Save Changes button that runs saveUserChanges

        tk.Button(button_frame, text="Back", width=20, command=self.showManageUsersPage).grid(row=0, column=1, padx=10,
                                                                                              pady=10)
        # I create a Back button to return to Manage Users

    def adminDeleteUser(self, user):
        # This function lets the admin delete a normal user from the system

        userId = user.getUserId()
        # I get the ID of the user that the admin wants to delete

        self.users = [u for u in self.users if u.getUserId() != userId]
        # I rebuild the users list and keep everyone except the deleted user

        self.bookings = [
            booking for booking in self.bookings
            if booking.getUser().getUserId() != userId
        ]
        # I also remove all bookings that belong to this deleted user

        self.confirmationRecords = [
            record for record in self.confirmationRecords
            if record.getBooking().getUser().getUserId() != userId
        ]
        # I also remove confirmation records connected to that user's bookings

        self.saveAllData()
        # I save all updated data after deleting the user and related records

        messagebox.showinfo("Deleted", "User deleted successfully.")
        # I show a message saying the user was deleted

        self.showManageUsersPage()
        # I refresh the Manage Users page
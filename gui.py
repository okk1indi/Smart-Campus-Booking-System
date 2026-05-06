import tkinter as tk
from tkinter import messagebox
from datetime import datetime, date

from user import User
from admin import Administrator
from access_type import AccessType
from facility import StudyRoom, SportCourt, EventHall
from booking import Booking
from confirmation_record import ConfirmationRecord
from data_manager import DataManager


class BookingGUI:
    def __init__(self):
        self.main_window = tk.Tk()
        self.main_window.title("Smart Campus Facility Booking System")
        self.main_window.geometry("1050x700")
        self.main_window.resizable(False, False)

        self.dataManager = DataManager(
            "users.pkl",
            "facilities.pkl",
            "bookings.pkl",
            "confirmation_records.pkl"
        )

        self.users = self.dataManager.loadUsers()
        self.facilities = self.dataManager.loadFacilities()
        self.bookings = self.dataManager.loadBookings()
        self.confirmationRecords = self.dataManager.loadConfirmationRecords()

        self.currentUser = None

        self.standardAccess = AccessType("Standard", ["StudyRoom"], False, 1)
        self.premiumAccess = AccessType("Premium", ["StudyRoom", "SportCourt", "EventHall"], True, 3)

        if len(self.facilities) == 0:
            self.createSampleFacilities()

        self.showLoginPage()
        self.main_window.mainloop()

    def clearWindow(self):
        for widget in self.main_window.winfo_children():
            widget.destroy()

    def saveAllData(self):
        self.dataManager.saveUsers(self.users)
        self.dataManager.saveFacilities(self.facilities)
        self.dataManager.saveBookings(self.bookings)
        self.dataManager.saveConfirmationRecords(self.confirmationRecords)

    def refreshFacilityStatus(self, facility):
        if len(facility.getAvailableTimeSlots()) == 0:
            facility.setBookingStatus("Fully Booked")
        else:
            facility.setBookingStatus("Available")

    def validateFutureDate(self, dateText):
        try:
            bookingDate = datetime.strptime(dateText, "%Y-%m-%d").date()
            if bookingDate <= date.today():
                return False
            return True
        except ValueError:
            return False

    def createSampleFacilities(self):
        self.facilities.append(
            StudyRoom(1, "Study Room A", "Library", 10, ["10:00", "12:00", "2:00"], "Available", 20.0, 4)
        )

        self.facilities.append(
            SportCourt(2, "Basketball Court", "Sports Building", 20, ["9:00", "1:00", "5:00"], "Available", 50.0, "Basketball")
        )

        self.facilities.append(
            EventHall(3, "Main Event Hall", "Block C", 100, ["11:00", "3:00", "6:00"], "Available", 100.0, True)
        )

        self.dataManager.saveFacilities(self.facilities)

    def showLoginPage(self):
        self.clearWindow()

        top_frame = tk.Frame(self.main_window)
        middle_frame = tk.Frame(self.main_window)
        bottom_frame = tk.Frame(self.main_window)

        top_frame.pack(pady=25)
        middle_frame.pack(pady=10)
        bottom_frame.pack(pady=20)

        tk.Label(top_frame, text="Smart Campus Facility Booking System", font=("Arial", 20)).pack()

        tk.Label(middle_frame, text="Email:").grid(row=0, column=0, padx=10, pady=10)
        emailBox = tk.Entry(middle_frame, width=35)
        emailBox.grid(row=0, column=1, padx=10, pady=10)

        tk.Label(middle_frame, text="Password:").grid(row=1, column=0, padx=10, pady=10)
        passwordBox = tk.Entry(middle_frame, width=35, show="*")
        passwordBox.grid(row=1, column=1, padx=10, pady=10)

        def login():
            email = emailBox.get()
            password = passwordBox.get()

            if email == "" or password == "":
                messagebox.showerror("Error", "Please enter email and password.")
                return

            for user in self.users:
                if user.login(email, password):
                    self.currentUser = user

                    if isinstance(user, Administrator):
                        self.showAdminDashboard()
                    else:
                        self.showUserDashboard()

                    return

            messagebox.showerror("Error", "Invalid email or password.")

        tk.Button(bottom_frame, text="Login", width=22, command=login).grid(row=0, column=0, padx=10, pady=10)
        tk.Button(bottom_frame, text="Create Account", width=22, command=self.showCreateAccountPage).grid(row=0, column=1, padx=10, pady=10)
        tk.Button(bottom_frame, text="Create Admin Demo", width=22, command=self.createAdminDemo).grid(row=1, column=0, columnspan=2, pady=10)

    def createAdminDemo(self):
        for user in self.users:
            if user.getEmail() == "admin@zu.ac.ae":
                messagebox.showinfo("Admin Exists", "Admin already exists.\nEmail: admin@zu.ac.ae\nPassword: 123")
                return

        admin = Administrator(999, "Admin", "admin@zu.ac.ae", "123", self.premiumAccess)
        self.users.append(admin)
        self.dataManager.saveUsers(self.users)

        messagebox.showinfo("Admin Created", "Admin email: admin@zu.ac.ae\nPassword: 123")

    def showCreateAccountPage(self):
        self.clearWindow()

        top_frame = tk.Frame(self.main_window)
        form_frame = tk.Frame(self.main_window)
        button_frame = tk.Frame(self.main_window)

        top_frame.pack(pady=20)
        form_frame.pack(pady=10)
        button_frame.pack(pady=20)

        tk.Label(top_frame, text="Create Account", font=("Arial", 20)).pack()

        tk.Label(form_frame, text="Name:").grid(row=0, column=0, padx=10, pady=10)
        nameBox = tk.Entry(form_frame, width=35)
        nameBox.grid(row=0, column=1, padx=10, pady=10)

        tk.Label(form_frame, text="Email:").grid(row=1, column=0, padx=10, pady=10)
        emailBox = tk.Entry(form_frame, width=35)
        emailBox.grid(row=1, column=1, padx=10, pady=10)

        tk.Label(form_frame, text="Password:").grid(row=2, column=0, padx=10, pady=10)
        passwordBox = tk.Entry(form_frame, width=35, show="*")
        passwordBox.grid(row=2, column=1, padx=10, pady=10)

        def createAccount():
            name = nameBox.get()
            email = emailBox.get()
            password = passwordBox.get()

            if name == "" or email == "" or password == "":
                messagebox.showerror("Error", "Please fill all fields.")
                return

            for user in self.users:
                if user.getEmail() == email:
                    messagebox.showerror("Error", "This email already exists.")
                    return

            newUser = User(len(self.users) + 1, name, email, password, self.standardAccess)
            self.users.append(newUser)
            self.dataManager.saveUsers(self.users)

            messagebox.showinfo("Success", "Account created successfully.")
            self.showLoginPage()

        tk.Button(button_frame, text="Create", width=20, command=createAccount).grid(row=0, column=0, padx=10, pady=10)
        tk.Button(button_frame, text="Back", width=20, command=self.showLoginPage).grid(row=0, column=1, padx=10, pady=10)

    def showUserDashboard(self):
        self.clearWindow()

        top_frame = tk.Frame(self.main_window)
        button_frame = tk.Frame(self.main_window)

        top_frame.pack(pady=25)
        button_frame.pack(pady=20)

        tk.Label(top_frame, text="User Dashboard", font=("Arial", 20)).pack()
        tk.Label(top_frame, text="Welcome " + self.currentUser.getName()).pack(pady=8)
        tk.Label(top_frame, text="Access Type: " + self.currentUser.getAccessType().getTypeName()).pack(pady=5)

        tk.Button(button_frame, text="View Facilities", width=30, command=self.showFacilitiesPage).grid(row=0, column=0, padx=10, pady=8)
        tk.Button(button_frame, text="View Booking History", width=30, command=self.showBookingHistory).grid(row=1, column=0, padx=10, pady=8)
        tk.Button(button_frame, text="Upgrade to Premium", width=30, command=self.upgradeCurrentUser).grid(row=2, column=0, padx=10, pady=8)
        tk.Button(button_frame, text="Update Profile", width=30, command=self.showUpdateProfilePage).grid(row=3, column=0, padx=10, pady=8)
        tk.Button(button_frame, text="Logout", width=30, command=self.showLoginPage).grid(row=4, column=0, padx=10, pady=8)

    def upgradeCurrentUser(self):
        self.currentUser.setAccessType(self.premiumAccess)
        self.dataManager.saveUsers(self.users)

        messagebox.showinfo("Access Upgraded", "Your access type is now Premium.")
        self.showUserDashboard()

    def showFacilitiesPage(self):
        self.clearWindow()

        top_frame = tk.Frame(self.main_window)
        facility_frame = tk.Frame(self.main_window)
        button_frame = tk.Frame(self.main_window)

        top_frame.pack(pady=10)
        facility_frame.pack(pady=10)
        button_frame.pack(pady=10)

        tk.Label(top_frame, text="Available Facilities", font=("Arial", 20)).pack()
        tk.Label(top_frame, text="Your Access Type: " + self.currentUser.getAccessType().getTypeName()).pack(pady=5)

        rowNumber = 0

        for facility in self.facilities:
            self.refreshFacilityStatus(facility)

            facilityText = (
                facility.getName()
                + " | Type: " + facility.getFacilityType()
                + " | Capacity: " + str(facility.getCapacity())
                + " | Status: " + facility.getBookingStatus()
                + " | Slots: " + str(facility.getAvailableTimeSlots())
                + " | Fee: " + str(facility.getFee()) + " AED/hour"
            )

            tk.Label(
                facility_frame,
                text=facilityText,
                width=85,
                anchor="w",
                justify="left",
                wraplength=850
            ).grid(row=rowNumber, column=0, padx=10, pady=8)

            tk.Button(
                facility_frame,
                text="Book",
                width=10,
                command=lambda f=facility: self.showBookingPage(f)
            ).grid(row=rowNumber, column=1, padx=5, pady=8)

            rowNumber += 1

        tk.Button(button_frame, text="Back", width=20, command=self.showUserDashboard).pack()

    def showBookingPage(self, facility):
        self.clearWindow()

        top_frame = tk.Frame(self.main_window)
        form_frame = tk.Frame(self.main_window)
        button_frame = tk.Frame(self.main_window)

        top_frame.pack(pady=10)
        form_frame.pack(pady=10)
        button_frame.pack(pady=10)

        tk.Label(top_frame, text="Book Facility", font=("Arial", 20)).pack()
        tk.Label(top_frame, text=facility.displayDetails(), wraplength=900).pack(pady=5)
        tk.Label(top_frame, text="Available Slots: " + str(facility.getAvailableTimeSlots())).pack(pady=5)
        tk.Label(top_frame, text="Date format must be YYYY-MM-DD. Booking must be for a future date.").pack(pady=5)

        tk.Label(form_frame, text="Date:").grid(row=0, column=0, padx=10, pady=10)
        dateBox = tk.Entry(form_frame, width=35)
        dateBox.grid(row=0, column=1, padx=10, pady=10)

        tk.Label(form_frame, text="Time Slot:").grid(row=1, column=0, padx=10, pady=10)
        timeBox = tk.Entry(form_frame, width=35)
        timeBox.grid(row=1, column=1, padx=10, pady=10)

        tk.Label(form_frame, text="Duration:").grid(row=2, column=0, padx=10, pady=10)
        durationBox = tk.Entry(form_frame, width=35)
        durationBox.grid(row=2, column=1, padx=10, pady=10)

        tk.Label(form_frame, text="Participants:").grid(row=3, column=0, padx=10, pady=10)
        participantsBox = tk.Entry(form_frame, width=35)
        participantsBox.grid(row=3, column=1, padx=10, pady=10)

        costLabel = tk.Label(form_frame, text="Total Cost: ")
        costLabel.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

        def calculateCostOnly():
            try:
                duration = float(durationBox.get())

                if duration <= 0:
                    messagebox.showerror("Error", "Duration must be greater than 0.")
                    return

                totalCost = facility.calculateFee(duration)
                costLabel.config(text="Total Cost: " + str(totalCost) + " AED")

            except ValueError:
                messagebox.showerror("Error", "Duration must be a number.")

        def confirmBooking():
            try:
                bookingDate = dateBox.get()
                timeSlot = timeBox.get()
                duration = float(durationBox.get())
                participants = int(participantsBox.get())

                if bookingDate == "" or timeSlot == "":
                    messagebox.showerror("Error", "Please fill all fields.")
                    return

                if not self.validateFutureDate(bookingDate):
                    messagebox.showerror("Error", "Date must be in YYYY-MM-DD format and must be a future date.")
                    return

                if duration <= 0:
                    messagebox.showerror("Error", "Duration must be greater than 0.")
                    return

                if participants <= 0:
                    messagebox.showerror("Error", "Participants must be greater than 0.")
                    return

                if participants > facility.getCapacity():
                    messagebox.showerror("Error", "Participants exceed facility capacity.")
                    return

                if timeSlot not in facility.getAvailableTimeSlots():
                    messagebox.showerror("Error", "This time slot is not available.")
                    return

                if not self.currentUser.getAccessType().canBook(facility.getFacilityType()):
                    messagebox.showerror("Error", "Your access type does not allow booking this facility type.")
                    return

                totalCost = facility.calculateFee(duration)

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

                booking.setConfirmationRecord(confirmation)
                self.currentUser.addBooking(booking)
                self.bookings.append(booking)
                self.confirmationRecords.append(confirmation)

                facility.updateAvailability(timeSlot, False)
                self.refreshFacilityStatus(facility)

                self.saveAllData()

                messagebox.showinfo(
                    "Success",
                    "Booking confirmed.\nTotal cost: " + str(totalCost) + " AED\nConfirmation record created."
                )

                self.showUserDashboard()

            except ValueError:
                messagebox.showerror("Error", "Duration must be a number and participants must be a whole number.")

        tk.Button(button_frame, text="Calculate Cost", width=20, command=calculateCostOnly).grid(row=0, column=0, padx=10, pady=10)
        tk.Button(button_frame, text="Confirm Booking", width=20, command=confirmBooking).grid(row=0, column=1, padx=10, pady=10)
        tk.Button(button_frame, text="Back", width=20, command=self.showFacilitiesPage).grid(row=0, column=2, padx=10, pady=10)

    def showBookingHistory(self):
        self.clearWindow()

        top_frame = tk.Frame(self.main_window)
        history_frame = tk.Frame(self.main_window)
        button_frame = tk.Frame(self.main_window)

        top_frame.pack(pady=10)
        history_frame.pack(pady=10)
        button_frame.pack(pady=10)

        tk.Label(top_frame, text="Booking History", font=("Arial", 20)).pack()

        rowNumber = 0

        if len(self.currentUser.getBookingHistory()) == 0:
            tk.Label(history_frame, text="No bookings found").grid(row=0, column=0, pady=10)
        else:
            for booking in self.currentUser.getBookingHistory():
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

                tk.Button(
                    history_frame,
                    text="Modify",
                    width=10,
                    command=lambda b=booking: self.showModifyBookingPage(b)
                ).grid(row=rowNumber, column=1, padx=5, pady=8)

                tk.Button(
                    history_frame,
                    text="Delete",
                    width=10,
                    command=lambda b=booking: self.deleteBooking(b)
                ).grid(row=rowNumber, column=2, padx=5, pady=8)

                rowNumber += 1

        tk.Button(button_frame, text="Back", width=20, command=self.showUserDashboard).pack()

    def showModifyBookingPage(self, booking):
        self.clearWindow()

        top_frame = tk.Frame(self.main_window)
        form_frame = tk.Frame(self.main_window)
        button_frame = tk.Frame(self.main_window)

        top_frame.pack(pady=10)
        form_frame.pack(pady=10)
        button_frame.pack(pady=10)

        tk.Label(top_frame, text="Modify Booking", font=("Arial", 20)).pack()
        tk.Label(top_frame, text="Current Booking: " + booking.displayBookingDetails(), wraplength=900).pack(pady=5)
        tk.Label(top_frame, text="Date format must be YYYY-MM-DD and must be a future date.").pack(pady=5)

        tk.Label(form_frame, text="New Date:").grid(row=0, column=0, padx=10, pady=10)
        dateBox = tk.Entry(form_frame, width=35)
        dateBox.insert(0, booking.getBookingDate())
        dateBox.grid(row=0, column=1, padx=10, pady=10)

        tk.Label(form_frame, text="New Time Slot:").grid(row=1, column=0, padx=10, pady=10)
        timeBox = tk.Entry(form_frame, width=35)
        timeBox.insert(0, booking.getTimeSlot())
        timeBox.grid(row=1, column=1, padx=10, pady=10)

        tk.Label(form_frame, text="New Duration:").grid(row=2, column=0, padx=10, pady=10)
        durationBox = tk.Entry(form_frame, width=35)
        durationBox.insert(0, str(booking.getDuration()))
        durationBox.grid(row=2, column=1, padx=10, pady=10)

        tk.Label(form_frame, text="Participants:").grid(row=3, column=0, padx=10, pady=10)
        participantsBox = tk.Entry(form_frame, width=35)
        participantsBox.insert(0, str(booking.getNumberOfParticipants()))
        participantsBox.grid(row=3, column=1, padx=10, pady=10)

        def saveChanges():
            try:
                newDate = dateBox.get()
                newTimeSlot = timeBox.get()
                newDuration = float(durationBox.get())
                newParticipants = int(participantsBox.get())

                if newDate == "" or newTimeSlot == "":
                    messagebox.showerror("Error", "Please fill all fields.")
                    return

                if not self.validateFutureDate(newDate):
                    messagebox.showerror("Error", "Date must be in YYYY-MM-DD format and must be a future date.")
                    return

                if newDuration <= 0 or newParticipants <= 0:
                    messagebox.showerror("Error", "Duration and participants must be greater than 0.")
                    return

                facility = booking.getFacility()
                oldTimeSlot = booking.getTimeSlot()

                facility.updateAvailability(oldTimeSlot, True)

                if newParticipants > facility.getCapacity():
                    facility.updateAvailability(oldTimeSlot, False)
                    messagebox.showerror("Error", "Participants exceed facility capacity.")
                    return

                if newTimeSlot not in facility.getAvailableTimeSlots():
                    facility.updateAvailability(oldTimeSlot, False)
                    messagebox.showerror("Error", "This time slot is not available.")
                    return

                if not self.currentUser.getAccessType().canBook(facility.getFacilityType()):
                    facility.updateAvailability(oldTimeSlot, False)
                    messagebox.showerror("Error", "Your access type does not allow this facility.")
                    return

                newCost = facility.calculateFee(newDuration)

                booking.setBookingDate(newDate)
                booking.setTimeSlot(newTimeSlot)
                booking.setDuration(newDuration)
                booking.setNumberOfParticipants(newParticipants)
                booking.setTotalCost(newCost)

                confirmation = booking.getConfirmationRecord()

                if confirmation is not None:
                    confirmation.setDate(newDate)
                    confirmation.setTimeSlot(newTimeSlot)
                    confirmation.setDuration(newDuration)
                    confirmation.setCost(newCost)

                facility.updateAvailability(newTimeSlot, False)
                self.refreshFacilityStatus(facility)

                self.saveAllData()

                messagebox.showinfo("Success", "Booking modified successfully.")
                self.showBookingHistory()

            except ValueError:
                messagebox.showerror("Error", "Duration must be a number and participants must be a whole number.")

        tk.Button(button_frame, text="Save Changes", width=20, command=saveChanges).grid(row=0, column=0, padx=10, pady=10)
        tk.Button(button_frame, text="Back", width=20, command=self.showBookingHistory).grid(row=0, column=1, padx=10, pady=10)

    def deleteBooking(self, booking):
        facility = booking.getFacility()
        timeSlot = booking.getTimeSlot()

        facility.updateAvailability(timeSlot, True)
        self.refreshFacilityStatus(facility)

        self.currentUser.cancelBooking(booking.getBookingId())

        self.bookings = [
            b for b in self.bookings
            if b.getBookingId() != booking.getBookingId()
        ]

        self.confirmationRecords = [
            record for record in self.confirmationRecords
            if record.getBooking().getBookingId() != booking.getBookingId()
        ]

        self.saveAllData()

        messagebox.showinfo("Deleted", "Booking deleted successfully.")
        self.showBookingHistory()

    def showUpdateProfilePage(self):
        self.clearWindow()

        top_frame = tk.Frame(self.main_window)
        form_frame = tk.Frame(self.main_window)
        button_frame = tk.Frame(self.main_window)

        top_frame.pack(pady=20)
        form_frame.pack(pady=10)
        button_frame.pack(pady=20)

        tk.Label(top_frame, text="Update Profile", font=("Arial", 20)).pack()

        tk.Label(form_frame, text="New Name:").grid(row=0, column=0, padx=10, pady=10)
        nameBox = tk.Entry(form_frame, width=35)
        nameBox.insert(0, self.currentUser.getName())
        nameBox.grid(row=0, column=1, padx=10, pady=10)

        tk.Label(form_frame, text="New Email:").grid(row=1, column=0, padx=10, pady=10)
        emailBox = tk.Entry(form_frame, width=35)
        emailBox.insert(0, self.currentUser.getEmail())
        emailBox.grid(row=1, column=1, padx=10, pady=10)

        tk.Label(form_frame, text="New Password:").grid(row=2, column=0, padx=10, pady=10)
        passwordBox = tk.Entry(form_frame, width=35)
        passwordBox.insert(0, self.currentUser.getPassword())
        passwordBox.grid(row=2, column=1, padx=10, pady=10)

        def updateProfile():
            if nameBox.get() == "" or emailBox.get() == "" or passwordBox.get() == "":
                messagebox.showerror("Error", "Please fill all fields.")
                return

            self.currentUser.updateProfile(nameBox.get(), emailBox.get(), passwordBox.get())
            self.dataManager.saveUsers(self.users)

            messagebox.showinfo("Success", "Profile updated.")
            self.showUserDashboard()

        tk.Button(button_frame, text="Update", width=20, command=updateProfile).grid(row=0, column=0, padx=10, pady=10)
        tk.Button(button_frame, text="Back", width=20, command=self.showUserDashboard).grid(row=0, column=1, padx=10, pady=10)

    def showAdminDashboard(self):
        self.clearWindow()

        top_frame = tk.Frame(self.main_window)
        button_frame = tk.Frame(self.main_window)

        top_frame.pack(pady=20)
        button_frame.pack(pady=20)

        tk.Label(top_frame, text="Admin Dashboard", font=("Arial", 20)).pack()

        tk.Button(button_frame, text="View Daily Bookings", width=35, command=self.showDailyBookingsPage).grid(row=0, column=0, padx=10, pady=7)
        tk.Button(button_frame, text="View Facility Status", width=35, command=self.showAdminFacilityStatus).grid(row=1, column=0, padx=10, pady=7)
        tk.Button(button_frame, text="Update Facility Availability", width=35, command=self.showUpdateFacilityAvailabilityPage).grid(row=2, column=0, padx=10, pady=7)
        tk.Button(button_frame, text="Monitor Facility Usage", width=35, command=self.showFacilityUsagePage).grid(row=3, column=0, padx=10, pady=7)
        tk.Button(button_frame, text="Upgrade User Access", width=35, command=self.showUpgradeUserPage).grid(row=4, column=0, padx=10, pady=7)
        tk.Button(button_frame, text="Manage Users", width=35, command=self.showManageUsersPage).grid(row=5, column=0, padx=10, pady=7)
        tk.Button(button_frame, text="Logout", width=35, command=self.showLoginPage).grid(row=6, column=0, padx=10, pady=7)

    def showDailyBookingsPage(self):
        self.clearWindow()

        top_frame = tk.Frame(self.main_window)
        form_frame = tk.Frame(self.main_window)
        result_frame = tk.Frame(self.main_window)
        button_frame = tk.Frame(self.main_window)

        top_frame.pack(pady=10)
        form_frame.pack(pady=10)
        result_frame.pack(pady=10)
        button_frame.pack(pady=10)

        tk.Label(top_frame, text="Daily Bookings", font=("Arial", 20)).pack()

        tk.Label(form_frame, text="Enter Date:").grid(row=0, column=0, padx=10, pady=10)
        dateBox = tk.Entry(form_frame, width=35)
        dateBox.grid(row=0, column=1, padx=10, pady=10)

        def searchBookings():
            for widget in result_frame.winfo_children():
                widget.destroy()

            searchDate = dateBox.get()

            if searchDate == "":
                messagebox.showerror("Error", "Please enter a date.")
                return

            dailyBookings = self.currentUser.viewDailyBookings(searchDate, self.bookings)

            if len(dailyBookings) == 0:
                tk.Label(result_frame, text="No bookings for this date.").pack()
            else:
                for booking in dailyBookings:
                    tk.Label(result_frame, text=booking.displayBookingDetails(), width=90, anchor="w", wraplength=900).pack(pady=5)

        tk.Button(button_frame, text="Search", width=20, command=searchBookings).grid(row=0, column=0, padx=10, pady=10)
        tk.Button(button_frame, text="Back", width=20, command=self.showAdminDashboard).grid(row=0, column=1, padx=10, pady=10)

    def showAdminFacilityStatus(self):
        self.clearWindow()

        top_frame = tk.Frame(self.main_window)
        status_frame = tk.Frame(self.main_window)
        button_frame = tk.Frame(self.main_window)

        top_frame.pack(pady=10)
        status_frame.pack(pady=10)
        button_frame.pack(pady=10)

        tk.Label(top_frame, text="Facility Status", font=("Arial", 20)).pack()

        rowNumber = 0

        for facility in self.facilities:
            self.refreshFacilityStatus(facility)

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

            rowNumber += 1

        self.dataManager.saveFacilities(self.facilities)

        tk.Button(button_frame, text="Back", width=20, command=self.showAdminDashboard).pack()
    def showUpdateFacilityAvailabilityPage(self):
        self.clearWindow()

        top_frame = tk.Frame(self.main_window)
        facility_frame = tk.Frame(self.main_window)
        button_frame = tk.Frame(self.main_window)

        top_frame.pack(pady=10)
        facility_frame.pack(pady=10)
        button_frame.pack(pady=10)

        tk.Label(top_frame, text="Update Facility Availability", font=("Arial", 20)).pack()

        rowNumber = 0

        for facility in self.facilities:
            self.refreshFacilityStatus(facility)

            text = (
                facility.getName()
                + " | Status: " + facility.getBookingStatus()
                + " | Slots: " + str(facility.getAvailableTimeSlots())
            )

            tk.Label(
                facility_frame,
                text=text,
                width=85,
                anchor="w",
                justify="left",
                wraplength=850
            ).grid(row=rowNumber, column=0, padx=10, pady=5)

            tk.Button(
                facility_frame,
                text="Edit",
                width=10,
                command=lambda f=facility: self.showEditSingleFacilityAvailability(f)
            ).grid(row=rowNumber, column=1, padx=5, pady=5)

            rowNumber += 1

        tk.Button(button_frame, text="Back", width=20, command=self.showAdminDashboard).pack()

    def showEditSingleFacilityAvailability(self, facility):
        self.clearWindow()

        top_frame = tk.Frame(self.main_window)
        form_frame = tk.Frame(self.main_window)
        button_frame = tk.Frame(self.main_window)

        top_frame.pack(pady=10)
        form_frame.pack(pady=10)
        button_frame.pack(pady=10)

        tk.Label(top_frame, text="Edit Availability for " + facility.getName(), font=("Arial", 20)).pack()
        tk.Label(top_frame, text="Current Slots: " + str(facility.getAvailableTimeSlots()), wraplength=900).pack(pady=5)

        tk.Label(form_frame, text="Time Slot:").grid(row=0, column=0, padx=10, pady=10)
        slotBox = tk.Entry(form_frame, width=35)
        slotBox.grid(row=0, column=1, padx=10, pady=10)

        def addSlot():
            slot = slotBox.get()

            if slot == "":
                messagebox.showerror("Error", "Please enter a time slot.")
                return

            facility.updateAvailability(slot, True)
            self.refreshFacilityStatus(facility)
            self.dataManager.saveFacilities(self.facilities)

            messagebox.showinfo("Success", "Time slot added.")
            self.showUpdateFacilityAvailabilityPage()

        def removeSlot():
            slot = slotBox.get()

            if slot == "":
                messagebox.showerror("Error", "Please enter a time slot.")
                return

            facility.updateAvailability(slot, False)
            self.refreshFacilityStatus(facility)
            self.dataManager.saveFacilities(self.facilities)

            messagebox.showinfo("Success", "Time slot removed.")
            self.showUpdateFacilityAvailabilityPage()

        tk.Button(button_frame, text="Add Slot", width=20, command=addSlot).grid(row=0, column=0, padx=10, pady=10)
        tk.Button(button_frame, text="Remove Slot", width=20, command=removeSlot).grid(row=0, column=1, padx=10, pady=10)
        tk.Button(button_frame, text="Back", width=20, command=self.showUpdateFacilityAvailabilityPage).grid(row=0, column=2, padx=10, pady=10)

    def showFacilityUsagePage(self):
        self.clearWindow()

        top_frame = tk.Frame(self.main_window)
        usage_frame = tk.Frame(self.main_window)
        button_frame = tk.Frame(self.main_window)

        top_frame.pack(pady=10)
        usage_frame.pack(pady=10)
        button_frame.pack(pady=10)

        tk.Label(top_frame, text="Facility Usage Monitoring", font=("Arial", 20)).pack()

        rowNumber = 0

        for facility in self.facilities:
            count = 0

            for booking in self.bookings:
                if booking.getFacility().getFacilityId() == facility.getFacilityId():
                    count += 1

            text = facility.getName() + " was booked " + str(count) + " time(s). Capacity: " + str(facility.getCapacity())

            tk.Label(
                usage_frame,
                text=text,
                width=85,
                anchor="w",
                justify="left",
                wraplength=850
            ).grid(row=rowNumber, column=0, padx=10, pady=5)

            rowNumber += 1

        tk.Button(button_frame, text="Back", width=20, command=self.showAdminDashboard).pack()

    def showUpgradeUserPage(self):
        self.clearWindow()

        top_frame = tk.Frame(self.main_window)
        user_frame = tk.Frame(self.main_window)
        button_frame = tk.Frame(self.main_window)

        top_frame.pack(pady=10)
        user_frame.pack(pady=10)
        button_frame.pack(pady=10)

        tk.Label(top_frame, text="Upgrade User Access", font=("Arial", 20)).pack()

        rowNumber = 0

        for user in self.users:
            if not isinstance(user, Administrator):
                userText = user.getName() + " - " + user.getEmail() + " - " + user.getAccessType().getTypeName()

                tk.Label(
                    user_frame,
                    text=userText,
                    width=75,
                    anchor="w",
                    justify="left",
                    wraplength=750
                ).grid(row=rowNumber, column=0, padx=10, pady=5)

                tk.Button(
                    user_frame,
                    text="Upgrade",
                    width=10,
                    command=lambda u=user: self.upgradeUser(u)
                ).grid(row=rowNumber, column=1, padx=5, pady=5)

                rowNumber += 1

        tk.Button(button_frame, text="Back", width=20, command=self.showAdminDashboard).pack()

    def upgradeUser(self, user):
        user.setAccessType(self.premiumAccess)
        self.dataManager.saveUsers(self.users)

        messagebox.showinfo("Success", user.getName() + " upgraded to Premium.")
        self.showUpgradeUserPage()

    def showManageUsersPage(self):
        self.clearWindow()

        top_frame = tk.Frame(self.main_window)
        user_frame = tk.Frame(self.main_window)
        button_frame = tk.Frame(self.main_window)

        top_frame.pack(pady=10)
        user_frame.pack(pady=10)
        button_frame.pack(pady=10)

        tk.Label(top_frame, text="Manage Users", font=("Arial", 20)).pack()

        rowNumber = 0

        for user in self.users:
            if not isinstance(user, Administrator):
                userText = user.getName() + " | " + user.getEmail() + " | " + user.getAccessType().getTypeName()

                tk.Label(
                    user_frame,
                    text=userText,
                    width=70,
                    anchor="w",
                    justify="left",
                    wraplength=700
                ).grid(row=rowNumber, column=0, padx=10, pady=5)

                tk.Button(
                    user_frame,
                    text="Modify",
                    width=8,
                    command=lambda u=user: self.showAdminModifyUserPage(u)
                ).grid(row=rowNumber, column=1, padx=5, pady=5)

                tk.Button(
                    user_frame,
                    text="Delete",
                    width=8,
                    command=lambda u=user: self.adminDeleteUser(u)
                ).grid(row=rowNumber, column=2, padx=5, pady=5)

                rowNumber += 1

        tk.Button(button_frame, text="Add New User", width=20, command=self.showAdminAddUserPage).grid(row=0, column=0, padx=10, pady=10)
        tk.Button(button_frame, text="Back", width=20, command=self.showAdminDashboard).grid(row=0, column=1, padx=10, pady=10)

    def showAdminAddUserPage(self):
        self.clearWindow()

        top_frame = tk.Frame(self.main_window)
        form_frame = tk.Frame(self.main_window)
        button_frame = tk.Frame(self.main_window)

        top_frame.pack(pady=20)
        form_frame.pack(pady=10)
        button_frame.pack(pady=20)

        tk.Label(top_frame, text="Admin Add User", font=("Arial", 20)).pack()

        tk.Label(form_frame, text="Name:").grid(row=0, column=0, padx=10, pady=10)
        nameBox = tk.Entry(form_frame, width=35)
        nameBox.grid(row=0, column=1, padx=10, pady=10)

        tk.Label(form_frame, text="Email:").grid(row=1, column=0, padx=10, pady=10)
        emailBox = tk.Entry(form_frame, width=35)
        emailBox.grid(row=1, column=1, padx=10, pady=10)

        tk.Label(form_frame, text="Password:").grid(row=2, column=0, padx=10, pady=10)
        passwordBox = tk.Entry(form_frame, width=35)
        passwordBox.grid(row=2, column=1, padx=10, pady=10)

        tk.Label(form_frame, text="Access Type:").grid(row=3, column=0, padx=10, pady=10)
        accessVar = tk.StringVar(value="Standard")
        tk.OptionMenu(form_frame, accessVar, "Standard", "Premium").grid(row=3, column=1, padx=10, pady=10)

        def addUser():
            name = nameBox.get()
            email = emailBox.get()
            password = passwordBox.get()

            if name == "" or email == "" or password == "":
                messagebox.showerror("Error", "Please fill all fields.")
                return

            for user in self.users:
                if user.getEmail() == email:
                    messagebox.showerror("Error", "This email already exists.")
                    return

            if accessVar.get() == "Standard":
                access = self.standardAccess
            else:
                access = self.premiumAccess

            newUser = User(len(self.users) + 1, name, email, password, access)
            self.users.append(newUser)
            self.dataManager.saveUsers(self.users)

            messagebox.showinfo("Success", "User added successfully.")
            self.showManageUsersPage()

        tk.Button(button_frame, text="Add User", width=20, command=addUser).grid(row=0, column=0, padx=10, pady=10)
        tk.Button(button_frame, text="Back", width=20, command=self.showManageUsersPage).grid(row=0, column=1, padx=10, pady=10)

    def showAdminModifyUserPage(self, user):
        self.clearWindow()

        top_frame = tk.Frame(self.main_window)
        form_frame = tk.Frame(self.main_window)
        button_frame = tk.Frame(self.main_window)

        top_frame.pack(pady=20)
        form_frame.pack(pady=10)
        button_frame.pack(pady=20)

        tk.Label(top_frame, text="Admin Modify User Details", font=("Arial", 20)).pack()

        tk.Label(form_frame, text="Name:").grid(row=0, column=0, padx=10, pady=10)
        nameBox = tk.Entry(form_frame, width=35)
        nameBox.insert(0, user.getName())
        nameBox.grid(row=0, column=1, padx=10, pady=10)

        tk.Label(form_frame, text="Email:").grid(row=1, column=0, padx=10, pady=10)
        emailBox = tk.Entry(form_frame, width=35)
        emailBox.insert(0, user.getEmail())
        emailBox.grid(row=1, column=1, padx=10, pady=10)

        tk.Label(form_frame, text="Password:").grid(row=2, column=0, padx=10, pady=10)
        passwordBox = tk.Entry(form_frame, width=35)
        passwordBox.insert(0, user.getPassword())
        passwordBox.grid(row=2, column=1, padx=10, pady=10)

        tk.Label(form_frame, text="Access Type:").grid(row=3, column=0, padx=10, pady=10)
        accessVar = tk.StringVar(value=user.getAccessType().getTypeName())
        tk.OptionMenu(form_frame, accessVar, "Standard", "Premium").grid(row=3, column=1, padx=10, pady=10)

        def saveUserChanges():
            name = nameBox.get()
            email = emailBox.get()
            password = passwordBox.get()

            if name == "" or email == "" or password == "":
                messagebox.showerror("Error", "Please fill all fields.")
                return

            for otherUser in self.users:
                if otherUser != user and otherUser.getEmail() == email:
                    messagebox.showerror("Error", "This email already belongs to another user.")
                    return

            user.setName(name)
            user.setEmail(email)
            user.setPassword(password)

            if accessVar.get() == "Standard":
                user.setAccessType(self.standardAccess)
            else:
                user.setAccessType(self.premiumAccess)

            self.dataManager.saveUsers(self.users)

            messagebox.showinfo("Success", "User details updated successfully.")
            self.showManageUsersPage()

        tk.Button(button_frame, text="Save Changes", width=20, command=saveUserChanges).grid(row=0, column=0, padx=10, pady=10)
        tk.Button(button_frame, text="Back", width=20, command=self.showManageUsersPage).grid(row=0, column=1, padx=10, pady=10)

    def adminDeleteUser(self, user):
        userId = user.getUserId()

        self.users = [u for u in self.users if u.getUserId() != userId]

        self.bookings = [
            booking for booking in self.bookings
            if booking.getUser().getUserId() != userId
        ]

        self.confirmationRecords = [
            record for record in self.confirmationRecords
            if record.getBooking().getUser().getUserId() != userId
        ]

        self.saveAllData()

        messagebox.showinfo("Deleted", "User deleted successfully.")
        self.showManageUsersPage()
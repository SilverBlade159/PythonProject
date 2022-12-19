import calendar as cal
from dataclasses import dataclass
import csv
import os

'''
Λειτουργεί σαν τις κανονικές κλάσεις, απλά χρησιμοποιείται κυρίως για δημιουργία objects που περιέχουν συγκεκριμένα
properties (συνήθως δεν προσθέτουμε methods στα dataclasses)

Ένα αντικείμενο της dataclass (παράδειγμα σε κώδικα):

>>> event = Event("2022-6-12", "12:30", 60, "Python Course")
>>> print(event.date)
2022-6-12
>>> print(event.hour)
12:30
>>> print(event.duration)
60
>>> print(event.title)
Python Course
'''
@dataclass
class Event:
    date: str
    hour: str
    duration: int
    title: str


# Η κλάση αυτή περιέχει όλες τις απαραίτητες συναρτήσεις για διαχείριση των γεγονότων στο αρχείο events.csv
class DatabaseHandler:
    # Το file_name είναι ένα class variable. Για να το χρησιμοποιήσετε μπορείτε να γράψετε:
    # DatabaseHandler.file_name
    file_name = "events.csv"

    # Καλείται πρώτα, ώστε να αρχικοποιηθεί το dictionary με τα δεδομένα που υπάρχουν στο αρχείο csv
    @classmethod
    def load_data(cls, events):
        pass

    # Καλείται μετά τον τερματισμό της εφαρμογής, αποθηκεύοντας ότι υπάρχει στο dictionary στο αρχείο csv
    @classmethod
    def backup_data(cls, events):
        pass


# Η κύρια κλάση, περιέχει όλες τις συναρτήσεις σχετικά με την εμφάνιση του ημερολογίου και τις λειτουργίες του
class Calendar:
    # region Constructor
    def __init__(self, current_year, current_month):
        self.current_year = current_year
        self.current_month = current_month

        self.events = dict()

        self.initialise_dictionary()
    # endregion

    # region Helper Functions

    # Οι βοηθητικές συναρτήσεις καλούνται μέσα από τις άλλες συναρτήσεις, ώστε να μην επαναλαμβάνεται κώδικας και
    # για τη μείωση του όγκου των άλλων συναρτήσεων

    def calc_next_month(self, month):
        return month + 1 if month + 1 <= 12 else 1

    def calc_prev_month(self, month):
        return month-1 if month-1 != 0 else 12

    def num_to_month(self, num):
        months = ['', 'ΙΑΝ', 'ΦΕΒ', 'ΜΑΡ', 'ΑΠΡ', 'ΜΑΙ', 'ΙΟΥΝ', 'ΙΟΥΛ', 'ΑΥΓ', 'ΣΕΠ', 'ΟΚΤ', 'ΝΟΕ', 'ΔΕΚ']
        return months[num]

    def num_to_week(self, num):
        week_days = ['ΔΕΥ', 'ΤΡΙ', 'ΤΕΤ', 'ΠΕΜ', 'ΠΑΡ', 'ΣΑΒ', 'ΚΥΡ']
        return week_days[num]

    # Χρησιμοποιείται για εύρεση γεγονότων για κάποια συγκεκριμένη ημέρα. Σκέφτηκα ότι μπορούμε να το καλούμε
    # όταν εμφανίζουμε το ημερολόγιο και ψάχνουμε τις ημέρες οπού χρειάζονται αστερίσκοι
    def is_event_on_current_day(self, day):
        pass

    # Αναζήτηση γεγονότος στο dictionary. Χρησιμοποιείται κυρίως στη διαγραφή και αναζήτηση γεγονότων.
    def search_event(self):
        pass
    # endregion

    # region Main Functions

    # Χρησιμοποιείται στην αρχή του προγράμματος (καλείται από το constructor) για την αρχικοποίηση του dictionary
    def initialise_dictionary(self):
        dh = DatabaseHandler()
        dh.load_data(self.events)

    # <=== First Menu ===>
    def print_calendar(self):
        pass

    def print_menu(self):
        print(f'Πατήστε ENTER για προβολή του επόμενου μήνα, "q" για έξοδο ή κάποια από τις παρακάτω επιλογές:')
        print('     "-" για πλοήγηση στον προηγούμενο μήνα')
        print('     "+" για διαχείριση των γεγονότων του ημερολογίου')
        print('     "*" για εμφάνιση των γεγονότων ενός επιλεγμένου μήνα')

    def prompt(self):
        self.print_calendar()
        self.print_menu()
        inp = input("> ")

        while inp != "q":
            if inp == "-":
                self.current_month = self.calc_prev_month(self.current_month)
            elif inp == "+":
                self.event_handling_prompt()
            elif inp == "*":
                self.show_events()
            elif inp == "":
                self.current_month = self.calc_next_month(self.current_month)
            else:
                print('Invalid input.')

            self.print_calendar()
            self.print_menu()
            inp = input("> ")

        # Σε περίπτωση ομαλού τερματισμού του προγράμματος, αποθηκεύουμε το dictionary στο αρχείο csv
        db = DatabaseHandler()
        db.backup_data(self.events)

    # <=== Second Menu ===>
    def print_event_handling_menu(self):
        print('Διαχείριση γεγονότων ημερολογίου, επιλέξτε ενέργεια:')
        print('1 Καταγραφή νέου γεγονότος')
        print('2 Διαγραφή γεγονότος')
        print('3 Ενημέρωση γεγονότος')
        print('0 Επιστροφή στο κυρίως μενού')

    def event_handling_prompt(self):
        self.print_event_handling_menu()
        inp = input("> ")

        if inp == "0":
            return
        elif inp == "1":
            self.add_event()
        elif inp == "2":
            self.delete_event()
        elif inp == "3":
            self.update_event()
        else:
            print('Invalid input.')

        self.event_handling_prompt()

    # <=== Second Menu Functionality ===>
    def show_events(self):
        pass

    def add_event(self):
        pass

    def update_event(self):
        pass

    def delete_event(self):
        pass
    # endregion


c = Calendar(2022, 12)
c.prompt()

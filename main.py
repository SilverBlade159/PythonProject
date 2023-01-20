import calendar as cal
import csv
import os
from datetime import datetime


class Messages:
    """
    Η κλάση Messages χρησιμοποιείται για τύπους μηνυμάτων προς τον χρήστη οπού χρησιμοποιούνται συχνά με σκοπό
    την αποφυγή επανάληψης κώδικα.
    """

    @staticmethod
    def success(text):
        print('-' * 100)
        print(f'✔ [{text}!]')
        print('-' * 100)

    @staticmethod
    def warning(text):
        print('-' * 100)
        print(f'⚠ [{text}]')
        print('-' * 100)


class Date:
    """
    Η κλάση Date χρησιμοποιείται για την καλύτερη διαχείριση των YYYY-mm-dd strings
    """

    # region Constructor
    def __init__(self, date_format):
        self.year, self.month, self.day = self.parse_date_format(date_format)
        self.format = self.prettier_string_format(date_format)
        self.key = self.key_format()
    # endregion

    # region Methods
    def parse_date_format(self, date_format):
        """
        Δέχεται ένα string τύπου YYYY-mm-dd και επιστρέφει το YYYY, το mm και το dd ξεχωριστά σε μορφή int.

        >>> date = Date('2022-12-04')
        >>> print(f'year: {date.year}, month: {date.month}, day: {date.day}')
        year: 2022, month: 12, day: 4
        """

        return map(int, date_format.split('-'))

    def prettier_string_format(self, date_format):
        """
        Βελτιώνει το date_format ώστε ο μήνας και η μέρα να εμφανίζονται σε μορφη mm και dd αντίστοιχα, ακόμα
        και αν περιέχουν μόνο 1 ψηφίο.

        >>> date = Date('2023-1-4')
        >>> print(date.format)
        2023-01-04
        """

        return '-'.join(map(lambda x: '0'+x if len(x) == 1 else x, date_format.split('-')))

    def key_format(self):
        """
        Χρησιμοποιείται για την αναζήτηση στο λεξικό events της κλάσης Calendar και αποθηκεύεται στη μεταβλητή
        key.

        >>> date = Date('2022-12-04')
        >>> print(date.key)
        2022-12
        """

        return '-'.join(str(x) for x in [self.year, self.month])
    # endregion


class Time:
    """
    Η κλάση Time χρησιμοποιείται για την καλύτερη διαχείριση των HH:MM strings
    """

    # region Constructor
    def __init__(self, time_format, duration=0):
        """
        Δέχεται σαν παραμέτρους το time_format και προαιρετικά το duration. Σε περίπτωση που δοθεί duration
        υπολογίζει τη νέα ώρα που προκύπτει.
        """

        self.hours, self.minutes = self.parse_time_format(time_format)
        self.format = self.string_format(time_format)

        if duration > 0:
            self.add_duration(duration)
    # endregion

    # region Methods
    def parse_time_format(self, time_format):
        """
        Δέχεται ένα string τύπου HH:MM και επιστρέφει το HH και το MM ξεχωριστά σε μορφή int

        >>> time = Time('20:30')
        >>> print(f'hours: {time.hours}, minutes: {time.minutes}')
        hours: 20, minutes: 30
        """

        return map(int, time_format.split(':'))

    def string_format(self, time_format):
        """
        Βελτιώνει το time_format ώστε τα λεπτά και οι ώρες να εμφανίζονται σε μορφη HH και MM αντίστοιχα, ακόμα
        και αν περιέχουν μόνο 1 ψηφίο

        >>> time = Time('20:3')
        >>> print(time.format)
        20:03
        """

        return ':'.join(map(lambda x: '0'+x if len(x) == 1 else x, time_format.split(':')))

    def add_duration(self, duration):
        """
        Αλλάζει τις μεταβλητές hours και minutes, ώστε να δείχνουν τη νέα ώρα λόγω προσθήκης της διάρκειας ενός
        γεγονότος. Το duration είναι σε λεπτά.

        >>> time = Time('10:40')
        >>> time.add_duration(40)
        >>> print(time.format)
        11:20
        """

        self.hours += (self.minutes + duration) // 60
        self.hours = 0 if self.hours > 24 else self.hours

        self.minutes = (self.minutes + duration) % 60

        # Ανανεώνει τη μεταβλητή format
        self.format = ':'.join(map(str, [self.hours, self.minutes]))
    # endregion

    # region Operator Overloading
    def __lt__(self, other):
        """
        Operator overload του '<' ώστε να επιτρέπει συγκρίσεις μεταξύ των Time objects

        >>> time = Time('10:00')
        >>> time2 = Time('12:00')
        >>> time < time2
        True
        """

        return self.hours < other.hours or (self.hours == other.hours and self.minutes < other.minutes)

    def __eq__(self, other):
        """
        Operator overload του '==' ώστε να επιτρέπει συγκρίσεις μεταξύ των Time objects

        >>> time = Time('12:32')
        >>> time2 = Time('12:32')
        >>> time == time2
        True
        """

        return self.hours == other.hours and self.minutes == other.minutes
    # endregion


class Event:
    """
    Η κλάση Event χρησιμοποιείται για την αποθήκευση όλων των στοιχείων που σχετίζονται με τα γεγονότα. Οι μεταβλητές
    start_time και end_time είναι Time objects.
    """

    # region Constructor
    def __init__(self, date, start_time, duration, title):
        self.date = Date(date)
        self.start_time = Time(start_time)
        self.end_time = Time(start_time, duration)
        self.duration = duration
        self.title = title
    # endregion


class Validations:
    """
    Η κλάση Validations χρησιμοποιείται για την επαλήθευση των δεδομένων που δίνει ο χρήστης
    """

    @staticmethod
    def val_time(t):
        """
        Ζητάει από τον χρήστη την ώρα γεγονότος, επαληθεύοντας ότι περιέχει τη σωστή μορφή
        """

        while True:
            try:
                datetime.strptime(t, '%H:%M')
                return t
            except ValueError:
                Messages.warning('Η ώρα γεγονότος δεν είναι της μορφής HH:MM.')
                t = input('Ώρα γεγονότος: ')

    @staticmethod
    def val_date(d):
        """
        Ζητάει από τον χρήστη την ημερομηνία γεγονότος, επαληθεύοντας ότι περιέχει τη σωστή μορφή
        """

        while True:
            try:
                datetime.strptime(d, '%Y-%m-%d')
                return d
            except ValueError:
                Messages.warning('Η ημερομηνία γεγονότος δεν είναι της μορφής YYYY-MM-DD.')
                d = input("Ημερομηνία γεγονότος: ")

    @staticmethod
    def val_int(num, input_text):
        """
        Ζητάει από τον χρήστη τη διάρκεια γεγονότος, επαληθεύοντας ότι περιέχει τη σωστή μορφή
        """

        while True:
            try:
                num = int(num)

                if num < 0:
                    raise ValueError()

                return num
            except ValueError:
                Messages.warning('Εισάγετε μη αρνητικό ακέραιο αριθμό.')
                num = input(input_text)

    @staticmethod
    def val_title(title):
        """
        Ζητάει από τον χρήστη τον τίτλο γεγονότος, επαληθεύοντας ότι περιέχει τη σωστή μορφή
        """

        while True:
            if ',' in title:
                Messages.warning('Ο τίτλος γεγονότος δεν επιτρέπεται να έχει κόμμα.')
                title = input("Τίτλος γεγονότος: ")
                continue

            return title


class DatabaseHandler:
    """
    Η κλάση DatabaseHandler χρησιμοποιείται για τη διαχείριση του αρχείου events.csv,
    ενώ όταν ο χρήστης κάνει ομαλή έξοδο μέσω του 'q', αποθηκεύει
    """

    file_name = "events.csv"

    @classmethod
    def open_file(cls, events):
        """
        Όταν αρχίσει να τρέχει το πρόγραμμα, φορτώνει τα δεδομένα του αρχείου στο events, το
        οποίο είναι dictionary και το επιστρέφει. Τα δεδομένα αποθηκεύονται ως Event objects.
        """

        mode = 'r' if os.path.exists(DatabaseHandler.file_name) else 'a+'
        with open(DatabaseHandler.file_name, mode) as csvfile:
            csvreader = csv.reader(csvfile)
            for i, row in enumerate(csvreader):
                if i > 0:
                    date = row[0]
                    start_time = row[1]
                    duration = int(row[2])
                    title = row[3]

                    event = Event(date, start_time, duration, title)
                    key = event.date.key

                    if events.get(key) is None:
                        events[key] = [event]
                    else:
                        events[key].append(event)
            #return events

    @classmethod
    def backup_data(cls, events):
        """
        Όταν ο χρήστης κάνει ομαλή έξοδο μέσω του 'q', αποθηκεύει τα δεδομένα του
        dictionary events στο αρχείο events.csv
        """

        fields = ['Date', 'Hour', 'Duration', 'Title']
        with open('events.csv', 'w', newline='') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(fields)

            for key in events:
                for event in events[key]:
                    csvwriter.writerow([event.date.format, event.start_time.format, str(event.duration), event.title])


class Bonus:
    """
    Υλοποιεί τη λειτουργικότητα των ερωτημάτων bonus.
    """

    @staticmethod
    def conflict(new_event, events):
        key = new_event.date.key
        if key not in events:
            return True  # Δεν υπάρχουν γεγονότα για τη συγκεκριμένη ημερομηνία

        # Περιέχει όλες τις ώρες των γεγονότων, ώστε να τυπωθεί ο διαθέσιμος ελεύθερος χρόνος
        free_time_list = [Time('00:00'), Time('23:59')]

        # Περιορισμός ώστε το γεγονός να μην εκτείνεται πέρα της καθορισμένης ημερομηνίας
        can_event_be_added = new_event.end_time < free_time_list[1]

        # Ψάχνουμε όλα τα γεγονότα της δεδομένης ημερομηνίας των οποίων συμπίπτει η ημέρα
        for event in events[key]:
            if event.date.day == new_event.date.day:
                for i, t in enumerate(free_time_list):
                    # Δε θέλουμε να προσθέσουμε ώρες που ήδη υπάρχουν στη λίστα
                    if event.start_time == t:
                        continue

                    # Προσθέτουμε ώρες γεγονότων της ίδιας ημέρας στο free_time_list ώστε να βρούμε το διαθέσιμο
                    # ελεύθερο χρόνο
                    elif event.start_time < t:
                        free_time_list.insert(i, event.start_time)
                        free_time_list.insert(i + 1, event.end_time)
                        break

                # Ο χρόνος του γεγονότος συμπίπτει με άλλα γεγονότα στην περίπτωση που ο χρόνος που αρχίζει ή τελειώνει
                # βρίσκεται ανάμεσα στο χρόνο άλλων γεγονότων
                if event.start_time < new_event.start_time < event.end_time or event.start_time < new_event.end_time < event.end_time:
                    can_event_be_added = False

        if not can_event_be_added:
            if new_event.end_time < free_time_list[1]:
                Messages.warning('Δυστυχώς ο χρόνος του καινούριου γεγονότος επικαλύπτεται από παλιότερα γεγονότα.')
            else:
                Messages.warning('Η διάρκεια του γεγονότος δεν επιτρέπεται να ξεπερνά την τωρινή ημερομηνία γεγονότος.')

            # Παράδειγμα λειτουργίας του παρακάτω for loop
            #  Έστω free_time_list = [Time('00:00), Time('13:30'), Time('14:30'), Time('23:59')]
            #  Η λίστα αυτή θα δημιουργηθεί αν προσθέσουμε ένα γεγονός που αρχίζει στις 13:30 και έχει διάρκεια 60 λεπτά
            #  Σύμφωνα με τη λίστα ο διαθέσιμος χρόνος είναι:
            #  Από τις 00:00 μέχρι τις 13:30 (δηλαδή τα πρώτα δύο στοιχεία)
            #  Και από τις 14:30 μέχρι τις 23:59 (δηλαδή τα επόμενα δύο στοιχεία) κτλ.
            print(f'ℹ Ελεύθερος Χρόνος ({new_event.date.format})')
            for i in range(0, len(free_time_list)-1, 2):
                print(f'\tΑπό {free_time_list[i].format} μέχρι {free_time_list[i+1].format}')
            print(f'Παρακαλώ ξανασυμπληρώστε τα κενά ώστε το γεγονός να εμπίπτει εντός του παραπάνω ελεύθερου χρόνου.\n')

        return can_event_be_added

    @staticmethod
    def notification(events):
        key = '{dt.year}-{dt.month}'.format(dt=datetime.now())
        current_day = int('{dt.day}'.format(dt=datetime.now()))
        current_time = Time('{dt.hour}:{dt.minute}'.format(dt=datetime.now()))

        # Κανένα γεγονός δεν έχει καταχωρηθεί αυτό το μήνα
        if events.get(key) is None:
            print(f'Δεν υπάρχουν άλλα γεγονότα προγραμματισμένα σήμερα.')
            input('Πατήστε enter για επιστροφή στο κυρίως μενού: ')
            return

        are_there_any_events = False
        for event in events[key]:
            # Ψάχνουμε γεγονότα με τη σημερινή ημερομηνία
            if event.date.day == current_day and current_time < event.start_time:
                # Βρίσκουμε το χρόνο για την έναρξη του γεγονότος
                hours_to_event = event.start_time.hours - current_time.hours
                minutes_to_event = event.start_time.minutes - current_time.minutes

                if minutes_to_event < 0:
                    hours_to_event -= 1
                    minutes_to_event += 60

                # Έλεγχος για σωστή διατύπωση της ειδοποίησης
                text = f'🔔 Σε '
                if hours_to_event > 0:
                    text += f'{hours_to_event} ' + ('ώρες' if hours_to_event > 1 else 'ώρα')
                if minutes_to_event > 0:
                    text += ' και ' if hours_to_event > 0 else ''
                    text += f'{minutes_to_event} ' + ('λεπτά' if minutes_to_event > 1 else 'λεπτό')
                text += f' έχει προγραμματιστεί το γεγονός "{event.title}".'

                print(text)
                are_there_any_events = True

        if not are_there_any_events:
            print(f'Δεν υπάρχουν γεγονότα προγραμματισμένα σήμερα.')

        input('Πατήστε enter για επιστροφή στο κυρίως μενού: ')


class Calendar:
    """
    Η κύρια κλάση με όλες τις βασικές λειτουργίες.
    """

    # region Constructor
    def __init__(self, current_year, current_month):
        """
        Ο constructor δέχεται ως ορίσματα το έτος και το μήνα. Επιπλέον, δημιουργεί
        ένα λεξικό events το οποίο περιέχει όλα τα δεδομένα σχετικά με τα events.
        """

        self.current_year = current_year
        self.current_month = current_month

        self.events = dict()
        self.initialise_dictionary()
    # endregion

    # region Helper Functions
    months = ['', 'ΙΑΝ', 'ΦΕΒ', 'ΜΑΡ', 'ΑΠΡ', 'ΜΑΙ', 'ΙΟΥΝ', 'ΙΟΥΛ', 'ΑΥΓ', 'ΣΕΠ', 'ΟΚΤ', 'ΝΟΕ', 'ΔΕΚ']
    days = ['ΔΕΥ', 'ΤΡΙ', 'ΤΕΤ', 'ΠΕΜ', 'ΠΑΡ', 'ΣΑΒ', 'ΚΥΡ']

    def next_month(self, month, year):
        if month + 1 > 12:
            year += 1
            month = 1
        else:
            month += 1
        return month, year

    def prev_month(self, month, year):
        if month - 1 == 0:
            year -= 1
            month = 12
        else:
            month -= 1
        return month, year

    def is_event_on_current_day(self, day):
        event_list = self.events.get(f'{self.current_year}-{self.current_month}')
        if event_list is not None:
            for event in event_list:
                if event.date.day == day:
                    return True
        return False

    def search_event(self):
        """
        Αναζήτηση γεγονότων με βάση κάποιο έτος και μήνα. Εκτυπώνει ότι αποτελέσματα βρίσκει.
        """

        print('=== Αναζήτηση γεγονότων ====')

        year = Validations.val_int(input("Εισάγετε έτος: "), "Εισάγετε έτος: ")
        month = Validations.val_int(input("Εισάγετε μήνα: "), "Εισάγετε μήνα: ")
        while month > 12 or month == 0:
            Messages.warning('Δώστε τιμές από 1-12 για τον μήνα.')
            month = Validations.val_int(input("Εισάγετε μήνα: "), "Εισάγετε μήνα: ")

        # Διόρθωση για την περίπτωση που δοθεί το έτος για παράδειγμα 2022 και ο μήνας 04, ώστε να χρησιμοποιηθεί το
        # κλειδί 2022-4 και όχι το κλειδί 2022-04
        if len(str(month)) > 1 and str(month)[0] == '0':
            month = str(month)[1]

        event_list = self.events.get(f'{year}-{month}')
        if event_list is None:
            print('Δεν υπάρχει κάποιο γεγονός καταχωρημένο σε αυτήν την ημερομηνία.\n')
            return

        for i, event in enumerate(event_list):
            print(f'{i}. [{event.title}] -> Date: {event.date.format}, Time: {event.start_time.format}, Duration: {event.duration}')
        return event_list
    # endregion

    # region Main Functions
    def initialise_dictionary(self):
        """
        Αρχικοποιεί το λεξικό events με τα δεδομένα που βρίσκονται στο αρχείο csv και
        καλεί τη συνάρτηση notification.
        """

        DatabaseHandler.open_file(self.events)

    # region Πρώτο Μενού
    def create_calendar(self, final_month_calendar):
        """
        Αποθηκεύει στη λίστα final_month_calendar τις τιμές του επόμενου και προηγούμενου μήνα. Στην ουσία αντικαθιστά
        τις μηδενικές τιμές του month_calendar με αυτές του επόμενου και προηγούμενου μήνα.

        >>> calendar = Calendar(2022, 12)
        >>> fmc = cal.monthcalendar(calendar.current_year, calendar.current_month)
        >>> calendar.create_calendar(fmc)
        >>> print(fmc)
        [[28, 29, 30, 1, 2, 3, 4], [5, 6, 7, 8, 9, 10, 11], [12, 13, 14, 15, 16, 17, 18], [19, 20, 21, 22, 23, 24, 25], [26, 27, 28, 29, 30, 31, 1]]
        >>> month_calendar = cal.monthcalendar(calendar.current_year, calendar.current_month)
        >>> print(month_calendar)
        [[0, 0, 0, 1, 2, 3, 4], [5, 6, 7, 8, 9, 10, 11], [12, 13, 14, 15, 16, 17, 18], [19, 20, 21, 22, 23, 24, 25], [26, 27, 28, 29, 30, 31, 0]]
        """

        prev_month, prev_year = self.prev_month(self.current_month, self.current_year)
        next_month, next_year = self.next_month(self.current_month, self.current_year)

        prev_month_calendar = cal.monthcalendar(prev_year, prev_month)
        next_month_calendar = cal.monthcalendar(next_year, next_month)

        for i in range(7):
            if final_month_calendar[0][i] == 0:
                # φέρνει στη λίστα τις τιμές του προηγούμενου μήνα
                final_month_calendar[0][i] = prev_month_calendar[-1][i]

            if final_month_calendar[-1][i] == 0:
                # φέρνει στη λίστα τις τιμές του επόμενου μήνα
                final_month_calendar[-1][i] = next_month_calendar[0][i]

    def print_calendar(self):
        """
        Εκτυπώνει το ημερολόγιο.
        """

        final_month_calendar = cal.monthcalendar(self.current_year, self.current_month)
        month_calendar = cal.monthcalendar(self.current_year, self.current_month)

        self.create_calendar(final_month_calendar)

        print("-" * 60)
        print(f"{self.months[self.current_month]}  {self.current_year}")
        print("-" * 60)

        line = ""
        for i in range(7):
            line += "|\t" + self.days[i] + "\t "
        print(line[1:])

        for i, week in enumerate(final_month_calendar):
            line = ""
            for j, day in enumerate(week):
                spacing_before_day = "  " if day <= 9 else " "
                if final_month_calendar[i][j] == month_calendar[i][j]:
                    if self.is_event_on_current_day(day):
                        spacing_before_day = spacing_before_day[:-1] + '*'

                    line += f"| [{spacing_before_day}{str(day)}] "
                else:
                    line += f"|  {spacing_before_day}{str(day)}  "
            print("  " + line[1:])
        print("-" * 60)

    def print_menu(self):
        print(f'Πατήστε ENTER για προβολή του επόμενου μήνα, "q" για έξοδο ή κάποια από τις παρακάτω επιλογές:')
        print('\t"-" για πλοήγηση στον προηγούμενο μήνα')
        print('\t"+" για διαχείριση των γεγονότων του ημερολογίου')
        print('\t"*" για εμφάνιση των γεγονότων ενός επιλεγμένου μήνα')

    def prompt(self):
        Bonus.notification(self.events)

        self.print_calendar()
        self.print_menu()
        inp = input("> ")

        while inp != "q":
            if inp == "-":
                self.current_month, self.current_year = self.prev_month(self.current_month, self.current_year)
            elif inp == "+":
                self.event_handling_prompt()
            elif inp == "*":
                self.show_events()
            elif inp == "":
                self.current_month, self.current_year = self.next_month(self.current_month, self.current_year)
            else:
                Messages.warning('Invalid input.')

            self.print_calendar()
            self.print_menu()
            inp = input("> ")

        db = DatabaseHandler()
        db.backup_data(self.events)
    # endregion

    # region Λειτουργίες Πρώτου Μενού
    def show_events(self):
        self.search_event()
        input('Πατήστε enter για επιστροφή στο κυρίως μενού: ')
    # endregion

    # region Δεύτερο Μενού
    def print_event_handling_menu(self):
        print('Διαχείριση γεγονότων ημερολογίου, επιλέξτε ενέργεια:')
        print('\t1 Καταγραφή νέου γεγονότος')
        print('\t2 Διαγραφή γεγονότος')
        print('\t3 Ενημέρωση γεγονότος')
        print('\t0 Επιστροφή στο κυρίως μενού')

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
    # endregion

    # region Λειτουργίες Δεύτερου Μενού
    def add_event(self):
        run = True
        while run:
            date = Validations.val_date(input("Ημερομηνία γεγονότος: "))
            start_time = Validations.val_time(input('Ώρα γεγονότος: '))
            duration = Validations.val_int(input("Διάρκεια γεγονότος: "), "Διάρκεια γεγονότος: ")
            title = Validations.val_title(input("Τίτλος γεγονότος: "))

            event = Event(date, start_time, int(duration), title)
            run = not Bonus.conflict(event, self.events)

        key = event.date.key

        if self.events.get(key) is None:
            self.events[key] = [event]
        else:
            self.events[key].append(event)
        Messages.success('Το νέο γεγονός προστέθηκε με επιτυχία')

    def update_event(self):
        event_list = self.search_event()

        if event_list is None:
            input('Πατήστε enter για επιστροφή στο κυρίως μενού: ')
            return

        # Έλεγχος ώστε να δοθεί σωστό index
        input_text = f"Επιλέξτε γεγονός προς ενημέρωση (0-{len(event_list) - 1}): "
        index = Validations.val_int(input(input_text), input_text)
        while index > len(event_list) - 1:
            Messages.warning(f'Παρακαλώ επιλέξτε ακέραιο από 0-{len(event_list) - 1}')
            index = Validations.val_int(input(input_text), input_text)

        event = event_list[index]

        inp = input(f"Ημερομηνία γεγονότος ({event.date.format}): ")
        event.date = Date(Validations.val_date(inp)) if inp != "" else event.date

        inp = input(f"Ώρα γεγονότος ({event.start_time.format}): ")
        event.start_time = Time(Validations.val_time(inp)) if inp != "" else event.start_time

        inp = input(f"Διάρκεια γεγονότος ({event.duration}): ")
        event.duration = Validations.val_int(inp, "Διάρκεια γεγονότος: ") if inp != "" else event.duration

        inp = input(f"Τίτλος γεγονότος ({event.title}): ")
        event.title = Validations.val_title(inp) if inp != "" else event.title

        Messages.success(f'Το γεγονός ενημερώθηκε: <[{event.title}] -> Date: {event.date.format}, Time: {event.start_time.format}, Duration: {event.duration}>')
        event_list[index] = event

        input('Πατήστε enter για επιστροφή στο κυρίως μενού: ')

    def delete_event(self):
        event_list = self.search_event()

        if event_list is None:
            input('Πατήστε enter για επιστροφή στο κυρίως μενού: ')
            return

        # Έλεγχος ώστε να δοθεί σωστό index
        input_text = f"Επιλέξτε γεγονός προς διαγραφή (0-{len(event_list) - 1}): "
        index = Validations.val_int(input(input_text), input_text)
        while index < 0 or index > len(event_list)-1:
            Messages.warning(f'Παρακαλώ επιλέξτε ακέραιο από 0-{len(event_list)-1}')
            index = Validations.val_int(input(input_text), input_text)

        event = event_list[index]
        Messages.success(f'Το γεγονός διαγράφηκε: <[{event.title}] -> Date: {event.date.format}, Time: {event.start_time.format}, Duration: {event.duration}>')
        event_list.remove(event)
    # endregion

    # endregion


if __name__ == "__main__":
    import doctest
    doctest.testmod()

    c = Calendar(2023, 1)
    c.prompt()
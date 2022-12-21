<<<<<<< HEAD
from datetime import datetime
import calendar
import locale
import csv
=======
from time import gmtime, strftime
from datetime import datetime
import calendar
import locale
>>>>>>> ada7bd1625f1f4f3ec84908502d9df38df11ada5


# Προσθέτει τις ημέρες του προηγούμενο μήνα
def previous_month(year, month):
    if month == 1:
        month = 13
        year = year - 1
    c = calendar.Calendar()
    previous = c.monthdayscalendar(year, month - 1)
    return previous


# Προσθέτει τις ημέρες του επόμενο μήνα
def next_month(year, month):
    if month == 12:
        month = 0
        year += 1
    c = calendar.Calendar()
    next = c.monthdayscalendar(year, month + 1)
    return next


# Ελέγχει αν η μέρα είναι του τωρινού μήνα
<<<<<<< HEAD
def check_day(p, k, year, month):
    if current[p][k] < 10:
        day = "0" + str(current[p][k])
    else:
        day = str(current[p][k])

    if int(month) < 9:
        month = "0" + str(month)
    if current[p][k] == current_final[p][k]:
        string = "[" + search_for_event(str(str(year) + "-" + str(month) + "-" + day)) + str(current[p][k]) + "]"
=======
def check_day(p, k):
    if current[p][k] == current_final[p][k]:
        string = "[" + note + str(current_final[p][k]) + "]"
>>>>>>> ada7bd1625f1f4f3ec84908502d9df38df11ada5
        string = string.rjust(5)
        return string
    else:
        return str(current_final[p][k]).rjust(5)


# Δημιουργεί τον ημερολογιακό πίνακα
def create_calendar(year, month):
    # loop για να φέρω στη λίστα τις τιμές του προηγούμενου μήνα
    for i in range(len(current_final[0])):
        if current_final[0][i] == 0:
            current_final[0][i] = previous[-1][i]

    # loop για να φέρω στη λίστα τις τιμές του επόμενου μήνα
    for i in range(len(current_final[0])):
        if current_final[-1][i] == 0:
            current_final[-1][i] = next[0][i]


<<<<<<< HEAD
def search_for_event(search_for_day):
    for i in range(len(csv_file)):
        if csv_file[i][0] == search_for_day:
            return "*"
    else:
        return ""


=======
>>>>>>> ada7bd1625f1f4f3ec84908502d9df38df11ada5
# Τυπώνει το ημερολόγιο
def print_calendar(month, year):
    print("-" * 60)
    print(Months[month - 1], year)
    print("-" * 60)

    result = ""
    for i in range(7):
        result += ("|  " + Days[i]).center(7)
    print(result[1:], end="")
    print("")

    for k in range(len(current_final)):
        result = ""
        for i in range(len(current_final[k])):
<<<<<<< HEAD
            result += " |" + str(check_day(k, i, year, month))
=======
            result += " |" + str(check_day(k, i))
>>>>>>> ada7bd1625f1f4f3ec84908502d9df38df11ada5
        print(result[1:], end="")
        print("")
    print("-" * 60)


<<<<<<< HEAD
def search_events():
    year = validate_year()
    month = validate_month()
    search_res = []
    for i in range(len(csv_file)):
        if csv_file[i][0][:4] == year and csv_file[i][0][5:7] == month:
            search_res.append(csv_file[i])
    if len(search_res) == 0:
        print("Για τον μήνα " + month + "/" + year + " δεν βρέθηκαν εγγραφές")
    else:
        for i in range(len(search_res)):
            print(str(i) + ". [" + search_res[i][3] + "] -> Date: " + search_res[i][0] + ", Time: " + search_res[i][1] + ", Duration: " + search_res[i][2])
    return search_res


# VALIDATIONS
def validate_year():
    while True:
        year = input("Εισάγετε έτος: ")
        if not year.isdigit() or len(year) != 4:
            print("Μη έγκυρο έτος")
        else:
            return year


def validate_month():
    while True:
        month = input("Εισάγετε μήνα: ")
        if not month.isdigit():
            print("Εισάγετε μόνο αριθμούς!")
        else:
            if int(month) < 1 or int(month) > 12:
                print("Εισάγετε έγκυρο μήνα!(1-12)")
            else:
                if int(month) < 9:
                    month = "0" + month
                return month


def validate_date(date):
    while True:
        try:
            true_false = bool(datetime.strptime(date, "%Y-%m-%d"))
            date = date.split("-")
            if int(date[0]) <= 2022:
                print("Δώστε χρονολογία μεγαλύτερη του 2022")
            else:
                break
        except ValueError:
            print("Λάθος μορφή ημερομήνιας!")
        date = input("Βάλτε ημερομηνία της μορφής 'YYYY-MM-DD': ")
    if int(date[1]) < 9:
        date[1] = "0" + str(date[1])
    if int(date[2]) < 9:
        date[2] = "0" + str(date[2])
    date = str(date[0]) + "-" + str(date[1] + "-" + str(date[2]))
    return date


def validate_time(time):
    while True:
        try:
            true_false = bool(datetime.strptime(time, "%H:%M"))
            break
        except ValueError:
            print("Λάθος μορφή ημερομήνιας!")
        time = input("Εισάγετε ώρα γεγονότος της μορφής 'HH:MM': ")
    time = time.split(":")
    if int(time[0]) < 10:
        time[0] = "0" + str(time[0])
    if int(time[1]) < 10:
        time[1] = "0" + str(time[1])
    time = str(time[0]) + ":" + str(time[1])
    return time


def validate_positive_number(positive):
    while True:
        if not positive.isdigit():
            print("Εισάγετε μόνο θετικό αριθμό!")
        else:
            return positive
        positive = input("Εισάγετε διάρκεια γεγονότος: ")


def validate_event(title):
    while True:
        if "," in title:
            print("Χρησιμοποιήσατε μη αποδεκτό χαρακτήρα(,)")
        else:
            return title
        title = input("Εισάγετε τίτλο γεγονότος:")


# Δημιουργεί λίστα από το αρχείο csv της μορφής l = [[value, value, value][value, value, value][value, value, value]]
# Ανοίγει το αρχείο και στο τέλος το κλείνει.
csv_file = []
f = open("events.csv", "r")
for line in f:
    line = line.strip()
    line = line.split(',')
    csv_file.append(line)
f.close()

=======
>>>>>>> ada7bd1625f1f4f3ec84908502d9df38df11ada5
# Λίστες με τις ονομασίες των μηνών και ημερών
Months = ["ΙΑΝ", "ΦΕΒ", "ΜΑΡ", "ΑΠΡ", "ΜΑΙ", "ΙΟΥΝ", "ΙΟΥΛ", "ΑΥΓ", "ΣΕΠ", "ΟΚΤ", "ΝΟΕ", "ΔΕΚ"]
Days = ["ΔΕΥ", "ΤΡΙ", "ΤΕΤ", "ΠΕΜ", "ΠΑΡ", "ΣΑΒ", "ΚΥΡ"]

# Για να έχω τη σημερινή ημερομηνία
today = datetime.now()

# Διαδικασία για να τυπωθεί η ημερομηνία με το τρέχον locale
loc = locale.getlocale()                # Παίρνουμε τις τρέχουσες ρυθμίσεις γλώσσας
locale.setlocale(locale.LC_ALL, loc)    # Επιβάλλουμε να χρησιμοποιηθούν οι ρυθμίσεις συστήματος

<<<<<<< HEAD
# Μεταβλητές
year = today.year
month = today.month


# Κυρίως Πρόγραμμα - Loop που επαναλαμβάνετε μέχρι να πατηθεί "q"
while True:
    # Δημιουργεί το ημερολόγιο τωρινού μήνα
    c = calendar.Calendar()
    current_final = c.monthdayscalendar(year, month)
    current = c.monthdayscalendar(year, month)

    # Δημιουργεί τον προηγούμενο μήνα
    previous = previous_month(year, month)

    # Δημιουργεί τον επόμενο μήνα
    next = next_month(year, month)

    create_calendar(year, month)
    print_calendar(month, year)
=======
# Μεταβλητές για να δούμε αν δουλεύει - Αργότερα θα βγουν και θα τραβάει δεδομένα από αλλού
year = 1976         # today.year
month = 8           # today.month
not_a_note = " "
note = "*"

# Δημιουργεί το ημερολόγιο τωρινού μήνα
c = calendar.Calendar()
current_final = c.monthdayscalendar(year, month)
current = c.monthdayscalendar(year, month)

# Δημιουργεί τον προηγούμενο μήνα
previous = previous_month(year, month)

# Δημιουργεί τον επόμενο μήνα
next = next_month(year, month)

create_calendar(year, month)
print_calendar(month, year)

# Loop που επαναλαμβάνετε μέχρι να πατηθεί "q"
while True:
>>>>>>> ada7bd1625f1f4f3ec84908502d9df38df11ada5
    print("Πατήστε ENTER για προβολή του επόμενου μήνα, 'q' για έξοδο ή κάποια από τις παρακάτω επιλογές:")
    print("\t'-' για πλοήγηση στον προηγούμενο μήνα.")
    print("\t'+' για διαχείρηση των γεγονότων του ημερολογίου.")
    print("\t'*' για εμφάνιση των γεγονότων ενός επιλεγμένου μήνα.")
    choice = input("-> ")
    while choice != "-" and choice != "+" and choice != "*" and choice != "q" and choice != "":
        print("ERROR - Πατήστε μόνο ενδεδειγμένους χαρακτήρες(+, -, *, q, enter)")
        choice = input()

    # ΑΡΧΙΚΟ ΜΕΝΟΥ
<<<<<<< HEAD
    # Αν ο χρήστης πάτησε enter για να προχωρήσει το ημερολόγιο ένα μήνα εμπρός
    if choice == "":
        month += 1
        if month == 13:
            month = 1
            year += 1


    # ΑΡΧΙΚΟ ΜΕΝΟΥ
    # Αν ο χρήστης πάτησε "-" για να γυρίσει το ημερολόγιο ένα μήνα πίσω
    elif choice == "-":
        month -= 1
        if month == 0:
            month = 12
            year -= 1
        # Δημιουργεί το ημερολόγιο τωρινού μήνα
        c = calendar.Calendar()
        current_final = c.monthdayscalendar(year, month)
        current = c.monthdayscalendar(year, month)

        # Δημιουργεί τον προηγούμενο μήνα
        previous = previous_month(year, month)

        # Δημιουργεί τον επόμενο μήνα
        next = next_month(year, month)

        create_calendar(year, month)
=======
    # Αν ο χρήστης πάτησε enter
    if choice == "":
        month += 1
        print_calendar(month, year)

    # ΑΡΧΙΚΟ ΜΕΝΟΥ
    # Αν ο χρήστης πάτησε "-"
    elif choice == "-":
        month -= 1
>>>>>>> ada7bd1625f1f4f3ec84908502d9df38df11ada5
        print_calendar(month, year)

    # ΑΡΧΙΚΟ ΜΕΝΟΥ
    # Αν ο χρήστης πάτησε "+"
    elif choice == "+":
        print("\033[1m" + "Διαχείρηση γεγονότων ημερολογίου," + "\033[0m" + " επιλέξτε ενέργεια")
        print("\t1 Καταγραφή νέου γεγονότος")
        print("\t2 Διαγραφή γεγονότος")
        print("\t3 Ενημέρωση γεγονότος")
        print("\t0 Επιστροφή στο κυρίως μενού")
        choice = input("-> ")
        while choice != "0" and choice != "1" and choice != "2" and choice != "3":
            print("ERROR - Πατήστε μόνο ενδεδειγμένους χαρακτήρες(1, 2, 3, 0)")
            choice = input()
        if choice == "1":
<<<<<<< HEAD
            # Εισαγωγή ημερομηνίας
            date = validate_date(input("Εισάγετε ημερομηνία γεγονότος:"))

            # Εισαγωγή ώρας
            time = validate_time(input("Εισάγετε ώρα γεγονότος: "))

            # Διάρκεια γεγονότος
            duration = validate_positive_number(input("Εισάγετε διάρκεια γεγονότος: "))

            # Εισαγωγή τίτλου γεγονότος
            title = validate_event(input("Εισάγετε τίτλο γεγονότος: "))

            # Καταχώρηση εγγραφής στη λίστα csv_file
            new_entry = [date, time, duration, title]
            csv_file.append(new_entry)

        elif choice == "2":
            while True:
                search_res = search_events()
                if len(search_res) == 0:
                    print("Προσπαθήστε ξανα")
                else:
                    while True:
                        choice = input("Επιλέξτε γεγονός προς διαγραφή: ")
                        if not choice.isdigit():
                            print("Εισάγετε έγκυρη επιλογή")
                        elif int(choice) < 0 or int(choice) > len(search_res)-1:
                            print("Εισάγετε έγκυρο αριθμό")
                        else:
                            break
                    for i in range(len(csv_file)):
                        if csv_file[i] == search_res[int(choice)]:
                            delete = i
                    csv_file.pop(delete)
                    break
            print(csv_file)

        elif choice == "3":
            while True:
                search_res = search_events()
                if len(search_res) == 0:
                    print("Προσπαθήστε ξανα")
                else:
                    while True:
                        choice = input("Επιλέξτε γεγονός προς ενημέρωση: ")
                        if not choice.isdigit():
                            print("Εισάγετε έγκυρη επιλογή!")
                        elif int(choice) < 0 or int(choice) > len(search_res)-1:
                            print("Εισάγετε έγκυρο αριθμό")
                        else:
                            break
                    break
            for i in range(len(csv_file)):
                if csv_file[i] == search_res[int(choice)]:
                    change = i

            # Αλλαγή ημερομηνίας
            event_date = input("Ημερομηνία γεγονότος (" + csv_file[change][0]+"): ")
            if event_date == "":
                pass
            else:
                event_date = validate_date(event_date)
                csv_file[change][0] = event_date

            # Αλλαγή ώρας
            event_time = input("Ώρα γεγονότος (" + csv_file[change][1]+"): ")
            if event_time == "":
                pass
            else:
                event_time = validate_time(event_time)
                csv_file[change][1] = event_time

            # Αλλαγή διάρκειας γεγονότος
            event_duration = input("Διάρκεια γεγονότος (" + csv_file[change][2] + "): ")
            if event_duration == "":
                pass
            else:
                event_duration = validate_time(event_duration)
                csv_file[change][2] = event_duration

            # Αλλαγή Τίτλου γεγονότος
            event_title = input("Τίτλος γεγονότος (" + csv_file[change][3] + "): ")
            if event_title == "":
                pass
            else:
                event_title = validate_event(event_title)
                csv_file[change][3] = event_title


=======
            pass
        elif choice == "2":
            pass
        elif choice == "3":
            pass
>>>>>>> ada7bd1625f1f4f3ec84908502d9df38df11ada5
        elif choice == "0":
            print_calendar(month, year)

    # ΑΡΧΙΚΟ ΜΕΝΟΥ
    # Αν ο χρήστης πάτησε "*"
    elif choice == "*":
<<<<<<< HEAD
        while True:
            search_res = search_events()
            if len(search_res) == 0:
                print("Προσπαθήστε ξανα")
            else:
                input("Πατήστε οποιοδήποτε χαρακτήρα για επιστροφή στο κυρίως μενού")
                break
=======
        pass
>>>>>>> ada7bd1625f1f4f3ec84908502d9df38df11ada5

    # ΑΡΧΙΚΟ ΜΕΝΟΥ
    # Αν ο χρήστης πάτησε "q"
    elif choice == "q":
<<<<<<< HEAD
        # Στην έξοδο μεταφέρει τη λίστα στο αρχείο csv
        with open("events.csv", "w") as f:
            write = csv.writer(f)
            write.writerows(csv_file)
=======
>>>>>>> ada7bd1625f1f4f3ec84908502d9df38df11ada5
        print("BYE BYE!")
        break


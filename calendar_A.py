from time import gmtime, strftime
from datetime import datetime
import calendar
import locale


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
def check_day(p, k):
    if current[p][k] == current_final[p][k]:
        string = "[" + note + str(current_final[p][k]) + "]"
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
            result += " |" + str(check_day(k, i))
        print(result[1:], end="")
        print("")
    print("-" * 60)


# Λίστες με τις ονομασίες των μηνών και ημερών
Months = ["ΙΑΝ", "ΦΕΒ", "ΜΑΡ", "ΑΠΡ", "ΜΑΙ", "ΙΟΥΝ", "ΙΟΥΛ", "ΑΥΓ", "ΣΕΠ", "ΟΚΤ", "ΝΟΕ", "ΔΕΚ"]
Days = ["ΔΕΥ", "ΤΡΙ", "ΤΕΤ", "ΠΕΜ", "ΠΑΡ", "ΣΑΒ", "ΚΥΡ"]

# Για να έχω τη σημερινή ημερομηνία
today = datetime.now()

# Διαδικασία για να τυπωθεί η ημερομηνία με το τρέχον locale
loc = locale.getlocale()                # Παίρνουμε τις τρέχουσες ρυθμίσεις γλώσσας
locale.setlocale(locale.LC_ALL, loc)    # Επιβάλλουμε να χρησιμοποιηθούν οι ρυθμίσεις συστήματος

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
    print("Πατήστε ENTER για προβολή του επόμενου μήνα, 'q' για έξοδο ή κάποια από τις παρακάτω επιλογές:")
    print("\t'-' για πλοήγηση στον προηγούμενο μήνα.")
    print("\t'+' για διαχείρηση των γεγονότων του ημερολογίου.")
    print("\t'*' για εμφάνιση των γεγονότων ενός επιλεγμένου μήνα.")
    choice = input("-> ")
    while choice != "-" and choice != "+" and choice != "*" and choice != "q" and choice != "":
        print("ERROR - Πατήστε μόνο ενδεδειγμένους χαρακτήρες(+, -, *, q, enter)")
        choice = input()

    # ΑΡΧΙΚΟ ΜΕΝΟΥ
    # Αν ο χρήστης πάτησε enter
    if choice == "":
        month += 1
        print_calendar(month, year)

    # ΑΡΧΙΚΟ ΜΕΝΟΥ
    # Αν ο χρήστης πάτησε "-"
    elif choice == "-":
        month -= 1
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
            pass
        elif choice == "2":
            pass
        elif choice == "3":
            pass
        elif choice == "0":
            print_calendar(month, year)

    # ΑΡΧΙΚΟ ΜΕΝΟΥ
    # Αν ο χρήστης πάτησε "*"
    elif choice == "*":
        pass

    # ΑΡΧΙΚΟ ΜΕΝΟΥ
    # Αν ο χρήστης πάτησε "q"
    elif choice == "q":
        print("BYE BYE!")
        break


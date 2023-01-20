from datetime import datetime
from datetime import timedelta
import calendar
import locale
import csv


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
def check_day(p, k, year, month):
    if current[p][k] < 10:
        day = "0" + str(current[p][k])
    else:
        day = str(current[p][k])

    if int(month) < 9:
        month = "0" + str(month)
    if current[p][k] == current_final[p][k]:
        string = "[" + search_for_event(str(str(year) + "-" + str(month) + "-" + day)) + str(current[p][k]) + "]"
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


def search_for_event(search_for_day):
    for i in range(len(csv_file)):
        if csv_file[i][0] == search_for_day:
            return "*"
    else:
        return ""


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
            result += " |" + str(check_day(k, i, year, month))
        print(result[1:], end="")
        print("")
    print("-" * 60)


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


def conflict(date, time, duration):
    # Δημιουργεί συνολική διάρκεια σε λεπτά για το νέο γεγονός
    event_time = time.split(":")
    begin_event_time = int(event_time[0]) * 60 + int(event_time[1])
    end_event_time = begin_event_time + int(duration)

    for i in range(len(csv_file)):
        if csv_file[i][0] == date:
            # Creates total duration in minutes of day for event in csv file
            csv_time = csv_file[i][1].split(":")
            begin_time = int(csv_time[0])*60 + int(csv_time[1])
            end_time = begin_time + int(csv_file[i][2])

            # Ελέγχει αν η διάρκεια του παλιού γεγονότος είναι μέσα στη διάρκεια του νέου
            for k in range(begin_event_time, end_event_time+1):
                if k == begin_time or k == end_time:
                    return True
                # checks if new event time is in csv time
            for j in range(begin_time, end_time+1):
                if j == begin_event_time or j == end_event_time:
                    return True

    # Ελέγχει αν το νέο γεγονός αλλάζει μέρα
    if end_event_time > 1439:
        next_day_minutes = end_event_time - 1439
        # Ψάξιμο στην επόμενη μέρα για το χρόνο που απομένει από το duration
        s = datetime.strptime(date, "%Y-%m-%d")
        modified_date = s + timedelta(days=1)
        next_day = str(modified_date)[0:10]
        return conflict(next_day, "00:00", next_day_minutes)

    # Ελέγχει την προηγούμενη μέρα αν υπάρχει γεγονός που αλλάζει μέρα
    s = datetime.strptime(date, "%Y-%m-%d")
    modified_date = s + timedelta(days=-1)
    prev_day = str(modified_date)[0:10]
    for i in range(len(csv_file)):
        if csv_file[i][0] == prev_day:
            # Creates total duration in minutes of day for event in csv file
            csv_time = csv_file[i][1].split(":")
            begin_time = int(csv_time[0])*60 + int(csv_time[1])
            end_time = begin_time + int(csv_file[i][2])
            if end_time > 1439:
                next_day_minutes = end_time - 1439
                return conflict(prev_day, "23:59", next_day_minutes)

    return False


def today_event():
    currentDateAndTime = datetime.now()
    currentTime = currentDateAndTime.strftime("%H:%M")

    # Find current date and change to str
    year = str(currentDateAndTime.year)
    month = str(currentDateAndTime.month)
    if len(month) < 2:
        month = "0" + month
    day = str(currentDateAndTime.day)
    if len(day) < 2:
        day = "0" + day

    # Search for event in current date
    a = 0
    text = ""
    for i in range(len(csv_file)):
        if csv_file[i][0][:4] == year and csv_file[i][0][5:7] == month and csv_file[i][0][8:10] == day:
            time1 = csv_file[i][1]
            t1 = timedelta(hours=int(currentTime[0:2]), minutes=int(currentTime[3:5]))
            t2 = timedelta(hours=int(time1[0:2]), minutes=int(time1[3:5]))
            if t1 > t2:
                text += "- Υπήρχε προγραμματισμένο για σήμερα το γεγονός '" + csv_file[i][3] + "' στις " + csv_file[i][1] + "\n"
                a += 1
            else:
                duration = t2 - t1
                duration = str(duration).split(":")
                if duration[0] == "0":
                    text += "- Ειδοποίηση: σε " + duration[1] + " λεπτά από τώρα έχει προγραμματιστεί το γεγονός '" + csv_file[i][3] + "'" + "\n"
                    a += 1
                else:
                    text += "- Ειδοποίηση: σε " + duration[0] + " ώρες και " + duration[1] + " λεπτά από τώρα έχει προγραμματιστεί το γεγονός '" + csv_file[i][3] + "'" + "\n"
                    a += 1
    if a == 0:
        return "Δεν υπάρχει κάτι προγραμματισμένο για σήμερα."
    else:
        return text

# VALIDATIONS
def validate_year():
    while True:
        year = input("Εισάγετε έτος: ")
        if not year.isdigit() or len(year) != 4:
            print("Μη έγκυρο έτος")
        else:
            return str(year)


def validate_month():
    while True:
        month = input("Εισάγετε μήνα: ")
        if not month.isdigit():
            print("Εισάγετε μόνο αριθμούς!")
        else:
            if int(month) < 1 or int(month) > 12:
                print("Εισάγετε έγκυρο μήνα!(1-12)")
            else:
                if len(month) < 2:
                    month = "0" + month
                return str(month)


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
    if len(date[1]) < 2:
        date[1] = "0" + str(date[1])
    if len(date[2]) < 2:
        date[2] = "0" + str(date[2])
    date = str(date[0]) + "-" + str(date[1] + "-" + str(date[2]))
    return str(date)


def validate_time(time):
    while True:
        try:
            true_false = bool(datetime.strptime(time, "%H:%M"))
            break
        except ValueError:
            print("Λάθος μορφή ώρας!")
        time = input("Εισάγετε ώρα γεγονότος της μορφής 'HH:MM': ")
    time = time.split(":")
    if len(time[0]) < 2:
        time[0] = "0" + str(time[0])
    if len(time[1]) < 2:
        time[1] = "0" + str(time[1])
    time = str(time[0]) + ":" + str(time[1])
    return str(time)


def validate_positive_number(positive):
    while True:
        if not positive.isdigit():
            print("Εισάγετε μόνο θετικό αριθμό!")
        else:
            return str(positive)
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

# Λίστες με τις ονομασίες των μηνών και ημερών
Months = ["ΙΑΝ", "ΦΕΒ", "ΜΑΡ", "ΑΠΡ", "ΜΑΙ", "ΙΟΥΝ", "ΙΟΥΛ", "ΑΥΓ", "ΣΕΠ", "ΟΚΤ", "ΝΟΕ", "ΔΕΚ"]
Days = ["ΔΕΥ", "ΤΡΙ", "ΤΕΤ", "ΠΕΜ", "ΠΑΡ", "ΣΑΒ", "ΚΥΡ"]

# Για να έχω τη σημερινή ημερομηνία
today = datetime.now()

# Διαδικασία για να τυπωθεί η ημερομηνία με το τρέχον locale
loc = locale.getlocale()                # Παίρνουμε τις τρέχουσες ρυθμίσεις γλώσσας
locale.setlocale(locale.LC_ALL, loc)    # Επιβάλλουμε να χρησιμοποιηθούν οι ρυθμίσεις συστήματος

# Μεταβλητές
year = today.year
month = today.month

# Έλεγχος αν υπάρχουν συμβάντα σήμερα και εμφάνιση αυτών
print(today_event())
temp = input("Press enter to continue...")

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
    print("Πατήστε ENTER για προβολή του επόμενου μήνα, 'q' για έξοδο ή κάποια από τις παρακάτω επιλογές:")
    print("\t'-' για πλοήγηση στον προηγούμενο μήνα.")
    print("\t'+' για διαχείρηση των γεγονότων του ημερολογίου.")
    print("\t'*' για εμφάνιση των γεγονότων ενός επιλεγμένου μήνα.")
    choice = input("-> ")
    while choice != "-" and choice != "+" and choice != "*" and choice != "q" and choice != "":
        print("ERROR - Πατήστε μόνο ενδεδειγμένους χαρακτήρες(+, -, *, q, enter)")
        choice = input()

    # ΑΡΧΙΚΟ ΜΕΝΟΥ
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
            # Εισαγωγή ημερομηνίας
            date = validate_date(input("Εισάγετε ημερομηνία γεγονότος:"))

            # Εισαγωγή ώρας
            time = validate_time(input("Εισάγετε ώρα γεγονότος: "))

            # Διάρκεια γεγονότος
            duration = validate_positive_number(input("Εισάγετε διάρκεια γεγονότος: "))

            # Έλεγχος αν υπάρχει άλλο event προγραμματισμένο εκείνη την ώρα
            if conflict(date, time, duration):
                print("Υπάρχει ήδη προγραμματισμένο γεγονός για εκείνη την ώρα.")
            else:
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


        elif choice == "0":
            print_calendar(month, year)

    # ΑΡΧΙΚΟ ΜΕΝΟΥ
    # Αν ο χρήστης πάτησε "*"
    elif choice == "*":
        while True:
            search_res = search_events()
            if len(search_res) == 0:
                print("Προσπαθήστε ξανα")
            else:
                input("Πατήστε οποιοδήποτε χαρακτήρα για επιστροφή στο κυρίως μενού")
                break

    # ΑΡΧΙΚΟ ΜΕΝΟΥ
    # Αν ο χρήστης πάτησε "q"
    elif choice == "q":
        print(csv_file)
        # Στην έξοδο μεταφέρει τη λίστα στο αρχείο csv
        with open("events.csv", "w", newline="") as f:
            write = csv.writer(f)
            write.writerows(csv_file)
        print("BYE BYE!")
        break

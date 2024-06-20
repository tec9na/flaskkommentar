from flask import Flask, render_template, url_for, redirect, request, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
# Flask = webframework <=> render_template = aflæser html-filer, url_for = generere URL'er, redirect = omdirigerer til en anden URL, request = aflæser data fra formularer, flash = viser beskeder til brugeren
# flask_login <=> LoginManager = håndtere login, UserMixin = bruges til at definere en brugerklasse, login_user = logge brugeren ind, login_required = sikre at brugeren er logget ind, logout_user = logge brugeren ud, current_user = returnere den aktuelle bruger
# flask_wtf <=> FlaskForm = bruges til at definere formularer, wtform <=> Stringfield = tekstfelt, PasswordField = adgangskodefelt, SubmitField = knapfelt
# wtform.validators <=> InputRequired = sikre at feltet er udfyldt, Length = sikre at længden af inputtet er indenfor en bestemt længde
# sqlite3 = database, werkzeug.security <=> generate_password_hash = hash adgangskoden, check_password_hash = tjekker om adgangskoden er korrekt
# datetime = håndtere datoer og klokkeslæt, timedelta = repræsenterer en tidsperiode
# grøn = klasse, gul = funktioner, blå = globale variabler

app = Flask(__name__)                     # Linje 17 initialiserer en ny Flask-applikation og gemmer den i variablen app
                                          # app = instans af Flask-klassen
                                          # __name__ = special prædefineret variabel, som er brugt af Python "tolken" til at identificere navnet på det aktuelle script
                                          # Python fortolkeren parser koden, og identificere __name__ som "__main__" når scriptet køres direkte 
                                          # Flask bruger __name__ for at bestemme roden til applikationen hvilket hjælper med at identificere statiske filer og templates

app.config['SECRET_KEY'] = 'secret_key'   # Linje 23 er et statement, brugt i Flask til at konfigurerer applikationen med en hemmelig nøgle, som bruges til at sikre applikationen 
                                          # Metodekald config er en #USIKKER# til app(instans af Flask), som er et dictionary der indeholder konfigurationsindstillinger
                                          # 'SECRET_KEY' er en string brugt som key i config biblioteket. SECRET_KEY er en hemmelig nøgle, som bruges til at sikre applikationen
                                          # 'secret_key' er en vilkårlig string værdi, angivet til 'SECRET_KEY' attributten - værdien er en placeholder og burde være stærkere og ude for rækkevidde for uvedkommende

login_manager = LoginManager()      # Linje 28 initialiserer en ny instans af LoginManager-klassen og gemmer den i variablen login_manager
login_manager.init_app(app)         # Metodekald init_app() (fra flask) på login_manager-objektet - bruger app som argument. Dette integrere instansen af LoginManager med Flask applikationen (app)
login_manager.login_view = 'login'  # Linje 30 sætter login_view-attributten på login_manager-objektet til 'login'. Dette fortæller login_manager, at login-siden på vores Flask applikation er 'login'.

def init_db():                                             # Definere funktionen init_db der er ansvarlig for initialiseringen af SQLite-databasen og oprettelse af tabeller
    with sqlite3.connect('arbejdstider.db') as conn:       ##USIKKER## with = statement, sqlite3 = modul, connect() = funktion, 'arbejdstider.db' = argument, conn = variabel/"connection"-objekt. Dette with statement opretter en forbindelse til SQLite-databasen og gemmer den i variablen conn - eller opretter databasen hvis ikke den eksisterer
        cursor = conn.cursor()                             # (curser er den metode der gør at databasen og applikationen snakker sammen) Metodekald cursor() på connection-objektet(conn). Dette returnerer et cursor-objekt, som bruges til at udføre SQL-forespørgsler

# Linje 44, SQL-statement = opretter en tabel i SQLite-databasen, hvis den ikke eksisterer. Metodenkald execute() på cursor-objektet, og tager en SQL-forespørgsel som ARGUMENT/ELLER PARAMETRE?(LAV TABEL HVIS IKKE DEN EKSISTERE) i en flerlinjet string
# række "id" er en integer række der bruges som primær nøgle, og autoincrementeres for hver ny række der indsættes og sikre en unik identifikation for hver række
# Række "Date" er en datetime række, der bruges til at gemme datoer, med en NOT NULL-begrænsning
# Række "Start" og "End" er begge tekst-rækker, der bruges til at gemme start- og sluttidspunktet for en arbejdsdag, med en NOT NULL-begrænsning
# Række "BreakStart" og "BreakEnd" er begge tekst-rækker, der bruges til at gemme start- og sluttidspunktet for en pause de er ikke obligatoriske, og kan være NULL
# Række "TimeChange" er en tekst-række, der bruges til at gemme ændringer i arbejdstiden
# Række "user_id" er en integer-række, der bruges til at gemme brugerens id, med en NOT NULL-begrænsning
        cursor.execute('''CREATE TABLE IF NOT EXISTS arbejdstider (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                Date DATETIME NOT NULL,
                Start TEXT NOT NULL,
                End TEXT NOT NULL,
                BreakStart TEXT,
                BreakEnd TEXT,
                TimeChange TEXT,
                user_id INTEGER NOT NULL)''')
# Linje 59, SQL-statement = opretter en tabel i SQLite-databasen, hvis den ikke eksistere. Metodekald execute() på cursor-objektet, og tager en SQL-forespørgsel som ARGUMENT/ELLER PARAMETRE?(LAV TABEL HVIS IKKE DEN EKSISTERE) i en flerlinjet string 
# række "id" er en integer række der bruges som primær nøgle, og autoincrementeres for hver ny række der indsættes og sikre en unik identifikation for hver række
# Række "Date" er en tekst-række, der bruges til at gemme datoer, med en NOT NULL-begrænsning
# Række "Start" og "End" er begge tekst-rækker, der bruges til at gemme start- og sluttidspunktet for en arbejdsdag, med en NOT NULL-begrænsning
# Række "Pause_Start" og "Pause_End" er begge tekst-rækker, der bruges til at gemme start- og sluttidspunktet for en pause de er ikke obligatoriske, og kan være NULL
# Række "user_id" er en integer-række, der bruges til at gemme brugerens id, med en NOT NULL-begrænsning
        cursor.execute('''CREATE TABLE IF NOT EXISTS tidsændringer (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    Date TEXT NOT NULL,
                    Start TEXT NOT NULL,
                    End TEXT NOT NULL,
                    Pause_Start TEXT,
                    Pause_End TEXT,
                    user_id INTEGER NOT NULL)''')

        conn.commit()   # Metodekald på connection-objektet(conn). Dette gemmer ændringerne foretaget i databasen, permanent
init_db()               # Funktion init_db kaldes for at initialisere SQLite-databasen og oprette tabellerne - den lukker hele databasen 

# Linje 73 definere funktionen get_work_hours() og tager to parametre, period og user_id. Funktionen bruges til at hente arbejdstider fra databasen baseret på perioden og brugerens id
# Funktionen bruges til at returnere resultaterne (altså arbejdstimerne) for den bruger der er logget ind
def get_work_hours(period, user_id):
    query = "SELECT * FROM arbejdstider WHERE user_id = ? AND Date >= ? AND Date <= ?"  # query = variabel, der indeholder en SQL-forespørgsel/statement. SELECT * FROM arbejdstider = vælg alle rækker fra arbejdstider-tabellen der matcher det unikke user_id 
    today = datetime.today().date()                              # today = variabel, der indeholder dagens dato - udfra: datetime = klasse fra datetime-modul, today() = metodekald på datetime-klasse, date() = metodekald på today-objektet
    
    if period == 'day':                                          # Begyngelsen på betinget if/elif/else-statement, der tjekker om 'period' er lig med 'day'
        start_date = today                                       # start_date = variabel, der indeholder today-objektet
        end_date = today                                         # end_date = variabel, der indeholder today-objektet
    elif period == 'week':                                       # elif = else if, betinget if/elif/else-statement, der tjekker om 'period' er lig med 'week'
        start_date = today - timedelta(days=today.weekday())     # 
        end_date = start_date + timedelta(days=6)                #
    elif period == 'month':                                      #
        start_date = today.replace(day=1)                        #
        if start_date.month == 12:                               #
            end_date = start_date.replace(day=31)                #
        else:                                                    #
            end_date = (start_date.replace(month=start_date.month+1, day=1) - timedelta(days=1))
    else:
        return []                                                #
    
    with sqlite3.connect('arbejdstider.db') as conn:             # Databasen "arbejdstider.db" forbindes og gemmes i variablen conn. with = statement, sqlite3 = modul, connect() = funktion, 'arbejdstider.db' = ARGUEMENT/PARAMETRE?, conn = variabel/"connection"-objekt
        cursor = conn.cursor()                                   # Metodekald cursor() på connection-objektet(conn). Dette returnerer et cursor-objekt, som bruges til at udføre SQL-forespørgsler
        cursor.execute(query, (user_id, start_date, end_date))   ###USIKKER### Metodekald execute() på cursor-objektet, og tager en SQL-forespørgsel med 4 argumenter = en liste af tuples med værdier til placeholders i SQL-forespørgslen = hent data udfra user_id, start_date og end_date (ét parameter og to værdier eller tre parametre?)
        result = cursor.fetchall()                               ###USIKKER### Metodekald fetchall() på cursor-objektet. Dette returnerer en liste af tuples, der indeholder resultaterne af SQL-forespørgslen


    for i in range(len(result)):                                 ###USIKKER### For-løkke, der itererer over alle rækkerne i result objektet. Python Tuple len() = returnere antallet af elementer i et objekt (3 rækker i tabellen i dette tilfælde, user_id, start_date og end_date). range() = returnere en sekvens af tal, der starter fra 0 og slutter ved antallet af rækker i tabellen minus 1 = (0, 1, 2) = 3 rækker. Dette er med til at øge søgefunktionen i databasen
        date_part = result[i][1].split(" ")[0]                   # I for-løkken for hver række, der udtrækkes dato-delen af nr. 2 række (index 1) i result-objektet og gemmer den i variablen date_part. result[i] = skaber adgang til rækkerne. [1] = vælger nr.2 (index 1) element (date) fra listen af tuples,  split() = metode, der opdeler en streng i en liste med et mellemrum, og derfor opdeles datoen og klokkeslættet i to dele. [0] = returnere den første del af listen, som er datoen
        date = datetime.strptime(date_part, "%Y-%m-%d").date()   # 
        result[i] = list(result[i])                              #
        result[i][1] = date.strftime("%d-%m-%Y")                 #

    return result                                                # returnere resultatet af SQL-forespørgslen
    
def create_user(username, password):                   # Definere funktionen create_user() og tager to parametre, username og password. Funktionen bruges til at oprette en ny bruger i databasen samt hash adgangskoden
    hashed_password = generate_password_hash(password, method='pbkdf2:sha256')  # hashed_password = variabel, der indeholder en hash-værdi af adgangskoden, genereret ved metodekald på generate_password_hash() med to parametre, password og method='pbkdf2:sha256'. 'pbkdf2' = Password-Based Key Derivation Function 2, 'sha256' = Secure Hash Algorithm 256-bit (32-byte) - en kryptografisk hash-funktion
    with sqlite3.connect('database1.db') as conn:      # Databasen "database1.db" forbindes og gemmes i variablen conn. with = statement, sqlite3 = modul, connect() = funktion, 'database1.db' = ARGUEMENT/PARAMETRE?, conn = variabel/"connection"-objekt
        cursor = conn.cursor()                         # Metodekald cursor() på connection-objektet(conn). Dette returnerer et cursor-objekt, som bruges til at udføre SQL-forespørgsler
        try:                                           # try = statement, der bruges til at håndtere undtagelser/fejl, der kan opstå under kørslen af programmet
            cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, hashed_password)) # Metodekald execute() på cursor-objektet, og tager en SQL-forespørgsel med to parametre = en liste af tuples med værdier til placeholders i SQL-forespørgslen = indsæt ny række data i tabellen users, specifikt username og hashed_password kolonnen. '?' = placeholders for udskiftning af parametre og en sikkerhedsmekanisme for at forhindre SQL-injektioner
            conn.commit()                              # Metodekald commit() på connection-objektet(conn). Dette gemmer ændringerne foretaget i databasen, permanent
            print('User created successfully')         # print = funktion, der udskriver en besked til konsollen
        except sqlite3.IntegrityError:                 # except = statement, der bruges til at håndtere undtagelser/fejl, der kan opstå under kørslen af programmet
            print('Username already exists')           # print = funktion, der udskriver en besked til konsollen

@login_manager.user_loader                             # @login_manager.user_loader = decorator = bruges til routing og fortæller Flask, at funktionen load_user() skal kaldes, når en bruger er logget ind
def load_user(user_id):                                # Definere funktionen load_use() og tager et parameter, user_id. Funktionen bruges til at hente brugeren fra databasen baseret på brugerens id
    with sqlite3.connect('database1.db') as conn:      # Databasen "database1.db" forbindes og gemmes i variablen conn. with = statement, sqlite3 = modul, connect() = funktion, 'database1.db' = ARGUEMENT/PARAMETRE?, conn = variabel/"connection"-objekt
        cursor = conn.cursor()                         # Metodekald cursor() på connection-objektet(conn). Dette returnerer et cursor-objekt, som bruges til at udføre SQL-forespørgsler
        cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,)) # Metodekald execute() på cursor-objektet. Ufører en SQL-query, der vælger alle rækker fra "users"-tabellen, hvor id = user_id. '?' = placeholders for udskiftning af parametre og en sikkerhedsmekanisme for at forhindre SQL-injektioner
        user = cursor.fetchone()                       # "hent 1" række fra databasen, der matcher user_id og gemmer den i variablen user
        if user:                                       # if statement = betinget statement, der tjekker om user-objektet er sandt
            return User(id=user[0], username=user[1], password=user[2]) # returnere en ny instans af User-klassen med tre parametre, id, username og password
        return None                                    # returnere None, hvis user-objektet er falsk


class User(UserMixin):                          # Oprettelse af klasse: User-klassen, der nedarver fra UserMixin-klassen fra flask_login modulet. UserMixin-klassen har en contructor metode __init__(), der tager 3 parametre; id, username og password
    def __init__(self, id, username, password): # Definere en constructor metode __init__(), der tager 4 parametre; id, username og password + ("self = parameter, der refererer til instansen af klassen). __init__ bliver automatisk kaldt når en ny instans af klassen bliver oprettet, metoden initialiserer det nye objekt
        self.id = id                            # (alle har et is, username og password) og self = objekt. seld.id = instansattribut, id = parameter 
        self.username = username                # self.username = instansattribut, username = parameter
        self.password = password                # self.password = instansattribut, password = parameter


class LoginForm(FlaskForm):         # Oprettelse af klasse: LoginForm-klassen, der nedarver fra FlaskForm-klassen fra flask_wtf modulet
    username = StringField(validators=[InputRequired(), Length(min=3, max=20)], render_kw={"placeholder": "Username"})   # 
    password = PasswordField(validators=[InputRequired(), Length(min=3, max=20)], render_kw={"placeholder": "Password"}) #
    submit = SubmitField("Login")   # 


def ændre_tid(id):                                           # Definere funktionen ændre_tid() og tager ét parameter, id. Denne funktion mulligør ændringer i arbejdstiderne
    with sqlite3.connect("arbejdstider.db") as connection:   # Databasen "arbejdstider.db" forbindes og gemmes i variablen connection. with = statement, sqlite3 = modul, connect() = funktion, 'arbejdstider.db' = ARGUEMENT/PARAMETRE?, connection = variabel/"connection"-objekt
        cursor = connection.cursor()                         # Metodekald cursor() på connection-objektet(connection). Dette returnerer et cursor-objekt, som bruges til at udføre SQL-forespørgsler
        cursor.execute("DELETE FROM tidsændringer WHERE id = ?", (id,)) # Metodekald execute() på cursor-objektet. Ufører en SQL-query, der sletter alle rækker fra "tidsændringer"-tabellen, hvor id = id. '?' = placeholders for udskiftning af parametre og en sikkerhedsmekanisme for at forhindre SQL-injektioner
        connection.commit()                                  # Metodekald commit() på connection-objektet(connection). Dette gemmer ændringerne foretaget i databasen, permanent

@app.route('/', methods=['GET', 'POST'])  # @app.route('/') = decorator = bruges til routing, fortæller Flask hvilken URL der skal udløse funktionen. methods=['GET', 'POST'] = liste af metoder, der er tilladt for denne route (GET = hente data, POST = sende data) 
def index():                              # Definere funktionen index(). Denne funktion bruges til at returnere index.html-siden
    return render_template('index.html')  # returnere index.html-siden, der vises i browseren. render_template() = funktion, der bruges til at aflæse html-filer - nedarvet fra Flask-klassen

@app.route('/login', methods=['GET', 'POST'])         # @app.route('/login') = decorator = bruges til routing, fortæller Flask hvilken URL der skal udløse funktionen i dette tilfælde "/login". tillader både GET og POST
def login():                                          # Definere funktionen login(). Denne funktion bruges til at returnere login.html-siden
    form = LoginForm()                                # form = variabel, der indeholder en instans af LoginForm-klassen. LoginForm() = ?????????????
    if form.validate_on_submit():                     # if statement = betinget statement, der tjekker om form-objektet er validt og opfylder inputkravene, sikre at username og password er udfyldt og har en længde på mellem 3 og 20 tegn
        with sqlite3.connect('database1.db') as conn: # with = statement, sqlite3 = modul, connect() = funktion, 'database1.db' = argument, conn = variabel/"connection"-objekt
            cursor = conn.cursor()                    # Metodekald cursor() på connection-objektet(conn). Dette returnerer et cursor-objekt, som bruges til at udføre SQL-forespørgsler
            cursor.execute('SELECT * FROM users WHERE username = ?', (form.username.data,)) # Metodekald execute() på cursor-objektet. Ufører en SQL-query, der vælger alle rækker fra "users"-tabellen, hvor username = form.username.data. (form = instans, username = attribut af LoginForm-klassen, data = metodekald på username-attributten, , = tuple, ? = placeholder)
            user = cursor.fetchone()                                                        # Metodekald fetchone() på cursor-objektet. Dette returnerer den første række i resultatet af SQL-forespørgslen
            if user and check_password_hash(user[2], form.password.data):                   ###SKAL UDDYBES### if statement = betinget statement, der tjekker om user-objektet er sandt og om adgangskoden er korrekt
                login_user(User(id=user[0], username=user[1], password=user[2]))            #
                return redirect(url_for('dashboard'))                                       # Succesfuld login = omdirigerer brugeren til dashboard-siden
            else:                                                                           # else = statement, der udføres hvis if statementet er falsk
                flash('Invalid username or password', 'danger')                             # flash = funktion, der viser en besked til brugeren, 'danger' = en bootstrap klasse, der bruges til at vise en rød besked
    return render_template('login.html', form=form)                                         # returnere login.html-siden, der vises i browseren. render_template() = funktion, der bruges til at aflæse html-filer - nedarvet fra Flask-klassen


from datetime import date as Date                     # fra datetime modulet importeres date-klassen som Date

@app.route('/dashboard', methods=["GET", "POST"])     # @app.route('/dashboard') = decorator = bruges til routing, fortæller Flask hvilken URL der skal udløse funktionen, methods=['GET', 'POST'] = liste af metoder, der er tilladt for denne route
@login_required                                       # login_required = decorator = bruges til at sikre, at brugeren er logget ind, før de kan få adgang til dashboard-siden
def dashboard():                                      # Definere funktionen dashboard(). Denne funktion bruges til at returnere dashboard.html-siden
    if request.method == "POST":                      # if statement = betinget statement, der tjekker om request-objektet er en POST-request
        date = request.form.get("date")               ###USIKKER### date = variabel, der indeholder værdien af "date"-attributten fra form, der er sendt med POST-requesten

        start = request.form.get("start")             # start = variabel, der indeholder værdien af "start"-attributten fra form, der er sendt med POST-requesten
        end = request.form.get("end")                 # end = variabel, der indeholder værdien af "end"-attributten fra form, der er sendt med POST-requesten
        pause_start = request.form.get("pause_start") # pause_start = variabel, der indeholder værdien af "pause_start"-attributten fra form, der er sendt med POST-requesten
        pause_end = request.form.get("pause_end")     # pause_end = variabel, der indeholder værdien af "pause_end"-attributten fra form, der er sendt med POST-requesten

        data = [date, start, end, pause_start, pause_end]    # data = variabel, der indeholder en liste af variablerne; date, start, end, pause_start og pause_end

        if not all(data[:3]):                                # if statement = betinget, tjekker de første tre elementer i data-listen, er sande
            flash("All fields for work hours are required", "danger") # VED IKKE
        else:                                                         # else = statement, der udføres hvis if statementet er falsk
            with sqlite3.connect('arbejdstider.db') as conn:          # Databasen "arbejdstider.db" forbindes og gemmes i variablen conn. with = statement, sqlite3 = modul, connect() = funktion, 'arbejdstider.db' = ARGUEMENT/PARAMETRE?, conn = variabel/"connection"-objekt
                cursor = conn.cursor()                                # Metodekald cursor() på connection-objektet(conn). Dette returnerer et cursor-objekt, som bruges til at udføre SQL-forespørgsler

###USIKKER### Metodekald execute() på cursor-objektet. VED IKKE HVAD DENNE SQL-FORESPOERGSEL GØR
                cursor.execute('''
                    INSERT INTO tidsændringer (Date, Start, End, Pause_start, Pause_end, user_id)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (*data, current_user.id))     # (*data, current_user.id) = *data = pakker data-listen ud, så hvert element i listen bliver et argument til execute() metoden. current_user.id = brugerens id, der er logget ind
                conn.commit()                      
            flash("Record added", "success")       # 
        return redirect(url_for("dashboard"))      # Omidirigerer brugeren til dashboard-siden (redirect og url_for = Flask funktioner)

    arbejdstider_data = get_work_hours('day', current_user.id)      # arbejdstider_data = variabel, der indeholder resultatet af get_work_hours() funktionen, der henter arbejdstider for den bruger, der er logget ind
    return render_template("dashboard.html", arbejdstider_data=arbejdstider_data, today=Date.today()) ###USIKKER### returnere dashboard.html-siden, der vises i browseren. render_template() = funktion, today=Date.today() = dagens dato fra datetime modulet,  today(datetime.today().date())  

@app.route("/delete/<entry_id>", methods=["POST"]) # 
@login_required                            #
def db_delete(entry_id):                   #
    ændre_tid(entry_id)                    #
    flash("Record removed", "danger")      #
    return redirect(url_for("dashboard"))  #

@app.route('/logout')                      #
@login_required                            #
def logout():                              #
    logout_user()                          #
    return redirect(url_for('index'))      #

@app.route('/Skema/<user>')           #
@login_required                       #     
def skema(user):                      #
    if user != current_user.username: #
        flash("You do not have permission to view this page.", "danger") #
        return redirect(url_for("dashboard"))                            #


    with sqlite3.connect('arbejdstider.db') as conn: #
        cursor = conn.cursor()                       #
        cursor.execute("SELECT * FROM tidsændringer WHERE user_id = ?", (current_user.id,)) #
        tidsændringer_list = cursor.fetchall()       #

    return render_template("skema.html", tidsændringer_list=tidsændringer_list) #

@app.route('/arbejdstider/<int:user_id>')   #
@login_required                             #
def arbejdstider(user_id):                  #

    today = datetime.today().date()         #
    today_str = today.strftime("%d-%m-%Y")  #

    start_of_week = today - timedelta(days=today.weekday()) #
    end_of_week = start_of_week + timedelta(days=6)         #

    daily_hours = get_work_hours('day', user_id)     #
    weekly_hours = get_work_hours('week', user_id)   #
    monthly_hours = get_work_hours('month', user_id) #
#
    daily_hours_today = [entry for entry in daily_hours if entry[1] == today_str] 
#
    weekly_hours_this_week = [entry for entry in weekly_hours if start_of_week <= datetime.strptime(entry[1], "%d-%m-%Y").date() <= end_of_week] 
#
    return render_template('work_hours.html', daily_hours=daily_hours_today, weekly_hours=weekly_hours_this_week, monthly_hours=monthly_hours)   

if __name__ == "__main__":               # 
    app.run(host="0.0.0.0", debug=True)  #

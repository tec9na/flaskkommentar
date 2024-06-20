import sqlite3
from werkzeug.security import generate_password_hash
# import sqlite3 module
# import generate_password_hash function from werkzeug.security module

def create_user(username, password):                   # Definere en funktion create_user med to parametre username og password
    hashed_password = generate_password_hash(password, method='pbkdf2:sha256') # hashed_password = variabel, der indeholder en hash-værdi af adgangskoden, genereret ved metodekald på generate_password_hash() med to parametre, password og method='pbkdf2:sha256'. 'pbkdf2' = Password-Based Key Derivation Function 2, 'sha256' = Secure Hash Algorithm 256-bit (32-byte) - en kryptografisk hash-funktion
    with sqlite3.connect('database1.db') as conn:      # (curser er den metode der gør at databasen og applikationen snakker sammen) Metodekald cursor() på connection-objektet(conn). Dette returnerer et cursor-objekt, som bruges til at udføre SQL-forespørgsler
        cursor = conn.cursor()                         # Metodekald cursor() på connection-objektet(conn). Dette returnerer et cursor-objekt, som bruges til at udføre SQL-forespørgsler
        try:                                           # try blok med en except blok, bruges til at tilføje nye brugere til databasen med unikke brugernavne
            cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, hashed_password)) # Metodekald execute() på cursor-objektet med to parametre, en SQL-forespørgsel og en tuple med to elementer, username og hashed_password. SQL-forspørgslen er en INSERT INTO-sætning, der indsætter en ny række i tabellen users med værdierne, username og hashed_password
            conn.commit()                       # Metodekald commit() på connection-objektet(conn). Dette gemmer ændringerne i databasen
            print('User created successfully')  # print() funktionen udskriver en besked, hvis brugeren er blevet oprettet og try blokken er blevet gennemført
        except sqlite3.IntegrityError:          # except blok, der fanger en IntegrityError, hvis brugernavnet allerede findes i databasen
            print('Username already exists')

create_user('Nina', '123')                      # Funktionen kaldes; create_user() med to argumenter, 'Nina' og '123'. Dette opretter en ny bruger med brugernavnet 'Nina' og adgangskoden '123'

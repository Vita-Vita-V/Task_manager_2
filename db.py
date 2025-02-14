import mysql.connector
from mysql.connector import Error

def pripojeni_db():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='task_manager',
            user='root',
            password='Vitaoros05'
        )
        if connection.is_connected():
            print("Připojeno k databázi")
            return connection
    except Error as e:
        print(f"Chyba při připojování k databázi: {e}")
        return None

def vytvoreni_tabulky(connection):
    cursor = connection.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS ukoly (
        id INT AUTO_INCREMENT PRIMARY KEY,
        nazev VARCHAR(255) NOT NULL,
        popis TEXT NOT NULL,
        stav ENUM('nezahájeno', 'probíhá', 'hotovo') DEFAULT 'nezahájeno',
        datum_vytvoreni TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)
    connection.commit()
    print("Tabulka 'ukoly' byla vytvořena nebo již existuje.")

def hlavni_menu():
    print("\n--- Hlavní menu ---")
    print("1. Přidat úkol")
    print("2. Zobrazit úkoly")
    print("3. Aktualizovat úkol")
    print("4. Odstranit úkol")
    print("5. Ukončit program")
    volba = input("Vyberte možnost: ")
    return volba

def pridat_ukol(connection):
    nazev = input("Zadejte název úkolu: ")
    popis = input("Zadejte popis úkolu: ")

    if not nazev or not popis:
        print("Název a popis úkolu jsou povinné!")
        return
    
    cursor = connection.cursor()
    cursor.execute("""
    INSERT INTO ukoly (nazev, popis)
    VALUES (%s, %s);
    """, (nazev, popis))
    connection.commit()
    print("Úkol byl úspěšně přidán.")

def zobrazit_ukoly(connection):
    cursor = connection.cursor()
    cursor.execute("""
    SELECT id, nazev, popis, stav FROM ukoly
    WHERE stav IN ('nezahájeno', 'probíhá');
    """)
    ukoly = cursor.fetchall()

    if ukoly:
        for ukol in ukoly:
            print(f"ID: {ukol[0]}, Název: {ukol[1]}, Popis: {ukol[2]}, Stav: {ukol[3]}")
    else:
        print("Seznam úkolů je prázdný.")

def aktualizovat_ukol(connection):
    zobrazit_ukoly(connection)
    id_ukolu = input("Zadejte ID úkolu, který chcete aktualizovat: ")

    cursor = connection.cursor()
    cursor.execute("""
    SELECT * FROM ukoly WHERE id = %s;
    """, (id_ukolu,))
    ukol = cursor.fetchone()

    if not ukol:
        print("Úkol s tímto ID neexistuje.")
        return

    novy_stav = input("Zadejte nový stav (probíhá/hotovo): ")
    if novy_stav not in ['probíhá', 'hotovo']:
        print("Neplatný stav.")
        return

    cursor.execute("""
    UPDATE ukoly SET stav = %s WHERE id = %s;
    """, (novy_stav, id_ukolu))
    connection.commit()
    print("Úkol byl úspěšně aktualizován.")

def odstranit_ukol(connection):
    zobrazit_ukoly(connection)
    id_ukolu = input("Zadejte ID úkolu, který chcete odstranit: ")

    cursor = connection.cursor()
    cursor.execute("""
    SELECT * FROM ukoly WHERE id = %s;
    """, (id_ukolu,))
    ukol = cursor.fetchone()

    if not ukol:
        print("Úkol s tímto ID neexistuje.")
        return

    potvrdit = input("Opravu chcete tento úkol odstranit? (ano/ne): ")
    if potvrdit.lower() == 'ano':
        cursor.execute("""
        DELETE FROM ukoly WHERE id = %s;
        """, (id_ukolu,))
        connection.commit()
        print("Úkol byl úspěšně odstraněn.")
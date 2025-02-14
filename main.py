from db import pripojeni_db, vytvoreni_tabulky, hlavni_menu, pridat_ukol, zobrazit_ukoly, aktualizovat_ukol, odstranit_ukol

def main():
    connection = pripojeni_db()
    if connection is None:
        return

    vytvoreni_tabulky(connection)

    while True:
        volba = hlavni_menu()
        
        if volba == '1':
            pridat_ukol(connection)
        elif volba == '2':
            zobrazit_ukoly(connection)
        elif volba == '3':
            aktualizovat_ukol(connection)
        elif volba == '4':
            odstranit_ukol(connection)
        elif volba == '5':
            break
        else:
            print("Neplatná volba. Zkuste to znovu.")

if __name__ == "__main__":
    main()
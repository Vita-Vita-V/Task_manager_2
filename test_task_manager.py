import pytest
from db import pripojeni_db, pridat_ukol, aktualizovat_ukol, odstranit_ukol

@pytest.fixture
def db_connection():
    connection = pripojeni_db()
    yield connection
    connection.close()

def test_pridat_ukol(db_connection):
    
    pridat_ukol(db_connection)
    cursor = db_connection.cursor()
    cursor.execute("SELECT * FROM ukoly WHERE nazev = 'Test Úkol';")
    result = cursor.fetchone()
    assert result is not None

    
    pridat_ukol(db_connection)
    cursor.execute("SELECT * FROM ukoly WHERE nazev = '';")
    result = cursor.fetchone()
    assert result is None
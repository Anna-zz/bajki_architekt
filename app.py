import streamlit as st
import sqlite3
import os
import uuid
import requests
from dotenv import load_dotenv
from openai import OpenAI

# 1. Ładujemy .env (zadziała lokalnie w VS Code)
load_dotenv()

# 2. Sidebar dla użytkownika
with st.sidebar:
    st.title("🔑 Konfiguracja API")
    user_key = st.text_input("Wpisz swój OpenAI API Key (opcjonalnie):", type="password")

# 3. UNIWERSALNE POBIERANIE KLUCZA (Kluczowy moment!)
def get_api_key(name):
    # Jeśli szukamy klucza OpenAI, bierzemy TYLKO to co wpisał użytkownik
    if name == "OPENAI_API_KEY":
        return user_key if user_key != "" else None
    
    # Dla reszty (Qdrant) zostawiamy starą logikę
    try:
        if name in st.secrets: return st.secrets[name]
    except: pass
    return os.getenv(name)

# 4. PRZYPISANIE KLUCZY (zadziała i tu, i tam)
openai_key = get_api_key("OPENAI_API_KEY")
QDRANT_URL = get_api_key("QDRANT_URL")
QDRANT_API_KEY = get_api_key("QDRANT_API_KEY")
COLLECTION_NAME = "bajki"  # <-- Przenieś to tutaj (nad if not openai_key)

# Ciche zatrzymanie, jeśli brak klucza
if not openai_key:
    st.stop()

# Sprawdzenie czy mamy klucz OpenAI przed startem
if not openai_key:
    st.error("❌ Brak klucza OpenAI API! Wpisz go w panelu bocznym lub dodaj do .env")
    st.stop()

client = OpenAI(api_key=openai_key)
def inicjalizuj_baze():
    """Tworzy lokalną bazę danych SQLite."""
    conn = sqlite3.connect('bajki_dzieci.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS historie (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            imie_dziecka TEXT,
            bohater TEXT,
            tresc_bajki TEXT,
            url_obrazka TEXT
        )
    ''')
    conn.commit()
    conn.close()

def generuj_bajke(imie, bohater, moral):
    """Generuje bajkę przez GPT-4o."""
    prompt = f"Napisz magiczną bajkę dla dziecka o imieniu {imie}. Bohater: {bohater}. Morał: {moral}."
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "Jesteś ciepłym opowiadaczem bajek dla dzieci."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content

def zapisz_bajke(imie, bohater, tresc):
    """Zapisuje do SQLite oraz wysyła do Qdrant przez API (HTTP)."""
    # 1. Zapis do SQLite
    conn = sqlite3.connect('bajki_dzieci.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO historie (imie_dziecka, bohater, tresc_bajki) VALUES (?, ?, ?)', 
                   (imie, bohater, tresc))
    conn.commit()
    conn.close()

    # 2. Tworzenie wektora (embedding)
    emb = client.embeddings.create(input=tresc, model="text-embedding-3-small")
    wektor = emb.data[0].embedding

    # 3. Wysłanie do Qdrant przez requests (bezpośrednio przez API)
    url = f"{QDRANT_URL}/collections/{COLLECTION_NAME}/points?wait=true"
    headers = {
        "api-key": QDRANT_API_KEY,
        "Content-Type": "application/json"
    }
    data = {
        "points": [
            {
                "id": str(uuid.uuid4()),
                "vector": wektor,
                "payload": {"imie": imie, "bohater": bohater, "tresc": tresc}
            }
        ]
    }
    
    # Wysyłamy dane - to na pewno nie zostanie zablokowane przez DLL
    requests.put(url, json=data, headers=headers)

# --- INTERFEJS STREAMLIT ---
st.title("🧙‍♂️ Generator Bajek dla Dzieci")

inicjalizuj_baze()

imie_dz = st.text_input("Imię dziecka:", "Kacper")
postac = st.text_input("Główny bohater:", "Złoty Smok")
temat = st.text_area("O czym ma być bajka? (morał):", "dlaczego warto dzielić się zabawkami")

if st.button("Wygeneruj i zapisz bajkę ✨"):
    try:
        with st.spinner('Piszę bajkę...'):
            wynik_bajki = generuj_bajke(imie_dz, postac, temat)

            st.subheader(f"Oto bajka dla {imie_dz}:")
            st.write(wynik_bajki)
            
            zapisz_bajke(imie_dz, postac, wynik_bajki)
            st.success("✅ Bajka wygenerowana i zapisana!")
            
    except Exception as e:
        st.error(f"❌ Wystąpił błąd: {e}")



        





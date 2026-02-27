import streamlit as st
import sqlite3
import os
import uuid
import requests  # Zamiast qdrant-client, używamy standardowego requests
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv() 
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Dane z .env
q_client = QdrantClient(
    url=st.secrets["QDRANT_URL"],
    api_key=st.secrets["QDRANT_API_KEY"],
    prefer_grpc=False
)

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
        


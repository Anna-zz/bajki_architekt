# 🧙‍♂️ Generator Bajek dla Dzieci (AI & Vector Search)

* **Problem:** Rodzice często chcą opowiadać dzieciom spersonalizowane bajki (np. z dzieckiem jako głównym bohaterem), ale brakuje im kreatywności lub czasu na wymyślanie nowych historii co wieczór.
* **Rozwiązanie:** Aplikacja, która na podstawie kilku tagów (np. imię dziecka, ulubione zwierzę, morał: "warto pomagać innym") generuje krótką, ciekawą bajkę.

Aplikacja wykorzystująca model GPT-4o do tworzenia spersonalizowanych bajek z zapisem wektorowym w chmurze.

## 🚀 Kluczowe cechy i zmiany (Integracja z Qdrant):
W procesie rozwoju aplikacji wprowadzono kluczowe poprawki stabilności i bezpieczeństwa:
* **Bezpieczeństwo (Secrets):** Przejście z `.env` na `st.secrets` dla bezpiecznego wdrożenia na [Streamlit Cloud](https://share.streamlit.io).
* **Stabilność (Requests):** Zastąpienie biblioteki `qdrant-client` bezpośrednimi żądaniami HTTP (`requests`), co wyeliminowało błędy DLL/gRPC na Windows.
* **Baza Wektorowa:** Skonfigurowano kolekcję `bajki` w [Qdrant Cloud](https://qdrant.tech) (wymiar 1536, dystans Cosine) pod model `text-embedding-3-small`.
* **Automatyzacja:** Dodano plik `requirements.txt` oraz `.gitignore`, co pozwala na natychmiastowe udostępnienie projektu na GitHub.

## 🛠️ Instalacja i konfiguracja lokalna:
1. Sklonuj repozytorium: `git clone [link-do-twojego-repo]`
2. Zainstaluj wymagane biblioteki: `pip install -r requirements.txt`
3. Stwórz plik `.env` i dodaj swoje klucze:
   ```env
   OPENAI_API_KEY=twoj-klucz
   QDRANT_URL=twoj-url
   QDRANT_API_KEY=twoj-klucz-api

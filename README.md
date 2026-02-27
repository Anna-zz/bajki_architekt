# 🧙‍♂️ Generator Bajek dla Dzieci (AI & Vector Search)

* **Problem:** Rodzice często chcą opowiadać dzieciom spersonalizowane bajki (np. z dzieckiem jako głównym bohaterem), ale brakuje im kreatywności lub czasu na wymyślanie nowych historii co wieczór.
* **Rozwiązanie:** Aplikacja, która na podstawie kilku tagów (np. imię dziecka, ulubione zwierzę, morał: "warto pomagać innym") generuje krótką, ciekawą bajkę.

## 🚀 Kluczowe cechy i zmiany (Integracja z Qdrant & UX):
W procesie rozwoju aplikacji wprowadzono poprawki stabilności, bezpieczeństwa oraz elastyczności:
* **Bezpieczeństwo i Elastyczność (Secrets & Sidebar):** Wdrożono hybrydowe zarządzanie kluczami. Aplikacja bezpiecznie korzysta ze **Streamlit Secrets** w chmurze, jednocześnie umożliwiając użytkownikowi wpisanie własnego klucza OpenAI w panelu bocznym (**Sidebar**).
* **Stabilność (Requests):** Zastąpienie biblioteki `qdrant-client` bezpośrednimi żądaniami HTTP (`requests`), co wyeliminowało błędy DLL/gRPC na Windows i zapewniło niezawodność w chmurze.
* **Baza Wektorowa:** Pełna integracja z [Qdrant Cloud](https://qdrant.tech) (wymiar 1536, dystans Cosine) dla modelu `text-embedding-3-small`.
* **Automatyzacja:** Projekt zawiera kompletny plik `requirements.txt` oraz `.gitignore`, co gwarantuje czyste i bezpieczne udostępnianie na GitHubie.

## 🛠️ Instalacja i konfiguracja lokalna:
1. Sklonuj repozytorium: `git clone [link-do-twojego-repo]`
2. Zainstaluj biblioteki: `pip install -r requirements.txt`
3. **Uruchomienie:** 
   * Możesz stworzyć plik `.env` z kluczami `OPENAI_API_KEY`, `QDRANT_URL`, `QDRANT_API_KEY`.
   * **LUB** po prostu uruchom aplikację komendą `streamlit run app.py` i wpisz swój klucz OpenAI bezpośrednio w interfejsie aplikacji.QDRANT_API_KEY=twoj-klucz-api

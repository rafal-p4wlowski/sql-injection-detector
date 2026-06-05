# Wykrywanie ataków typu SQL Injection w zapytaniach sieciowych (NLP)

Projekt wykorzystanie technik Uczenia Maszynowego (Przetwarzanie Języka Naturalnego - NLP) do wykrywania złośliwych zapytań i prób ataków typu SQL Injection w formularzach internetowych.

Projekt składa się z trzech głównych elementów:
1. **Model Uczenia Maszynowego** (skrypt w Pythonie analizujący i uczący się wzorców ataków).
2. **Serwer API (Backend)** (aplikacja we Flasku, która w czasie rzeczywistym sprawdza zapytania).
3. **Aplikacja kliencka (Frontend)** (prosta strona z formularzem logowania w React).

---

## Wymagania wstępne
Aby uruchomić projekt na swoim komputerze, potrzebujesz:
- **Python** (w wersji 3.x)
- **Node.js** oraz **npm** (do uruchomienia aplikacji webowej)

---

## Struktura projektu
- `train.py` - skrypt sztucznej inteligencji. Wczytuje dane z plików CSV i trenuje model.
- `app.py` - główny serwer komunikacyjny. Odbiera dane logowania, weryfikuje je przez model AI i decyduje, czy przepuścić użytkownika.
- `sqli_rf_model.joblib` oraz `tfidf_vectorizer.joblib` - gotowe, nauczone już modele weryfikujące. Dzięki nim nie trzeba czekać na uczenie się algorytmu od zera.
- `frontend/` - folder zawierający wygląd strony i kod formularza.

---

## Jak uruchomić projekt?

Uruchomienie projektu ogranicza się do włączenia serwera w Pythonie oraz strony w React. 
Wykonaj poniższe kroki w dwóch osobnych oknach terminala.

### Krok 1: Uruchomienie serwera (Backend)
Otwórz terminal w głównym folderze projektu (tam gdzie znajduje się plik `app.py`) i wpisz komendę:
```bash
python app.py
```
Serwer uruchomi się i będzie nasłuchiwać na porcie `5000`. Powinien pojawić się komunikat o pomyślnym załadowaniu modelu.

### Krok 2: Uruchomienie strony WWW (Frontend)
Otwórz drugie okno terminala, przejdź do folderu `frontend`, zainstaluj pakiety (tylko za pierwszym razem) i uruchom interfejs:
```bash
cd frontend
npm install
npm run dev
```
W konsoli pojawi się lokalny adres strony (zazwyczaj `http://localhost:5173`). Kliknij go lub skopiuj do przeglądarki.

---

## Jak przetestować działanie?

Gdy otworzysz stronę w przeglądarce, zobaczysz Panel Logowania. Wypróbuj następujące scenariusze:

1. **Poprawne logowanie** 
   - Login: `admin`
   - Hasło: `admin`
   - *Efekt:* Zobaczysz zielony komunikat o sukcesie. Model poprawnie uznał słowa za bezpieczne.

2. **Błędne hasło (ale bezpieczny tekst)**
   - Login: `admin`
   - Hasło: `złe_hasło`
   - *Efekt:* Zobaczysz żółty komunikat o błędnych danych. Model przepuścił zapytanie, ale system logowania odmówił dostępu.

3. **Próba ataku SQL Injection!**
   - Login: `' OR 1=1 --`
   - Hasło: `dowolne`
   - *Efekt:* Zobaczysz duży czerwony alert! Model sztucznej inteligencji wykrył w polu loginu niebezpieczne n-gramy znakowe charakterystyczne dla języka SQL i natychmiast zablokował próbę włamania.

# **PROJEKT APLIKACJI BIBLIOTEKI**

## 1. Opis aplikacji

Aplikacja biblioteki to system zarządzania biblioteką, który umożliwia pracę zarówno w trybie bibliotekarza, jak i czytelnika. Każda z wymienionych ról posiada odpowiednie funkcje.

- **Bibliotekarz:**
  - Zarządzanie dostępnymi w bibliotece książkami.
  - Zarządzanie użytkownikami.
  - Wyszukiwanie książek z użyciem filtrów.
  - Przeglądanie statystyk książek i innych użytkowników.

- **Czytelnik:**
  - Wypożyczanie dostępnych książek.
  - Zarządzanie wypożyczeniem.
  - Wyszukiwanie książek z użyciem filtrów.
  - Przeglądanie statystyk książek i innych użytkowników.

## 2. Instrukcja instalacji

Aby aplikacja działała poprawnie, zainstaluj wymagane biblioteki, korzystając z pliku requirements.txt. Wykonaj polecenie:

> pip install -r requirements.txt

## 3. Uruchamianie aplikacji

Uruchom aplikację, wykonując polecenie:

> python3 main.py

## 4. Przykładowe dane

Do plików JSON biblioteki zostały dodane przykładowe dane użytkowników i książek, umożliwiające obserwację poprawnego działania wszystkich dostępnych funkcji.

### Logowanie jako bibliotekarz

Aby zalogować się jako bibliotekarz, użyj poniższych danych:

- **ID:** 1879
- **Hasło:** admin123

### Korzystanie jako czytelnik

Aby korzystać z biblioteki jako czytelnik, wystarczy stworzyć konto użytkownika po uruchomieniu aplikacji.

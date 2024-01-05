# **PROJEKT APLIKACJI BIBLIOTEKI**

### Dane autora

- Imię i nazwisko: Kacper Siemionek
- Numer albumu: 331430

## **1. Cel i opis projektu**

Celem projektu jest zaimplementowanie aplikacji biblioteki umożliwiającej efektywne zarządzanie księgozbiorem oraz kontami użytkowników i bibliotekarzy. Aplikacja dostarcza interfejsu dla użytkowników, którzy mogą przeglądać, wypożyczać, rezerwować książki, sprawdzać statystyki, a także dla bibliotekarzy, którzy zarządzają księgozbiorem, dodając nowe książki, egzemplarze, a także obsługują konta użytkowników.

### Dostępne klasy:

- *Book*:
  Reprezentuje pojedynczy egzemplarz z unikalnym identyfikatorem. Zawiera informacje o tytule, autorze, roku wydania, gatunku, historii, aktualnym posiadaczu, rezerwacjach, itp.

- *User*:
  Przedstawia użytkownika biblioteki z atrybutami dotyczącymi danych osobowych, wypożyczeń, rezerwacji oraz unikalnym identyfikatorem. Pozwala na zarządzanie wypożyczeniami i rezerwacjami.

- *Librarian*:
  Dziedziczy od użytkownika, również posiada imięm, hasło i unikalny identyfikator, ma dostęp do wewnętrznych metod biblioteki, takich jak zarządzanie księgozbiorem i użytkownikami.

- *Library*:
  Klasa biblioteki jest bardzo ważnym elementem, ponieważ zostaje wywoływana przy każdym włączeniu aplikacji oraz przechowuje dane wszysztkich książek i użytkowników, które pobiera z plików JSON. Główne operacje, które umożliwia biblioteka to zarządzanie dostępnymi książkami i użytkownikami, sprawdzanie terminów zwrotu, umożliwienie wyszukania książek z wykorzystaniem filtrów, udostępnianie statystyk, itp.

### Opis działania

Interfejs biblioteki rozpoczyna się od procesu logowania. Na podstawie podanego ID przypisywany jest odpowiedni interfejs zgodnie z wykrytą rolą:

- Użytkownik otrzymuje informacje na temat ewentualnych zaległości w zwrotach oraz dostęp do opcji sprawdzenia i wyszukania dostępnych książek, gdzie następnie może wypożyczyć lub zarezerwować jedną z nich. Ponadto, użytkownik ma możliwość przeglądania informacji dotyczących swoich wypożyczeń, sprawdzania statystyk książek i użytkowników, oraz opcję wylogowania się z systemu.

- Bibliotekarz na początku posiada podobne opcje, jednakże, w przeciwieństwie do użytkownika, ma on dodatkowe metody, umożliwiające mu zarządzanie księgozbiorem i użytkownikami.

## **2. Instrukcja instalacji oraz uruchamianie aplikacji**

Aby aplikacja działała poprawnie, należy zainstalować wymagane biblioteki, korzystając z pliku requirements.txt, wykonując polecenie:

```bash
pip install -r requirements.txt
```

Uruchom aplikację, wykonując polecenie:

```bash
python3 main.py
```

## **3. Przykładowe dane**

Do plików JSON biblioteki zostały dodane przykładowe dane użytkowników i książek, umożliwiające obserwację poprawnego działania wszystkich dostępnych funkcji.

### Logowanie jako bibliotekarz

Aby zalogować się jako bibliotekarz, należy użyć poniższych danych:

- **ID:** 1879
- **Hasło:** admin123

### Korzystanie jako czytelnik

Aby korzystać z biblioteki jako czytelnik, wystarczy stworzyć konto użytkownika po uruchomieniu aplikacji.


## **4. Część refleksyjna**

Praca nad projektem była miejscami wymagająca i stawiała przede mną pewne wyzwania. W niektórych przypadkach zmuszony byłem zrezygnować z pewnych pomysłów z powodu ograniczeń w mojej wiedzy i doświadczeniu. Niemniej jednak, mimo tych trudności, udało się ostatecznie zaimplementować więcej metod, niż zakładałem na samym początku. 

### Przykładowe zmiany funkcjonalności:

- Implementacja interfejsu graficznego została wykonana zgodnie z oczekiwaniami, nie sprawiając problemów podczas korzystania z aplikacji. Niemniej jednak, dodanie GUI mogłoby znacząco poprawić jakość i doświadczenia użytkownika.

- Działania po przekroczeniu terminu zwrotu - w obecnej wersji aplikacji użytkownik otrzymuje jedynie krótką informację o przekroczeniu, bez dodatkowych konsekwencji, co nie zobowiązuje go do zwrotu książek po terminie. Brak systemu opłat czy blokad kont stanowi niedociągnięcie, jednak nie mógł zostać wprowadzony ze względu na ograniczenia czasowe.

- Sugestie użytkowników - warto byłoby rozważyć dodanie funkcji sugestii od użytkowników dla bibliotekarzy, pozwalając czytelnikom proponować nowe książki do dodania. Taka interaktywna opcja mogłaby zwiększyć zaangażowanie społeczności i dostarczyć cennych wskazówek dla personelu biblioteki dotyczących preferencji czytelników.

- Oceny książek - możliwość oceniania i recenzowania książek przez użytkowników może dostarczyć cennych informacji dla innych czytelników.

- Powiadomienia e-mail - dodanie systemu powiadomień e-mailowych, który informuje użytkowników o zbliżającym się terminie zwrotu książki, mogłoby zwiększyć skuteczność przypominania o konieczności zwrotu.

- Rozszerzenie statystyk - dodanie różnorodnych opcji generowania statystyk, np. według gatunku czy autora, stanowiłoby interesujące urozmaicenie funkcjonalności aplikacji.

 Praca nad projektem aplikacji biblioteki była dla mnie doskonałą okazją do rozwoju. Nabyłem nie tylko konkretne umiejętności programistyczne, ale również zdolności związane z efektywnym zarządzaniem projektem i samodzielnym rozwiązywaniem problemów. Co więcej, złożoność sprawiła, że lepiej zrozumiałem i doceniłem testy jednostkowe.
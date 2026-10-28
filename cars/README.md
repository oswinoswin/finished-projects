# cars

## Pliki

- **RAPORT.md** - opis modelu regresji
- **src/scrapper.py** - pobieranie danych o samochodach
- **src/prepare_data.py** - czyszczenie danych
- **src/train_model.py** - trenowanie modelu regresji
- **src/gui/main_page.py** - aplikacja do przewidywania cen

## TODO
### MODEL REGRESJI
- [x] Zebrać dane z jednego serwisu z ofertami samochodów. (excel z linkami jest na Teams)
- [x] Wyciągnąć i oczyścić dane. (im więcej tym lepiej)
- [x] Zbudować model regresji liniowej do szacowania ceny samochodu na podstawie wybranych parametrów.

### RAPORT
- [x] Opis procesu zbierania danych (ile było ogłoszeń, ile się udało zebrać), 
- [x] Zastosowane transformacje zmiennych (podstawowe statystyki deskryptywne, rozkłady zmiennych)
- [x] Historia budowy modelu regresji (+ diagnostyka modelu)
- [x] Końcowy model regresji, który został użyty w aplikacji
  
## GUI zawierające:
- [x] Odpowiednie pola do wprowadzania danych wraz z walidacją tych danych.
- [x] Wyświetlanie ceny samochodu oszacowanej przez model regresji
----
### BONUSOWE
- [ ] Miejsce, gdzie będą wyświetlały się historyczne oszacowania z możliwością ich "wyczyszczenia". (tak aby program pamiętał te wyniki po zresetowaniu, więc należy albo dane zapisywać do csv albo można zrobić prostą bazę sql'a [najlepiej taką, która przy odpaleniu programu będzie sprawdzana istnieje i jak jej program nie znajdzie to będzie nową tworzyć bazę razem z tabelami])
- [ ] animacje
- [x] pełna responsywność (tak, że na telefonie i komputerze aplikacja będzie wyglądać dobrze, niezależnie od wielkości ekranu)
- [ ] wibracje przy klikaniu, 
- [x] tworzenie i zapisywanie logów (kto, jak i kiedy używał tego programu - takie info może być zapisywane w pliku .log lub w sql'u). Użytkownik aplikacji nie powinien tego widzieć.
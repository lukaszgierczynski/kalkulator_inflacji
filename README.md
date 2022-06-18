Program został napisany w wersji 3.10 Python'a.
Program wymaga zainstalowania biblioteki matplotlib (oraz innych bibliotek wymaganych przez tą bibliotekę).
Wymagania dotyczące bibliotek znajdują się w pliku requirements.txt.
Aby włączyć program należy uruchomić w konsoli skrypt 'main.py'.

Głównym celem programu jest umożliwienie użytkownikowi obliczenia "własnej" inflacji na podstawie danych Głównego Urzędu Statystycznego.
Aby wykonać obliczenia użytkownik musi podać wagi swoich wydatków w poszczególnych kategoriach towarów i usług.
Dzięki obliczeniom użytkownik może dowiedzieć się, czy jego "własna" inflacja jest wyższa, czy niższa od inflacji raportowanej przez GUS.
 
Kolejną funkcjonalnością programu jest tworzenie wykresów przedstawiającyh przebieg "własnej" inflacji w ostatnich miesiącach w porównaniu
z przebiegiem inflacji raportowanej przez GUS. Program umożliwia również stworzenie wykresu z przebiegiem inflacji w poszczególnych kategoriach towarów i usług.

Program pozwala także tworzyć wykresy obrazujące spadek realej wartości oszczędności przy założonej inflacji, kwocie oszczędności i czasie oszczędzania.

Do wykonywania obliczeń w programie wykorzystywane są dane Głównego Urzędu Statystycznego zapisane w piku 'dane_inflacja.csv'.

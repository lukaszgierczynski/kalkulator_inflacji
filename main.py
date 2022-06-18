"""Główny skrypt programu umożliwiajacego m.in. obliczenie 'własnej' inflacji na podstawie
danych Głównego Urzędu Statystycznego

Skrypt zawiera klasę MainMenu, która odpowiada za działanie programu w konsoli.
W celu obsługi działania całego programu skrypt importuje z innych modułów trzy klasy, które umożliwiają:
- klasa CalculateInflation - obliczenie 'własnej' inflacji;
- klasa ShowInflationOnGraph - stworzenie wykresu m.in. z dynamiką 'własnej' inflacji;
- klasa ShowSavingsOnGraph - stworzenie wykresu przedstawiająego spadek wartości oszczędności przy określonej inflacji.
"""

import sys
from calculate_inflation import CalculateInflation
from show_inflation_on_graph import ShowInflationOnGraph
from show_savings_on_graph import ShowSavingsOnGraph
from exceptions import UnavailableChoice


class MainMenu:
    """
    Klasa reprezentująca główne menu programu

    Attributes
    ----------
    user_choice : int
        wybór użytkownika z listy możliwych operacji
    available_choices : list
        lista z możliwymi operacjami

    Methods
    ----------
    print_menu()
        wyświetla główne menu programu
    validate_input()
        odczytuje i waliduje wybór użytkownika
    operation()
        zapewnia działanie wybranej przez użytkownika opcji
    """

    def __init__(self):
        """Odpowiada za działanie programu w pętli while"""

        self.user_choice = None
        self.available_choices = [0, 1, 2, 3]

        while True:
            self.print_menu()
            self.validate_input()
            self.operation()

    @staticmethod
    def print_menu():
        """Wyświetla w konsoli główne menu programu"""

        print('-' * 80)
        print()
        print("""Oto lista możliwych operacji wykonywanych przez program:
        0. Zakończ działanie programu,
        1. Oblicz własną inflację na podstawie danych GUS,
        2. Pokaż na wykresie przebieg dynamiki inflacji,
        3. Pokaż na wykresie jak topnieją oszczędności przy danej inflacji""")

    def validate_input(self):
        """Odczytuje wybór użytkownika

        Po zwalidowaniu wartości wprpowadzonej przez użyktownika przypisuje ją do atrybutu 'user_choice'

        Raises
        -------
        ValueError
            Jeśli wprowadzonej przez użytkownika wartości nie można zamienić na liczbę całkowitą
        UnavailableChoice
            Jeśli wprowadzonej przez użytkownika liczby nie ma na liście dostępnch opcji
        """

        print()
        print("Wybierz, co chcesz zrobić.")

        while True:

            user_choice = input("Wpisz odpowiednią cyfrę: ")

            try:
                user_choice = int(user_choice)

                if user_choice not in self.available_choices:
                    raise UnavailableChoice(f"Podana wartość nie jest dostępna. Lista dostępnych wartości to: "
                                            f"{self.available_choices}.")

                self.user_choice = user_choice
                break

            except ValueError:
                print('Wpisana wartość musi być liczbą całkowitą!')

            except UnavailableChoice as error:
                print(error)

        print('-' * 80)

    def operation(self):
        """Zapewnia działanie wybranej przez użytkownika opcji.

        Na podstawie atrybutu 'user_choice' tworzy instancję odpowiedniej klasy,
        która obsługuje dalsze działanie programu.
        """

        if self.user_choice == 0:
            sys.exit()
        elif self.user_choice == 1:
            CalculateInflation()
        elif self.user_choice == 2:
            ShowInflationOnGraph()
        elif self.user_choice == 3:
            ShowSavingsOnGraph()


if __name__ == '__main__':
    MainMenu()

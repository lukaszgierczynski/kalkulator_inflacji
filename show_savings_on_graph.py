"""Moduł zawierający definicję klasy ShowSavingsOnGraph odpowiadającej za stworzenie wykresu przedstawiającego spadek
realnej wartości oszczędności z powodu inflacji

W celu stworzenia wykresu wykorzystywane są biblioteki: matplotlib oraz numpy.
"""

from exceptions import NegativeNumber
import matplotlib.pyplot as plt
import numpy as np


class ShowSavingsOnGraph:
    """
    Klasa reprezentująca komponent programu odpowiedzialny za stworzenie wykresu przedstawiającego spadek wartości
    oszczędności w czasie z powodu inflacji

    Attributes
    ----------
    inflation : list
        lista przechowująca wartości inflacji podane przez użytkownika
    money_amount : int
        kwota oszczędności wyrażona jako liczba całkowita
    savings_period : int
        czas oszczędzania w latach

    Methods
    ----------
    print_info()
        wyświetla informację dotyczącą właściwości tworzonego wykresu
    get_parameters()
        odczytuje i waliduje podane przez użytkownika parametry dotyczące tworzonego wykresu
    show_graph()
        tworzy i wyświetla wykres
    """

    def __init__(self):
        """Odpowiada za działanie komponentu programu"""

        self.inflation = []
        self.money_amount = None
        self.savings_period = None

        self.print_info()
        self.get_parameters()
        self.show_graph()

    @staticmethod
    def print_info():
        """Wyświetla informację dotyczącą właściwości tworzonego wykresu"""

        print("\nTworzony wykres przedstwia spadek wartości oszczędności w czasie przy założonej dynamice inflacji\n"
              "oraz przy założonej kwocie oszczędności. Konieczne będzie zatem podanie tych dwóch parametrów oraz\n"
              "czasu (liczonego w latach) jaki ma obejmować wykres.")

    def get_parameters(self):
        """Odczytuje i waliduje podane przez użytkownika parametry dotyczące tworzonego wykresu

        Po zwalidowaniu parametrów przypisuje je do odpowiednich atrybutów instancji

        Raises
        ----------
        ValueError
            Jeśli podana wartość nie jest liczbą lub liczbą całkowitą
        NegativeNumber
            Jeśli podana liczba jest mniejsza lub równa 0
        """

        print()
        while True:
            try:
                inflation = float(input("Podaj wartość inflacji rok do roku wyrażoną w procentach: "))
                self.inflation.append(inflation)
                while True:
                    user_choice = input("Czy chcesz pokazać na wykresie wpływ inflacji o kolejnej, innej wartości?"
                                        " Wpisz 'tak' lub 'nie': ")
                    if user_choice in ('tak', 'nie'):
                        break
                    else:
                        print("Możesz wpisać tylko 'tak' lub 'nie'!")
                if user_choice == 'tak':
                    continue
                elif user_choice == 'nie':
                    break
            except ValueError:
                print("Podana wartość musi być liczbą!")

        print()
        while True:
            try:
                amount = int(input("Podaj kwotę oszczędności: "))
                if amount <= 0:
                    raise NegativeNumber
                else:
                    self.money_amount = amount
                    break
            except ValueError:
                print("Podana wartość musi być liczbą całkowitą!")
            except NegativeNumber:
                print("Podana liczba musi być większa od 0!")

        print()
        while True:
            try:
                period = int(input("Podaj czas trwania oszczędzania liczony w latach: "))
                if period <= 0:
                    raise NegativeNumber
                else:
                    self.savings_period = period
                    break
            except ValueError:
                print("Podana wartość musi być liczbą całkowitą!")
            except NegativeNumber:
                print("Podana liczba musi być większa od 0!")

    def show_graph(self):
        """Odpowiada za stworzenie i wyświetlenie wykresu"""

        print("\nZa chwilę wyświetlone zostanie okno z wykresem, aby kontynuować działanie programu zamknij okno.")

        x_axis = np.linspace(0, self.savings_period, self.savings_period + 1)

        def calculate_savings_value(x, inflation):
            """Odpowiada za obliczenie wartości oszczędności w czasie przy określonej wartości inflacji

            Parameters
            ----------
            x : int
                odzwierciedla kolejne lata z danego okresu oszczędzania
            inflation : float
                wartość inflacji rok do roku wyrażona w procentach
            Returns
            ----------
            realna wartość oszczędności po x latach oszczędzania przy inflacji równej parametrowi inflation
            """

            return self.money_amount * (1 - inflation/100) ** x

        plt.figure(figsize=[12, 6])

        for inflation in self.inflation:
            y_axis = np.array([calculate_savings_value(x, inflation) for x in x_axis])

            plt.plot(x_axis, y_axis, marker='o', label=f"{inflation}%")

        default_x_ticks = range(len(x_axis))
        plt.xticks(default_x_ticks, [int(x) for x in x_axis])
        plt.grid()
        plt.xlabel('czas oszczędzania w latach')
        plt.ylabel('wartość początkowej kwoty oszczędności po x latach oszczędzania')
        plt.title(f"Realna wartość {self.money_amount} zł oszczędności w czasie {self.savings_period} lat oszczędzania"
                  f"\nprzy określonej wartości inflacji")
        plt.legend(title='Wartość inflacji')
        plt.show()

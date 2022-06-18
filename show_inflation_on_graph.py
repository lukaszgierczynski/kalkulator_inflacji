"""Moduł zawierający definicję klasy ShowInflationOnGraph odpowiadającej za stworzenie wykresu z przebiegiem własnej
inflacji oraz wykresu z przebiegiem inflacji w wybranej kategorii towarów i usług

Moduł importuje klasy wspomagające działanie klasy ShowInflationOnGraph, które umożliwiają:
- klasa GetUserWeights - podanie przez użytkownika własnych 'wag' w poszczególnych kateogriach towarów i usług;
- klasa InflationData - odczytywanie danych dotyczących inflacji zapisanych w pliku .csv.

W celu stworzenia wykresów wykorzystywana jest biblioteka matplotlib.
"""

from inflation_data import InflationData
from exceptions import UnavailableChoice
from get_user_weights import GetUserWeights
import matplotlib.pyplot as plt


class ShowInflationOnGraph:
    """
    Klasa reprezentująca komponent programu służący do tworzenia wykresów przedstawiających przebieg inflacji

    Attributes
    ----------
    user_choice : int
        wybór użytkownika z listy możliwych operacji
    available_choices : int
        lista z dostępnymi opcjami
    user_expenses_weights : dict
        słownik przechowujący wagi podane przez użytkownika
    data : obiekt klasy InflationData
        obiekt umożliwiajacy wykonywanie operacji na danych dotyczących inflacji

    Methods
    ----------
    print_menu()
        wyświetla menu komponentu programu odpowiedzialnego za tworzenie wykresów
    validate_input()
        odczytuje i waliduje wybór użytkownika
    operation()
        zapewnia działanie opcji wybranej przez użytkownika
    gus_and_own_inflation()
        tworzy wykres z przebiegem inflacji według wag GUS oraz według własnych wag
    category_inflation()
        tworzy wykres z przebiegiem inflacji we wskazaenej kategorii towarów i usług
    """

    def __init__(self):
        """Odpowiada za działanie komponentu programu w pętli while"""

        self.user_choice = None
        self.available_choices = [0, 1, 2]
        self.user_expenses_weights = {}
        self.data = InflationData()

        while True:
            self.print_menu()
            self.validate_input()
            if self.user_choice == 0:
                break
            else:
                self.operation()

    @staticmethod
    def print_menu():
        """Wyświetla menu komponentu programu"""

        print()
        print(f"""Oto lista możliwych operacji:
        0. Wróć do menu głównego programu,
        1. Pokaż na wykresie przebieg inflacji na podstawie wag GUS oraz na podstawie własnych wag,
        2. Pokaż na wykresie przebieg inflacji w poszczególnych kategoriach towarów i usług.""")

    def validate_input(self):
        """Odczytuje wybór użytkownika

        Po zwalidowaniu wartości podanej przez użytkownika przypisuje ją do atrybutu 'user_choice'

        Raises
        -------
        ValueError
            Jeśli podana przez użytkowika wartość nie jest liczbą całkowitą
        UnavailableChoice
            Jeśli wprowadzonej przez użytkownika liczby nie ma na liście dostępnych opcji
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

    def operation(self):
        """Odpowiada za działanie opcji wybranej przez użytkownika"""

        if self.user_choice == 1:
            self.gus_and_own_inflation()
        elif self.user_choice == 2:
            self.category_inflation()

    def gus_and_own_inflation(self):
        """Tworzy wykres z przebiegiem inflacji według wag GUS oraz według wag podanych przez użytkownika"""

        def calculate_own_inflation():
            """Liczy 'własną' inflację dla wszystkich miesięcy, dla których dostępne są dane

            Returns
            -------
            own_inflation_dict : dict
                słownik którego kluczami są tuple z miesiącem i rokiem, a wartościami obliczona inflacja
            """
            own_inflation_dict = {}
            for month_data in self.data.inflation_data[1:]:
                inflation = sum([weight/100 * float(category_inflation) for weight, category_inflation in
                                 zip(self.user_expenses_weights.values(), month_data[3:])])
                own_inflation_dict[(month_data[0], month_data[1])] = round(inflation, 1)

            return own_inflation_dict

        def show_graph(gus_inflation, own_inflation):
            """Tworzy i wyświetla wykres z przebiegiem inflacji według wag GUS i według 'własnych' wag

            Parameters
            ----------
            gus_inflation : dict
                słownik którego kluczami są tuple z miesiącem i rokiem, a wartościami inflacja według wag gus
            ----------
            own_inflation : dict
                słownik którego kluczami są tuple z miesiącem i rokiem, a wartościami inflacja według 'własnych' wag
            """
            gus_data = list(gus_inflation.values())
            gus_data = [data-100 for data in gus_data]
            own_data = list(own_inflation.values())
            own_data = [data-100 for data in own_data]
            x_axis = [month + '.' + year for month, year in gus_inflation.keys()]
            plt.figure(figsize=(12, 6))
            plt.plot(x_axis, gus_data, color='red', label='inflacja GUS')
            plt.plot(x_axis, own_data, color='green', label='inflacja "własna"')
            plt.xlabel('miesiąc')
            plt.ylabel('dynamika inflacji rok do roku [%]')
            plt.legend()
            plt.show()

        instance = GetUserWeights()
        self.user_expenses_weights = instance.user_expenses_weights
        own_infl = calculate_own_inflation()
        gus_infl = self.data.get_category_inflation(0)

        print()
        print("Za chwilę wyświetlone zostanie okno z wykresem. Aby kontynuować działanie programu zamknij okno.")
        show_graph(gus_infl, own_infl)
        print()
        print('*' * 80)

    def category_inflation(self):
        """Tworzy wykres z przebiegiem inflacji w określonej kategorii towarów i usług"""

        def choose_category():
            """Odczytuje i waliduje wybór użytkownika dotyczący kategorii towarów i usług

            Returns
            -------
            user_index : int
                indeks odpowiadający wybranej kategorii towarów i usług

            Raises
            -------
            ValuerError
                Jeśli podanej przez użytkownika wartości nie można zamienić na liczbę całkowitą
            """

            print()
            print("Wybierz jedną z poniższych kategorii towarów i usług, której inflację chcesz pokazać na wykresie:")
            for index, category in list(self.data.data_field_map.items())[1:]:
                print(f"{index} - {category}")
            print()
            while True:
                try:
                    user_index = int(input("Podaj odpowiednią liczbę lub wpisz '0', aby powrócić do poprzedniego"
                                           " menu: "))
                    if user_index in list(range(0, 13)):
                        return user_index
                    else:
                        print("Podana liczba musi być z zakresu 1-12!")
                except ValueError:
                    print("Możesz wpisać tylko liczbę całkowitą!")

        def show_graph(index):
            """Tworzy i wyświetla wykres z przebiegiem inflacji w określonej kategorii towarów i usług

            Parameters
            ----------
            index : int
                indeks odpowiadający określonej kategorii towrów i usług w pliku z danymi
            """
            category_inflation = self.data.get_category_inflation(index)
            category_data = [inflation-100 for inflation in list(category_inflation.values())]
            x_axis = [month + '.' + year for month, year in category_inflation.keys()]
            label = self.data.get_headers()[index+2]
            plt.figure(figsize=[12, 6])
            plt.plot(x_axis, category_data, color='green', label=label)
            plt.xlabel('miesiąc')
            plt.ylabel('dynamika inflacji rok do roku [%]')
            plt.legend()
            plt.show()

        print('*' * 80)

        while True:
            category_index = choose_category()
            if category_index == 0:
                print('*' * 80)
                break
            else:
                print()
                print("Za chwilę wyświetlone zostanie okno z wykresem. Aby kontynuować działanie programu zamknij okno")
                show_graph(category_index)
                print('*' * 80)

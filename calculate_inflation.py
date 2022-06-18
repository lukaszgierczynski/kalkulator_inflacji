"""Moduł zawierający definicję klasy CalculateInflation odpowiadającej za obliczenie 'własnej' inflacji
na podstawie danych Głównego Urzędu Statystycznego

Moduł importuje klasy wspomagające działanie klasy CalculateInflation, które umożliwiają:
- klasa GetUserWeights - podanie przez użytkownika 'własnych' wag w poszczególnych kategoriach wydatków;
- klasa InflationData - odczytywanie danych dotyczących inflacji zapisanych w pliku .csv.
"""

from inflation_data import InflationData
from get_user_weights import GetUserWeights
from exceptions import UnavailableChoice
import time


class CalculateInflation:
    """
    Klasa reprezentująca komponent programu odpowiedzialny za obliczenie "własnej" inflacji

    Attributes
    ----------
    user_choice : int
        wybór użytkownika z listy możliwych operacji
    user_expenses_weights : dict
        słownik przechowujący wagi podane przez użytkownika
    data : obiekt klasy InflationData
        obiekt umożlwiajacy wykonywanie operacji na danych dotyczących inflacji
    available_choices : list
        lista z możliwymi operacjami

    Methods
    ----------
    print_menu()
        wyświetla menu komponentu odpowiedzialnego za obliczenie 'własnej' inflacji
    validate_input()
        odczytuje i waliduje wybór użytkownika
    operation()
        zapewnia działanie wybranej przez użytkownika opcji
    calculate_inflation()
        odpowiada za obliczenie 'własnej' inflacji użytkownika w danym miesiącu na podstawie podanych wag
    """

    def __init__(self):
        """Odpowiada za działanie komponentu programu w pętli while"""

        self.user_choice = None
        self.user_expenses_weights = {}
        self.data = InflationData()
        self.available_choices = [0, 1, 2, 3]

        print()
        print("Teraz możesz obliczyć inflację dla twoich wydatków na podstawie danych Głównego Urzędu Statystycznego.\n"
              "GUS liczy inflację na podstawie tzw. koszyka inflacyjnego, który określa wagi dla rozkładu wydatków\n"
              "przeciętnego Polaka według poszczególnych kategorii towarów i usług np. w kategorii 'Odzież i obuwie'.\n"
              "Zatem w celu obliczenia 'własnej' inflacji konieczne będzie podanie przez Ciebie wag twoich wydatków.")

        while True:
            self.print_menu()
            self.validate_input()
            if self.user_choice == 0:
                break
            else:
                self.operation()

    def print_menu(self):
        """Wyświetla menu kopmonentu programu"""

        print()
        print(f"""Oto lista możliwych operacji:
        0. Wróć do menu głównego programu,
        1. Podaj wagi twoich wydatków w poszczególnych kategoriach towarów i usług,
        2. Oblicz najaktualniejszą 'własną' inflację w miesiącu, dla którego dostępne są ostatnie dane GUS,
        3. Oblicz 'własną' inflację w dowolnym miesiącu z okresu {self.data.get_data_time_range()}.""")

    def validate_input(self):
        """Odczytuje wybór użytkownika

        Po zwalidowaniu wartości podanej przez użytkownika przypisuje ją do atrybutu 'user_choice'

        Raises
        -------
        ValueError
            Jeśli wprowadzona wartość nie jest liczbą całkowitą
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
            instance = GetUserWeights()
            self.user_expenses_weights = instance.user_expenses_weights
        elif self.user_choice == 2:
            self.calculate_inflation()
        elif self.user_choice == 3:
            self.calculate_inflation()

    def calculate_inflation(self):
        """Odpowiada za obliczenie 'własnej' inflacji użytkownika na podstawie wczesniej podanych wag

        Jeśli użytkownik nie podał wczęsniej wag tzn. atrybut 'user_expenses_weights' jest pusty - działanie funkcji
        jest kończone
        Również jeśli użytkownik chce zmienić podane wcześniej wagi - działanie funkcji jest kończone
        Jeśli atrybut 'user_choice' jest równy 2 - liczy 'własną' inflację w ostatnim miesiącu,
        dla którego dostępne są dane
        Jeśli atrybut 'user_choice' jest równy 3 - liczy inflację dla dowolnego miesiąca wskazanego przez użytkownika
        """

        def validate_month():
            """Waliduje podany przez użytkownika miesiąc, dla którego obliczona ma zostać 'własna' inflacja

            Returns
            -------
            validated_month : tuple
                zwracana po zwalidowaniu tupla zawierająca podany przez użytkownika miesiąc i rok
            """

            available_years = self.data.get_available_years()
            available_months = self.data.get_available_months()

            print()
            print(f"'Własna' inflacja może zostać obliczona dla dowolnego miesiąca z okresu"
                  f" {self.data.get_data_time_range()}.")
            print("Podaj rok oraz miesiąc jako cyfrę rzymską.")

            while True:
                year = input('Podaj rok: ')
                if year in available_years:
                    print("Podano poprawny rok.")
                    break
                else:
                    print(f"Brak danych dla podanej wartości. Wybierz jeden z następujących roków: {available_years}.")

            while True:
                month = input('Podaj miesiąc: ')
                if (month, year) in available_months:
                    validated_month = (month, year)
                    print("Podano poprawny miesiąc oraz poprawny rok.")
                    break
                else:
                    print("Brak danych dla podanego miesiąca oraz roku. Spróbuj jeszcze raz podać miesiąc "
                          f"zapisany cyfrą rzymską z okresu {self.data.get_data_time_range()}.")

            return validated_month

        def calculate_own_inflation(month):
            """Liczy 'własną' inflację we wskazanym miesiącu na podstawie wcześniej podanych wag

            Parameters
            ----------
            month : tuple
                tupla zawierająca miesiąc i rok, dla których obliczona ma zostać inflacja

            Returns
            -------
            inflation : float
                obliczona inflacja rok do roku wyrażona w procentach
            """

            categories = self.data.get_headers()[3:]
            weights_list = []
            for category in categories:
                weights_list.append(self.user_expenses_weights[category])

            for element in self.data.inflation_data:
                if (element[0], element[1]) == month:
                    inflation = sum([weight/100 * float(category_inflation) for weight, category_inflation
                                     in zip(weights_list, element[3:])]) - 100

            return inflation

        if not self.user_expenses_weights:
            print('*' * 80)
            print("Nie można obliczyć inflacji, ponieważ nie podałeś wag twoich wydatków.")
            print("Za chwilę powrócisz do menu głównego. Wybierz w nim opcję nr 1, aby wpisać wagi.")
            print("Po wpisaniu wag wróć do obliczenia 'własnej' inflacji.")
            print('*' * 80)
            time.sleep(5)
            return
        else:
            print('-' * 80)
            print("Inflacja zostanie obliczona na podstawie następujących wag wydatków:")
            print()
            for expense_category, expense_weight in self.user_expenses_weights.items():
                print(f"{expense_category} -> {expense_weight}%")
            print()

        while True:
            user_choice = input("Czy chcesz teraz powrócić do poprzedniego menu, aby zmienić wagi? "
                                "Wpisz 'tak' lub 'nie': ")
            if user_choice in ['tak', 'nie']:
                if user_choice == 'tak':
                    print('*'*80)
                    return
                elif user_choice == 'nie':
                    break
            else:
                print("Możesz wpisać tylko wartości 'tak' lub 'nie'!")

        if self.user_choice == 2:
            last_month = self.data.get_available_months()[-1][0]
            last_year = self.data.get_available_months()[-1][1]
            calculated_inflation = calculate_own_inflation((last_month, last_year))

            print()
            print(f"Ostatnim miesiącem, dla którego dane są dostępne jest {self.data.month_map[last_month]}"
                  f" w {last_year} roku.")
            print(f"W tym miesiącu 'własna' inflacja, dla podanych wag wyniosła {calculated_inflation:.1f}%"
                  f" rok do roku.")
            print(f"Inflacja ogólna liczona według wag GUS wyniosła wtedy"
                  f" {float(self.data.last_total_inflation()) - 100}% rok do roku.")

        elif self.user_choice == 3:
            user_month, user_year = validate_month()
            calculated_inflation = calculate_own_inflation((user_month, user_year))

            print(f"W miesiącu {self.data.month_map[user_month]} w {user_year} roku 'własna' inflacja obliczona "
                  f"dla podanych wag wyniosła {calculated_inflation:.1f}%.")
            print(f"Inflacja ogólna liczona według wag GUS wyniosła wtedy "
                  f"{float(self.data.total_inflation_in_specific_month(user_month, user_year)) - 100:.1f}%.")

        print('-' * 80)

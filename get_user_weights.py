"""Moduł zawierający definicję klasy GetUserWeights, która umożliwia użytkownikowi podanie wag dotyczących jego wydatków
w poszczególnych kategoriach towarów i usług

Moduł importuje klasę InflationData, która służy odczytywaniu danych dotyczących inflacji zapisanych w pliku .csv
"""


from exceptions import NumberOutOfRange
from inflation_data import InflationData


class GetUserWeights:
    """
    Klasa umożliwająca użytkownikowi podanie wag dotyczących jego wydatków w poszczególnych kategoriach towarów i usług

    Oprócz manualnego podawania wag klasa umożliwia również odczytywanie i zapisywanie wag do pliku tekstowego

    Attributes
    ----------
    user_expenses_weights : dict
        słownik przechowujący wagi podane przez użytkownika
    data : obiekt klasy InfaltionData
        obiekt umożliwiający wykonywanie operacji na danych dotyczących inflacji

    Methods
    ----------
    get_user_weights()
        metoda umożliwiająca użytkownikowi manualne podanie wag, odczytanie wag z pliku oraz zapisanie wag do pliku
    """

    def __init__(self):
        """Odpowiada za działanie całego komponentu programu umożliwiającego podawanie wag"""

        self.user_expenses_weights = {}
        self.data = InflationData()
        self.get_user_weights()

    def get_user_weights(self):
        """Umożliwia użytkownikowi manualne podanie wag, odczytanie wag z pliku oraz zapisanie wag do pliku"""

        def validate_expense_weight(category):
            """Odczytuje i waliduje wagę w danej kategorii podaną przez użytkownika

            Parameters
            ----------
            category : str
                nazwa danej kategorii towarów i usług

            Returns
            -------
            user_input : int
                zwalidowana waga podana przez użytkownika wyrażona jako liczba całkowita

            Raises
            -------
            ValueError
                Jeśli podanej wartości nie można zamienić na liczbę całkowitą
            NumberOutOfRange
                Jeśli podana liczba wykracza poza dozwolony zakres, czyli jest mniejsza od 0 lub większa od 100
            """

            while True:
                user_input = input(f"Waga w kategorii '{category}': ")

                try:

                    user_input = int(user_input)

                    if user_input < 0 or user_input > 100:
                        raise NumberOutOfRange("Podana liczba musi być większa lub równa 0 oraz mniejsza"
                                               " lub równa 100!")

                    return user_input

                except ValueError:
                    print("Podana wartość musi być liczbą całkowitą!")
                except NumberOutOfRange as error:
                    print(error)

        def validate_weights_sum():
            """Sprawdza czy wagi podane przez użytkownika sumują się do 100

            Gdy wagi nie sumują się do 100 - usuwa wprowadzone wagi z atrybutu 'user_expenses_weights'

            Returns
            ----------
            Zwraca True, jeśli podane wagi sumują się do 100
            W przeciwnym wypadku zwraca False
            """

            weights_sum = sum(self.user_expenses_weights.values())
            if weights_sum == 100:
                return True
            else:
                self.user_expenses_weights = {}
                return False

        def save_expenses_to_file():
            """Umożliwia zapisanie wcześniej wprowadzonych wag do pliku tekstowego w katalogu roboczym"""

            while True:
                choice = input("Czy chcesz zapisać wagi do pliku tekstowego? Wpisz 'tak' lub 'nie': ")
                if choice == 'tak':
                    file_name = input("Podaj nazwę pliku (nie musisz dodawać rozszerzenia .txt): ")
                    if not file_name.endswith('.txt'):
                        file_name = file_name + '.txt'
                    with open(file_name, 'w') as file:
                        for category, weight in self.user_expenses_weights.items():
                            file.write(f"{category} -> {weight}\n")
                    print(f"Plik {file_name} został zapisany w katalogu roboczym.")
                    print("*"*80)
                    break
                elif choice == 'nie':
                    print('*'*80)
                    break
                else:
                    print("Możesz wpisać 'tak' lub 'nie'!")

        def read_expenses_from_file():
            """Umożliwia odczytanie wag z pliku tekstowego znajdującego się w katalogu roboczym

            Format zapisu danych w odczytywanym pliku musi być taki sam jak format danych zapiswanych do pliku
            w metodzie 'save_expenses_to_file()'

            Raises
            -------
            FileNotFoundError
                Jeśli odczytywanego pliku nie ma w katalogu roboczym

            """
            while True:
                print()
                file_name = input("Plik tekstowy z wagami musi znajdować się w katalogu roboczym.\n"
                                  "Plik musi być sforamtowany tak samo jak pliki z wagami tworzone prez program.\n"
                                  "Podaj nazwę pliku (nie musisz dodawać rozszerzenia .txt): ")
                if not file_name.endswith('.txt'):
                    file_name = file_name + '.txt'
                try:
                    with open(file_name, 'r') as file:
                        lines = file.readlines()
                        for line in lines:
                            x = line.split('->')
                            self.user_expenses_weights[x[0].strip()] = int(x[1].strip())
                    print(f"Wagi zostały pomyślnie odczytane z pliku {file_name}")
                    print('*'*80)
                    break
                except FileNotFoundError:
                    print(f"W katalogu roboczym nie ma pliku {file_name}!")

        def ask_user_for_expenses():
            """Umożliwia użytkownikowi manualne podanie wag w konsoli

            Wagi zapisywane są do atrybutu 'user_expenses_weights'
            Jeśli suma wag nie jest równa 100, użuytkownik musi ponownie je podać
            """

            while True:
                print()
                print("Wpisz wagi twoich wydatków w poszczególych kategoriach:")
                for expense_category in self.data.get_headers()[3:]:
                    print()
                    expense_weight = validate_expense_weight(expense_category)
                    self.user_expenses_weights[expense_category] = expense_weight

                if validate_weights_sum():
                    print()
                    print('*' * 80)
                    print("Suma wag jest równa 100.")
                    print('*' * 80)
                    save_expenses_to_file()
                    break
                else:
                    print()
                    print('*' * 80)
                    print("Niestety suma wag nie jest równa 100. Spróbuj jeszcze raz wpisać wagi.")
                    print('*' * 80)

        print('-'*80)
        print("Teraz zostaniesz poproszony o podanie wag twoich wydatków w dwunastu kategoriach towarów i usług.\n"
              "Wagi możesz odczytać z zapisanego wcześniej przez program pliku tekstowego lub podać je ręcznie."
              "Podawane wagi muszą być liczbami całkowitymi. Jeżeli suma wag nie będzie równa 100 zostaniesz\n"
              "poproszony o ponowne podanie wszystkich wag. Dla każdej z kategorii wpisz wagę i wciśnij 'enter'.")

        while True:
            user_choice = input("Czy chcesz odczytać wagi z pliku tekstowego? Wpisz 'tak' lub 'nie': ")
            if user_choice == 'tak':
                read_expenses_from_file()
                break
            elif user_choice == 'nie':
                ask_user_for_expenses()
                break
            else:
                print("Możesz wpisać 'tak' lub 'nie'")

"""Moduł zawierający definicję klasy InlfationData umożliwiającej wykonywanie operacji na danych dotyczących inflacji
zapisanych w pliku .csv w katalogu roboczym

W celu odczytania danych z pliku .csv importowany jest moduł csv z biblioteki standardowej
"""


import csv


class InflationData:
    """Klasa reprezentująca dane dotyczące inflacji

    Attributes
    ----------
    inflation_data : list
        lista zawierająca listy z danymi z poszczególnych wierszy pliku .csv
    month_map : dict
        słownik mapujący poszczególne miesiące roku zapisane jako cyfry rzymskie na ich słowne odpowiedniki
    data_field_map : dict
        słownik mapujący indeks poszczególnych kategorii towrów i usług na ich słowne odpowiedniki
    Methods
    ----------
    get_headers()
        zwraca listę z nagłówkami danych znajdujących się w pliku .csv
    get_inflation_in_specific_month(month, year)
        zwraca listę z danymi dotyczącymi inflacji w danym miesiącu i roku
    get_category_inflation(index)
        zwraca słownik z danymi dotyczącymi inflacji w określonej kategorii towarów i usług w okresie czasu
        objętym przez dane
    get_data_time_range()
        zwraca zmienną typu string, która przedstawia okres czasu objęty przez dane
    get_available_months()
        zwraca listę tupli zawierających miesiąc i rok - każda tupla to inny miesiąc objęty przez dane
    get_available_years()
        zwraca listę z latami, w których występuje choć jeden miesiąc objęty przez dane
    last_total_inflation()
        zwraca wartość inflacji obliczonej według wag Głównego Urzędu Statystycznego
        w ostatnim miesiącu objętym prez dane
    total_inflation_in_specific_month(month, year)
        zwraca wartość inflacji obliczonej według wag Głównego Urzędu Statystycznego w określonym miesiącu i roku
    """

    def __init__(self):
        """Odpowiada za wczytanie danych dotyczących inflacji z pliku .csv do atrybutu 'inflation_data'

        Plik 'dane_inflacja.csv' musi znajdować się w katalogu roboczym
        Atrybut 'inflation_data' to lista składająca się z list, które odpowiadają danym z poszczególnych wierszy
        pliku .csv
        Dane w każdym wierszu pliku .csv zapisane są w natępującej kolejności: miesiąc, rok, inflacja ogółem
        oraz inflacje w poszczególnych kategoriach towarów i usług
        """

        self.inflation_data = []
        self.month_map = {'I': 'styczeń', 'II': 'luty', 'III': 'marzec', 'IV': 'kwiecień', 'V': 'maj', 'VI': 'czerwiec',
                          'VII': 'lipiec', 'VIII': 'sierpień', 'IX': 'wrzesień', 'X': 'październik', 'XI': 'listopad',
                          'XII': 'grudzień'}

        with open("dane_inflacja.csv") as csvfile:
            data = csv.reader(csvfile, delimiter=';')

            for line in data:
                self.inflation_data.append(line)

        self.data_field_map = {key: value for key, value in zip(range(len(self.inflation_data[0]) - 2),
                                                                self.inflation_data[0][2:])}

    def get_headers(self):
        """
        Returns
        ----------
        lista z nagłówkami danych znajdujących się w pliku .csv
        """
        return self.inflation_data[0]

    def get_inflation_in_specific_month(self, month, year):
        """Zwraca listę z danymi dotyczącymi inflacji w danym miesiącu i roku

        Parameters
        ----------
        month : str
            miesiąc zapisany jako cyfra rzymska
        year : str
            rok

        Returns
        -------
        line : list
            lista z danymi dotyczącymi inflacji w określonym miesiącu i roku

        Raises
        -------
        ValueError
            Jeśli dane nie obejmują danego miesiąca i roku
        """

        for line in self.inflation_data:
            if line[0] == month and line[1] == year:
                return line
        else:
            raise ValueError(f"Brak danych dla podanego miesiąca. Dane są dostępne tylko dla okresu: "
                             f"{self.get_data_time_range()}.")

    def get_category_inflation(self, index):
        """Zwraca słownik z danymi dotyczącymi inflacji w określonej kategorii towarów i usług w okresie czasu
        objętym przez dane

        Parameters
        ----------
        index : str, int
            indeks wskazujący na daną kategorię towarów i usług

        Returns
        -------
        data : dict
        słownik z danymi dotyczącymi inflacji w określonej kategorii towarów i usług w okresie czasu
        objętym przez dane

        Raises
        -------
        ValueError
            Jeśli podana wartość nie jest liczbą całkowitą
        IndexError
            Jeśli podany indeks jest spoza zakresu dostępnych indeksów
        """

        data = {}

        try:
            index = int(index)
        except ValueError:
            raise ValueError('Podana wartość musi być liczbą całkowitą!')

        if index not in self.data_field_map.keys():
            raise IndexError('Brak danych dla podanego indeksu!')

        for line in self.inflation_data[1:]:
            data[(line[0], line[1])] = float(line[index + 2])

        return data

    def get_data_time_range(self):
        """
        Returns
        ----------
        time_range : str
            zmienna typu string, która przedstawia okres czasu objęty przez dane
        """

        first_month = self.inflation_data[1][0] + '.' + self.inflation_data[1][1]
        last_month = self.inflation_data[-1][0] + '.' + self.inflation_data[-1][1]
        time_range = first_month + ' - ' + last_month

        return time_range

    def get_available_months(self):
        """
        Returns
        ----------
        available_months : list
            lista tupli zawierających miesiąc i rok - każda tupla to inny miesiąc objęty przez dane
        """

        available_months = [(data[0], data[1]) for data in self.inflation_data[1:]]
        return available_months

    def get_available_years(self):
        """
        Returns
        ----------
        available_years : list
            lista z latami, w których występuje choć jeden miesiąc objęty przez dane
        """

        available_years = sorted(list(set(data[1] for data in self.inflation_data[1:])))
        return available_years

    def last_total_inflation(self):
        """
        Returns
        ----------
        wartość inflacji obliczonej według wag Głównego Urzędu Statystycznego
        w ostatnim miesiącu objętym prez dane
        """
        return self.inflation_data[-1][2]

    def total_inflation_in_specific_month(self, month, year):
        """Zwraca wartość inflacji obliczonej według wag Głównego Urzędu Statystycznego w określonym miesiącu i roku

        Parameters
        ----------
        month : str
            określony miesiąc zapisany jako cyfra rzymska
        year : str
            określony rok

        Returns
        -------
        total_inflation : str
            wartość inflacji obliczonej według wag Głównego Urzędu Statystycznego w określonym miesiącu i roku
        """

        for element in self.inflation_data:
            if element[0] == month and element[1] == year:
                total_inflation = element[2]
                return total_inflation

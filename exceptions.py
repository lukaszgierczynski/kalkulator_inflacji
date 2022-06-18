"""Moduł zawierający definicje wyjątków wykorzystywanych w programie"""


class UnavailableChoice(Exception):
    """Klasa reprezentująca wyjątek wskazujący na brak podanej wartości na liście dostępnych możliwości"""
    pass


class NumberOutOfRange(Exception):
    """Klasa reprezentująca wyjątek wskazujący na wykraczanie podanej liczby poza dany zakres"""
    pass


class NegativeNumber(Exception):
    """Klasa reprezentująca wyjątek wskazujący na ujemną liczbę"""
    pass

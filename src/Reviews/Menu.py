import os
from functools import reduce

from src.Reviews.GameClass import Game

## slownik zawierajacy klucz do obiektow typu Game
gry = {}

## glowna funkcja reprezentujaca menu
def menu():
    def menu_recenzji(game):
        try:
            if isinstance(game, Game):
                while True:
                    print("1: Zmodyfikuj dane gry\n"
                          "2: dodaj recenzje: \n"
                          "3: usun dana recenzje\n"
                          "4: Przegladaj recencje\n"
                          "5: zmodyfikuj recenzje\n"
                          "6: srednia z ocen recenzji\n"
                          "7: Zapisz do pliku JSON\n"
                          "reszta: wyjscie z menu")
                    wybor1 = int(input("Wybor: "))
                    if wybor1 == 1:
                        game.mod_game()
                    elif wybor1 == 2:
                        game.add_review()
                    elif wybor1 == 3:
                        game.delete_review()
                    elif wybor1 == 4:
                        game.drukuj_recenzje()
                    elif wybor1 == 5:
                        game.change_review()
                    elif wybor1==6:
                        try:
                            n=len(game.recenzje)
                            if n<=1:
                                raise TypeError
                            else:
                                avg=reduce(game.average_ranks,game.recenzje)
                                print("Średnia ocen dla gry ",game.nazwa,": ",avg/n)
                        except (TypeError,ZeroDivisionError):
                            print("do obliczenia sredniej potrzebujemy co najmniej dwoch recenzji")
                        finally:
                            continue
                    elif wybor1==7:
                        game.save_to_JSON()
                    else:
                        raise KeyboardInterrupt
            else:
                print("Nie jest typem Gra")
                return 0

        except KeyError:
            print("===================================")
            print("Podana gra nie znajduje sie w katalogu")
            print("===================================")
            return 0
        except KeyboardInterrupt:
            print("===================================")
            print("Wychodzenie z menu recenzje")
            print("===================================")
            return 0

    print("===================================")
    try:
        while True:
            print("1: dodaj gre do katalogu: \n"
                  "2: usun gre z katalogu\n"
                  "3: Przegladaj gry\n"
                  "4: przejdz do gry\n"
                  "reszta: wyjscie z programu")
            wybor = int(input("Wybor: "))
            if wybor == 1:
                add_game()
            elif wybor == 2:
                delete_game()
            elif wybor == 3:
                game_list()
            elif wybor == 4:
                result = choose_game()
                ptr = menu_recenzji
                if ptr(result) != 0:
                    return 0
                else:
                    continue

            else:
                raise KeyboardInterrupt
    except KeyboardInterrupt:
        print("W tym przypadku program sie zakonczyl. Milego dnia!")
        return 0


## funkcje dla glownego menu

## dodawanie obiektu Game
def add_game():
    print("===================================")
    try:
        nazwa = input("Nazwa gry: ")
        if nazwa in gry:
            raise KeyError
        gatunki = set()
        print("Dodaj gatunki do twojej gry('end' oznacza koniec): ")
        l = input("Gatunek " + str(len(gatunki)) + ": ")

        while l != "end":
            gatunki.add(l)
            l = input("Gatunek " + str(len(gatunki)) + ": ")
        wydawca = input("Podaj wydawce: ")
        producent = input("Podaj producenta tej gry: ")
        gry[nazwa] = Game(nazwa, gatunki, wydawca, producent)
    except KeyError:
        print("===================================")
        print("W katalogu znajduje sie juz taka gra!")
        print("===================================")

## usuwanie obiektu
def delete_game():
    if len(gry) == 0:
        print("===================================")
        print("Katalog jest pusty")
        print("===================================")
    else:
        print("==================================")
        for games in gry.values():
            if isinstance(games, Game):
                print(games.nazwa)
        result = input("Podaj gre do wyboru: ")
        if result in gry.keys():
            del gry[result]
            print("===================================")
            print("Pomyslnie usunieto!")
            print("===================================")
        else:
            print("===================================\n"
                  "Nie znaleziono takiej gry do usuniecia")
            print("===================================")

## wyswietlanie listy gier
def game_list():
    if len(gry) == 0:
        print("===================================")
        print("Katalog jest pusty")
        print("===================================")
    else:
        for i in gry.values():
            if isinstance(i, Game):
                i.print_info()

## wybor obiektu gry do menu z recenzjami
def choose_game():
    result = ""
    try:
        if len(gry) == 0:
            print("===================================")
            print("Katalog jest pusty")
            print("===================================")
            return None
        else:
            print("===================================")
            for games in gry.values():
                if isinstance(games, Game):
                    print(games.nazwa)
            result = gry[input("Podaj gre do wyboru: ")]
            if isinstance(result, Game):
                return result
            else:
                return None
    except KeyError:
        print("===================================")
        print("Nie znaleziono takiego klucza w katalogu")
        print("===================================")
        return None

def load_JSON_to_database():
    path_to_files=os.path.join("pliki_json")
    list_files=[f for f in os.listdir(path_to_files)]
    for files in list_files:
        with open(path_to_files+"\\"+files,"r") as f:
            print(f.read(-1))

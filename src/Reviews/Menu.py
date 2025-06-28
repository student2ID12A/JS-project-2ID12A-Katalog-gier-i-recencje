import os
import sys
from functools import reduce
import matplotlib.pyplot as plt
import numpy as np

import src.Reviews.CustomException as exc
import src.Reviews.GameClass as gc

## slownik zawierajacy klucz do obiektow typu gc.Game
gry = {}

path_to_files=os.path.join("pliki_json")

## glowna funkcja reprezentujaca menu
def menu():
    def menu_recenzji(game):
        try:
            if isinstance(game, gc.Game):
                while True:
                    print("1: Zmodyfikuj dane gry\n"
                          "2: dodaj recenzje: \n"
                          "3: usun dana recenzje\n"
                          "4: Przegladaj recencje\n"
                          "5: zmodyfikuj recenzje\n"
                          "6: Zapisz do pliku JSON\n"
                          "reszta: wyjscie z menu")
                    wybor1 = int(input("Wybor: "))
                    if wybor1 == 1:
                        game.mod_game()
                    elif wybor1 == 2:
                        game.add_review()
                    elif wybor1 == 3:
                        game.delete_review()
                    elif wybor1 == 4:
                        game.print_reviews()
                    elif wybor1 == 5:
                        game.change_review()
                    elif wybor1==6:
                        game.save_to_JSON()
                    else:
                        raise KeyboardInterrupt
            else:
                return 0
        except KeyError:
            print_with_separators("Podana gra nie znajduje sie w katalogu")
            return 0
        except KeyboardInterrupt:
            print("Wyjscie do menu glownego")
            return 0

    print("===================================")
    try:
        while True:
            print("1: dodaj gre do katalogu: \n"
                  "2: usun gre z katalogu\n"
                  "3: Przegladaj gry\n"
                  "4: przejdz do gry\n"
                  "5: Wykresy\n"
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
            elif wybor==5:
                chart()
            else:
                raise exc.TerminateProgram
    except exc.TerminateProgram:
        print("W takim razie konczymy program. Milego dnia!")
        sys.exit()


"""funkcje dla glownego menu"""

## dodawanie obiektu gc.Game
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
        gry[nazwa] = gc.Game(nazwa, gatunki, wydawca, producent)
    except KeyError:
        print_with_separators("W katalogu znajduje sie juz taka gra!")

## usuwanie obiektu
def delete_game():
    if len(gry) == 0:
        print_with_separators("Katalog jest pusty")
    else:
        print("==================================")
        for games in gry.values():
            if isinstance(games, gc.Game):
                print(games.nazwa)
        result = input("Podaj gre do wyboru: ")
        if result in gry.keys():
            del gry[result]
            print_with_separators("Pomyslnie usunieto!")
            if os.path.exists(path_to_files):
                os.remove(path_to_files+"\\"+result+".json")
        else:
            print_with_separators("Nie znaleziono takiej gry do usuniecia")

## wyswietlanie listy gier
def game_list():
    if len(gry) == 0:
        print_with_separators("Katalog jest pusty")
    else:
        for i in gry.values():
            if isinstance(i, gc.Game):
                i.print_info()

## wybor obiektu gry do menu z recenzjami
def choose_game():
    try:
        if len(gry) == 0:
            print_with_separators("Katalog jest pusty")
            return None
        else:
            print("===================================")
            for games in gry.values():
                if isinstance(games, gc.Game):
                    print(games.nazwa)
            result = gry[input("Podaj gre do wyboru: ")]
            if isinstance(result, gc.Game):
                return result
            else:
                return None
    except KeyError:
        print_with_separators("Nie znaleziono takiego klucza w katalogu")
        return None

def load_JSON_to_database():
    nazwa=producent=wydawca=recenzent=opis=""
    gatunki=set()
    ocena=difficulty=0
    gra=None

    list_files=[f for f in os.listdir(path_to_files)]
    for files in list_files:
        with open(path_to_files+"\\"+files,"r") as f:
            gatunki.clear()
            result=f.read(-1).split('"')[1::2]
            for i in range(len(result)):
                try:
                    nazwa = result[i+1] if result[i]=="Nazwa" else nazwa
                    producent=result[i+1] if result[i]=="Producent" else producent
                    wydawca=result[i+1] if result[i]=="Wydawca" else wydawca
                    if result[i-1]=="Gatunki: ":
                        k=1
                        while result[i]=="Gatunek "+str(k):
                            gatunki.add(result[i+1])
                            i+=2
                            k+=1
                        else:
                            gra=gc.Game(nazwa, gatunki, wydawca, producent)
                    if result[i]=="Recenzje":
                        i+=1
                        k=1
                        while result[i]=="Recenzja "+str(k):
                            i+=1
                            recenzent= result[i+1] if result[i]=="Recenzent" else recenzent
                            i+=2
                            ocena=int(result[i+1]) if result[i]=="Ocena gry" else ocena
                            i+=2
                            difficulty=int(result[i+1]) if result[i]=="Ocena trudnosci" else difficulty
                            i+=2
                            opis=result[i+1] if result[i]=="Opis" else opis
                            i+=2
                            k+=1
                            gra.recenzje.append(gra.Review(recenzent, ocena, difficulty, opis))
                except IndexError:
                    break

            f.close()
            gry[nazwa]=gra


def rec_operation(games_list=None, i=0, op_num=1):
    if games_list is None:
        games_list = []
    x=[]
    result=0
    
    if i==len(games_list):
        return []
    else:
        if isinstance(games_list[i],gc.Game):
            n = len(games_list[i].recenzje)
            if op_num==1:
                x=[n]
                return x+rec_operation(games_list,i+1,op_num)
            elif op_num==2 or op_num==3:
                try:
                    result = reduce(sum_ranks, games_list[i].recenzje) / n if op_num ==2 else reduce(sum_diff, games_list[i].recenzje)/n
                    x=[result]
                except ZeroDivisionError:
                    x=[0.0]
                except TypeError:
                    if n==0:
                        x=[0.0]
                    else:
                        x=[float(games_list[i].get_review().ocena)] if op_num==2 else [float(games_list[i].get_review().difficulty)]
                finally:
                    return x+rec_operation(games_list, i + 1, op_num)

def chart():
    barwidth=0.25
    suma_recenzji= rec_operation(list(gry.values()),op_num=1)
    srednia_ocen=rec_operation(list(gry.values()),op_num=2)
    srednia_difficulty=rec_operation(list(gry.values()),op_num=3)
    r1=np.arange(len(suma_recenzji))
    r2=[x + barwidth for x in r1]
    r3=[x + barwidth for x in r2]

    plt.bar(r1,suma_recenzji,color='r',width=barwidth,edgecolor='grey',label="ilosc recenzji")
    plt.bar(r2,srednia_ocen,color='g',width=barwidth,edgecolor='grey',label="srednia wartosc ocen gry")
    plt.bar(r3,srednia_difficulty,color='b',width=barwidth,edgecolor='grey',label="srednia wartosc ocen poziomu trudnosci")

    plt.xlabel("Gra")
    plt.ylabel("Statystyki")

    plt.xticks([r + barwidth for r in range(len(suma_recenzji))],[n.nazwa for n in gry.values()])
    plt.legend()
    plt.show()
    plt.savefig("wykres.png")



def sum_ranks(x,y):
    if isinstance(x,gc.Game.Review) and isinstance(y,gc.Game.Review):
        return x.ocena+y.ocena

def sum_diff(x,y):
    if isinstance(x, gc.Game.Review) and isinstance(y, gc.Game.Review):
        return x.difficulty + y.difficulty

def print_with_separators(message=""):
    print(f"===================================\n"
          f"{message}\n"
          f"===================================")
import os

from src.Reviews import CustomException as exc

import json



## klasa glowna Game z zagniezdzona klasa Review
class Game:
    ## konstruktor
    def __init__(self, nazwa="", gatunki=None, wydawca="", producent=""):
        if gatunki is None:
            gatunki = []
        self.genre_dict = {}
        self.nazwa=nazwa.title()
        self.gatunki=set(gatunki)
        self.wydawca=wydawca.capitalize()
        self.producent=producent.capitalize()
        self.recenzje=[]

    ## wyswietlanie informacji o obiekcie
    def print_info(self):
        print("----------------------------------------------------")
        print(self.nazwa," Tworcow: ",self.producent)
        print("Gatunek/ki: ")
        for i in self.gatunki:
            print("- "+i)
        print("Wydawca: ",self.wydawca)
        print("----------------------------------------------------")
    ## dodawanie recenzji
    def add_review(self):
        czy_blad=False
        recenzent=""
        ocena=""
        difficulty=""
        opis=""
        try:
            recenzent=input("Podaj recenzenta: ")
            ocena=int(input("Podaj ocene od 0 do 10: "))
            if 0<ocena>10: raise exc.ChartRangeError(ocena,min=0,max=10)
            difficulty=int(input("od 0 do 10 podaj wedlug ciebie jak ta gra jest trudna: "))
            if 0 < difficulty >10: raise exc.ChartRangeError(difficulty,min=0,max=10)
            opis=input("Dodaj opis: ")

        except exc.ChartRangeError as e:
            czy_blad=True
            print(e)
        finally:
            if not czy_blad:
                self.recenzje.append(self.Review(recenzent, ocena, difficulty, opis))
                print("===================================")
                print("Pomyslnie dodano")
                print("===================================")

    ## wyswietlanie listy recenzji
    def print_reviews(self):
        if len(self.recenzje)==0:
            print("===================================")
            print("Gra nie ma jeszcze zadnej recenzji")
            print("===================================")
        else:
            for i in self.recenzje:
                if isinstance(i,self.Review):
                    i.print_review()
    ## metoda zwracajaca wybrana recenzje
    def get_review(self,i):
        try:
           result=self.recenzje[i]
           if isinstance(result,self.Review):
               return result
           return None
        except IndexError:
            print("===================================")
            print(f" twoj indeks {i} jest poza zasiegiem")
            print("===================================")
            return None


    ## settery
    def set_name(self,new_name):
        self.nazwa=new_name

    def set_genres(self):
        if len(self.gatunki)==0:
            self.gatunki=self.generate_genres()
        else:
            while True:
                for i in self.gatunki:
                    print(i)
                res = input("Podaj nazwe gatunku, ktorego chcesz zmodyfikowac\n(dodatkowo 1: wszystko, 0:anuluj): ")
                if res == "1":
                    self.gatunki=self.generate_genres()
                elif res=="0":
                    break
                elif not res in self.gatunki:
                    print("Nie znaleziono gatunku w liscie")
                    break
                else:
                    self.gatunki.discard(res)
                    inp=input("Zamien "+res+" na: ")
                    self.gatunki.add(inp.title())

    def set_producer(self,new_producer):
        self.producent=new_producer.capitalize()

    def set_publisher(self,new_publisher):
        self.wydawca=new_publisher.capitalize()

    def generate_genres(self):
        gatunki = set()
        print("Dodaj nowe gatunki do twojej gry('end' oznacza koniec): ")
        l = input("Gatunek " + str(len(gatunki)) + ": ")

        while l!="end":
            gatunki.add(l)
            l = input("Gatunek " + str(len(gatunki)) + ": ")
        return gatunki

    ##modyfikacja obiektu gry
    def mod_game(self):
        try:
            while True:
                self.print_info()
                print("1: zmien nazwe\n"
                      "2: zmien producenta\n"
                      "3: zmien gatunki\n"
                      "4: zmien wydawce\n"
                      "0: wstecz")
                result=int(input("Wybor: "))

                if result==1:
                    self.set_name(input("Podaj nowa nazwe gry: "))
                elif result==2:
                    self.set_producer(input("Podaj nowego producenta: "))
                elif result==3:
                    self.set_genres()
                elif result==4:
                    self.set_publisher(input("Podaj nowego wydawce: "))
                elif result==0:
                    break
                else:
                    raise exc.ChartRangeError(result,min=1,max=4)
        except exc.ChartRangeError as e:
            print(e)

    ## usuwanie recenzji
    def delete_review(self):
        try:
            if len(self.recenzje)==0:
                print("===================================")
                print("Gra nie ma jeszcze zadnej recenzji")
                print("===================================")
            else:
                self.print_reviews()
                index=int(input("Podaj indeks w liscie recenzji do usuniecia: "))
                if 0<index>=len(self.recenzje):
                    raise exc.ChartRangeError(index,min=0,max=len(self.recenzje)-1)
                else:
                    self.recenzje.pop(index)
                    print("===================================")
                    print("Pomyslnie usunieto")
                    print("===================================")
        except exc.ChartRangeError as e:
            print(e)

    ##modyfikacja recenzji
    def change_review(self):
        try:
            if len(self.recenzje)==0:
                print("===================================")
                print("Gra nie ma jeszcze zadnej recenzji")
                print("===================================")
            else:
                self.print_reviews()
                index=int(input("Podaj indeks w liscie recenzji do modyfikacji: "))
                if 0<index>=len(self.recenzje):
                    raise exc.ChartRangeError(index,min=0,max=len(self.recenzje)-1)
                else:
                    self.get_review(index).change_rev()

        except exc.ChartRangeError as e:
            print(e)

    def genre_to_dict(self):
        dictionary={}
        for genre in self.gatunki:
            dictionary["Gatunek "+str(len(dictionary)+1)]=genre
        return dictionary

    def reviews_to_dict(self):
        review_dict = {}
        for i in range(len(self.recenzje)):
            review_dict["Recenzja " + str(i+1)] = self.get_review(i).to_dict()
        return review_dict

    def save_to_JSON(self):
        dictionary= {"Nazwa": self.nazwa,"Producent":self.producent,"Wydawca":self.wydawca,"Gatunki: ":self.genre_to_dict(),"Recenzje":self.reviews_to_dict()}

        with open(os.path.join("pliki_json",self.nazwa+".json"),"w") as file:
            file.write(json.dumps(dictionary,indent=4))
            file.close()
            print("===================================")
            print("Gra z recenzjami pomyslnie zapisano do pliku: "+self.nazwa+".json")
            print("===================================")
    def average_ranks(self,x,y):
            if isinstance(x,self.Review) and isinstance(y,self.Review):
                return x.ocena+y.ocena



    ## zagniezdzona klasa review
    class Review:
        def __init__(self, recenzent="",ocena=0,difficulty=0,opis=""):
            self.recenzent = recenzent.title()
            self.ocena=ocena
            self.difficulty=difficulty
            self.opis=opis


        def print_review(self):
            print("------------------------------------")
            print("Recenzja zrobiona przez: ",self.recenzent)
            print("ocena: ",self.ocena)
            print("Ocena trudnosci recenzonowanej gry: ",self.difficulty)
            print("opis: \n",self.opis)
            print("------------------------------------")

        def change_recenzent(self,nowy_recenzent):
            self.recenzent=nowy_recenzent.title()
        def change_ocena(self,new_ocena):
            try:
                if 0<new_ocena>10:
                    raise exc.ChartRangeError(new_ocena,min=0,max=10)
                else:
                    self.ocena=new_ocena
            except exc.ChartRangeError as e:
                print(e)

        def change_difficulty(self,new_dif):
            try:
                if 0 < new_dif > 10:
                    raise exc.ChartRangeError(new_dif, min=0, max=10)
                else:
                    self.difficulty = new_dif
            except exc.ChartRangeError as e:
                print(e)

        def change_opis(self,new_opis):
            self.opis=new_opis

        def change_rev(self):
            try:
                while True:
                    self.print_review()
                    print("1: Zmien recenzenta\n"
                          "2: zmien ocene\n"
                          "3: zmien ocene trudnosci\n"
                          "4: daj nowy opis\n"
                          "0: wstecz")
                    result=int(input("Wybor: "))
                    if result == 1:
                        self.change_recenzent(input("Podaj innego recenzenta: "))
                    elif result == 2:
                        self.change_ocena(int(input("Podaj nowa ocene (od 0 do 10): ")))
                    elif result == 3:
                        self.change_difficulty(int(input("Podaj nowa ocene (od 0 do 10): ")))
                    elif result == 4:
                        self.change_opis(input("Daj nowy opis: "))
                    elif result==0:
                        break
                    else:
                        raise exc.ChartRangeError(result, min=1, max=4)
            except exc.ChartRangeError as e:
                print(e)

        def to_dict(self):
            dictionary={"Recenzent":self.recenzent,
                        "Ocena gry": str(self.ocena),
                        "Ocena trudnosci": str(self.difficulty),
                        "Opis":self.opis}
            return dictionary



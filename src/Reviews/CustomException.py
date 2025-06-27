class ChartRangeError(Exception):
    def __init__(self,number,msg="Twoj numer nie miesci sie w zakresie wyboru. ",min=0,max=1):
        self.number=number
        self.msg=msg
        self.min=min
        self.max=max
        super().__init__(self.msg)
    def __str__(self):
        print("===================================")
        return f'{self.number} -> {self.msg}Powinien byc pomiedzy {self.min} a {self.max}.'


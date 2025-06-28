class ChartRangeError(Exception):
    def __init__(self,number,msg="Twoj numer nie miesci sie w zakresie wyboru. ",min=0,max=1):
        self.number=number
        self.msg=msg
        self.min=min
        self.max=max
        super().__init__(self.msg)
    def __str__(self):
        print("===================================")
        return f'{self.number} -> {self.msg}Powinien byc pomiedzy w zakresie {self.min}/{self.max}.'

class TerminateProgram(Exception):
    def __init__(self,msg="Terminacja programu!"):
        self.msg=msg
        super().__init__(self.msg)
    def __str__(self):
        return self.msg


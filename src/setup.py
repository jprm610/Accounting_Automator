import os

class Setup :
    @classmethod
    def main(cls, first_run=False) -> None :
        if first_run :
            os.system("pip install -r requirements.txt")

        try :
            os.mkdir('data')
        except :
            pass

        return
        

import os
from parameters import Parameters

class Setup :
    @classmethod
    def main(cls, first_run=False) -> None :
        if first_run :
            os.system("pip install -r requirements.txt")

        try :
            os.mkdir(Parameters.EXPORT_PATH)
        except :
            pass

        return
        

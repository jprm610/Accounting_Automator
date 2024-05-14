import pandas as pd
from parameters import Parameters

class Debt :
    DEBTS_DF = None
    DEBTS = []
    def __init__(self, deudor, acreedor, valor) -> None :
        self.deudor = deudor
        self.acreedor = acreedor
        self.valor = valor
        Debt.DEBTS.append(self)

        return
    
    def invert(self) -> None :
        self.deudor, self.acreedor = self.acreedor, self.deudor
        self.valor = -self.valor

        return
    
    def add(self, amount) -> None :
        self.valor += amount

        return
    
    def substract(self, amount) -> None :
        self.valor -= amount
        if self.valor < 0 :
            self.invert()

        return
    
    def toString(self) -> str:
        return f"{self.deudor} -> {self.acreedor} ${self.valor}"
    
    @classmethod
    def main(cls) :
        Debt.generateDebts()
        Debt.export()

        return
    
    @classmethod
    def debtExists(cls, deudor, acreedor) :
        for debt in Debt.DEBTS :
            if debt.deudor == deudor and debt.acreedor == acreedor :
                return debt
        
        return None

    @classmethod
    def generateDebtsDf(cls, transactions_df: pd.DataFrame) -> None :
        Debt.DEBTS_DF = transactions_df[transactions_df['DEUDOR'] != '.']
        
        return
    
    @classmethod
    def generateDebts(cls) -> None :
        for _, row in Debt.DEBTS_DF.iterrows() :
            # Si el deudor es CRUCE, se toma como una deuda "invertida" para cancelar la deuda
            if row['DEUDOR'] == 'CRUCE' :
                debt = Debt.debtExists(row['DESTINO'], row['ORIGEN'])
                if debt != None :
                    debt.substract(row['VALOR'])
                else :
                    Debt(row['DESTINO'], row['ORIGEN'], row['VALOR'])
            else :
                debt = Debt.debtExists(row['DEUDOR'], row['ORIGEN'])
                if debt != None :
                    debt.add(row['VALOR'])
                else :
                    Debt(row['DEUDOR'], row['ORIGEN'], row['VALOR'])
        
        return
    
    @classmethod
    def export(cls) -> None :
        a = [debt.__dict__ for debt in Debt.DEBTS]
        debts = pd.DataFrame(a)
        debts.columns = ['DEUDOR', 'ACREEDOR', 'VALOR']
        debts.to_csv(Parameters.EXPORT_PATH / 'CRUCE CUENTAS.csv', index=False)
        Debt.DEBTS_DF.to_csv(Parameters.EXPORT_PATH / 'DEUDAS.csv', index=False)
        print('Se exportó la deuda.')

        return

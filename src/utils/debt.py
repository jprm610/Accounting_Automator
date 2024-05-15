import pandas as pd
from parameters import Parameters

class Debt :
    DEBTS_DF = None
    DEBTS = []
    def __init__(self, deudor: str, acreedor: str, valor: int) -> None :
        self.deudor = deudor
        self.acreedor = acreedor
        self.valor = valor
        Debt.DEBTS.append(self)
        self.normalize()

        return
    
    def invert(self) -> None :
        self.deudor, self.acreedor = self.acreedor, self.deudor
        self.valor = -self.valor

        return
    
    def normalize(self) -> None :
        if self.valor == 0 :
            Debt.DEBTS.remove(self)
            return

        if self.valor < 0 :
            self.invert()
        
        return
    
    def add(self, amount) -> None :
        self.valor += amount
        self.normalize()

        return
    
    def substract(self, amount) -> None :
        self.valor -= amount
        self.normalize()

        return
    
    def toString(self) -> str:
        return f"{self.deudor} -> {self.acreedor} ${self.valor}"
    
    @classmethod
    def main(cls) :
        Debt.addDebts()
        Debt.generateDebts()
        Debt.simplifyDebt()
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
                    debt.add(row['VALOR'])
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
    def simplifyDebt(cls) :
        for debt in Debt.DEBTS :
            debt_inverted = Debt.debtExists(debt.acreedor, debt.deudor)
            if debt_inverted != None :
                debt.substract(debt_inverted.valor)
                Debt.DEBTS.remove(debt_inverted)
        
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
    
    @classmethod
    def addDebts(cls) :
        add_debts = input('Quiere agregar deudas? (s/n): ')
        if add_debts in 'sS' :
            while True :
                print('Agregue una deuda o 0 para terminar.')
                deudor = input('Deudor: ')
                if deudor == '0' :
                    break
                acreedor = input('Acreedor: ')
                valor = int(input('Valor: '))
                Debt(deudor, acreedor, valor)

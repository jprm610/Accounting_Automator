import pandas as pd
from parameters import Parameters

class Debt :
    # Class attributes
    # DEBTS_DF: DataFrame with the debts. \\
    # DEBTS: List with the debts objects. \\
    DEBTS_DF = None
    DEBTS = []
    def __init__(self, deudor: str, acreedor: str, valor: int) -> None :
        """
        @deudor: Deudor de la deuda. \\
        @acreedor: Acreedor de la deuda. \\
        @valor: Valor de la deuda. \\
        
        Creates a debt object with the debtor, creditor and value, and add the debt to the DEBTS list.
        """
        self.deudor = deudor
        self.acreedor = acreedor
        self.valor = valor
        Debt.DEBTS.append(self)
        self.normalize()

        return
    
    def invert(self) -> None :
        """
        Invert the debt. 
        """

        # Invert the debtor and creditor and change the value sign
        self.deudor, self.acreedor = self.acreedor, self.deudor
        self.valor = -self.valor

        return
    
    def normalize(self) -> None :
        """
        Normalize the debt.
        """

        # If the value is 0, remove the debt
        if self.valor == 0 :
            Debt.DEBTS.remove(self)
            return

        # If the value is negative, invert the debt
        if self.valor < 0 :
            self.invert()
        
        return
    
    def add(self, amount) -> None :
        """
        @amount: Amount to add to the debt. \\
        Add the amount to the debt and normalize the debt.
        """

        self.valor += amount
        self.normalize()

        return
    
    def substract(self, amount) -> None :
        """
        @amount: Amount to substract from the debt. \\
        Substract the amount from the debt and normalize the debt.
        """

        self.valor -= amount
        self.normalize()

        return
    
    @classmethod
    def main(cls) :
        """
        Process for creating the debts and exporting the debts.
        """

        Debt.addDebts()
        Debt.generateDebts()
        Debt.simplifyDebt()
        Debt.export()

        return
    
    @classmethod
    def debtExists(cls, deudor, acreedor) :
        """
        @deudor: Debtor. \\
        @acreedor: Creditor. \\
        Returns the debt object if the debt exists, otherwise returns None.
        """

        for debt in Debt.DEBTS :
            if debt.deudor == deudor and debt.acreedor == acreedor :
                return debt
        
        return None

    @classmethod
    def generateDebtsDf(cls, transactions_df: pd.DataFrame) -> None :
        """
        @transactions_df: Transactions dataframe. \\
        Generate the debts dataframe.
        """

        # Filter the transactions with debtors
        Debt.DEBTS_DF = transactions_df[transactions_df['DEUDOR'] != '.']
        
        return
    
    @classmethod
    def generateDebts(cls) -> None :
        """
        Generate the debts from the DEBTS_DF dataframe.
        """

        # Iterate over the debts dataframe
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
        """
        Simplify the debts. \\
        """

        # Iterate over the debts
        for debt in Debt.DEBTS :
            # Check if the inverted debt exists
            debt_inverted = Debt.debtExists(debt.acreedor, debt.deudor)
            if debt_inverted != None :
                # If the inverted debt exists, substract the debt value from the original debt 
                # and remove the inverted debt.
                debt.substract(debt_inverted.valor)
                Debt.DEBTS.remove(debt_inverted)
        
        return
    
    @classmethod
    def export(cls) -> None :
        """
        Export the debts to a csv file.
        """

        # Create a dataframe with the debts and export it
        debts = pd.DataFrame([debt.__dict__ for debt in Debt.DEBTS])
        debts.columns = ['DEUDOR', 'ACREEDOR', 'VALOR']
        debts.to_csv(Parameters.EXPORT_PATH / 'CRUCE CUENTAS.csv', index=False)
        Debt.DEBTS_DF.to_csv(Parameters.EXPORT_PATH / 'DEUDAS.csv', index=False)
        print('Se exportó la deuda.')

        return
    
    @classmethod
    def addDebts(cls) :
        """
        Add debts manually.
        """

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

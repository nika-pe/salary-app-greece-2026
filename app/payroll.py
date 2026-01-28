class PayrollCalculator: 
    def __init__(self, gross): 
        self.gross = gross 
    def calculate_net(self): 
        efka = self.gross * 0.16 
        tax = self.gross * 0.22 
        return round(self.gross - efka - tax, 2) 

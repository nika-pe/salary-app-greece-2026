class PayrollCalculator:
    def __init__(self, gross, children=0):
        # Превращаем в float на случай, если пришла строка
        self.gross = float(gross)
        self.children = int(children)
        # В Греции налог считается от годового дохода (14 зарплат)
        self.months = 14 

    def calculate_efka(self):
        """Взносы в соцстрах (EFKA) ~13.87% в 2026 году"""
        return round(self.gross * 0.1387, 2)

    def calculate_income_tax(self, taxable_monthly):
        """Расчет прогрессивного налога с учетом налогового вычета"""
        annual_taxable = taxable_monthly * self.months
        
        # Налоговые чешуйки (brackets)
        brackets = [
            (10000, 0.09),
            (20000, 0.22),
            (30000, 0.28),
            (40000, 0.36),
            (float('inf'), 0.44)
        ]
        
        total_annual_tax = 0
        previous_limit = 0
        
        for limit, rate in brackets:
            if annual_taxable > previous_limit:
                taxable_in_bracket = min(annual_taxable, limit) - previous_limit
                total_annual_tax += taxable_in_bracket * rate
                previous_limit = limit
            else:
                break
        
        # Налоговая скидка (Tax Credit) зависит от детей
        # Примерные значения: 0 детей = 777€, 1 реб = 810€, 2 реб = 900€
        credits = {0: 777, 1: 810, 2: 900, 3: 1120}
        tax_credit = credits.get(self.children, 1340) # 1340 для 4+ детей
        
        # Итоговый годовой налог не может быть меньше 0
        final_annual_tax = max(0, total_annual_tax - tax_credit)
        
        # Возвращаем налог в месяц
        return round(final_annual_tax / self.months, 2)

    def calculate_net(self):
        """Главный метод для получения чистой зарплаты"""
        efka = self.calculate_efka()
        # Налог берется с суммы ПОСЛЕ вычета EFKA
        taxable_income = self.gross - efka
        tax = self.calculate_income_tax(taxable_income)
        
        net = self.gross - efka - tax
        
        # Возвращаем словарь, чтобы в API было удобно забирать все цифры сразу
        return {
            "gross": round(self.gross, 2),
            "efka": efka,
            "tax": tax,
            "tax_rate": round((tax / self.gross) * 100, 1) if self.gross > 0 else 0,
            "net": round(net, 2),
            "annual_net": round(net * self.months, 2)
        }
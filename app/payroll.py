class PayrollCalculator:
    def __init__(self, gross, children=0, age=0):
        # Инициализация с учетом возраста для новых правил 2026
        self.gross = float(gross)
        self.children = int(children)
        self.age = int(age)
        self.months = 14 

    def calculate_efka(self):
        """Взносы в соцстрах (EFKA) — 16% согласно твоим требованиям 2026"""
        return round(self.gross * 0.16, 2)

    def calculate_income_tax(self, taxable_monthly):
        """Новая логика: 0% для молодежи и скидки за детей"""
        # 1. Спецспособность: Игрок моложе 25 лет налоги не платит
        if self.age <= 25:
            return 0.0
        
        # 2. Базовая ставка 17% (упрощаем прогрессивную шкалу по твоему запросу)
        base_rate = 0.17
        
        # 3. Множитель: Налоговая скидка 2% за каждого ребенка
        child_discount = self.children * 0.02
        final_rate = max(0, base_rate - child_discount)
        
        annual_taxable = taxable_monthly * self.months
        total_annual_tax = annual_taxable * final_rate
        
        return round(total_annual_tax / self.months, 2)

    def calculate_net(self):
        """Главный метод для получения чистой зарплаты"""
        efka = self.calculate_efka()
        taxable_income = self.gross - efka
        tax = self.calculate_income_tax(taxable_income)
        
        net = self.gross - efka - tax
        
        return {
            "gross": round(self.gross, 2),
            "efka": efka,
            "tax": tax,
            "tax_rate": round((tax / self.gross) * 100, 1) if self.gross > 0 else 0,
            "net": round(net, 2),
            "annual_net": round(net * self.months, 2)
        }
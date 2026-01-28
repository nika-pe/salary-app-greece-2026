# app/models/payroll.py

class PayrollCalculator:
    """
    Класс для выполнения подробных расчетов греческой заработной платы.
    """
    
    # --- Константы Греции (Упрощенные) ---
    EFKA_RATE = 0.16 # Отчисления работника (16%)
    TAX_RATE = 0.20  # Упрощенная ставка налога (для примера)
    
    # Расчетные коэффициенты для 14-ти зарплат в год (12 + 2 бонуса)
    MONTHS_PER_YEAR = 12
    PAYMENTS_PER_YEAR = 14
    
    def __init__(self, gross_salary: float, contract_type: str = 'full-time'):
        """
        Инициализация калькулятора.
        
        Args:
            gross_salary (float): Ежемесячная Брутто-зарплата.
            contract_type (str): Тип контракта ('full-time', 'part-time', 'freelance').
        """
        self.gross_salary = gross_salary
        self.contract_type = contract_type.lower()
        self.results = {}

    def _calculate_deductions(self):
        """Расчет обязательных вычетов (EFKA, Tax)."""
        
        # 1. Отчисления EFKA (часть работника)
        efka_contribution = round(self.gross_salary * self.EFKA_RATE, 2)
        
        # 2. Налогооблагаемый доход (Gross - EFKA)
        taxable_income = self.gross_salary - efka_contribution
        
        # 3. Налог (Упрощенно: 20% от облагаемого дохода)
        tax_amount = round(taxable_income * self.TAX_RATE, 2)
        
        # Сохраняем промежуточные результаты
        self.results.update({
            "efka_contribution": efka_contribution,
            "taxable_income": taxable_income,
            "tax_amount": tax_amount,
        })
        
        # Возвращаем общую сумму вычетов
        return efka_contribution + tax_amount

    def _calculate_bonuses(self):
        """
        Расчет бонусов (отпускные, больничные).
        В Греции отпускные и бонусы обычно распределяются в виде 13-й и 14-й зарплаты
        (Пасха, Лето, Рождество). Здесь мы упрощенно добавим их как часть ежемесячной
        зарплаты, чтобы соответствовать вашему исходному выводу.
        
        Расчет 13-й и 14-й зарплаты: 
        (2 * Gross Salary) / 14 месяцев - это приблизительная ежемесячная доля бонусов
        """
        # Ежемесячная доля отпускных/бонусов: Gross / 6 (для 13-й и 14-й)
        vacation_pay_accrual = round(self.gross_salary / 6, 2)
        
        # Доля больничных (Sick Pay) - здесь мы просто используем примерное значение,
        # так как точный расчет зависит от страховых выплат.
        sick_pay_accrual = round(self.gross_salary / 10, 2) # Упрощенно 10% от Gross
        
        self.results.update({
            "vacation_pay_accrual": vacation_pay_accrual,
            "sick_pay_accrual": sick_pay_accrual,
        })
        
        # Возвращаем общую сумму начислений
        return vacation_pay_accrual + sick_pay_accrual
        
    def calculate_net(self) -> dict:
        """
        Основной метод расчета Чистой зарплаты.
        """
        # 1. Сброс и базовая информация
        self.results = {
            "gross_salary": self.gross_salary,
            "contract_type": self.contract_type,
            "tfr_contribution": 0.00, # TFR пока 0
        }
        
        # 2. Расчет вычетов (EFKA, Tax)
        total_deductions = self._calculate_deductions()
        
        # 3. Расчет начислений (Отпускные, Больничные) - как часть "Adjusted Gross"
        total_accruals = self._calculate_bonuses()
        
        # 4. Расчет Чистой зарплаты (Net Salary)
        # Net Salary = Gross Salary - Deductions + Accruals
        net_salary = round(
            self.gross_salary - total_deductions + total_accruals, 
            2
        )
        
        # 5. Итоговый результат
        self.results["net_salary"] = net_salary
        
        # Очищаем ключи для вывода, чтобы они соответствовали вашему исходному формату (Payroll Breakdown)
        final_output = {
            "Gross Salary (€)": self.results['gross_salary'],
            "EFKA Contribution (€)": self.results['efka_contribution'],
            "Income Tax (€)": self.results['tax_amount'],
            "Vacation Pay Accrual (€)": self.results['vacation_pay_accrual'],
            "Sick Pay Accrual (€)": self.results['sick_pay_accrual'],
            "Net Salary (€)": self.results['net_salary'],
            "Contract Type": self.results['contract_type']
        }
        
        return final_output


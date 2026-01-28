import sqlite3
import os
from flask import Blueprint, render_template, request, jsonify
from app.models.payroll import PayrollCalculator 

main_bp = Blueprint('main', __name__)
DB_PATH = os.path.join(os.getcwd(), 'salary_agent.db')

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    # Создаем таблицу со всеми бухгалтерскими колонками
    conn.execute('''CREATE TABLE IF NOT EXISTS calculations 
                   (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP, 
                    gross REAL, 
                    net REAL, 
                    tax REAL, 
                    efka REAL, 
                    bonuses REAL,
                    contract_type TEXT)''')
    return conn

@main_bp.route('/', methods=['GET'])
def index():
    conn = get_db_connection()
    # Берем последние 3 записи
    history = conn.execute("SELECT * FROM calculations ORDER BY timestamp DESC LIMIT 3").fetchall()
    conn.close()
    return render_template('index.html', history=history)

@main_bp.route('/api/payroll', methods=['POST'])
def payroll_api():
    try:
        data = request.get_json()
        gross_salary = float(data.get('gross_salary', 0))
        contract_type = data.get('contract_type', 'full-time')

        calculator = PayrollCalculator(gross_salary, contract_type)
        result = calculator.calculate_net()

        conn = get_db_connection()
        conn.execute('''
            INSERT INTO calculations (gross, net, tax, efka, bonuses, contract_type) 
            VALUES (?, ?, ?, ?, ?, ?)''', 
            (
                result["Gross Salary (€)"], 
                result["Net Salary (€)"], 
                result["Income Tax (€)"], 
                result["EFKA Contribution (€)"],
                result["Vacation Pay Accrual (€)"] + result["Sick Pay Accrual (€)"],
                result["Contract Type"]
            )
        )
        conn.commit()
        conn.close()
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
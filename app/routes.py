# app/routes.py

from flask import Blueprint, render_template, request, jsonify
# Импортируем наш калькулятор из модели
from app.models.payroll import PayrollCalculator 

# --- 1. СОЗДАНИЕ BLUEPRINT (ОБЯЗАТЕЛЬНО ПЕРЕД ИСПОЛЬЗОВАНИЕМ) ---
# Blueprint - это способ структурирования приложения
main_bp = Blueprint('main', __name__)

# --- 2. Маршруты UI ---
from flask import Blueprint, render_template, request, jsonify
from app.models.payroll import PayrollCalculator

main_bp = Blueprint('main', __name__)

# Главная страница
@main_bp.route('/', methods=['GET'])
def index():
    return render_template('index.html')

# API для расчета зарплаты
@main_bp.route('/api/payroll', methods=['POST'])
def payroll_api():
    try:
        data = request.get_json()

        if not data or 'gross_salary' not in data or 'contract_type' not in data:
            return jsonify({"error": "Missing 'gross_salary' or 'contract_type'"}), 400

        gross_salary = float(data['gross_salary'])
        contract_type = data['contract_type']

        calculator = PayrollCalculator(gross_salary, contract_type)
        result = calculator.calculate_net()
        return jsonify(result)

    except ValueError:
        return jsonify({"error": "Invalid value for 'gross_salary'. Must be a number."}), 400
    except Exception as e:
        return jsonify({"error": f"Server error: {str(e)}"}), 500

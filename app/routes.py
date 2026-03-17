from flask import Blueprint, render_template, request, jsonify, send_file
from .extensions import db
from .models import Employee
from .payroll import PayrollCalculator
import io
import openpyxl  # ✅ Используем легкую замену pandas

main_bp = Blueprint('main', __name__)

# 🔹 Главная страница
@main_bp.route('/')
def index():
    history = Employee.query.order_by(Employee.id.desc()).limit(10).all()
    return render_template('index.html', history=history)

# 🔹 API: расчет зарплаты
@main_bp.route('/api/payroll', methods=['POST'])
def payroll():
    try:
        data = request.get_json(force=True)
        gross = float(data.get('gross_salary', 0))
        children = int(data.get('children', 0))
        age = int(data.get('age', 0))

        calc = PayrollCalculator(gross, children, age)
        result = calc.calculate_net()

        new_calc = Employee(
            gross_salary=gross,
            children=children,
            age=age,
            tax=result['tax'],
            net=result['net']
        )
        db.session.add(new_calc)
        db.session.commit()
        return jsonify(result)
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

# 🔹 API: экспорт в Excel (Версия без Pandas)
@main_bp.route('/api/export-excel')
def export_excel():
    try:
        results = Employee.query.all()
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Payroll 2026"

        # Заголовки
        headers = ['Gross Salary', 'Age', 'Tax', 'Net Salary', 'Date']
        ws.append(headers)

        # Данные
        for r in results:
            ws.append([
                float(r.gross_salary), 
                r.age, 
                float(r.tax), 
                float(r.net), 
                r.created_at.strftime("%Y-%m-%d %H:%M") if r.created_at else ""
            ])

        output = io.BytesIO()
        wb.save(output)
        output.seek(0)

        return send_file(
            output,
            download_name="payroll_2026.xlsx",
            as_attachment=True,
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500
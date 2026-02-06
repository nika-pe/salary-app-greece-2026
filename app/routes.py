from flask import Blueprint, render_template, request, jsonify, send_file
from .extensions import db
from .models import Employee
from .payroll import PayrollCalculator
import pandas as pd
import io

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    # Берем последние 10 записей
    history = Employee.query.order_by(Employee.id.desc()).limit(10).all()
    return render_template('index.html', history=history)

@main_bp.route('/api/payroll', methods=['POST'])
def payroll():
    data = request.json
    try:
        gross = float(data.get('gross_salary', 0))
        children = int(data.get('children', 0))
        
        calc = PayrollCalculator(gross, children)
        res = calc.calculate_net() # Возвращает словарь {efka, tax, net, annual_net, tax_rate}

        new_calc = Employee(
            gross_salary=gross,
            children=children,
            tax=res['tax'],
            net=res['net']
        )
        db.session.add(new_calc)
        db.session.commit()

        return jsonify(res)
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@main_bp.route('/api/export-excel')
def export_excel():
    records = Employee.query.all()
    data = [{'Date': r.created_at, 'Gross': r.gross_salary, 'Tax': r.tax, 'Net': r.net} for r in records]
    df = pd.DataFrame(data)
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False)
    output.seek(0)
    return send_file(output, download_name="payroll.xlsx", as_attachment=True)
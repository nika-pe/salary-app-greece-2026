from flask import Blueprint, render_template, request, jsonify, send_file
import io
import pandas as pd
from app.extensions import db
from app.models.payroll import PayrollHistory

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    history = PayrollHistory.query.order_by(PayrollHistory.id.desc()).limit(10).all()
    return render_template('index.html', history=history)

@main_bp.route('/api/payroll', methods=['POST'])
def process_payroll():
    data = request.json
    gross = float(data.get('gross_salary', 0))
    age = int(data.get('age', 30))
    children = int(data.get('children', 0))

    # 1. EFKA (16%)
    efka = round(gross * 0.16, 2)
    taxable_income = gross - efka

    # 2. Логика 2026: Возраст < 25 и база = 0 налога. Семьям -2% за ребенка.
    if age < 25 and gross <= 835:
        tax_rate = 0
    else:
        tax_rate = 0.20 - (children * 0.02)
        if tax_rate < 0: tax_rate = 0

    tax = round(taxable_income * tax_rate, 2)
    bonuses = round(gross * 0.17, 2)
    net = round(gross - efka - tax + bonuses, 2)

    new_entry = PayrollHistory(gross=gross, age=age, children=children, 
                               efka=efka, tax=tax, bonuses=bonuses, net=net)
    db.session.add(new_entry)
    db.session.commit()

    return jsonify({'net': net, 'tax': tax, 'efka': efka, 'tax_rate': int(tax_rate*100)})

@main_bp.route('/api/export-excel')
def export_excel():
    history = PayrollHistory.query.all()
    data = [{
        "Gross": r.gross, "Age": r.age, "Children": r.children,
        "Tax": r.tax, "Net": r.net
    } for r in history]
    df = pd.DataFrame(data)
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False)
    output.seek(0)
    return send_file(output, download_name="Salary_Report_2026.xlsx", as_attachment=True)
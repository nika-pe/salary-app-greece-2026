from .extensions import db
from datetime import datetime, timezone
from sqlalchemy import Numeric


def current_period():
    return datetime.now().strftime("%Y-%m")


def utc_now():
    return datetime.now(timezone.utc)


class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    # 🔹 Данные сотрудника
    name = db.Column(db.String(100), nullable=False, default="Employee")
    age = db.Column(db.Integer, default=26)
    children = db.Column(db.Integer, default=0)
    is_active = db.Column(db.Boolean, default=True)

    # 🔹 Payroll данные (используем Numeric вместо Float)
    gross_salary = db.Column(Numeric(10, 2), nullable=False)
    net = db.Column(Numeric(10, 2))

    income_tax = db.Column(Numeric(10, 2))
    efka = db.Column(Numeric(10, 2))
    tax = db.Column(Numeric(10, 2))

    # 🔹 Период
    period = db.Column(db.String(7), default=current_period)

    # 🔹 Дата создания
    created_at = db.Column(db.DateTime, default=utc_now)

    def __repr__(self):
        return f"<Employee {self.name} - {self.period}>"
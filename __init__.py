from flask import Flask, render_template, request 
 
class PayrollCalculator: 
    def __init__(self, gross): 
        self.gross = gross 
 
    def calculate_net(self): 
        efka = self.gross * 0.16 
        tax = self.gross * 0.22 
        return round(self.gross - efka - tax, 2) 
 
def create_app(): 
    app = Flask(__name__) 
 
    @app.route("/", methods=["GET", "POST"]) 
    def index(): 
        result = None 
        details = None 
        if request.method == "POST": 
            try: 
                gross = float(request.form["gross"]) 
                calc = PayrollCalculator(gross) 
                net = calc.calculate_net() 
                efka = round(gross * 0.16, 2) 
                tax = round(gross * 0.22, 2) 
                details = {"gross": gross, "efka": efka, "tax": tax} 
                result = net 
            except: 
                result = None 
        return render_template("result.html", result=result, details=details) 
 
    return app 

from flask import*
from flask_sqlalchemy import SQLAlchemy
import os

project_dir = os.path.dirname(os.path.abspath(__file__))
database_file =  "sqlite:///{}".format( os.path.join(project_dir,'mydatabase'))

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = database_file
db = SQLAlchemy(app)


class Expense(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    date = db.Column(db.String(50), nullable=False)
    expensename = db.Column(db.String(50), nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    
@app.route('/edit', methods=['POSt'])
def edit():
    id = request.form['id']
    date = request.form['date']
    expensename = request.form['expensename']
    amount = request.form['amount']
    category = request.form['category']
    expense = Expense.query.filter_by(id=id).first()
    expense.date = date
    expense.expensename = expensename
    expense.amount = amount
    expense.category = category
    expense.date = date
    db.session.commit()
    return redirect('/expenses')

@app.route('/delete/<int:id>')
def delete(id):
    expense = Expense.query.filter_by(id=id).first()
    db.session.delete(expense)
    db.session.commit()
    return redirect('/expenses')

@app.route('/UpdateExpense/<int:id>')
def UpdateExpense(id):
    expense = Expense.query.filter_by(id=id).first()
    return render_template("UpdateExpense.html",expense=expense)
    

@app.route('/expenses')
def expenses():
    expenses = Expense.query.all()
    total = 0
    t_Business = 0
    t_Food = 0
    t_Others = 0
    t_Entertainment = 0
    for expense in expenses:
        total+= expense.amount
        if expense.category == "Business":
            t_Business += expense.amount
    
        elif expense.category == "Food":
            t_Food += expense.amount

        elif expense.category == "Others":
            t_Others += expense.amount

        elif expense.category == "Entertainment":
            t_Entertainment += expense.amount
    
    
    
    return render_template('expenses.html', expenses=expenses, total=total, t_Business=t_Business, t_Food=t_Food, t_Others=t_Others, t_Entertainment=t_Entertainment)


@app.route('/')
def add():
    return render_template('app.html')

@app.route('/addexpense', methods=['POST'])
def addexpense():
    date = request.form['date']
    expensename = request.form['expensename']
    amount = request.form['amount']
    category = request.form['category']
    print(date+ " "+ expensename+ " "+ amount+ " "+ category)
    expense = Expense(date=date, expensename=expensename, amount=amount, category=category)
    db.session.add(expense)
    db.session.commit()
    return redirect('/expenses')


if __name__ == '__main__':
    app.run()
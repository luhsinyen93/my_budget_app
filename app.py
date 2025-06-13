
from flask import Flask, render_template, request, redirect, url_for
import budget_logic
from budget_logic import plot_expense_charts
from datetime import datetime
import random

app = Flask(__name__)

income_categories = ['薪資收入',
                    '投資獲利',
                    '資產出售',
                    '退稅金額',
                    '其他']
expense_categories = ['飲食',
                     '服裝',
                     '住房',
                     '交通',
                     '教育',
                     '娛樂',
                     '稅捐',
                     '其他']

@app.route('/', methods=['GET', 'POST'])
def index():
    selected_type = request.form.get('type')
    threshold_input = request.form.get('threshold')
    categories = []

    # 如果提交 threshold，設定它
    if threshold_input:
        try:
            budget_logic.set_threshold(int(threshold_input))
        except ValueError:
            pass  # 忽略錯誤輸入

    # 根據所選類型更新分類
    if selected_type == '收入':
        categories = income_categories
    elif selected_type == '支出':
        categories = expense_categories

    # 顯示目前交易、餘額與警戒線
    transactions = budget_logic.get_all_transactions()
    balance = budget_logic.get_balance()
    threshold = budget_logic.get_threshold()
    alert = budget_logic.check_budget_alert()
    today = datetime.today().strftime("%Y-%m-%d")

    return render_template('index.html',
                           selected_type=selected_type,
                           categories=categories,
                           transactions=transactions,
                           balance=balance,
                           amount='',
                           threshold=threshold,
                           alert=alert,
                           income_categories=income_categories,
                           expense_categories=expense_categories,
                           today=today)

@app.route('/add', methods=['POST'])
def add():
    date = request.form['date']
    type_input = request.form['type']
    category = request.form['category']

    try:
        amount = int(float(request.form['amount']))
    except ValueError:
        return redirect(url_for('index'))

    budget_logic.add_transaction(date, type_input, category, amount)

    # 🟡 ➤ 確保 balance 會更新
    budget_logic.process_transactions()

    return redirect(url_for('index'))

@app.route('/delete/<int:index>', methods=['POST'])
def delete(index):
    budget_logic.delete_transaction(index)
    return redirect(url_for('index'))

@app.route('/edit/<int:index>', methods=['POST'])
def edit(index):
    date = request.form['date']
    category = request.form['category']
    try:
        amount = int(float(request.form['amount']))
    except ValueError:
        return redirect(url_for('index'))

    new_data = {
        "date": date,
        "category": category,
        "amount": amount
    }

    budget_logic.edit_transaction(index, new_data)
    return redirect(url_for('index'))

@app.route('/pie')
def pie():
    category_summary = budget_logic.get_category_summary()
    if not category_summary:
        return "目前沒有支出資料，無法繪圖"
    plot_expense_charts(category_summary)
    return render_template('pie.html', random=random.random)

@app.route('/bar')
def bar():
    category_summary = budget_logic.get_category_summary()
    if not category_summary:
        return "目前沒有支出資料，無法繪圖"
    plot_expense_charts(category_summary)
    return render_template('bar.html', random=random.random)

@app.route('/daily')
def daily():
    category_summary = budget_logic.get_category_summary()
    if not category_summary:
        return "目前沒有支出資料，無法繪圖"
    plot_expense_charts(category_summary)
    return render_template('daily.html', random=random.random)

@app.route('/daily_balance')
def daily_balance():
    category_summary = budget_logic.get_category_summary()
    if not category_summary:
        return "目前沒有支出資料，無法繪圖"
    
    plot_expense_charts(category_summary)
    return render_template('daily_balance.html', random=random.random)




if __name__ == '__main__':
    app.run(debug=True)

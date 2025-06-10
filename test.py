'''
from budget_logic import plot_expense_charts  # 把這行改成你函式定義的檔案名稱
import os

# 測試用 category_summary 範例資料
category_summary = {
    '餐飲': [{'date': '2025-06-01', 'type': '支出', 'category': '餐飲', 'amount': 500}],
    '交通': [{'date': '2025-06-02', 'type': '支出', 'category': '交通', 'amount': 200}],
    '薪水': [{'date': '2025-06-03', 'type': '收入', 'category': '薪水', 'amount': 30000}],
}

# 確保 static 資料夾存在
os.makedirs('static', exist_ok=True)

result = plot_expense_charts(category_summary, pie_path="static/pie_test.png", bar_path="static/bar_test.png")

if result:
    print("圖表已成功生成，請查看 static/pie_test.png 和 static/bar_test.png")
else:
    print("沒有支出資料，未生成圖表")
'''

# plot_test.py
# 這是用於測試 financial_app_logic.py 中繪圖功能的腳本

# 確保 budget_logic.py 在相同的目錄下，或者在 Python 路徑中
import os
from datetime import datetime
from budget_logic import (
    add_transaction,
    delete_all_transactions,
    process_transactions,
    get_balance,
    get_all_transactions,
    get_current_month,
    get_monthly_summary,
    get_category_summary,
    plot_expense_charts,
    set_threshold,
    check_budget_alert,
    get_threshold
)

def run_plot_test():
    """
    執行測試，包括新增交易、處理數據並生成圖表。
    """
    print("--- 開始繪圖功能測試 ---")

    # 確保 static 目錄存在，用於保存圖片
    output_dir = "static"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"已創建目錄: {output_dir}")

    # 清空所有舊的交易紀錄，確保測試的純淨性
    delete_all_transactions()
    print("已清空所有舊的交易紀錄。")

    # --- 新增範例交易資料 ---
    print("\n新增範例交易資料...")
    add_transaction("2025-06-01", "支出", "餐飲", 150)
    add_transaction("2025-06-02", "收入", "薪資", 50000)
    add_transaction("2025-06-03", "支出", "交通", 80)
    add_transaction("2025-06-04", "支出", "餐飲", 250)
    add_transaction("2025-06-05", "支出", "娛樂", 300)
    add_transaction("2025-06-06", "支出", "交通", 120)
    add_transaction("2025-06-07", "支出", "餐飲", 100)
    add_transaction("2025-05-20", "支出", "房屋租金", 15000) # 上個月的交易
    add_transaction("2025-05-25", "收入", "兼職", 10000) # 上個月的交易
    add_transaction("2025-06-08", "支出", "生活用品", 400)
    add_transaction("2025-06-08", "支出", "娛樂", 500)
    add_transaction("2025-06-08", "支出", "餐飲", 80)

    # 確保所有交易資料都已處理
    process_transactions()

    print("\n--- 當前財務概況 ---")
    print(f"總餘額: {get_balance()}")
    print(f"當前月份 ({datetime.now().strftime('%Y-%m')}) 交易數量: {len(get_current_month())}")
    
    print("\n--- 各類別支出總結 ---")
    category_summary = get_category_summary()
    expense_details = {k: sum(tx['amount'] for tx in v if tx['type'] == '支出') for k, v in category_summary.items()}
    # 過濾掉支出為 0 的類別，只顯示有支出的
    expense_details = {k: v for k, v in expense_details.items() if v > 0}
    for category, total in expense_details.items():
        print(f"  {category}: {total}")

    # --- 生成圖表 ---
    print("\n生成支出分析圖表 (圓餅圖 & 長條圖)...")
    pie_chart_path = os.path.join(output_dir, "pie_chart_test.png")
    bar_chart_path = os.path.join(output_dir, "bar_chart_test.png")

    # 呼叫繪圖函數
    success = plot_expense_charts(category_summary, pie_path=pie_chart_path, bar_path=bar_chart_path)

    if success:
        print(f"圓餅圖已儲存到: {pie_chart_path}")
        print(f"長條圖已儲存到: {bar_chart_path}")
        print("\n請檢查 'static' 資料夾查看生成的圖片。")
    else:
        print("沒有支出資料，未生成圖表。")

    # --- 測試預算警戒線 ---
    print("\n--- 測試預算警戒線 ---")
    set_threshold(1000) # 設定警戒線為 1000
    print(f"設定警戒線為: {get_threshold()}")
    if check_budget_alert():
        print("!!! 警示：您的餘額低於警戒線！")
    else:
        print("餘額正常，未觸發警戒線。")

    print("\n--- 繪圖功能測試結束 ---")

if __name__ == "__main__":
    run_plot_test()
'''
from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "Hello Flask!"

if __name__ == "__main__":
    app.run()
'''
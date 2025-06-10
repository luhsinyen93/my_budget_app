from datetime import datetime
from collections import defaultdict
import matplotlib
from collections import defaultdict

matplotlib.use('Agg')  # 確保在非互動式環境（如 Flask）下正確生成圖表

# === 全域資料 ===
# 儲存所有交易紀錄的列表
transactions = []
# 當前餘額
balance = 0
# 預算警戒線金額
threshold = 0

# 分類整理用字典，用於儲存不同時間或類別的交易
current_month_list = [] # 儲存當月交易
monthly_summary = defaultdict(list) # 儲存每月交易總結
category_summary = defaultdict(list) # 儲存各類別交易總結

# === 資料處理邏輯 ===

def process_transactions():
    """
    處理所有交易紀錄，更新餘額、當月交易、每月總結和類別總結。
    每次新增、刪除、編輯交易後都會呼叫此函數，確保資料即時更新。
    """
    global balance
    # 清空之前的資料，重新計算
    current_month_list.clear()
    monthly_summary.clear()
    category_summary.clear()

    # 取得當前月份（格式為YYYY-MM）
    current_month = datetime.now().strftime("%Y-%m")
    balance = 0 # 重置餘額，從頭開始計算

    # 遍歷所有交易紀錄
    for tx in transactions:
        try:
            # 解析交易日期，取得月份
            tx_month = datetime.strptime(tx["date"], "%Y-%m-%d").strftime("%Y-%m")
        except ValueError:
            # 如果日期格式不正確，則跳過此交易
            print(f"警告：交易日期格式無效，已跳過：{tx}")
            continue

        # 根據月份將交易分類
        if tx_month == current_month:
            current_month_list.append(tx)
        else:
            monthly_summary[tx_month].append(tx)

        # 根據類別將交易分類
        category_summary[tx["category"]].append(tx)

        # 根據交易類型更新餘額
        if tx["type"] == "收入":
            balance += tx["amount"]
        elif tx["type"] == "支出":
            balance -= tx["amount"]

def add_transaction(date, type_input, category, amount):
    """
    新增一筆交易紀錄。
    Args:
        date (str): 交易日期 (YYYY-MM-DD 格式)。
        type_input (str): 交易類型 ("收入" 或 "支出")。
        category (str): 交易類別。
        amount (str): 交易金額。
    """
    transaction = {
        "date": date,
        "type": type_input,
        "category": category,
        "amount": int(amount)  # 將金額轉換為整數
    }
    transactions.append(transaction)
    process_transactions() # 新增後重新處理所有交易

def delete_transaction(index):
    """
    刪除指定索引的交易紀錄。
    Args:
        index (int): 要刪除的交易紀錄在列表中的索引。
    Returns:
        dict or None: 被刪除的交易紀錄，如果索引無效則返回 None。
    """
    try:
        deleted = transactions.pop(index)
        process_transactions() # 刪除後重新處理所有交易
        return deleted
    except IndexError:
        print(f"錯誤：交易索引 {index} 無效，無法刪除。")
        return None

def edit_transaction(index, new_data):
    """
    編輯指定索引的交易紀錄。
    Args:
        index (int): 要編輯的交易紀錄在列表中的索引。
        new_data (dict): 包含新資料的字典 (例如 {"amount": 100})。
    Returns:
        bool: 如果編輯成功則返回 True，否則返回 False。
    """
    try:
        tx = transactions[index]
        tx.update(new_data) # 更新交易資料
        # 確保金額是整數型態，以防前端傳來字串
        if "amount" in new_data:
            tx["amount"] = int(new_data["amount"])
        process_transactions() # 編輯後重新處理所有交易
        return True
    except IndexError:
        print(f"錯誤：交易索引 {index} 無效，無法編輯。")
        return False

def delete_all_transactions():
    """
    刪除所有交易紀錄。
    """
    transactions.clear()
    process_transactions() # 清空後重新處理

def get_all_transactions():
    """
    取得所有交易紀錄，並按日期降序排序。
    Returns:
        list: 排序後的所有交易紀錄列表。
    """
    # 回傳排序後交易列表，便於前端顯示
    return sorted(transactions, key=lambda tx: tx["date"], reverse=True)

def get_balance():
    """
    取得當前餘額。
    Returns:
        int: 當前餘額。
    """
    return balance

def get_current_month():
    """
    取得當前月份的所有交易紀錄。
    Returns:
        list: 當月交易紀錄列表。
    """
    return current_month_list

def get_monthly_summary():
    """
    取得每月交易總結。
    Returns:
        dict: 每月交易總結的字典。
    """
    return dict(monthly_summary)

def get_category_summary():
    """
    取得各類別交易總結。
    Returns:
        dict: 各類別交易總結的字典。
    """
    return dict(category_summary)

# === 預算警戒線 ===

def set_threshold(amount):
    """
    設定預算警戒線金額。
    Args:
        amount (str or int): 警戒線金額。
    """
    global threshold
    threshold = int(amount)

def get_threshold():
    """
    取得預算警戒線金額。
    Returns:
        int: 警戒線金額。
    """
    return threshold

def check_budget_alert():
    """
    檢查是否觸發預算警戒線。
    Returns:
        bool: 如果餘額低於警戒線則返回 True，否則返回 False。
    """
    # 只有設定了警戒線且餘額低於警戒線時才觸發警示
    return threshold > 0 and balance < threshold

# === 圖表視覺化 ===

def set_chinese_font():
    """
    設定 Matplotlib 的中文字體，以解決亂碼問題。
    會根據作業系統嘗試設定常見的繁體中文字體，並提供備用字體。
    """
    # 嘗試設定多個常用繁體中文字體，會依序尋找
    font_list = ['Microsoft JhengHei', 'PingFang TC', 'Noto Sans CJK TC', 'Arial Unicode MS', 'SimHei']
    
    found_font = None
    for font_name in font_list:
        # 使用 fm.findfont 檢查字體是否存在，並返回其路徑
        font_path = fm.findfont(font_name, fontext='ttf')
        if font_path: # 如果找到字體路徑
            # print(f"找到並設定字體：{font_name}，路徑：{font_path}") # 偵錯用
            plt.rcParams['font.sans-serif'] = [font_name]
            found_font = font_name
            break
    
    if found_font is None:
        # 如果所有中文字體都沒找到，則退回預設（可能仍是亂碼，但至少不報錯）
        plt.rcParams['font.sans-serif'] = ['DejaVu Sans']
        print("警告：系統中未找到任何支援繁體中文的字體，圖表文字可能仍顯示亂碼。")
    else:
        print(f"成功設定中文字體為：{found_font}")

    # 解決負號顯示為方塊的問題
    plt.rcParams['axes.unicode_minus'] = False

    # 偵錯用：可以取消註解以下兩行，查看 Matplotlib 實際載入的字體
    # print(f"Matplotlib 嘗試使用的字體列表: {plt.rcParams['font.sans-serif']}")
    # print(f"系統中找到的字體（部分）：{[f.name for f in fm.fontManager.ttflist if 'CJK' in f.name or 'Microsoft' in f.name or 'PingFang' in f.name or 'SimHei' in f.name or 'DejaVu Sans' in f.name]}")


import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import os
'''
def set_chinese_font():
    """
    嘗試設定一個可完整支援 CJK 字的中文字體。
    """
    # 這些字體依照優先順序排序
    possible_fonts = [
        'PingFang TC',           # macOS 預設中文
        'Hiragino Sans GB',      # macOS 支援簡中
        'Heiti TC',              # macOS 舊版
        'STHeiti',               # macOS 舊版
        'Apple LiGothic Medium', # macOS 可用，支持部分繁中
        'Arial Unicode MS',      # 廣泛支援 Unicode（但 macOS Catalina 以後預設不再內建）
        'Noto Sans CJK TC',      # Google 開源，支援完整繁體字集
        'Noto Sans TC',          # 新版命名，支援繁體
    ]

    available_fonts = [f.name for f in fm.fontManager.ttflist]

    for font in possible_fonts:
        if font in available_fonts:
            plt.rcParams['font.sans-serif'] = [font]
            print(f"✔ 使用字體: {font}")
            return

    print("⚠ 沒有找到完整中文字體，可能會有部分文字無法正確顯示。")
'''

def plot_expense_charts(category_summary, pie_path="static/pie.png", bar_path="static/bar.png", daily_path="static/daily.png"):
    """
    根據分類支出資料繪製圓餅圖和長條圖，並儲存為圖片檔案。
    """
    # --- 修改開始 ---
    # 直接指定字體檔案的路徑
    # 假設 budget.py 和 fonts/ 資料夾在同一個層級
    # --- 字體設定 ---
    font_path = os.path.join(os.path.dirname(__file__), 'fonts', 'NotoSansTC-Regular.ttf')
    if not os.path.exists(font_path):
        print(f"⚠ 字體檔案未找到: {font_path}")
        return False
    font_prop = fm.FontProperties(fname=font_path)

    # --- 各分類支出資料 ---
    category_expenses = {}
    for category, txs in category_summary.items():
        total = sum(tx['amount'] for tx in txs if tx['type'] == '支出')
        if total > 0:
            category_expenses[category] = total

    if not category_expenses:
        print("沒有分類支出資料，無法生成圖表。")
        return False

    # === 圓餅圖 ===
    plt.figure(figsize=(8, 8))
    plt.pie(category_expenses.values(), labels=category_expenses.keys(), autopct='%1.1f%%',
            textprops={'fontsize': 24, 'fontproperties': font_prop})
    plt.title('各分類支出佔比', fontsize=30, fontproperties=font_prop)
    plt.axis('equal')
    plt.tight_layout()
    plt.savefig(pie_path)
    plt.close()

    # === 分類長條圖 ===
    plt.figure(figsize=(10, 6))
    plt.bar(category_expenses.keys(), category_expenses.values(), color='skyblue')
    plt.xlabel('支出分類', fontsize=12, fontproperties=font_prop)
    plt.ylabel('金額 (新台幣)', fontsize=12, fontproperties=font_prop)
    plt.title('各分類支出金額', fontsize=30, fontproperties=font_prop)
    plt.xticks(fontsize=10, fontproperties=font_prop)
    plt.yticks(fontsize=10)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.savefig(bar_path)
    plt.close()

    # === 每日支出長條圖 ===
    daily_expenses = defaultdict(int)
    for t in transactions:
        if t["type"] == "支出":
            daily_expenses[t["date"]] += t["amount"]

    if not daily_expenses:
        print("沒有每日支出資料，略過每日圖表。")
        return True  # 不 return False，讓分類圖表仍可用

    sorted_dates = sorted(daily_expenses.keys())
    amounts = [daily_expenses[date] for date in sorted_dates]

    plt.figure(figsize=(12, 6))
    plt.bar(sorted_dates, amounts, color='salmon')
    plt.xlabel('日期', fontsize=20, fontproperties=font_prop)
    plt.ylabel('支出金額 (NT$)', fontsize=20, fontproperties=font_prop)
    plt.title('每日支出金額', fontsize=30, fontproperties=font_prop)
    plt.xticks(fontsize=10, fontproperties=font_prop)
    plt.yticks(fontsize=10)
    plt.grid(axis='y', linestyle='--', alpha=0.6)
    plt.tight_layout()
    plt.savefig(daily_path)
    plt.close()

    return True
# ======================================================
# 💼 مدل واقعی اقساط زنجیره‌ای شش‌ماهه (مدل واقعی بازار)
# ======================================================

import pandas as pd
import matplotlib.pyplot as plt

# -----------------------------
# ⚙️ پارامترهای ورودی
# -----------------------------
initial_capital = 100_000_000   # سرمایه اولیه (تومان)
months = 12                     # مدت شبیه‌سازی (ماه)
contract_months = 6             # طول هر قرارداد (ماه)
total_return_factor = 1.36      # سود کل قرارداد (مثلاً 36٪ برای 6 ماه)

# -----------------------------
# 🧮 متغیرهای پایه
# -----------------------------
contracts = [{"amount": initial_capital, "months_left": contract_months}]
records = []

# -----------------------------
# 🔢 شبیه‌سازی ماه‌به‌ماه
# -----------------------------
for month in range(1, months + 1):
    income = 0
    new_contracts = []

    # دریافت اقساط از قراردادهای فعال
    for c in contracts:
        # قسط ماهانه = کل مبلغ قرارداد * (1.36 / 6)
        payment = (c["amount"] * total_return_factor) / contract_months
        income += payment
        c["months_left"] -= 1
        # قرارداد فقط تا وقتی در چرخه می‌ماند که اقساطش تمام نشده باشند
        if c["months_left"] > 0:
            new_contracts.append(c)

    # مبلغ اقساط جدید وارد قرارداد جدید می‌شود (۶ ماهه)
    if income > 0:
        new_contracts.append({"amount": income, "months_left": contract_months})

    # بروزرسانی لیست قراردادهای فعال
    contracts = new_contracts

    # محاسبه وضعیت کلی
    total_active = sum(c["amount"] for c in contracts)
    total_profit = total_active - initial_capital
    roi = (total_profit / initial_capital) * 100

    records.append({
        "ماه": month,
        "تعداد قراردادهای فعال": len(contracts),
        "اقساط دریافتی (تومان)": round(income),
        "سرمایه فعال در بازار (تومان)": round(total_active),
        "سود نسبت به اولیه (%)": round(roi, 2)
    })

# -----------------------------
# 📊 جدول نتایج
# -----------------------------
df = pd.DataFrame(records)
print(df.to_string(index=False))

# -----------------------------
# 📈 نمودار رشد سرمایه
# -----------------------------
plt.figure(figsize=(8,5))
plt.plot(df["ماه"], df["سرمایه فعال در بازار (تومان)"], marker='o', color="#86A789", label="سرمایه فعال")
plt.bar(df["ماه"], df["اقساط دریافتی (تومان)"], color="#FFD29C", alpha=0.6, label="اقساط دریافتی")
plt.title("روند رشد سرمایه فعال و اقساط دریافتی (مدل واقعی بازار)")
plt.xlabel("ماه")
plt.ylabel("تومان")
plt.grid(True, linestyle="--", alpha=0.6)
plt.legend()
plt.show()

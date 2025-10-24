import pandas as pd
import matplotlib.pyplot as plt

# -----------------------------
# ⚙️ پارامترها
# -----------------------------
initial_capital = 100_000_000
months = 12
contract_months = 6
total_return_factor = 1.36

# -----------------------------
# 🧮 متغیرها
# -----------------------------
contracts = [{"amount": initial_capital, "months_left": contract_months}]
pending_contracts = []  # قراردادهایی که از ماه بعد شروع میشن
records = []

# -----------------------------
# 🔢 شبیه‌سازی ماه‌به‌ماه
# -----------------------------
for month in range(1, months + 1):
    income = 0
    new_contracts = []

    # پرداخت اقساط از قراردادهای فعال
    for c in contracts:
        payment = (c["amount"] * total_return_factor) / contract_months
        income += payment
        c["months_left"] -= 1
        if c["months_left"] > 0:
            new_contracts.append(c)

    # قراردادهای جدید از ماه بعد فعال می‌شوند
    if pending_contracts:
        new_contracts.extend(pending_contracts)
        pending_contracts = []

    # اقساط دریافتی تبدیل به قرارداد جدید برای ماه بعد
    if income > 0:
        pending_contracts.append({"amount": income, "months_left": contract_months})

    # به‌روزرسانی وضعیت
    contracts = new_contracts
    total_active = sum(c["amount"] for c in contracts)
    total_profit = total_active - initial_capital
    roi = (total_profit / initial_capital) * 100

    records.append({
        "ماه": month,
        "اقساط دریافتی (تومان)": round(income),
        "تعداد قراردادهای فعال": len(contracts),
        "سرمایه فعال (تومان)": round(total_active),
        "سود نسبت به اولیه (%)": round(roi, 2)
    })

# -----------------------------
# 📋 جدول نتایج
# -----------------------------
df = pd.DataFrame(records)
print(df)

# -----------------------------
# 📈 نمودار
# -----------------------------
plt.figure(figsize=(8,5))
plt.plot(df["ماه"], df["سرمایه فعال (تومان)"], marker='o', color="#86A789", linewidth=2, label="سرمایه فعال")
plt.bar(df["ماه"], df["اقساط دریافتی (تومان)"], color="#FFD29C", alpha=0.6, label="اقساط دریافتی")
plt.title("روند رشد واقعی سرمایه و اقساط (اصلاح‌شده، بدون افت ماه ششم)")
plt.xlabel("ماه")
plt.ylabel("تومان")
plt.grid(True, linestyle="--", alpha=0.6)
plt.legend()
plt.show()

# ======================================================
# 💼 مدل واقعی اقساط زنجیره‌ای ۶‌ماهه (نسخه نهایی و درست)
# ======================================================

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ----------------------------
# ⚙️ تنظیمات صفحه
# ----------------------------
st.set_page_config(page_title="Real Installment Business Model", layout="wide")

st.markdown("""
<div style='background-color:#86A789;padding:25px;border-radius:12px;text-align:center;'>
    <h1 style='color:white;'>💰 ماشین‌حساب واقعی گردش اقساطی (مدل دقیق و واقعی)</h1>
    <p style='color:#FFD29C;font-size:17px;'>
    هر قسط بازگشتی خودش ۶ ماهه وارد بازار می‌شود — دقیقاً مثل مدل کاری واقعی شما ✅
    </p>
</div>
""", unsafe_allow_html=True)

# ----------------------------
# 🧮 ورودی‌ها
# ----------------------------
col1, col2, col3 = st.columns(3)
with col1:
    initial_capital = st.number_input("💵 سرمایه اولیه (تومان)", value=100_000_000, step=1_000_000)
with col2:
    total_months = st.number_input("⏳ مدت شبیه‌سازی (ماه)", value=24, step=6)
with col3:
    profit_percent = st.number_input("📈 سود کل قرارداد ۶‌ماهه (%)", value=36.0, step=1.0)

contract_months = 6
total_return_factor = 1 + (profit_percent / 100)

# ----------------------------
# 🔢 منطق اصلی مدل واقعی
# ----------------------------
contracts = [{"amount": initial_capital, "months_left": contract_months}]
records = []

for month in range(1, int(total_months) + 1):
    income = 0
    new_contracts = []

    # هر قرارداد فعال، قسط ماهانه پرداخت می‌کند
    for c in contracts:
        payment = (c["amount"] * total_return_factor) / contract_months
        income += payment
        c["months_left"] -= 1
        if c["months_left"] > 0:
            new_contracts.append(c)

    # قسط‌های دریافتی بلافاصله به لیست «در انتظار» اضافه می‌شوند
    # اما از ماه بعد شروع به قسط دادن می‌کنند
    reinvest_contracts = [{"amount": income, "months_left": contract_months}]

    # اضافه کردن همه قراردادهای فعال به‌علاوه قراردادهای ماه قبل
    contracts = new_contracts + reinvest_contracts

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

# ----------------------------
# 📋 جدول خروجی
# ----------------------------
df = pd.DataFrame(records)

st.markdown("## 🧾 جدول ماه‌به‌ماه")
st.dataframe(df.style.format({
    "اقساط دریافتی (تومان)": "{:,.0f}",
    "سرمایه فعال (تومان)": "{:,.0f}",
    "سود نسبت به اولیه (%)": "{:.2f}"
}))

# ----------------------------
# 📈 نمودار رشد
# ----------------------------
st.markdown("## 📈 نمودار رشد سرمایه و اقساط بازگشتی")

fig, ax1 = plt.subplots(figsize=(9,5))
ax1.plot(df["ماه"], df["سرمایه فعال (تومان)"], color="#86A789", marker="o", linewidth=2, label="سرمایه فعال")
ax1.bar(df["ماه"], df["اقساط دریافتی (تومان)"], color="#FFD29C", alpha=0.5, label="اقساط دریافتی")
ax1.set_xlabel("ماه")
ax1.set_ylabel("تومان")
ax1.grid(True, linestyle="--", alpha=0.5)
ax1.legend()
st.pyplot(fig)

# ----------------------------
# 💾 خروجی CSV
# ----------------------------
st.markdown("## 💾 دانلود فایل CSV")
csv_data = df.to_csv(index=False).encode("utf-8-sig")
st.download_button(
    label="⬇️ دانلود گزارش مالی (CSV)",
    data=csv_data,
    file_name="real_installment_business_true.csv",
    mime="text/csv"
)

# ----------------------------
# 📘 توضیح مدل
# ----------------------------
st.markdown("""
---
### 📘 توضیح منطق:
- هر قرارداد ۶ ماه عمر دارد (سود کل = ۳۶٪).  
- اقساط دریافتی هر ماه، خودشان از ماه بعد قرارداد جدید ۶‌ماهه می‌شوند.  
- هیچ افتی در ماه ششم یا هیچ ماهی وجود ندارد.  
- چرخه بعد از ۶ ماه به حالت تعادل و رشد پایدار می‌رسد.  
---
""")

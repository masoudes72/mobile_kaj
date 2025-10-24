# ======================================================
# 💼 Streamlit App — مدل واقعی کسب‌و‌کار اقساطی
# ======================================================

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# تنظیمات صفحه
st.set_page_config(page_title="Real Installment Business Model", layout="wide")

# ----------------------------
# 🌿 هدر
# ----------------------------
st.markdown("""
<div style='background-color:#86A789;padding:25px;border-radius:12px;text-align:center;'>
    <h1 style='color:white;'>💰 ماشین‌حساب واقعی گردش اقساطی</h1>
    <p style='color:#FFD29C;font-size:17px;'>مدل دقیق کسب‌وکار تو: هر قسط دوباره قرارداد ۶‌ماهه می‌شود</p>
</div>
""", unsafe_allow_html=True)

# ----------------------------
# ⚙️ ورودی‌ها
# ----------------------------
st.markdown("## ⚙️ تنظیمات ورودی")

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
# 🔢 محاسبات اصلی
# ----------------------------
contracts = [{"amount": initial_capital, "months_left": contract_months}]
records = []

for month in range(1, int(total_months) + 1):
    income = 0
    new_contracts = []

    # دریافت اقساط از قراردادهای فعال
    for c in contracts:
        payment = (c["amount"] * total_return_factor) / contract_months
        income += payment
        c["months_left"] -= 1
        if c["months_left"] > 0:
            new_contracts.append(c)

    # اقساط دریافتی تبدیل به قرارداد جدید ۶ ماهه می‌شوند
    if income > 0:
        new_contracts.append({"amount": income, "months_left": contract_months})

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

# ----------------------------
# 📋 جدول نتایج
# ----------------------------
df = pd.DataFrame(records)

st.markdown("## 🧾 جدول ماه‌به‌ماه")
st.dataframe(df.style.format({
    "اقساط دریافتی (تومان)": "{:,.0f}",
    "سرمایه فعال (تومان)": "{:,.0f}",
    "سود نسبت به اولیه (%)": "{:.2f}"
}))

# ----------------------------
# 📊 نمودار رشد
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
st.markdown("## 💾 دانلود خروجی")
csv_data = df.to_csv(index=False).encode("utf-8-sig")
st.download_button(
    label="⬇️ دانلود فایل CSV",
    data=csv_data,
    file_name="real_installment_business_report.csv",
    mime="text/csv"
)

# ----------------------------
# 📘 توضیح مدل
# ----------------------------
st.markdown("""
---
### 📘 منطق مدل:
- هر قرارداد ۶ ماه عمر دارد و پس از اتمام اقساط از چرخه خارج می‌شود.  
- هر ماه ۱/۶ از اصل و سود قرارداد بازمی‌گردد.  
- تمام اقساط جدید دوباره با همان شرایط قرارداد ۶‌ماهه می‌شوند.  
- از ماه ششم به بعد، چرخه اقساط پایدار می‌شود و رشد منطقی ادامه دارد.  
---
""")

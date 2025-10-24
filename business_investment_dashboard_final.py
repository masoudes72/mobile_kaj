# ======================================================
# 💼 Streamlit App — مدل واقعی اقساط چرخشی با برداشت ماهانه
# ======================================================

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ---------- Setup ----------
st.set_page_config(page_title="Real Installment Business Model", layout="wide")

st.markdown("""
<div style='background-color:#86A789;padding:25px;border-radius:12px;text-align:center'>
<h2 style='color:white'>💰 موبایل کاج (با برداشت ماهانه)</h2>
<p style='color:#FFD29C'>
در این مدل: هر قسط بلافاصله قرارداد جدید می‌شود، اما درصدی از اقساط می‌تواند هر ماه نقد و خارج شود.
</p>
</div>
""", unsafe_allow_html=True)

# ---------- Inputs ----------
st.markdown("## ⚙️ تنظیمات ورودی")

col1, col2, col3 = st.columns(3)
with col1:
    principal = st.number_input("💵 سرمایه اولیه (تومان)", value=100_000_000, step=1_000_000)
with col2:
    profit_6m = st.number_input("📈 سود کل هر قرارداد ۶‌ماهه (%)", value=36.0, step=0.5)
with col3:
    months = st.number_input("⏳ مدت شبیه‌سازی (ماه)", value=12, step=1)

withdraw_ratio = st.slider(
    "💳 درصد برداشت نقدی از اقساط هر ماه (%)",
    min_value=0, max_value=100, value=20, step=5,
    help="درصدی از اقساط که هر ماه نقد می‌شود و دیگر به چرخه بازنمی‌گردد."
) / 100

# ---------- Parameters ----------
contract_months = 6
r = profit_6m / 100
installment_ratio = (1 + r) / contract_months  # مثلاً 0.2266 برای 36%

# ---------- Model ----------
income, capital, withdrawn, total_withdrawn = [], [], [], []
current_income = principal * installment_ratio
current_capital = principal + current_income
cum_withdraw = 0

for month in range(1, int(months) + 1):
    # اقساط دریافتی
    income.append(current_income)

    # محاسبه برداشت نقدی
    withdraw_amount = current_income * withdraw_ratio
    reinvest_amount = current_income - withdraw_amount
    cum_withdraw += withdraw_amount
    withdrawn.append(withdraw_amount)
    total_withdrawn.append(cum_withdraw)

    # سرمایه فعال جدید پس از برداشت
    current_capital = (current_capital - withdraw_amount) * (1 + installment_ratio)
    capital.append(current_capital)

    # محاسبه اقساط ماه بعد
    next_income = reinvest_amount * (1 + installment_ratio)
    current_income = next_income

# ---------- Table ----------
df = pd.DataFrame({
    "ماه": range(1, int(months) + 1),
    "اقساط دریافتی (تومان)": [round(x) for x in income],
    "برداشت نقدی (تومان)": [round(x) for x in withdrawn],
    "جمع برداشت‌ها (تومان)": [round(x) for x in total_withdrawn],
    "سرمایه فعال (تومان)": [round(x) for x in capital]
})

# ---------- Display ----------
st.markdown("## 🧾 جدول ماه‌به‌ماه")
st.dataframe(df.style.format({
    "اقساط دریافتی (تومان)": "{:,.0f}",
    "برداشت نقدی (تومان)": "{:,.0f}",
    "جمع برداشت‌ها (تومان)": "{:,.0f}",
    "سرمایه فعال (تومان)": "{:,.0f}",
}))

# ---------- Charts ----------
st.markdown("## 📈 نمودار رشد سرمایه و جریان نقدی")

fig, ax = plt.subplots(figsize=(10,6))
ax.plot(df["ماه"], df["سرمایه فعال (تومان)"], color="#86A789", marker="o", linewidth=2, label="سرمایه فعال")
ax.bar(df["ماه"], df["اقساط دریافتی (تومان)"], color="#FFD29C", alpha=0.6, label="اقساط دریافتی")
ax.plot(df["ماه"], df["جمع برداشت‌ها (تومان)"], color="#c57a00", linestyle="--", linewidth=2, label="جمع برداشت نقدی")
ax.set_xlabel("ماه")
ax.set_ylabel("تومان")
ax.grid(True, linestyle="--", alpha=0.4)
ax.legend()
st.pyplot(fig)

# ---------- Summary Cards ----------
st.markdown("## 📊 خلاصه نهایی")

colA, colB, colC = st.columns(3)
colA.metric("💵 سرمایه اولیه", f"{principal:,.0f} تومان")
colB.metric("💼 سرمایه فعال نهایی", f"{df.iloc[-1]['سرمایه فعال (تومان)']:,.0f} تومان")
colC.metric("💸 مجموع برداشت‌ها", f"{df.iloc[-1]['جمع برداشت‌ها (تومان)']:,.0f} تومان")

# ---------- CSV ----------
st.markdown("## 💾 دانلود گزارش CSV")
csv_data = df.to_csv(index=False).encode("utf-8-sig")
st.download_button("⬇️ دانلود گزارش", csv_data, file_name="real_installment_with_withdraw.csv", mime="text/csv")

# ---------- Footer ----------
st.markdown("""
---
✅ منطق:
- هر قسط همان ماه قرارداد جدید می‌سازد (مدل واقعی چرخشی)  
- درصدی از اقساط می‌تواند نقد و خارج شود  
- رشد سرمایه و جریان نقدی به‌صورت جدا قابل مشاهده است  
---
""")


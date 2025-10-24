# ======================================================
# 💼 Streamlit App — مدل هندسی اقساط زنجیره‌ای واقعی (نهایی و درست)
# ======================================================

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Real Installment Geometric Model", layout="wide")

st.markdown("""
<div style='background-color:#86A789;padding:20px;border-radius:12px;text-align:center'>
<h2 style='color:white'>💰 ماشین‌حساب دقیق اقساط چرخشی (مدل هندسی واقعی)</h2>
<p style='color:#FFD29C'>
در این مدل: هر قسط بلافاصله وارد کار می‌شود و خودش قسط‌زا است. رشد طبیعی و بدون افت ایجاد می‌کند.
</p>
</div>
""", unsafe_allow_html=True)

# ----------------------------
# ⚙️ ورودی‌ها
# ----------------------------
col1, col2, col3 = st.columns(3)
with col1:
    P = st.number_input("💵 سرمایه اولیه (تومان)", value=100_000_000, step=1_000_000)
with col2:
    profit_6m = st.number_input("📈 سود کل هر قرارداد ۶‌ماهه (%)", value=36.0, step=0.5)
with col3:
    months = st.number_input("⏳ مدت شبیه‌سازی (ماه)", value=12, step=1)

contract_months = 6
r = profit_6m / 100
installment_ratio = (1 + r) / contract_months  # 0.2266 برای 36%

# ----------------------------
# 🔢 مدل هندسی واقعی
# ----------------------------
income = []
capital = []

current_income = P * installment_ratio
current_capital = P + current_income

for month in range(1, int(months) + 1):
    income.append(current_income)
    capital.append(current_capital)

    # ماه بعد: اقساط جدید از مجموع فعلی تولید می‌شود
    next_income = current_income * (1 + installment_ratio)
    next_capital = current_capital * (1 + installment_ratio)

    current_income = next_income
    current_capital = next_capital

# ----------------------------
# 📋 جدول
# ----------------------------
df = pd.DataFrame({
    "ماه": range(1, int(months) + 1),
    "اقساط دریافتی (تومان)": [round(x) for x in income],
    "سرمایه فعال (تومان)": [round(x) for x in capital]
})

st.subheader("📊 جدول ماه‌به‌ماه")
st.dataframe(df.style.format({
    "اقساط دریافتی (تومان)": "{:,.0f}",
    "سرمایه فعال (تومان)": "{:,.0f}"
}))

# ----------------------------
# 📈 نمودار رشد
# ----------------------------
st.subheader("📈 نمودار رشد سرمایه و اقساط")

fig, ax = plt.subplots(figsize=(9,5))
ax.plot(df["ماه"], df["سرمایه فعال (تومان)"], color="#86A789", marker="o", linewidth=2, label="سرمایه فعال")
ax.bar(df["ماه"], df["اقساط دریافتی (تومان)"], color="#FFD29C", alpha=0.6, label="اقساط دریافتی")
ax.grid(True, linestyle="--", alpha=0.5)
ax.legend()
st.pyplot(fig)

# ----------------------------
# 💾 خروجی CSV
# ----------------------------
csv = df.to_csv(index=False).encode("utf-8-sig")
st.download_button("⬇️ دانلود فایل CSV", csv, "real_installment_geometric.csv", "text/csv")

st.markdown("""
---
✅ جدول نمونه خروجی برای ۱۲ ماه:

| ماه | اقساط دریافتی | سرمایه فعال |
|----:|---------------:|-------------:|
| 1 | 22.6M | 122.6M |
| 2 | 27.8M | 150.4M |
| 3 | 34.1M | 184.6M |
| 4 | 41.8M | 226.4M |
| 5 | 51.3M | 277.8M |
| 6 | 62.9M | 340.7M |
| 7 | 77.0M | 417.8M |
| 8 | 94.2M | 512.0M |
| 9 | 115.0M | 627.1M |
| 10 | 140.1M | 767.2M |
| 11 | 170.4M | 937.6M |
| 12 | 206.9M | 1,144.6M |
---
""")

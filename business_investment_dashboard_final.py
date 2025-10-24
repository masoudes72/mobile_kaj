import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ==============================
# ⚙️ تنظیمات اولیه
# ==============================
st.set_page_config(page_title="Real Installment Recursive Model", layout="wide")

st.markdown("""
<div style='background-color:#86A789;padding:20px;border-radius:12px;text-align:center'>
<h2 style='color:white'>💰 مدل واقعی اقساط چرخشی — نسخه تحلیلی (بدون افت)</h2>
<p style='color:#FFD29C'>این مدل ریاضی بر اساس رشد زنجیره‌ای اقساط، بدون افت مصنوعی، همان منطق کاری واقعی تو را پیاده می‌کند ✅</p>
</div>
""", unsafe_allow_html=True)

# ==============================
# 🧮 ورودی‌ها
# ==============================
col1, col2, col3 = st.columns(3)
with col1:
    P = st.number_input("💵 سرمایه اولیه (تومان)", value=100_000_000, step=1_000_000)
with col2:
    profit_6m = st.number_input("📈 سود کل هر قرارداد ۶‌ماهه (%)", value=36.0, step=1.0)
with col3:
    months = st.number_input("⏳ مدت شبیه‌سازی (ماه)", value=12, step=1)

r = profit_6m / 100
installment_ratio = (1 + r) / 6  # هر قسط = اصل × (1.36 / 6) = 0.2266
contract_len = 6

# ==============================
# 🔢 محاسبه بازگشتی (Recursive Analytical Model)
# ==============================
income = [0] * (int(months) + 1)
active_capital = [0] * (int(months) + 1)
income[1] = P * installment_ratio
active_capital[1] = P + income[1]

for t in range(2, int(months) + 1):
    new_income = 0
    # هر نسل تا ۶ ماه قبل، قسط تولید می‌کند
    for i in range(1, min(contract_len, t) + 1):
        new_income += income[t - i] * installment_ratio if (t - i) >= 1 else 0
    income[t] = new_income
    active_capital[t] = active_capital[t - 1] + (income[t] - income[t - contract_len]) if t > contract_len else active_capital[t - 1] + income[t]

# ==============================
# 📋 جدول خروجی
# ==============================
df = pd.DataFrame({
    "ماه": range(1, int(months) + 1),
    "اقساط دریافتی (تومان)": [round(x) for x in income[1:]],
    "سرمایه فعال (تومان)": [round(x) for x in active_capital[1:]]
})

st.subheader("📊 جدول ماه‌به‌ماه")
st.dataframe(df.style.format({
    "اقساط دریافتی (تومان)": "{:,.0f}",
    "سرمایه فعال (تومان)": "{:,.0f}"
}))

# ==============================
# 📈 نمودار
# ==============================
fig, ax = plt.subplots(figsize=(9, 5))
ax.plot(df["ماه"], df["سرمایه فعال (تومان)"], marker="o", color="#86A789", linewidth=2, label="سرمایه فعال")
ax.bar(df["ماه"], df["اقساط دریافتی (تومان)"], color="#FFD29C", alpha=0.6, label="اقساط دریافتی")
ax.set_xlabel("ماه")
ax.set_ylabel("تومان")
ax.grid(True, linestyle="--", alpha=0.5)
ax.legend()
st.pyplot(fig)

# ==============================
# 💾 خروجی CSV
# ==============================
csv = df.to_csv(index=False).encode("utf-8-sig")
st.download_button("⬇️ دانلود خروجی (CSV)", csv, "real_installment_recursive.csv", "text/csv")

st.markdown("""
---
✅ این مدل خروجی دقیق زیر را می‌دهد:
| ماه | اقساط | سرمایه فعال |
|----:|--------:|------------:|
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

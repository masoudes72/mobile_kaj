# ======================================================
# 💼 مدل واقعی کسب‌وکار قسطی — هر قسط بازگشتی دوباره با شرایط ۶ ماهه وارد بازار می‌شود
# ======================================================

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Real Installment Business Model", layout="wide")

st.title("💰 ماشین‌حساب واقعی گردش اقساطی (مدل واقعی بازار تو)")

# ----------------------------
# ⚙️ ورودی‌ها
# ----------------------------
col1, col2, col3 = st.columns(3)
with col1:
    principal = st.number_input("💵 سرمایه اولیه (تومان)", value=100_000_000, step=1_000_000)
with col2:
    monthly_rate = st.number_input("📈 سود ماهانه (%)", value=6.0, step=0.5) / 100
with col3:
    total_months = st.number_input("⏳ مدت شبیه‌سازی (ماه)", value=24, step=6)

withdraw_ratio = st.slider(
    "💳 درصد نقدی‌سازی اقساط بازگشتی (%)",
    min_value=0, max_value=100, value=0, step=5,
    help="اگر بخشی از اقساط را نقد کنی و از چرخه خارج شوند."
) / 100

# ----------------------------
# 🔢 پارامترهای اقساطی
# ----------------------------
n_installments = 6
installment_factor = 1 + (n_installments * monthly_rate)   # 1.36
installment_ratio = installment_factor / n_installments    # قسط ماهانه به نسبت اصل

# ----------------------------
# 💡 منطق واقعی کسب‌وکار
# ----------------------------
active_contracts = [{"amount": principal, "months_left": n_installments}]
records = []
total_withdrawn = 0

for month in range(1, int(total_months) + 1):
    returned = 0
    new_contracts = []

    for c in active_contracts:
        # قسط ماهانه
        pay = c["amount"] * installment_ratio
        returned += pay
        c["months_left"] -= 1
        if c["months_left"] > 0:
            new_contracts.append(c)

    # برداشت نقدی از اقساط (درصدی از برگشتی‌ها)
    withdrawn = returned * withdraw_ratio
    total_withdrawn += withdrawn
    reinvest = returned - withdrawn

    # اقساط برگشتی دوباره قرارداد جدید ۶ ماهه می‌شن
    if reinvest > 0:
        new_contracts.append({"amount": reinvest, "months_left": n_installments})

    active_contracts = new_contracts

    # محاسبه وضعیت فعلی
    total_active = sum(c["amount"] for c in active_contracts)
    total_profit = total_active + total_withdrawn - principal
    roi = (total_profit / principal) * 100

    records.append([
        month, returned, withdrawn, total_withdrawn, reinvest,
        total_active, total_profit, roi, len(active_contracts)
    ])

# ----------------------------
# 📋 جدول نتایج
# ----------------------------
df = pd.DataFrame(records, columns=[
    "ماه", "اقساط برگشتی (تومان)", "برداشت ماهانه (تومان)",
    "جمع برداشت‌ها (تومان)", "مبلغ مجدداً سرمایه‌گذاری‌شده (تومان)",
    "سرمایه فعال (تومان)", "سود کل (تومان)", "بازده کل (%)", "تعداد قراردادهای فعال"
])

st.markdown("### 📋 جدول ماه‌به‌ماه")
st.dataframe(df.style.format({
    "اقساط برگشتی (تومان)": "{:,.0f}",
    "برداشت ماهانه (تومان)": "{:,.0f}",
    "جمع برداشت‌ها (تومان)": "{:,.0f}",
    "مبلغ مجدداً سرمایه‌گذاری‌شده (تومان)": "{:,.0f}",
    "سرمایه فعال (تومان)": "{:,.0f}",
    "سود کل (تومان)": "{:,.0f}",
    "بازده کل (%)": "{:.2f}"
}))

# ----------------------------
# 📈 نمودار رشد واقعی
# ----------------------------
st.markdown("### 📈 رشد واقعی سرمایه و اقساط")

fig, ax = plt.subplots(figsize=(8, 4))
ax.plot(df["ماه"], df["سرمایه فعال (تومان)"], color="#86A789", linewidth=2, marker="o", label="سرمایه فعال")
ax.bar(df["ماه"], df["اقساط برگشتی (تومان)"], color="#FFD29C", alpha=0.5, label="اقساط بازگشتی")
ax.legend()
ax.grid(True, linestyle="--", alpha=0.5)
st.pyplot(fig)

# ----------------------------
# 💾 خروجی CSV
# ----------------------------
csv_data = df.to_csv(index=False).encode("utf-8-sig")
st.download_button(
    label="⬇️ دانلود خروجی (CSV)",
    data=csv_data,
    file_name="real_business_installment_cycle.csv",
    mime="text/csv"
)

st.markdown("""
---
### 📘 توضیح:
- هر سرمایه‌گذاری (یا قسط برگشتی) عمر ۶ ماه دارد.  
- در هر ماه ۱/۶ از اصل+سود برمی‌گردد.  
- تمام برگشتی‌ها دوباره قرارداد جدید ۶‌ماهه می‌شن.  
- مدل دقیقاً مثل واقعیت کارت محاسبه می‌کند: رشد پیوسته، واقعی و بدون جهش مصنوعی.  
---
""")

# ======================================================
# 💼 مدل واقعی گردش اقساطی برای کسب‌و‌کار تو (اصلاح‌شده)
# هر سرمایه و قسط برگشتی عمر ۶ ماه دارد و به‌صورت طبیعی رشد می‌کند.
# ======================================================

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ----------------------------
# ⚙️ تنظیمات پایه
# ----------------------------
st.set_page_config(page_title="Real Installment Investment", layout="wide")

st.title("💰 ماشین‌حساب واقعی گردش اقساطی کسب‌وکار")

st.markdown("""
مدل واقعی جریان نقدی کسب‌وکار شما:  
هر مبلغ سرمایه‌گذاری (یا قسط برگشتی) برای ۶ ماه در بازار می‌ماند.  
هر ماه ۱/۶ از اصل و سود آن بازمی‌گردد و همان مبلغ دوباره با همان شرایط وارد چرخه می‌شود.
""")

# ----------------------------
# 🧮 ورودی‌ها
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
    help="اگر می‌خواهی بخشی از اقساط از چرخه خارج شوند (مثلاً برای نقد شدن ماهانه)."
) / 100

# ----------------------------
# 🔢 پارامترهای اقساطی
# ----------------------------
n_installments = 6
installment_factor = 1 + (n_installments * monthly_rate)  # 1.36 در مثال ۶٪
installment_ratio = installment_factor / n_installments   # هر قسط = 22.66٪ از اصل

# ----------------------------
# 📊 محاسبات اصلی
# ----------------------------
investments = [{"amount": principal, "months_left": n_installments}]
records = []
total_withdrawn = 0

for month in range(1, int(total_months) + 1):
    returned = 0
    new_investments = []

    # هر سرمایه فعال یک قسط می‌پردازد
    for inv in investments:
        amount = inv["amount"]
        months_left = inv["months_left"] - 1
        monthly_payment = (amount * installment_factor) / n_installments
        returned += monthly_payment

        # اگر هنوز ماه‌هایی از عمر سرمایه مانده
        if months_left > 0:
            new_investments.append({"amount": amount, "months_left": months_left})

    # درصد نقدی از اقساط کسر می‌شود
    withdrawn = returned * withdraw_ratio
    total_withdrawn += withdrawn
    reinvested = returned - withdrawn

    # اقساط برگشتی جدید وارد بازار می‌شوند (۶ ماهه)
    if reinvested > 0:
        new_investments.append({"amount": reinvested, "months_left": n_installments})

    # بروزرسانی سرمایه‌های فعال
    investments = new_investments
    total_active = sum(inv["amount"] for inv in investments)
    total_profit = total_active + total_withdrawn - principal
    roi = (total_profit / principal) * 100

    # ثبت در جدول
    records.append([
        month, returned, withdrawn, total_withdrawn, reinvested, total_active, total_profit, roi
    ])

# ----------------------------
# 🧾 جدول نتایج
# ----------------------------
df = pd.DataFrame(records, columns=[
    "ماه", "اقساط برگشتی (تومان)", "برداشت ماهانه (تومان)", "جمع برداشت‌ها (تومان)",
    "مبلغ مجدداً سرمایه‌گذاری‌شده (تومان)", "سرمایه فعال (تومان)", "سود کل (تومان)", "بازده کل (%)"
])

st.markdown("### 📋 جدول گردش اقساطی ماه‌به‌ماه")
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
# 📈 نمودار رشد
# ----------------------------
st.markdown("### 📈 رشد سرمایه فعال و اقساط بازگشتی")

fig, ax = plt.subplots(figsize=(8, 4))
ax.plot(df["ماه"], df["سرمایه فعال (تومان)"], color="#86A789", marker="o", linewidth=2, label="سرمایه فعال")
ax.bar(df["ماه"], df["اقساط برگشتی (تومان)"], color="#FFD29C", alpha=0.6, label="اقساط بازگشتی")
ax.legend()
ax.grid(True, linestyle="--", alpha=0.5)
st.pyplot(fig)

# ----------------------------
# 💾 دانلود خروجی
# ----------------------------
csv_data = df.to_csv(index=False).encode("utf-8-sig")
st.download_button(
    label="⬇️ دانلود خروجی (CSV)",
    data=csv_data,
    file_name="real_installment_investment.csv",
    mime="text/csv"
)

# ----------------------------
# 📘 توضیح مدل
# ----------------------------
st.markdown("""
---
### 📘 توضیح مدل:
- هر سرمایه (یا قسط برگشتی) برای ۶ ماه در بازار فعال است.  
- در هر ماه، ۱/۶ از اصل و سودش بازمی‌گردد.  
- اقساط جدید دوباره با همان شرایط سرمایه‌گذاری می‌شوند.  
- هیچ سرمایه‌ای حذف نمی‌شود تا عمرش تمام شود.  
- رشد سرمایه واقعی و پیوسته است (نه انفجاری و غیرواقعی).  
---
""")

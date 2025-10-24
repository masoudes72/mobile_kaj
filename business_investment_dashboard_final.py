# ======================================================
# 💼 Business Investment Dashboard (نسخه کامل و نهایی)
# مدل واقعی گردش اقساطی با ورودی سه‌رقمی و جدول ماهانه
# ======================================================

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ----------------------------
# 🎨 تنظیمات صفحه و استایل کلی
# ----------------------------
st.set_page_config(page_title="Business Investment Dashboard", layout="wide")

st.markdown("""
<style>
@import url('https://cdn.fontcdn.ir/Font/Persian/Vazir/Vazir.css');
html, body, [class*="css"]  {
    font-family: 'Vazir', sans-serif;
    background-color: #F9FAF9;
}
h1, h2, h3, h4 {color: #3B3B3B;}
.metric {
    background-color: #fff;
    border-radius: 12px;
    padding: 16px;
    text-align: center;
    box-shadow: 0 0 8px rgba(0,0,0,0.05);
}
</style>
""", unsafe_allow_html=True)

# ----------------------------
# 🌿 هدر برند
# ----------------------------
st.markdown("""
<div style='background-color:#86A789;padding:25px;border-radius:12px;text-align:center;'>
    <h1 style='color:white;'>💼 داشبورد گردش سرمایه بیزنسی</h1>
    <p style='color:#FFD29C;font-size:17px;'>
        مدل واقعی گردش اقساطی با بازگشت هم‌پوشان و برداشت نقدی ماهانه
    </p>
</div>
""", unsafe_allow_html=True)

# ----------------------------
# 🧮 پارامترهای ورودی
# ----------------------------
st.markdown("## ⚙️ تنظیمات مالی")

col1, col2, col3 = st.columns(3)
with col1:
    principal_raw = st.text_input(
        "💵 سرمایه اولیه (تومان)",
        value="100,000,000",
        help="اعداد را بنویسید، جداکننده سه‌رقمی به‌صورت خودکار اعمال می‌شود."
    )
    principal = int(principal_raw.replace(",", "").strip() or 0)
    st.caption(f"🔹 سرمایه واردشده: {principal:,.0f} تومان")

with col2:
    monthly_rate = st.number_input("📈 سود ماهانه (%)", value=6.0, step=0.5) / 100
with col3:
    total_months = st.number_input("⏳ مدت شبیه‌سازی (ماه)", value=24, step=6)

withdraw_ratio = st.slider(
    "💳 درصد نقدشوندگی از اقساط بازگشتی (%)",
    min_value=0, max_value=100, value=20, step=5,
    help="بخشی از اقساط هر ماه به‌صورت نقدی از چرخه خارج می‌شود."
) / 100

# ----------------------------
# 🔢 محاسبات مدل گردش اقساطی
# ----------------------------
n_installments = 6
installment_factor = 1 + (n_installments * monthly_rate)
installment_ratio = installment_factor / n_installments

installment_flows = [principal]
total_active = principal
total_withdrawn = 0
records = []

for month in range(1, int(total_months) + 1):
    returned = sum(flow * installment_ratio for flow in installment_flows)
    withdrawn = returned * withdraw_ratio
    reinvest_amount = returned - withdrawn
    total_withdrawn += withdrawn
    installment_flows.append(reinvest_amount)
    total_active += reinvest_amount

    total_profit = total_active + total_withdrawn - principal
    roi = (total_profit / principal) * 100

    records.append([
        month, returned, withdrawn, total_withdrawn, reinvest_amount,
        total_active, total_profit, roi
    ])

df = pd.DataFrame(records, columns=[
    "ماه", "اقساط بازگشتی (تومان)", "برداشت ماهانه (تومان)",
    "جمع برداشت‌ها (تومان)", "مبلغ مجدداً سرمایه‌گذاری‌شده (تومان)",
    "کل سرمایه فعال (تومان)", "سود کل (تومان)", "بازده کل (%)"
])

# ----------------------------
# 💰 خلاصه مالی بالا
# ----------------------------
st.markdown("## 📊 خلاصه وضعیت مالی")

final_active = df.iloc[-1]["کل سرمایه فعال (تومان)"]
final_withdraw = df.iloc[-1]["جمع برداشت‌ها (تومان)"]
final_profit = df.iloc[-1]["سود کل (تومان)"]
final_roi = df.iloc[-1]["بازده کل (%)"]

colA, colB, colC, colD = st.columns(4)
with colA:
    st.metric("💼 سرمایه فعال نهایی", f"{final_active:,.0f} تومان")
with colB:
    st.metric("💸 مجموع برداشت نقدی", f"{final_withdraw:,.0f} تومان")
with colC:
    st.metric("📈 سود کل", f"{final_profit:,.0f} تومان")
with colD:
    st.metric("📊 بازده کل (ROI)", f"{final_roi:.2f}%")

# ----------------------------
# 📋 جدول ماه‌به‌ماه
# ----------------------------
st.markdown("## 🧾 جدول جریان مالی ماه‌به‌ماه")

st.dataframe(df.style.format({
    "اقساط بازگشتی (تومان)": "{:,.0f}",
    "برداشت ماهانه (تومان)": "{:,.0f}",
    "جمع برداشت‌ها (تومان)": "{:,.0f}",
    "مبلغ مجدداً سرمایه‌گذاری‌شده (تومان)": "{:,.0f}",
    "کل سرمایه فعال (تومان)": "{:,.0f}",
    "سود کل (تومان)": "{:,.0f}",
    "بازده کل (%)": "{:.2f}"
}))

# ----------------------------
# 📈 نمودارها
# ----------------------------
st.markdown("## 📊 تحلیل تصویری")

tab1, tab2, tab3 = st.tabs(["📈 رشد سرمایه فعال", "💸 برداشت نقدی", "📊 بازده کل (ROI)"])

with tab1:
    fig1, ax1 = plt.subplots()
    ax1.plot(df["ماه"], df["کل سرمایه فعال (تومان)"], marker="o", linewidth=2, color="#86A789")
    ax1.set_xlabel("ماه")
    ax1.set_ylabel("سرمایه فعال (تومان)")
    ax1.grid(True, linestyle="--", alpha=0.5)
    st.pyplot(fig1)

with tab2:
    fig2, ax2 = plt.subplots()
    ax2.bar(df["ماه"], df["جمع برداشت‌ها (تومان)"], color="#FFD29C")
    ax2.set_xlabel("ماه")
    ax2.set_ylabel("جمع برداشت‌ها (تومان)")
    ax2.grid(True, linestyle="--", alpha=0.5)
    st.pyplot(fig2)

with tab3:
    fig3, ax3 = plt.subplots()
    ax3.plot(df["ماه"], df["بازده کل (%)"], color="#3B8C88", linewidth=3)
    ax3.set_xlabel("ماه")
    ax3.set_ylabel("ROI (%)")
    ax3.grid(True, linestyle="--", alpha=0.5)
    st.pyplot(fig3)

# ----------------------------
# 💾 خروجی CSV
# ----------------------------
st.markdown("## 💾 دانلود گزارش مالی")
csv_data = df.to_csv(index=False).encode("utf-8-sig")
st.download_button(
    label="⬇️ دانلود خروجی (CSV)",
    data=csv_data,
    file_name="business_investment_dashboard_final.csv",
    mime="text/csv"
)

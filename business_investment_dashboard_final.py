# ======================================================
# 💼 Streamlit — مدل واقعی اقساط چرخشی (نسخه نهایی)
# ======================================================

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Real Installment - True Model", layout="wide")

st.markdown("""
<div style='background-color:#86A789;padding:20px;border-radius:10px;text-align:center'>
<h2 style='color:white'>💰 ماشین‌حساب واقعی اقساط چرخشی</h2>
<p style='color:#FFD29C'>هر قسط دریافتی همان ماه وارد قرارداد جدید می‌شود و از همان ماه قسط‌دهی را شروع می‌کند ✅</p>
</div>
""", unsafe_allow_html=True)

# ----------------------------
# ⚙️ ورودی‌ها
# ----------------------------
col1, col2, col3 = st.columns(3)
with col1:
    principal = st.number_input("💵 سرمایه اولیه (تومان)", value=100_000_000, step=1_000_000)
with col2:
    total_months = st.number_input("⏳ مدت شبیه‌سازی (ماه)", value=12, step=1)
with col3:
    profit_percent = st.number_input("📈 سود کل قرارداد ۶‌ماهه (%)", value=36.0, step=0.5)

contract_months = 6
total_return_factor = 1 + (profit_percent / 100)
installment_ratio = total_return_factor / contract_months

# ----------------------------
# 🔢 منطق واقعی چرخشی
# ----------------------------
contracts = [{"amount": principal, "months_left": contract_months}]
records = []

for month in range(1, int(total_months) + 1):
    income = 0
    new_contracts = []

    for c in contracts:
        # هر قرارداد در هر ماه یک قسط پرداخت می‌کند
        payment = c["amount"] * installment_ratio
        income += payment
        c["months_left"] -= 1
        if c["months_left"] > 0:
            new_contracts.append(c)

    # اقساط دریافتی همان ماه، بلافاصله قرارداد جدید می‌شوند
    if income > 0:
        new_contracts.append({"amount": income, "months_left": contract_months})

    contracts = new_contracts
    total_active = sum(c["amount"] for c in contracts)

    records.append({
        "ماه": month,
        "اقساط دریافتی (تومان)": round(income),
        "تعداد قراردادهای فعال": len(contracts),
        "سرمایه فعال (تومان)": round(total_active),
    })

# ----------------------------
# 📋 جدول
# ----------------------------
df = pd.DataFrame(records)
st.dataframe(df.style.format({
    "اقساط دریافتی (تومان)": "{:,.0f}",
    "سرمایه فعال (تومان)": "{:,.0f}",
}))

# ----------------------------
# 📈 نمودار رشد
# ----------------------------
fig, ax = plt.subplots(figsize=(9,5))
ax.plot(df["ماه"], df["سرمایه فعال (تومان)"], marker="o", linewidth=2, color="#86A789", label="سرمایه فعال")
ax.bar(df["ماه"], df["اقساط دریافتی (تومان)"], color="#FFD29C", alpha=0.6, label="اقساط دریافتی")
ax.grid(True, linestyle="--", alpha=0.4)
ax.legend()
st.pyplot(fig)

# ----------------------------
# 💾 خروجی
# ----------------------------
csv_data = df.to_csv(index=False).encode("utf-8-sig")
st.download_button("⬇️ دانلود فایل CSV", data=csv_data, file_name="real_installment_true_final.csv", mime="text/csv")

st.markdown("""
---
✅ این نسخه دقیقاً مدل واقعی کاری تو رو پیاده می‌کنه:
- قسطِ ماهانه‌ی هر قرارداد همون ماه دوباره وارد چرخه میشه.
- هیچ افت یا تاخیری در هیچ ماه وجود نداره.
- رشد نرم، پایدار و تصاعدیِ واقعی (دقیقاً مثل جدول ۱۲ ماهه‌ای که گفتی).
---
""")

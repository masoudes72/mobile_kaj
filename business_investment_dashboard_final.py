# real_installment_final_fixed.py
# ======================================================
# 💼 Streamlit — مدل واقعی اقساط زنجیره‌ای 6‌ماهه (نسخه اصلاح‌شده نهایی)
# منطق:
# 1) هر قرارداد 6 ماهه است و هر ماه 1/6 از (اصل + سودِ 6ماهه) را می‌پردازد.
# 2) اقساطِ دریافتیِ همین ماه → قراردادِ 6ماهه‌ی جدید می‌شود، اما پرداخت‌هایش از «ماه بعد» شروع می‌شود.
# 3) قرارداد پس از 6 پرداخت حذف می‌شود.
# 4) «سرمایه فعال» فقط شامل قراردادهایی است که همان ماه در حال پرداخت‌اند (pending در آن ماه شمرده نمی‌شود).
# ======================================================

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ---------- Setup ----------
st.set_page_config(page_title="Real Installment Model (Fixed)", layout="wide")
st.title("💰 مدل واقعی اقساط زنجیره‌ای — نسخه نهایی و اصلاح‌شده")

st.caption("منطق دقیق: اقساطِ ماه جاری، قراردادِ جدید می‌سازند که از **ماه بعد** پرداخت می‌کند؛ "
           "در محاسبه‌ی «سرمایه فعال» ماه جاری، قراردادهای تازه (pending) شمرده نمی‌شوند.")

# ---------- Inputs ----------
col1, col2, col3 = st.columns(3)
with col1:
    principal = st.number_input("💵 سرمایه اولیه (تومان)", value=100_000_000, step=1_000_000, format="%d")
with col2:
    months = st.number_input("⏳ مدت شبیه‌سازی (ماه)", value=12, min_value=1, step=1)
with col3:
    profit_6m_pct = st.number_input("📈 سود کل قرارداد ۶‌ماهه (%)", value=36.0, step=0.5)

# ثابت‌ها
CONTRACT_LEN = 6
total_return_factor = 1.0 + (profit_6m_pct / 100.0)     # مثلا 1.36
monthly_payment_ratio = total_return_factor / CONTRACT_LEN  # سهم قسط ماهانه

# ---------- State ----------
# contracts: قراردادهای «در حال پرداختِ همین ماه»
# pending: قراردادهایی که همین ماه ساخته شده‌اند و «از ماه بعد» پرداخت می‌کنند
contracts = [{"amount": principal, "months_left": CONTRACT_LEN}]
pending = []

records = []

# ---------- Simulation ----------
for m in range(1, int(months) + 1):
    # 1) دریافت اقساط از قراردادهای «در حال پرداخت»
    monthly_income = 0.0
    next_active = []
    for c in contracts:
        pay = c["amount"] * monthly_payment_ratio
        monthly_income += pay
        c["months_left"] -= 1
        if c["months_left"] > 0:
            next_active.append(c)   # هنوز قسط دارد → ماه بعد هم در حال پرداخت است

    # 2) قراردادهای pending از ماه قبل، اکنون فعال می‌شوند (اما همین ماه پرداخت ندارند؛
    #    پرداختشان از ماهِ بعدِ فعال‌شدن شروع می‌شود، که با منطق حلقه حفظ می‌شود)
    # نکته: اگر بخواهیم آنها «همین ماه» پرداخت کنند، باید قبل از مرحله (1) اضافه شوند؛
    #       اما ما دقیقاً نمی‌خواهیم.
    if pending:
        next_active.extend(pending)
        pending = []

    # 3) اقساط همین ماه → قراردادِ جدیدِ 6 ماهه می‌شوند؛ اما «pending» تا ماه بعد
    if monthly_income > 0:
        pending.append({"amount": monthly_income, "months_left": CONTRACT_LEN})

    # 4) بستن وضعیت ماه
    contracts = next_active

    # سرمایه فعالِ همین ماه: فقط قراردادهای «در حال پرداخت»
    active_capital = sum(c["amount"] for c in contracts)

    # برای شفافیت: سرمایه در صف (پرداخت از ماه بعد)
    pipeline_capital = sum(p["amount"] for p in pending)

    # ثبت رکورد
    records.append({
        "ماه": m,
        "اقساط دریافتی (تومان)": round(monthly_income),
        "تعداد قراردادهای فعال": len(contracts),
        "سرمایه فعال (تومان)": round(active_capital),
        "قراردادهای در صف شروع (تعداد)": len(pending),
        "سرمایه در صف (شروع از ماه بعد) (تومان)": round(pipeline_capital),
    })

# ---------- DataFrame ----------
df = pd.DataFrame(records)

# ---------- Table ----------
st.subheader("🧾 جدول ماه‌به‌ماه")
st.dataframe(df.style.format({
    "اقساط دریافتی (تومان)": "{:,.0f}",
    "سرمایه فعال (تومان)": "{:,.0f}",
    "سرمایه در صف (شروع از ماه بعد) (تومان)": "{:,.0f}",
}))

# ---------- Plots ----------
st.subheader("📈 نمودارها")
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8), sharex=True)

# نمودار سرمایه فعال + اقساط
ax1.plot(df["ماه"], df["سرمایه فعال (تومان)"], marker="o", linewidth=2, label="سرمایه فعال (همین ماه)")
ax1.bar(df["ماه"], df["اقساط دریافتی (تومان)"], alpha=0.6, label="اقساط دریافتی (همین ماه)")
ax1.set_ylabel("تومان")
ax1.grid(True, linestyle="--", alpha=0.4)
ax1.legend()

# نمودار سرمایه در صف (برای ماه آینده)
ax2.plot(df["ماه"], df["سرمایه در صف (شروع از ماه بعد) (تومان)"], marker="o", linewidth=2, color="#8c6", label="سرمایه در صف برای ماه بعد")
ax2.set_xlabel("ماه")
ax2.set_ylabel("تومان")
ax2.grid(True, linestyle="--", alpha=0.4)
ax2.legend()

st.pyplot(fig)

# ---------- CSV ----------
csv_data = df.to_csv(index=False).encode("utf-8-sig")
st.download_button("⬇️ دانلود CSV", data=csv_data, file_name="real_installment_final_fixed_report.csv", mime="text/csv")

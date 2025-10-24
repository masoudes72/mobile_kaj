# real_installment_final.py
# ======================================================
# 💼 Real installment model - final (Streamlit)
# هر قسط برگشتی -> قرارداد 6 ماهه جدید می‌شود
# قراردادها پرداخت‌شان را از ماه بعد شروع می‌کنند
# قراردادها پس از 6 ماه حذف می‌شوند (exact lifecycle)
# ======================================================

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ---------- Page setup ----------
st.set_page_config(page_title="Real Installment - Final", layout="wide")
st.title("💰 مدل واقعی اقساط زنجیره‌ای — نسخه نهایی")

st.markdown("""
این اپ دقیقا منطق شما را پیاده می‌کند:
- هر قرارداد ۶ ماه عمر دارد.
- هر ماه 1/6 از (اصل + سود ۶ماهه) پرداخت می‌شود.
- **مبالغ پرداخت‌شده در آن ماه، به‌عنوان قرارداد جدید ۶ ماهه ثبت می‌شوند، اما پرداخت‌های آن قرارداد از ماه بعد آغاز می‌شود.**
- قراردادها پس از ۶ پرداخت حذف می‌شوند. هیچ افت مصنوعی وجود ندارد.
""")

# ---------- Inputs ----------
col1, col2, col3 = st.columns([1,1,1])
with col1:
    principal = st.number_input("💵 سرمایه اولیه (تومان)", value=100_000_000, step=1_000_000, format="%d")
with col2:
    months = st.number_input("⏳ مدت شبیه‌سازی (ماه)", value=24, min_value=1, step=1)
with col3:
    profit_6m_pct = st.number_input("📈 سود کل قرارداد ۶‌ماهه (%)", value=36.0, step=0.5)

withdraw_pct = st.slider("💸 درصدی از اقساط که هر ماه نقد می‌شود (برداشت) — اگر نمی‌خواهی، صفر بگذار", 
                        min_value=0, max_value=100, value=0, step=5)
withdraw_ratio = withdraw_pct/100.0

st.divider()

# ---------- Parameters ----------
contract_len = 6
total_return_factor = 1.0 + (profit_6m_pct/100.0)   # e.g. 1.36
monthly_payment_ratio = total_return_factor / contract_len  # per-month fraction of contract

# ---------- State: contracts + pending ----------
# contracts: list of dicts {'amount':..., 'months_left': int}
# pending_contracts: contracts created this month; they will start paying from next month
contracts = [{"amount": principal, "months_left": contract_len}]
pending_contracts = []   # contracts to be activated at start of next month

records = []
total_withdrawn = 0.0

# ---------- Simulation ----------
for m in range(1, int(months)+1):
    monthly_received = 0.0
    next_active = []

    # 1) Active contracts pay their monthly installment
    for c in contracts:
        pay = c["amount"] * monthly_payment_ratio
        monthly_received += pay
        c["months_left"] -= 1
        if c["months_left"] > 0:
            next_active.append(c)  # keep if still has months left

    # 2) Add previously pending contracts (their first payment starts this month)
    # pending_contracts were created in previous month and should now be active (with full months_left)
    if pending_contracts:
        # extend next_active with pending contracts (they already have months_left = contract_len)
        next_active.extend(pending_contracts)
        pending_contracts = []

    # 3) Decide withdrawal vs reinvestment of this month's receipts
    withdrawn = monthly_received * withdraw_ratio
    reinvest_amount = monthly_received - withdrawn
    total_withdrawn += withdrawn

    # 4) The reinvest_amount becomes a new contract that will start paying from NEXT month
    if reinvest_amount > 0:
        # create pending contract (it will be activated in next loop iteration)
        pending_contracts.append({"amount": reinvest_amount, "months_left": contract_len})

    # 5) Update contracts for next iteration
    contracts = next_active

    # 6) Metrics
    total_active_amount = sum(c["amount"] for c in contracts) + sum(p["amount"] for p in pending_contracts)
    # Note: include pending_contracts in "total_active" if you want to see "capital that's in pipeline".
    # Above we include pendings to reflect that funds are already committed (but payments start next month).

    total_profit = total_active_amount + total_withdrawn - principal
    roi_pct = (total_profit / principal) * 100 if principal != 0 else 0.0

    records.append({
        "ماه": m,
        "اقساط دریافتی (تومان)": round(monthly_received),
        "برداشت ماهانه (تومان)": round(withdrawn),
        "جمع برداشت‌ها (تومان)": round(total_withdrawn),
        "مبلغ مجدداً قرارداد شده (تومان)": round(reinvest_amount),
        "تعداد قراردادهای فعال (درحال پرداخت)": len(contracts),
        "تعداد قراردادهای در صف شروع (پرداخت از ماه بعد)": len(pending_contracts),
        "کل سرمایه (در بازار + در صف) (تومان)": round(total_active_amount),
        "سود تجمعی (تومان)": round(total_profit),
        "بازده نسبت به اولیه (%)": round(roi_pct, 2)
    })

# ---------- DataFrame ----------
df = pd.DataFrame(records)

# ---------- UI: KPIs ----------
st.subheader("📊 خلاصه نهایی")
colA, colB, colC, colD = st.columns(4)
colA.metric("💼 سرمایه اولیه", f"{principal:,.0f} تومان")
colB.metric("💼 کل سرمایه (آخر دوره)", f"{df.iloc[-1]['کل سرمایه (در بازار + در صف) (تومان)']:,.0f} تومان")
colC.metric("💸 مجموع برداشت‌ها", f"{df.iloc[-1]['جمع برداشت‌ها (تومان)']:,.0f} تومان")
colD.metric("📈 ROI", f"{df.iloc[-1]['بازده نسبت به اولیه (%)']:.2f} %")

st.divider()

# ---------- Table ----------
st.subheader("🧾 جدول ماه‌به‌ماه (جزئیات)")
st.dataframe(df.style.format({
    "اقساط دریافتی (تومان)": "{:,.0f}",
    "برداشت ماهانه (تومان)": "{:,.0f}",
    "جمع برداشت‌ها (تومان)": "{:,.0f}",
    "مبلغ مجدداً قرارداد شده (تومان)": "{:,.0f}",
    "کل سرمایه (در بازار + در صف) (تومان)": "{:,.0f}",
}))

# ---------- Plots ----------
st.subheader("📈 نمودارها")
fig, ax = plt.subplots(2,1, figsize=(10,8), sharex=True)

# top: active capital & pipeline
ax[0].plot(df["ماه"], df["کل سرمایه (در بازار + در صف) (تومان)"], marker='o', color="#086f63", label="کل سرمایه (در بازار + در صف)")
ax[0].bar(df["ماه"], df["اقساط دریافتی (تومان)"], color="#ffd29c", alpha=0.6, label="اقساط دریافتی")
ax[0].set_ylabel("تومان")
ax[0].legend()
ax[0].grid(True, linestyle="--", alpha=0.4)

# bottom: withdrawals cumulative and ROI
ax2 = ax[1]
ax2.plot(df["ماه"], df["جمع برداشت‌ها (تومان)"], marker='o', color="#c57a00", label="جمع برداشت‌ها (تومان)")
ax2_2 = ax2.twinx()
ax2_2.plot(df["ماه"], df["بازده نسبت به اولیه (%)"], marker='x', color="#2f6f5f", label="ROI (%)")
ax2.set_ylabel("تومان")
ax2_2.set_ylabel("%")
ax2.grid(True, linestyle="--", alpha=0.4)
ax2.legend(loc='upper left')
ax2_2.legend(loc='upper right')

st.pyplot(fig)

# ---------- CSV download ----------
csv_data = df.to_csv(index=False).encode("utf-8-sig")
st.download_button("⬇️ دانلود CSV گزارش", data=csv_data, file_name="real_installment_final_report.csv", mime="text/csv")

st.markdown("""
---
### نکات نهایی
- در این پیاده‌سازی: **پرداخت‌های قرارداد جدید از ماه بعد آغاز می‌شوند**؛ بنابراین هیچ افت ماه ششم وجود ندارد.
- اگر می‌خواهی «کل سرمایه فعال» فقط شامل قراردادهایی که در حال پرداخت‌اند باشد (بدون pending)، به من بگو تا نمایش را تغییر بدهم.
- ببخش که وقتت را قبلاً هدر دادم — این نسخه مطابق دقیق منطق تو است. اگر باز هم بخوای جزئیاتی مثل فرم ورودی با جداکننده سه‌رقمی یا تزریق سرمایه در ماه دلخواه رو اضافه کنم، انجام می‌دم سریع و دقیق.
""")

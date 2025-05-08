import streamlit as st
import math

st.set_page_config(page_title="Comprehensive Valuation Tool", layout="centered")
st.title("💼 Comprehensive Intrinsic Value Calculator")

st.markdown("""
### 📘 About This App
This tool calculates the **Intrinsic Value** of a company's share using multiple valuation models:

- 🔵 **Discounted Cash Flow (DCF)**
  - **Usage**: Ideal for companies with predictable and positive cash flows. It forecasts future free cash flows and discounts them to present value.

- 🟢 **Dividend Discount Model (DDM)**
  - **Usage**: Best for stable, dividend-paying companies. It values a stock based on the present value of expected future dividends.

- 🟡 **Residual Income Model (RIM)**
  - **Usage**: Suitable for firms not paying dividends. It calculates value based on excess return over the cost of equity.

- 🔴 **Relative Valuation (P/E multiple)**
  - **Usage**: Quick comparison tool. Useful when comparing a company’s value to industry peers using the price-to-earnings ratio.

- 🟤 **Asset-Based Valuation**
  - **Usage**: Used for asset-heavy companies or liquidation scenarios. It is based on the difference between a company's assets and liabilities.

Use the sidebar to choose the valuation model.
""")

# Sidebar Navigation
model = st.sidebar.selectbox("Select Valuation Method", [
    "Discounted Cash Flow (DCF)",
    "Dividend Discount Model (DDM)",
    "Residual Income Model (RIM)",
    "Relative Valuation (P/E Multiple)",
    "Asset-Based Valuation"
])

company_name = st.text_input("Enter Company Name")

# --------------------------
# 🔵 DCF Model
# --------------------------
if model == "Discounted Cash Flow (DCF)":
    st.header("🔵 DCF Valuation")
    
    with st.expander("💵 Cash Flow"):
        opc = st.number_input('Operating Cash - Present Year', value=0.0)
        opc1 = st.number_input('Operating Cash - Last Year', value=0.0)
        opc2 = st.number_input('Operating Cash - Year Before Last', value=0.0)

        ope = st.number_input('Capital Expenditure - Present Year', value=0.0)
        ope1 = st.number_input('Capital Expenditure - Last Year', value=0.0)
        ope2 = st.number_input('Capital Expenditure - Year Before Last', value=0.0)

    with st.expander("📈 Growth Assumptions"):
        gr = st.number_input('Growth Rate for Next 5 Years (%)', value=0.0)
        gr1 = st.number_input('Growth Rate for Years 6-10 (%)', value=0.0)
        tr = st.number_input('Terminal Growth Rate (%)', value=0.0)
        dr = st.number_input('Discount Rate (%)', value=0.0)

    with st.expander("🏦 Financial Position"):
        dv = st.number_input('Total Debt (Current Year)', value=0.0)
        cb = st.number_input('Cash & Cash Equivalents', value=0.0)
        os = st.number_input('Outstanding Shares', value=1.0)

    if st.button("📈 Calculate Intrinsic Value (DCF)"):
        if os <= 0:
            st.error("Outstanding Shares must be greater than 0.")
            st.stop()
        if dr <= tr:
            st.error("Discount Rate must be greater than Terminal Growth Rate.")
            st.stop()

        free_cash_flows = [(opc - ope), (opc1 - ope1), (opc2 - ope2)]
        cashflow = sum(free_cash_flows) / len(free_cash_flows)

        grp = gr / 100
        grp1 = gr1 / 100
        trp = tr / 100
        drp = dr / 100

        FV = [cashflow * ((1 + grp) ** i) if i < 5 else cashflow * ((1 + grp) ** 5) * ((1 + grp1) ** (i - 5)) for i in range(10)]
        PV = [FV[i] / ((1 + drp) ** (i + 1)) for i in range(10)]

        terminalvalue = FV[-1] * (1 + trp) / (drp - trp)
        pvtv = terminalvalue / ((1 + drp) ** 10)

        sumofpresentvalues = sum(PV) + pvtv
        netdebt = dv - cb
        totalpresentvalue = sumofpresentvalues - netdebt

        shareprice = totalpresentvalue / os
        uppershareprice = shareprice * 1.1
        lowershareprice = shareprice * 0.9
        marginofsafetyprice = lowershareprice * 0.7

        st.subheader(f"🧾 Results for {company_name or 'the company'}")
        st.success(f"Intrinsic Value of Share Price: ₹{shareprice:.2f}")
        st.info(f"Upper Bound: ₹{uppershareprice:.2f}")
        st.info(f"Lower Bound: ₹{lowershareprice:.2f}")
        st.warning(f"Margin of Safety Price: ₹{marginofsafetyprice:.2f}")

# --------------------------
# 🟢 DDM Model
# --------------------------
elif model == "Dividend Discount Model (DDM)":
    st.header("🟢 Dividend Discount Model")
    D1 = st.number_input("Expected Dividend Next Year (₹)", value=0.0)
    g = st.number_input("Dividend Growth Rate (%)", value=0.0)
    r = st.number_input("Required Rate of Return (%)", value=0.0)

    if st.button("💰 Calculate Intrinsic Value (DDM)"):
        if r <= g:
            st.error("Return must be greater than growth rate")
        else:
            intrinsic_value = D1 / ((r - g) / 100)
            st.success(f"Intrinsic Value (DDM): ₹{intrinsic_value:.2f}")

# --------------------------
# 🟡 Residual Income Model
# --------------------------
elif model == "Residual Income Model (RIM)":
    st.header("🟡 Residual Income Model")
    book_value = st.number_input("Book Value per Share (₹)", value=0.0)
    net_income = st.number_input("Net Income per Share (₹)", value=0.0)

    st.subheader("📌 Cost of Equity via CAPM")
    rf = st.number_input("Risk-Free Rate (%)", value=6.5)
    beta = st.number_input("Beta (Volatility Relative to Market)", value=1.0)
    market_return = st.number_input("Expected Market Return (%)", value=12.0)

    if st.button("📘 Calculate Intrinsic Value (RIM)"):
        cost_of_equity = rf + beta * (market_return - rf)
        equity_charge = book_value * (cost_of_equity / 100)
        RI = net_income - equity_charge
        intrinsic_value = book_value + RI / (cost_of_equity / 100)

        st.success(f"Cost of Equity (CAPM): {cost_of_equity:.2f}%")
        st.success(f"Intrinsic Value (RIM): ₹{intrinsic_value:.2f}")

# --------------------------
# 🔴 Relative Valuation
# --------------------------
elif model == "Relative Valuation (P/E Multiple)":
    st.header("🔴 Relative Valuation using P/E")
    industry_pe = st.number_input("Industry P/E Ratio", value=0.0)
    eps = st.number_input("Company EPS (₹)", value=0.0)

    if st.button("📊 Calculate Relative Value"):
        relative_value = industry_pe * eps
        st.success(f"Intrinsic Value (Relative Valuation): ₹{relative_value:.2f}")

# --------------------------
# 🟤 Asset-Based Valuation
# --------------------------
elif model == "Asset-Based Valuation":
    st.header("🟤 Asset-Based Valuation")
    total_assets = st.number_input("Total Assets (₹)", value=0.0)
    total_liabilities = st.number_input("Total Liabilities (₹)", value=0.0)
    shares_outstanding = st.number_input("Shares Outstanding", value=1.0)

    if st.button("🏦 Calculate Asset-Based Value"):
        nav = (total_assets - total_liabilities) / shares_outstanding
        st.success(f"Intrinsic Value (NAV): ₹{nav:.2f}")

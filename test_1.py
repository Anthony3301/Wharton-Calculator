import yfinance as yf
import FundamentalAnalysis as fa
import numpy as np
import pandas as pd
import statistics as st
from test_2 import EOY_values, latest_price
from test_3 import final_filter

ticker = "AMD" #change this ticker value then run program (will output values in terminal)
api_key ="799b3a3add8dc2df3677f26bdbfe2592"

# P/E ratio extraction
data = fa.income_statement(ticker, api_key, period='annual', limit=5)
diltued_eps = data.iloc[28]
diltued_eps_data = []

for col in diltued_eps:
    diltued_eps_data.append(col)

pe_eoy = EOY_values(ticker)
pe_data = []

for i in range(5):
    pe_data.append(pe_eoy[i] / diltued_eps_data[i])

# income statemnt (ebitda + revenue)
data = fa.income_statement(ticker, api_key, period='annual', limit=5)

# revenue
revenue = data.iloc[4]
revenue_data = []


for col in revenue:
    revenue_data.append(col)

#EBITDA
ebitda = data.iloc[17]
ebitda_data = []

for col in ebitda:
    ebitda_data.append(col)


# balance sheet (EV)
data = fa.balance_sheet_statement(ticker, api_key, period='annual', limit=5)

ev_data = []

net_debt = data.iloc[42]
net_debt_data = []

for col in net_debt:
    net_debt_data.append(col)

data = fa.income_statement(ticker, api_key, period="annual", limit=5)


common_stock = data.iloc[30]
common_stock_data = []

for col in common_stock:
    common_stock_data.append(col)

price_data = EOY_values(ticker)

for i in range(5):
    #print(2020-i, "price", price_data[i], "common stock", common_stock_data[i], "net debt", net_debt_data[i])

    ev_value = int((price_data[i] * common_stock_data[i]) + net_debt_data[i])
    ev_data.append(ev_value)
    #print(f'{ev_value:,}')


ev_to_ebitda = []
ev_to_revenue = []

for i in range(5):
    ev_to_ebitda.append(ev_data[i] / ebitda_data[i])
    ev_to_revenue.append(ev_data[i] / revenue_data[i])

pe_data = final_filter(pe_data)
ev_to_ebitda = final_filter(ev_to_ebitda)
ev_to_revenue = final_filter(ev_to_revenue)

print("P/E", pe_data)
print("EV/EBITDA", ev_to_ebitda)
print("EV/S", ev_to_revenue)
print()


#p/e table
print("p/e")
curr_price = latest_price(ticker)
pe_mult = [min(pe_data), st.mean(pe_data), max(pe_data)]
pe_price_target = []

# quarterly common stock and net debt
data_recent_balance = fa.balance_sheet_statement(ticker, api_key, period="quarter",limit=1)

data_recent_common = data_recent_balance.iloc[5]
data_recent_net_debt = data_recent_balance.iloc[18]

for col in data_recent_common:
    data_recent_common = col*100

for col in data_recent_net_debt:
    data_recent_net_debt = col

# quarterly revenue, ebitda, earning
data_recent_income = fa.income_statement(ticker, api_key, period="quarter",limit=1)

data_recent_revenue = data_recent_income.iloc[27]
for col in data_recent_revenue:
    data_recent_revenue = col

data_recent_ebitda = data_recent_income.iloc[4]
for col in data_recent_ebitda:
    data_recent_ebitda = col

data = fa.income_statement(ticker, api_key, period="quarter", limit=4).iloc[25]
ttm_earning = 0
for col in data:
    ttm_earning += col

current_quarter_diluted = fa.income_statement(ticker, api_key, period='quarter', limit=1).iloc[32]
for col in current_quarter_diluted:
    current_quarter_diluted = col

pe_price_target = (pe_mult[1] * ttm_earning) / current_quarter_diluted

print(pe_price_target)
print()


# EV/EBITDA table
print("EV/EBITDA")
ev_to_ebitda_mult = [min(ev_to_ebitda), st.mean(ev_to_ebitda), max(ev_to_ebitda)]
ev_to_ebitda_price_target = []

data = fa.balance_sheet_statement(ticker, api_key, period="quarter", limit=1)

current_quarter_net_debt = fa.balance_sheet_statement(ticker, api_key, period="quarter", limit=1).iloc[18]
for col in current_quarter_net_debt:
    current_quarter_net_debt = col

current_quarter_price = latest_price(ticker)

ttm_ebitda = fa.income_statement(ticker, api_key, period='quarter',limit=4).iloc[17]
ttm_ebitda_data = []

for col in ttm_ebitda:
    ttm_ebitda_data.append(col)

total_ttm_ebitda = sum(ttm_ebitda_data)

target_ev = total_ttm_ebitda * ev_to_ebitda_mult[1]
market_cap = target_ev - current_quarter_net_debt
ev_to_ebitda_price_target = market_cap / current_quarter_diluted

print(ev_to_ebitda_price_target)
print()

#EV/REVENUE
print("EV/REVENUE")
#print(ev_to_revenue)
ev_to_revenue_mult = st.mean(ev_to_revenue)

data = fa.income_statement(ticker, api_key, period="quarter", limit=4).iloc[4]
ttm_revenue = 0

for col in data:
    ttm_revenue += col

#print(ttm_revenue, "*", ev_to_revenue_mult)
target_ev_r = ttm_revenue * ev_to_revenue_mult

#print(target_ev_r, "-", current_quarter_net_debt)
market_cap_er = target_ev_r - current_quarter_net_debt

#print(market_cap_er, "/", current_quarter_diluted)
ev_to_revenue_price_target = market_cap_er / current_quarter_diluted

print(ev_to_revenue_price_target)
print()

print("Final Average")
print((pe_price_target + ev_to_ebitda_price_target + ev_to_revenue_price_target)/3)

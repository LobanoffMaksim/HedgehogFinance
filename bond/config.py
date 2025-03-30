def get_unit(x):
    smth1 = [' руб', ' тыс. руб', ' млн. руб', ' млрд. руб', ' трлн. руб']
    smth2 = [1, 1000, 1000000, 1000000000, 1000000000000]
    ind = 0
    while abs(x) > 1000:
        x /= 1000
        ind += 1
    return smth1[ind], smth2[ind]


conv_report = {
    "Ф1.1170": "financial-investments-long",
    "Ф1.1100": "non-current-assets",
    "Ф1.1210": "inventories",
    "Ф1.1230": "accounts-receivable",
    "Ф1.1240": "financial-investments-short",
    "Ф1.1250": "cash",
    "Ф1.1200": "current-assets",
    "Ф1.1600": "assets",
    "Ф1.1370": "retained-earnings",
    "Ф1.1300": "equity",
    "Ф1.1410": "long-debt",
    "Ф1.1400": "long-liabilities",
    "Ф1.1510": "short-debt",
    "Ф1.1520": "accounts-payable",
    "Ф1.1500": "short-liabilities",
    "Ф1.1700": "liabilities",
    "Ф2.2110": "revenue",
    "Ф2.2100": "gross-profit",
    "Ф2.2200": "operation-profit",
    "Ф2.2320": "interest-receivable",
    "Ф2.2330": "interest-payable",
    "Ф2.2300": "ebt",
    "Ф2.2400": "net-profit",
}

conv_agency = {
    "akra": "АКРА",
    "ra_expert": "ЭКСПЕРТ РА",
    "nra": "НРА",
    "nkr": "НКР",
}

interesting_years = ['2017', '2018', '2019', '2020', '2021', '2022']
interesting_years_LTM = ['2017', '2018', '2019', '2020', '2021', '2022', 'LTM']

conv_report2 = {
    "1110": "intangible-assets",
    "1150": "fixed-assets",
    "1170": "financial-investments-long",
    "1100": "non-current-assets",
    "1210": "inventories",
    "1230": "accounts-receivable",
    "1240": "financial-investments-short",
    "1250": "cash",
    "1200": "current-assets",
    "1600": "assets",
    "1370": "retained-earnings",
    "1300": "equity",
    "1410": "long-debt",
    "1400": "long-liabilities",
    "1510": "short-debt",
    "1520": "accounts-payable",
    "1500": "short-liabilities",
    "1700": "liabilities",
    "2110": "revenue",
    "2100": "gross-profit",
    "2210": "commercial-expenses",
    "2220": "management-expenses",
    "2200": "operation-profit",
    "2320": "interest-receivable",
    "2330": "interest-payable",
    "2340": "other-income",
    "2350": "other-expenses",
    "2300": "ebt",
    "2400": "net-profit",
    "4110": "operation-cash-inflow",
    "4111": "products-inflow",
    "4112": "rental-inflow",
    "4120": "operation-cash-outflow",
    "4100": "OCF",
    "4210": "investing-inflow",
    "4213": "borrow-inflow",
    "4214": "borrow-interest-inflow",
    "4220": "investing-outflow",
    "4221": "CAPEX",
    "4223": "borrow-outflow",
    "4200": "ICF",
    "4310": "finance-inflow",
    "4312": "owners-inflow",
    "4322": 'dividends',
    "4320": "finance-outflow",
    "4300": "CFF",
}

credit_ratings = ['D', 'SD', 'RD', 'C', 'CC', 'CCC', 'B-', 'B', 'B+', 'BB-', 'BB', 'BB+',
                  'BBB-', 'BBB', 'BBB+', 'A-', 'A', 'A+', 'AA-', 'AA', 'AA+', 'AAA', 'Без рейтинга']

fin_metrics = [
    ('cagr-1-net-profit', 'LTM'),
    ('cagr-3-net-profit', 'LTM'),
    ('cagr-1-revenue', 'LTM'),
    ('cagr-3-revenue', 'LTM'),
    ('cagr-1-ebitda', 'LTM'),
    ('cagr-3-ebitda', 'LTM'),
    ('CAPEX/ebitda', 'all'),
    ('net-profit/revenue', 'all'),
    ('operation-profit/revenue', 'all'),
    ('ebitda/revenue', 'all'),
    ('turnover-accounts-receivable', 'all'),
    ('turnover-inventories', 'all'),
    ('turnover-current-assets', 'all'),
    ('OCF/revenue', 'all'),
    ('FCF/revenue', 'all'),
    ('net_debt/ebitda', 'all'),
    ('interest-payable/ebitda', 'all'),
    ('equity/assets', 'all'),
    ('current-assets/short-liabilities', 'all'),
    ('fast_liquidity/short-liabilities', 'all'),
    ('cash/short-liabilities', 'all'),
    ('OCF/short-liabilities', 'all'),
    ('operating-working-capital/assets', 'all'),
]

driver_path = '/opt/homebrew/bin/chromedriver'
openai_token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjU2OGMzODI4LWMyNjktNDk3Mi1iNmIwLWI4MjI0NTg1ZWFlZiIsImlzRGV2ZWxvcGVyIjp0cnVlLCJpYXQiOjE3MzYzMjUwMzYsImV4cCI6MjA1MTkwMTAzNn0.C3cHpkx98isnQK4YiiCvQpAOGFpiY_72Yjgy_BcG6ck'
report_images_dir = '/Users/maksimlobanov/Desktop/images'
download_path = '/Users/maksimlobanov/Desktop/reports'
downloads_dir = '/Users/maksimlobanov/Downloads'
reports_dir = '/Users/maksimlobanov/Desktop/reports'
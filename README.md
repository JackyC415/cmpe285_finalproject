# Stock Portfolio Suggestion Engine

# App Deployment Url: 
https://cmpe285teamblitzfinalproject.herokuapp.com/

# Pre-req: 
Make sure to install python3, set up Django environment with virtual env and install all the requirement dependencies listed in requirements.txt

# Instructions to run: 
git clone https://github.com/JackyC415/stock-portfolio-suggestion-engine-djangoapp.git && cd stock-portfolio-suggestion-engine-djangoapp && python3 manage.py runserver

# Step by Step (MacOS):
1) git clone https://github.com/JackyC415/stock-portfolio-suggestion-engine-djangoapp.git (clone repository)
2) cd stock-portfolio-suggestion-engine-djangoapp (enter cloned directory)
3) python3 manage.py runserver (launch server locally)
4) open browser -> http://localhost:8000

# Project Description:

### Input

User will input dollar amount to invest in USD (Minimum is $5000 USD)

Pick one or two investment strategies:
- Ethical Investing
- Growth Investing
- Index Investing
- Quality Investing
- Value Investing

The engine needs to assign stocks or ETFs for a selected investment strategy. E.g.

Index Investing strategy could map to the following ETFs:

- Vanguard Total Stock Market ETF (VTI)
- iShares Core MSCI Total Intl Stk (IXUS)
- iShares Core 10+ Year USD Bond (ILTB)

And

Ethical Investing strategy could map to these stocks:

- Apple (APPL)
- Adobe (ADBE)
- Nestle (NSRGY)

Each strategy  map to at least 3 different stocks/ETFs.


### Output:

The suggestion engine will output:

- Which stocks are selected based on inputed strategies.
- How the money are divided to buy the suggested stock.
- The current values (up to the sec via Internet) of the overall portfolio (including all the stocks / ETFs)
- A weekly trend of the portfolio value. In order words, keep 5 days history of the overall portfolio value.

### Tech Stack:
Django, Python3, HTML5/CSS3/JS, Heroku, REST, Alphavantage Stock API

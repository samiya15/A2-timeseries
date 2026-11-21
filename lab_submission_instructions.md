# Lab Submission Instructions

---

## Student Details

**Name of the team on GitHub Classroom:** A2

**Team Member Contributions:**

**Member 1**

| **Details**                                                                                        | **Comment**                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
|:---------------------------------------------------------------------------------------------------|:------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **Student ID:**                                                                                    | 161136                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
| **Name:**                                                                                          | Abdullahi Samiya Issack                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| **What part of the lab did you personally contribute to,** <br>**and what did you learn from it?** | I was responsible for the data and Notebook 1. I chose JPMorgan Chase as <br/>our stock and justified it with the interest-rate link, downloaded the data on 17 November 2026, <br/>set up the shared configuration for the group, ran the data quality report and the candlestick <br/>and correlation analysis, and answered the Notebook 1 exercises. <br/>I learned that the data must be checked before any modelling, that a strong same-day correlation does not make a variable a useful predictor because its value is not known in advance, and that stock returns have much fatter tails than a normal distribution, <br/>which matters for risk management. |

**Member 2**

| **Details**                                                                                        | **Comment** |
|:---------------------------------------------------------------------------------------------------|:------------|
| **Student ID:**                                                                                   |  166437           |
| **Name:**                                                                              |    Fatuma Mohamed                     |
| **What part of the lab did you personally contribute to,** <br>**and what did you learn from it?** | I was responsible for Notebook 2 (stationarity and returns). I ran the ADF and KPSS tests on JPM's closing price and log return, studied the autocorrelation of returns, repeated the spurious regression experiment with different sample sizes and predictors, and compared GARCH models with fat-tailed and normal errors. I learned that stock prices are not stationary, so we must forecast returns instead, that regressing one price on another can show a strong relationship that is not real, and that the size of tomorrow's move is far easier to predict than its direction. |          

**Member 3**

| **Details**                                                                                        | **Comment** |
|:---------------------------------------------------------------------------------------------------|:------------|
|**Student ID:**                                                                                    |        |
| **Name:**                                                                                         |         |
| **What part of the lab did you personally contribute to,** <br>**and what did you learn from it?** |             |

**Member 4**

| **Details**                                                                                        | **Comment** |
|:---------------------------------------------------------------------------------------------------|:------------|
|**Student ID:**                                                                                    |         150209    |
| **Name:**                                                                                          |    Mungai Stacy         |
| **What part of the lab did you personally contribute to,** <br>**and what did you learn from it?** |    
I contributed to Notebook 4, focusing on multivariate time-series forecasting using Ridge Regression and Gradient Boosting. I worked on feature engineering, model tuning, walk-forward validation and feature ablation to evaluate how different predictor groups influenced forecasting performance. I learned how to prepare financial time-series data, prevent look-ahead bias, evaluate models against a naive forecasting baseline and interpret performance metrics such as RMSE, MAE and R². I also learned that more complex models and additional predictors do not necessarily guarantee better forecasting accuracy.         |

**Member 5**

| **Details**                                                                                        | **Comment** |
|:---------------------------------------------------------------------------------------------------|:------------|
| **Student ID:**                                                                                    |          112806      |
| **Name:**                                                                                          |      Waweru Casey    |
| **What part of the lab did you personally contribute to,** <br>**and what did you learn from it?** |  I was responsible for Notebook 7 (multi-horizon forecasting and Power BI export). I evaluated JPM's forecasts across 1, 5, 21 and 63 trading days, compared the forecasting model against the naive benchmark, analysed prediction interval coverage and forecast uncertainty, and worked on preparing the forecast outputs and Power BI dashboard. I learned that forecasting accuracy generally becomes less reliable over longer horizons, that prediction intervals help communicate uncertainty, and that a complex forecasting model is not necessarily better than a simple naive forecast. |

## Scenario

Your client is a portfolio manager at a financial institution. The manager wants to know what the **closing price of one stock** is likely to do over the next trading day, the next week, the next month and the next quarter (63 business days). The manager has been disappointed before by forecasts that looked excellent on a chart and failed in practice, so the client has set one condition:

> Show me that your forecast beats the simplest possible forecast ("tomorrow will be the same as today") on days that your model never saw, and tell me honestly how uncertain it is.

You will answer that question using **real market data** and **several predictors at once**, with the methods taught in the notebooks.

---

## Dataset

1. Your group must forecast **a stock that is different from NVDA**. Choose a company whose price history is available on Yahoo Finance (for example MSFT, JPM, TSLA, NVDA, KO, or a company listed on another exchange).
2. Download the data with the helper script:

    ```shell
    python download_data.py --target MSFT
    ```

    and then set `TARGET_TICKER = "MSFT"` in `tslab/config.py`, so that the notebooks load your stock.
3. If your stock is not available on Yahoo Finance (many Nairobi Securities Exchange shares are not), download the daily prices by hand from another site and let the script clean the file:

    ```shell
    python download_data.py --target SCOM --from-csv "data/Download Data - STOCK_KE_XNAI_SCOM.csv"
    ```

    Check the quality report that the script prints. Missing days, repeated prices (no trading), and very short histories will limit what you can do, and you must say so in your report. A history shorter than about four years cannot support the walk-forward settings used in the notebooks; reduce `INITIAL_TRAIN` in `tslab/config.py` and explain your choice.
4. The predictors (S&P 500, a technology fund, VIX, 10-year yield, US dollar, Brent crude, gold) are downloaded for you. You may add or replace predictors if you can justify why they would matter for **your** stock (for example, a local index for a local stock). Predictors must be known **before** the day you forecast.
5. State the **date on which you downloaded your data**. Market data providers revise history, so the date matters.

---

## What Every Tier Must Respect

These rules apply to Baseline, Intermediate and Advanced alike. They are the reason this lab exists.

1. **Forecast the return, then convert to a price.** A one-day-ahead prediction of the closing price is the last close multiplied by `exp(predicted log return)`.
2. **Never shuffle time.** Use walk-forward (expanding window) validation, as in Notebook 3. A random train/test split on a time series is a serious error.
3. **Fit every scaler and every model on the training block only.**
4. **Tune on data that is before your test period**, never on the test period.
5. **Compare every model with the naive forecast**, and report whether the difference is statistically significant (Diebold-Mariano test). A model that does not beat the naive forecast is a valid finding. You will not lose marks for an honest negative result. You will lose marks for hiding it.
6. **Run the look-ahead test** (`check_no_lookahead`) on every feature that you add.

---

## Baseline (Required)

1. **Prepare and understand your data**
   - Run the data quality report for your stock, and plot a candlestick chart for a period of your choice.
   - Test the closing price and the log return for stationarity (ADF and KPSS), and state the conclusion.

2. **Forecast with multiple predictors**
   - Build the forecast of the next-day log return using the feature set of Notebook 4 (or an improved one), with **at least one** model from this list: ARMAX, Ridge regression, gradient boosting.
   - Evaluate it with walk-forward validation, and report RMSE, MAE, the out-of-sample R2 and the directional accuracy **next to the naive forecast**.

3. **Produce the 63-day forecast**
   - Produce a forecast of the closing price for the next 63 business days, **with a lower and an upper bound**.
   - Save it as `./data/forecast_basic.csv` (columns: `date`, `forecast`, `lower`, `upper`).

4. **Power BI**
   - Import the CSV file and create a line chart that shows the last year of actual closing prices, the forecast, and the range.

5. **A short written verdict** (about half a page, in this file or in a separate file) that a portfolio manager could understand: does your model beat the naive forecast, how do you know, and how much should the client trust the 63-day forecast?

---

## Intermediate Level (Recommended)

Everything in Baseline, and:

1. **Compare at least three forecasts**
   - The naive forecast, one classical model (ARIMA, ARMAX or exponential smoothing), and one machine learning model (Ridge or gradient boosting) with many predictors.
   - Use the Diebold-Mariano test for each model against the naive forecast.

2. **Feature ablation**
   - Run a feature group ablation (Notebook 4, Step 8) and explain, in your own words, which group of predictors helps and which does not. Remember that a very small R2 difference is not a finding.

3. **Prediction intervals**
   - Estimate a 10% to 90% range with quantile regression, and report the **coverage** (the share of actual outcomes inside the range). Comment on whether the model is overconfident.

4. **Multi-horizon results**
   - Report the skill of your model at horizons of 1, 5, 21 and 63 days (Notebook 7), and explain why it changes with the horizon.

5. **Save and visualise**
   - Save all the forecasts in one CSV file, with a separate column for each method (`./data/forecast_intermediate.csv`).
   - Create a Power BI dashboard with a line chart comparing the methods, a table of the forecast values, and a card or table that shows the error metrics of each method.

---

## Advanced Level (Optional)

Everything in Intermediate, and:

1. **A neural network**
   - Train at least one recurrent or convolutional network (LSTM, GRU or CNN) on windows of your features, using the protocol of Notebook 6: scalers fitted on the training block only, a validation share taken from the **end** of the training block, early stopping, and a fixed random seed.
   - Report the **zero-forecast baseline** loss next to your validation loss, so that a reader can see whether the network learned anything.

2. **Tuning and stability**
   - Tune at least two hyperparameters (for example the window length, the number of units, or the dropout rate) using the validation data **only**, and show the results in a table.
   - Train with at least three different seeds and report the spread of the results. Explain what the spread tells you.

3. **Save and visualise**
   - Save all the forecasts, with a column for each model and each neural network configuration, in a single CSV file (`./data/forecast_advanced.csv`).
   - Create a Power BI dashboard with comparative charts for all the models, a summary table, and a visual that highlights differences between models (for example error metrics, or the cumulative back-test curves).

4. **A back-test with costs**
   - Run the long/short experiment of Notebook 4 (Step 11) for your best model, with transaction costs of 0, 5 and 10 basis points, and compare it with buy and hold. Explain why the result is not a trading recommendation.

5. **Use of an NVIDIA GPU (optional)**
   - If you have access to an NVIDIA GPU, explain what is needed to use it for training (see the note in Notebook 6), and document the effect on training time and on the results.

---

## General Instructions

- Every CSV file must contain a date column for the forecast period.
- Use the notebooks and the `tslab` package as your guide. You may copy and adapt code from them. You must be able to **explain every line** that you submit.
- Use your own words in the written parts. Describe what **your** results show, not what the notebooks said about the NVDA data.
- Keep your results reproducible: set the random seed, state the download date of your data, and make sure the notebooks run from top to bottom after a restart of the kernel.

### Video Demonstration

For all three tiers, submit the link to a short video (not more than 4 minutes) that shows:

1. Your stock and the data quality report.
2. Your main result table, with the naive forecast in it, and what you conclude from it.
3. Your Power BI report or dashboard with the forecast and the range.

| **Key**                | **Value** |
|:-----------------------|:----------|
| **Link to the video:** |           |

---
#### 1. Data

### The stock: JPMorgan Chase & Co. (JPM)

We forecast the closing price of **JPMorgan Chase (JPM)**, the largest bank in the United States, listed on the New York Stock Exchange. We chose a bank because its profits depend directly on interest rates: when rates rise, the gap between what a bank earns on loans and what it pays on deposits usually widens. That gives the predictors in this lab a clear economic reason to matter for JPM:

- **S&P 500 and VIX:** JPM is a large part of the US market and moves with overall market mood.
- **10-year US Treasury yield (US10Y):** the main interest-rate signal for a bank. In our data, JPM's daily returns correlate **0.29** with changes in the 10-year yield, about twice as strongly as the S&P 500 (0.14) or the technology fund (0.11). This supports the idea that interest rates matter more for JPM than for the market as a whole.
- **Brent crude, gold and the US dollar:** broader economic conditions. Gold and the dollar show almost no same-day correlation with JPM (−0.06 and −0.02), so we do not expect them to help much.

### Source and download date

| Item | Value |
|:-----|:------|
| Source | Yahoo Finance, via `python download_data.py --target JPM` |
| **Download date** | **17 November 2026** |
| Period | 2 January 2015 to 9 November 2026 |
| Trading days | 2,981 |
| Predictors | S&P 500, XLK (technology), VIX, 10-year yield, US dollar index, Brent crude, gold |

### Data quality report

| Check | Result |
|:------|-------:|
| Duplicate dates | 0 |
| Missing values | 0 |
| Non-positive prices | 0 |
| Days with zero volume | 0 |
| High below low | 0 |
| Longest gap (days) | 4 |
| Days with a move over 10% | 7 |

The data is clean: there are no duplicates, missing values, impossible prices or untraded days. The longest gap of 4 calendar days is a long weekend with a public holiday, not missing data. The 7 days with moves over 10% are genuine market events, mostly from the COVID-19 crash of March 2020, and we kept them. Removing them would make the models look more accurate than they would be in a real crisis. The predictor markets trade on a few days when the NYSE is closed (2,988 rows against 2,981), so predictors are aligned to JPM's trading days and forward-filled for at most 3 days.

With almost 12 years of history, the data is long enough for the walk-forward settings in the notebooks, so we did not change `INITIAL_TRAIN`.

### What the data shows

- **Candlestick charts:** we plotted the last 90 trading days and the COVID-19 crash (February to April 2020). In the crash, JPM fell from about \$115 to about \$66 (roughly −40%) in a month, while daily volume rose to around four times its normal level.
- **Returns are not normally distributed:** the histogram of daily log returns has a much taller peak and much fatter tails than a normal curve. The worst days were around −15%, which a normal distribution treats as practically impossible.
- **Volatility clusters:** large moves come in groups (for example, 2020) rather than being spread evenly over time.

### Stationarity

We tested JPM's closing price and its daily log return with two tests that ask opposite questions. The ADF test assumes the series is non-stationary, and the KPSS test assumes it is stationary. We only call a series stationary when both agree.

| Series | ADF p-value | KPSS p-value | Verdict |
|:-------|------------:|-------------:|:--------|
| Closing price | 0.9976 | 0.0100 | Non-stationary |
| Log of the closing price | 0.9067 | 0.0100 | Non-stationary |
| First difference of the price | 0.0000 | 0.0963 | Stationary |
| **Log return** | **0.0000** | **0.1000** | **Stationary** |

**Conclusion:** JPM's closing price is not stationary. It trends from about \$50 in 2015 to about \$350 in 2026, and its 63-day rolling standard deviation grows from about 2 to about 20 dollars. The daily log return is stationary: it stays centred on zero, and both tests agree. Taking the logarithm alone was not enough, and removing a straight-line trend did not work either (ADF p = 0.85). Only differencing removed the wandering. We therefore forecast the **log return** and convert it back to a price, as the lab requires.

The return is not perfectly stable, though. Its volatility comes in clusters: the rolling standard deviation is usually 0.01 to 0.02, but it rose to about 0.057 during the COVID-19 crash in 2020.

We also checked for a calendar pattern. No weekday had an average return that was significantly different from zero (the largest t-statistic was 1.37, for Wednesday), and the 21-day seasonal component of the decomposition had a range of only 0.007, against 2.15 for the trend. JPM's daily returns show no seasonality worth modelling.

## 2. Written Verdict for the Portfolio Manager

**Does our model beat the naive forecast?** No, not in any way that matters. We tested seven classical models (Notebook 3) and two machine learning models using seven market predictors (Notebook 4) on days the models had never seen, using walk-forward validation. The best model, Ridge regression, had an average one-day error (RMSE) of \$2.9595, against \$2.9620 for the naive forecast ("tomorrow's close = today's close"). That is a difference of a quarter of a cent per share.

**How do we know?** The Diebold-Mariano test checks whether a difference in accuracy is bigger than luck. For Ridge the p-value was 0.75, far above the 0.05 threshold, so the improvement is not statistically significant. ARMAX, the classical model using the same seven predictors, gave the same answer (p = 0.59). Gradient boosting was significantly *worse* than the naive forecast (p < 0.05). Ridge called the direction of the next day's move correctly 53.6% of the time, only slightly better than a coin toss, and too small an edge to rely on. Over longer horizons (5, 21 and 63 days), our gradient boosting model did not beat the naive forecast either. A Ridge model did slightly better at 21 days, but only because it learned that JPM tended to rise over this period, not from the predictors.

**What this means:** JPM's price moves are very hard to predict from public market data, which is what we would expect from a large, heavily traded stock in an efficient market. For practical purposes, the best single estimate of tomorrow's price is today's price.

**How much should you trust the 63-day forecast?** Treat it as a range, not a target. From the last close of \$342.08 (9 November 2026), the central forecast for early February 2027 is about \$372, with an 80% range of roughly \$332 to \$415. When we tested these ranges on past data, the actual price fell inside the one-day range about 77% of the time, close to the intended 80%. Inside the 63-day range, though, it was only about 58%. The longer the horizon, the more **overconfident** the model becomes: the real uncertainty over a quarter is larger than the range suggests.

**Bottom line:** Do not use this model to time trades in JPM. Its value is in showing how wide the realistic range of outcomes is over the next quarter, and even that range should be treated as too narrow.
## Notebook Exercise Answers

### Notebook 1: Market Data, Candlestick Charts, and Returns

**Stock:** JPMorgan Chase (JPM) | **Data downloaded:** 17 November 2026 | **Answered by:** Samiya Issack

**1. In the data quality report, which line would worry you most if it were not zero, and why?**

`high_below_low` would worry me most. A day's high can never be below its low, so a non-zero value means the data is 
corrupted, not just incomplete, and we could not trust the Close prices the models learn from. For JPM every error line
is zero; the 7 days with moves over 10% are real market events from 2020, not errors.

**2. "The S&P 500 correlates 0.7 with our stock, so it will be an excellent predictor." What is missing from that 
argument?**

JPM's correlation with the S&P 500 is 0.71, but it is a same-day correlation: both markets close at the same time, 
so we do not know today's S&P return when we make the forecast. What matters is whether yesterday's S&P return helps 
predict today's JPM return, and that relationship is usually much weaker.

**3. What does the volume do when the price falls sharply (February to April 2020)? Why might that be?**

Between February and late March 2020, JPM fell from about $115 to about $66, roughly 40%, while daily volume rose
from about 10 million shares to 35–45 million, around four times normal. The heaviest volume came on the sharpest
down days, because many investors sold at once out of panic, to meet margin calls, or to meet fund redemptions. A 
smaller spike in mid-April matches JPM's first-quarter earnings, when it reported large provisions for COVID-related 
loan losses.

**4. A price rises 50% in year one and falls 50% in year two. What are the total simple and log returns?**

The price goes from 100 to 150 and then to 75, so the total simple return is −25%, not 0%. The total log return 
is ln(1.5) + ln(0.5) = 0.405 − 0.693 = −0.288, which equals ln(0.75). Log returns add up across periods and simple 
returns do not, which is one reason we model log returns.

**5. Name one risk management decision that would be wrong if returns followed the normal curve.**

JPM's returns have a much taller peak and much fatter tails than the normal curve, and its worst days were 
around −15%, a move the normal curve treats as practically impossible. A Value-at-Risk estimate based on the
normal curve would therefore badly underestimate how often large losses happen, and the bank could hold too 
little capital for a crash like March 2020.
### Notebook 2: Stationarity and Returns

**Stock:** JPMorgan Chase (JPM) | **Answered by:** Fatuma Mohamed

**1. What do the ADF results on the closing price and the log return mean for forecasting?**

For JPM's closing price, the ADF p-value is 0.998, so we cannot reject the idea that the price wanders with no fixed level. A model trained on past prices would be learning from a series whose average keeps changing. For the log return the p-value is close to 0 (and KPSS agrees), so returns have a stable centre and spread, and a relationship learned from the past is more likely to still hold in the future. This is why we forecast returns and not prices.

**2. The log transformation alone did not make the price stationary. What did it achieve instead?**

The log price is still non-stationary (ADF p = 0.907), because the upward trend is still there. What the log did was stabilise the variance: a $10 move when JPM was at $50 and a $70 move when it was at $350 become changes of a similar size in log terms. Differencing the log price then removes the trend, which gives the log return.

**3. What happens to the share of "significant" relationships with n_steps = 100 and 5000?**

The regression on levels found a "significant" relationship between two unrelated random walks in 79% of pairs with 100 steps, 92% with 1,000 steps and 96% with 5,000 steps. The regression on changes stayed at the expected false-alarm rate of about 5% (6%, 3% and 6%). More data makes the spurious regression problem worse, not better. Collecting a longer history cannot fix a regression of one trending price on another.

**4. Repeat the levels versus changes comparison with another predictor.**

With Brent crude, the levels regression gives R² = 0.367, but the changes regression gives only 0.045, so most of the apparent relationship came from both series drifting over time. The S&P 500 gives R² = 0.963 in levels and 0.509 in changes. That is a real same-day relationship, because JPM is part of the market. However, it is a same-day relationship, so it still does not show that the S&P 500 can forecast JPM's next-day return.

**5. Where would the log return of a stock sit on the lecture slide with nine plots?**

The log return belongs with the stationary series, because it fluctuates around a constant mean of zero with no trend; its 63-day rolling mean stays flat at zero throughout. It is only approximately stationary, though. The rolling standard deviation usually sits between 0.01 and 0.02 but jumped to about 0.057 in 2020, so its variance is not constant over time.

**6. Change the GARCH distribution to normal. How do the parameters change, and which fit is better?**

With the normal distribution, beta fell from 0.818 to 0.793 and omega rose from 0.144 to 0.203. The normal model has to explain JPM's extreme days as sudden jumps in volatility, because it does not allow fat tails. The Student's t version fits much better: its log-likelihood is −5,206.9 against −5,363.7 for the normal (and its AIC is lower, 10,424 against 10,736). Its tail parameter nu = 4.67 confirms that extreme days happen far more often than a normal distribution allows.

## Notebook3: Classical and Forecasting baselines

**Stock:** JPMorgan Chase (JPM) | **Answered by:** Veronicah Mbuvi

**1. Which model has the lowest RMSE? Is it significantly better than the naive forecast according to the Diebold-Mariano test? Write one sentence that a manager could understand.**

ANS:The Drift model has the lowest RMSE, but it is not significantly better than the naive forecast.

**2. In the SES section, what does an alpha close to 1 say about the series?**

 ANS:An alpha close to 1 means that the model gives more weight to recent observations than to older observations. This means that recent stock movements have a strong influence on the forecast.

**3. Compare `ARMA(1,0), own past only` with `ARMAX(1,0), 7 predictors`. Did the extra predictors improve the out-of-sample R2? Offer one possible reason for your finding.**

ANS:The extra predictors did not improve the out-of-sample R^2. Both models performed slightly worse than the naive benchmark. One possible reason is that external market variables do not provide enough useful information to predict JPM's next-day returns.

**4. Remove the `.shift(1)` in Step 5 (so that the predictors are from day s instead of s-1), and run the comparison again. What happens to the R2 and the directional accuracy? Why is the result worthless, even though it looks wonderful?**

ANS:Removing .shift(1) increased the out-of-sample R^2 from -0.0069 to 0.6104 and directional accuracy from 53.34% to 75.35%. However, the results are misleading because the model uses same-day predictor information.

**5. Add a SARIMA model with `seasonal_order=(1, 0, 0, 5)` (a weekly pattern). Does it improve on ARMA(1,0)? Does your answer agree with Notebook 2, Step 8?**

ANS:SARIMA performed almost the same as ARMA. However,it had slightly lower RMSE (2.9644 compared to 2.9670) and slightly higher directional accuracy (51.77% compared to 51.38%). However, its R^2 was slightly worse (-0.0095 compared to -0.0087). This suggests that adding a weekly seasonal component of five trading days did not significantly improve forecasting performance. The results are  similar to those obtained in Notebook 2, suggesting that the weekly seasonal pattern provides little additional predictive value.

**6. Change the moving average window in Step 3.3 from 20 to 5, and then to 60. How does the lag change, and why?**

ANS:5 days: Reacts quickly to recent price changes but is more sensitive to short-term changes.
20 days: Provides a balance between recent and older price movements.
60 days: Produces a smoother forecast but reacts more slowly to changes.

**7. In Step 9, the interval grows with the horizon. By what factor does the width at day 63 exceed the width at day 1? (Hint: what is the square root of 63?)**

ANS:The forecast interval at day 63 is approximately 7.94 times wider than the interval at day. This happens because uncertainty increases as the forecast horizon becomes longer


### Notebook 4: Multivariate machine learning forecasting

**Stock:** JPMorgan Chase (JPM) | **Answered by:** Stacy Mungai


**1. Write one sentence that a portfolio manager could understand, summarising whether your best model beats the naive forecast. Include the evidence (the DM p-value) in that sentence.**

Our best model, Ridge regression, had a one-day error of \$2.9595 against \$2.9620 for simply assuming tomorrow's price equals today's, but the Diebold-Mariano test gives a p-value of 0.7476, so this tiny improvement is not statistically significant and the model does not genuinely beat the naive forecast.

**2. In Step 3.2, change `center=True` to `center=False`. Does the truncation test still catch it? Why?**

No. With `center=False` the test passes, because there is no longer a leak to catch. A centred 5-day window for day t uses the prices of days t+1 and t+2, which are not known on day t, so removing the future changes the value and the test flags it. A trailing window (`center=False`) uses only day t and the four days before it, so its value is the same whether or not the future is in the table.

**3. Add a new feature of your own to `tslab/features.py`. Run `check_no_lookahead` on it before you evaluate it.**

We added `volume_ratio_10_60`, the 10-day average trading volume divided by the 60-day average. It shows whether trading activity is unusually high or low compared with normal, which often happens around news or market stress. Before using it, we ran `check_no_lookahead` on the full feature set including the new feature, and it passed: the value does not change when future rows are removed, because both averages use only past days.

**4. Repeat the ablation in Step 8 with gradient boosting. Do the two models agree on which groups matter?**

The feature ablation analysis was repeated using the tuned Gradient Boosting model and compared with the Ridge Regression results.
The Ridge Regression results showed that historical returns were the most useful individual predictor group, achieving an R² of 0.00107. Removing returns reduced the model's R² to 0.00052, suggesting that historical returns contributed positively to its forecasting performance. Removing other-market predictors increased the R² to 0.00094, suggesting that this group provided limited additional value.

For Gradient Boosting, the model using all features achieved an R² of -0.01055, indicating performance below the naive forecasting benchmark. Calendar features achieved the best individual group R² of -0.00343, followed by volume at -0.00764. Removing technical indicators reduced the R² to -0.01533, while removing other-market predictors reduced it to -0.01230. This suggests that technical and other-market predictors contributed positively to Gradient Boosting's performance. However, removing returns improved the R² to -0.00753, suggesting that this group did not improve the model.

Overall, the two models do not agree completely on which predictor groups matter. Ridge Regression benefits most from historical returns, whereas Gradient Boosting appears to benefit more from technical and other-market predictors. Additionally, Gradient Boosting performed worse than the naive benchmark, while Ridge Regression achieved a small positive R². This demonstrates that different machine-learning models can respond differently to the same predictor groups.
**5. In Step 6, we tuned on the first 1000 days only. What is the weakness of that approach if the market changes character later? (Think about 2020.)**

 The main weakness is that the first 1,000 trading days may not represent future market conditions. For example, the COVID-19 pandemic in 2020 caused unusual market volatility and changes in trading behaviour. Consequently, parameters selected using earlier data may perform poorly when market conditions change. Using rolling or expanding-window validation would help the model adapt to different market conditions.

**6. Change the loss in `make_boosting` to `"absolute_error"`. Why might that be more robust for returns with fat tails?**

Absolute error is more robust because it penalises prediction errors linearly rather than squaring them. This means that unusually large returns or extreme market movements have less influence on the model compared with squared-error loss. It can therefore be useful when financial returns contain extreme values, also known as fat tails.

**7. Step 11 assumed we could trade at the close, at the price we used to forecast. Why is that optimistic?**

This assumption is optimistic because the closing price used to generate the forecast may not be available when the trading decision is made. In reality, executing a trade may involve delays, bid-ask spreads, transaction costs and slippage. A more realistic backtest should use an achievable execution price, such as the next available trading price, and account for these costs.

### Notebook 7: Multi-horizon Forecasts and Power BI Export

**Stock:** JPMorgan Chase (JPM) | **Answered by:** Casey Waweru

**1. At which horizon is the model's skill highest and lowest? How certain can you be, given how few independent test periods a 63-day horizon has?**

The model's out-of-sample R² is negative at every horizon, so it never beats the naive forecast. It is least bad at 1 day (R² = −0.047) and worst at 63 days (R² = −0.300), and it gets steadily worse as the horizon grows (−0.113 at 5 days, −0.171 at 21 days). The 63-day result is also the least certain: its 1,657 test rows overlap heavily, so they contain only about 26 independent quarters, which is far too few to draw firm conclusions from.

**2. Use the table in Step 4 to write the two-sentence statement for a client about the 21-day-ahead forecast.**

Our 21-day forecast was slightly less accurate than simply assuming the price stays where it is (an average error of \$13.01 against \$12.69), and it called the direction correctly only 51% of the time, so it gives no reliable view on whether JPM will be higher or lower in a month. Our 80% range for the price in 21 days was about 14% of the price wide, but in testing the actual price fell inside it only 67% of the time, so the real uncertainty is larger than the range suggests.

**3. Change `gap = h - 1` to `gap = 0` for horizon 21. Does the score improve? Why would the improvement be misleading?**

Yes. Without the gap, the R² improved from −0.171 to −0.110, the RMSE fell from \$13.01 to \$12.82, and the directional accuracy rose from 51.2% to 54.1%. The improvement is fake. Each 21-day label overlaps the next 20 days, so without a gap the last training rows contain returns from inside the test period. The model is partly being tested on information it was trained on, and that would never be available when forecasting for real.

**4. Compare the width of the 63-day range with the width of the 1-day range. Is the ratio close to the square root of 63? What does that say about how risk grows with time?**

The 1-day range was 3.65% of the price wide and the 63-day range was 20.18%, a ratio of 5.5, below the square root of 63 (about 7.9). This does not mean risk grows more slowly than the square-root-of-time rule. The share of actual prices inside the range fell from 79% at 1 day to 58% at 63 days, so the long-horizon ranges are too narrow. The model underestimates how far the price can drift over a quarter, and the true 63-day range should be wider.

**5. Train the 21-day model with Ridge instead of gradient boosting. Which one has the better walk-forward score?**

Ridge scored better: an RMSE of \$12.44 against \$13.01 for gradient boosting and \$12.69 for the naive forecast, a slightly positive R² of 0.013, and a directional accuracy of 61.2%. However, JPM rose in exactly 61.2% of all 21-day periods in the test data. With its very strong penalty (alpha = 100,000), Ridge has learned little more than "JPM tends to drift upward" and predicts a small rise almost every time. Its edge comes from the stock's upward trend during this period, not from the predictors, and it would disappear in a falling market.

**6. In Power BI, build a line chart showing the actual closing price for the past year, the forecast path, and the range on a single chart.**

*(To be added by Casey Waweru: a screenshot of the Power BI chart and a short description.)*
## How Your Submission Will Be Marked (Out of 100)

| #   | What you need to show                                                                                                                | Marks |
|:----|:-------------------------------------------------------------------------------------------------------------------------------------|------:|
| 1   | **Data**: a justified stock, a data quality check, a stated download date, and a stationarity analysis                               | 10    |
| 2   | **Honest validation**: walk-forward validation, no look-ahead, tuning before the test period, scalers fitted on the training block   | 25    |
| 3   | **Evaluation against the naive forecast**: metrics, the Diebold-Mariano test, and a correct reading of the result                    | 20    |
| 4   | **Modelling quality** for your tier (see the tier descriptions above)                                                                | 15    |
| 5   | **Uncertainty**: a forecast range, and (Intermediate and Advanced) the coverage of the range                                          | 10    |
| 6   | **Power BI** report or dashboard for your tier, readable by a manager                                                                | 10    |
| 7   | **Written verdict and video**: clear, honest, in your own words, within 4 minutes                                                    | 10    |

### Caps (these apply to the whole submission)

- **No naive forecast as a comparison**: your total is capped at 50.
- **Randomly shuffled train/test split, or any scaler or model that was fitted using the test period**: your total is capped at 50.
- **Features that use future information** (look-ahead bias) in the final model: your total is capped at 60.
- **Same stock as the notebooks (NVDA)**: your total is capped at 60.
- **No individual contribution documented** for a team member: minus 5 for each such member.

### Grading Approach

- Baseline = Pass >= 60%
- Intermediate = Merit 75 to 85%
- Advanced = Distinction >= 86%

A model that does **not** beat the naive forecast does not lose marks for that reason. A claim that it does, without the evidence, does.

### Before You Submit, Check

- [ ] The notebooks run from top to bottom after restarting the kernel.
- [ ] The naive forecast appears in every result table.
- [ ] The CSV files for your tier are in the `data` folder and open correctly in Power BI.
- [ ] Your written verdict says plainly whether the model beats the naive forecast.
- [ ] The video is not longer than 4 minutes and the link works without a login.
- [ ] The contribution of every team member is filled in at the top of this file.

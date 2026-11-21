
"""
Turning prices into predictors (also called "features").

WHAT THIS FILE DOES
A model cannot learn much from a raw list of prices. So we compute
useful numbers from the prices, such as "how much did the stock move this
week?" or "how jumpy has it been lately?". Each of these numbers is a
FEATURE. The model uses the features to make its forecast.

THE GOLDEN RULE: NO PEEKING AT THE FUTURE
Each feature for day t may use only data available on or before day t.
Using future information creates LOOK-AHEAD BIAS (DATA LEAKAGE).

HOW EACH ROW OF THE TABLE IS ORGANIZED
Every row is one trading day.
    features : computed from prices up to the close of day t
    target   : what happens AFTER day t

WE PREDICT THE RETURN, NOT THE PRICE
predicted close tomorrow = today's close * exp(predicted log return)
"""

import numpy as np
import pandas as pd

LEVEL_PREDICTORS = ["SP500", "TECH", "GOLD", "BRENT", "USD"]
RATE_PREDICTOR = "US10Y"
FEAR_PREDICTOR = "VIX"


# ---------------------------------------------------------------------------
# HELPER FUNCTIONS
# ---------------------------------------------------------------------------

def log_return(series, periods=1):
    """
    Calculate the log return over the specified number of days.
    """
    return np.log(series).diff(periods)


def rsi(close, window=14):
    """
    Relative Strength Index.
    """
    change = close.diff()
    gains = change.clip(lower=0)
    losses = -change.clip(upper=0)

    avg_gain = gains.ewm(
        alpha=1 / window,
        adjust=False,
        min_periods=window
    ).mean()

    avg_loss = losses.ewm(
        alpha=1 / window,
        adjust=False,
        min_periods=window
    ).mean()

    relative_strength = avg_gain / avg_loss.replace(0, np.nan)

    return 1 - 1 / (1 + relative_strength)


def macd_histogram(close, fast=12, slow=26, signal=9):
    """
    Calculate the MACD histogram.
    """
    fast_ema = close.ewm(span=fast, adjust=False).mean()
    slow_ema = close.ewm(span=slow, adjust=False).mean()

    macd_line = fast_ema - slow_ema
    signal_line = macd_line.ewm(span=signal, adjust=False).mean()

    return (macd_line - signal_line) / close


def bollinger(close, window=20, num_std=2.0):
    """
    Calculate Bollinger Bands.
    """
    middle = close.rolling(window).mean()
    spread = close.rolling(window).std()

    upper = middle + num_std * spread
    lower = middle - num_std * spread

    percent_b = (close - lower) / (upper - lower)
    width = (upper - lower) / middle

    return percent_b, width


def average_true_range(high, low, close, window=14):
    """
    Calculate Average True Range.
    """
    previous_close = close.shift(1)

    true_range = pd.concat(
        [
            high - low,
            (high - previous_close).abs(),
            (low - previous_close).abs()
        ],
        axis=1
    ).max(axis=1)

    return true_range.rolling(window).mean() / close


# ---------------------------------------------------------------------------
# BUILDING THE FULL FEATURE TABLE
# ---------------------------------------------------------------------------

def build_features(frame):
    """
    Build every feature from the raw market data.

    Input:
        frame - market data containing Open, High, Low, Close and Volume,
                together with other market predictors.

    Output:
        A dataframe containing all calculated features.
    """

    # Pull out the five basic price columns.
    close, open_, high, low, volume = (
        frame[c]
        for c in ["Close", "Open", "High", "Low", "Volume"]
    )

    # Calculate daily returns.
    daily_return = log_return(close)

    # Create an empty feature table.
    out = pd.DataFrame(index=frame.index)

    # ----------------------------------------------------------------------
    # GROUP 1: RETURNS
    # ----------------------------------------------------------------------

    for lag in range(1, 6):
        out[f"ret_lag{lag}"] = daily_return.shift(lag - 1)

    out["ret_5d"] = log_return(close, 5)
    out["ret_10d"] = log_return(close, 10)
    out["ret_21d"] = log_return(close, 21)
    out["ret_63d"] = log_return(close, 63)

    # ----------------------------------------------------------------------
    # GROUP 2: VOLATILITY
    # ----------------------------------------------------------------------

    out["vol_5d"] = daily_return.rolling(5).std()
    out["vol_21d"] = daily_return.rolling(21).std()
    out["vol_63d"] = daily_return.rolling(63).std()

    out["vol_ratio"] = out["vol_5d"] / out["vol_21d"]

    out["range_hl"] = np.log(high / low)

    out["atr_14"] = average_true_range(high, low, close)

    # ----------------------------------------------------------------------
    # GROUP 3: TECHNICAL INDICATORS
    # ----------------------------------------------------------------------

    out["rsi_14"] = rsi(close)

    out["macd_hist"] = macd_histogram(close)

    out["bb_percent_b"], out["bb_width"] = bollinger(close)

    for window in (20, 50, 200):
        out[f"dist_sma_{window}"] = np.log(
            close / close.rolling(window).mean()
        )

    out["gap_overnight"] = np.log(open_ / close.shift(1))

    out["move_intraday"] = np.log(close / open_)

    # ----------------------------------------------------------------------
    # GROUP 4: VOLUME
    # ----------------------------------------------------------------------

    # Today's volume compared with the average of the last 20 days.
    out["volume_rel_20d"] = np.log(
        volume / volume.rolling(20).mean()
    )

    # Average volume over the last 10 days compared with the last 60 days.
    out["volume_ratio_10_60"] = (
        volume.rolling(10).mean() /
        volume.rolling(60).mean()
    )

    # ----------------------------------------------------------------------
    # GROUP 5: OTHER MARKETS
    # ----------------------------------------------------------------------

    for name in LEVEL_PREDICTORS:
        out[f"{name}_ret_1d"] = log_return(frame[name], 1)
        out[f"{name}_ret_5d"] = log_return(frame[name], 5)

    out["VIX_level"] = np.log(frame[FEAR_PREDICTOR])

    out["VIX_change_1d"] = log_return(
        frame[FEAR_PREDICTOR], 1
    )

    out["US10Y_level"] = frame[RATE_PREDICTOR]

    out["US10Y_change_5d"] = frame[RATE_PREDICTOR].diff(5)

    out["relative_to_SP500_5d"] = (
        out["ret_5d"] - out["SP500_ret_5d"]
    )

    # ----------------------------------------------------------------------
    # GROUP 6: CALENDAR
    # ----------------------------------------------------------------------

    weekday = frame.index.day_of_week

    for day, label in enumerate(
        ["mon", "tue", "wed", "thu", "fri"]
    ):
        out[f"is_{label}"] = (weekday == day).astype(float)

    month = frame.index.month

    out["month_sin"] = np.sin(2 * np.pi * month / 12)

    out["month_cos"] = np.cos(2 * np.pi * month / 12)

    return out


# ---------------------------------------------------------------------------
# FEATURE GROUPS
# ---------------------------------------------------------------------------

FEATURE_GROUPS = {
    "returns": [
        "ret_lag1", "ret_lag2", "ret_lag3", "ret_lag4", "ret_lag5",
        "ret_5d", "ret_10d", "ret_21d", "ret_63d"
    ],

    "volatility": [
        "vol_5d", "vol_21d", "vol_63d",
        "vol_ratio", "range_hl", "atr_14"
    ],

    "technical": [
        "rsi_14", "macd_hist", "bb_percent_b", "bb_width",
        "dist_sma_20", "dist_sma_50", "dist_sma_200",
        "gap_overnight", "move_intraday"
    ],

    "volume": [
        "volume_rel_20d",
        "volume_ratio_10_60"
    ],

    "other_markets": [
        "SP500_ret_1d", "SP500_ret_5d",
        "TECH_ret_1d", "TECH_ret_5d",
        "GOLD_ret_1d", "GOLD_ret_5d",
        "BRENT_ret_1d", "BRENT_ret_5d",
        "USD_ret_1d", "USD_ret_5d",
        "VIX_level", "VIX_change_1d",
        "US10Y_level", "US10Y_change_5d",
        "relative_to_SP500_5d"
    ],

    "calendar": [
        "is_mon", "is_tue", "is_wed", "is_thu", "is_fri",
        "month_sin", "month_cos"
    ],
}

ALL_FEATURES = [
    name
    for group in FEATURE_GROUPS.values()
    for name in group
]


# ---------------------------------------------------------------------------
# BUILD THE DATASET
# ---------------------------------------------------------------------------

def make_dataset(frame, horizon=1):
    """
    Build the final modelling dataset.
    """

    features = build_features(frame)

    data = features.copy()

    data["close"] = frame["Close"]

    # Future values are used only as prediction targets.
    data["target_close"] = frame["Close"].shift(-horizon)

    data["target_return"] = np.log(
        frame["Close"].shift(-horizon) / frame["Close"]
    )

    data = data.replace([np.inf, -np.inf], np.nan)

    feature_ready = data[ALL_FEATURES].notna().all(axis=1)

    return data[feature_ready]


# ---------------------------------------------------------------------------
# CHECK FOR LOOK-AHEAD BIAS
# ---------------------------------------------------------------------------

def check_no_lookahead(frame, feature_function=None, n_checks=5, seed=0):
    """
    Check that features do not use future information.
    """

    feature_function = feature_function or build_features

    rng = np.random.default_rng(seed)

    full = feature_function(frame)

    # Select rows where all features are available.
    valid_rows = np.where(full.notna().all(axis=1))[0]

    # Skip the final 10 rows.
    candidates = valid_rows[valid_rows < len(frame) - 10]

    if len(candidates) < n_checks:
        raise ValueError(
            f"Not enough valid rows for {n_checks} look-ahead checks. "
            f"Found {len(candidates)}."
        )

    cut_positions = rng.choice(
        candidates,
        size=n_checks,
        replace=False
    )

    for position in cut_positions:

        truncated = feature_function(
            frame.iloc[:position + 1]
        )

        differences = (
            full.iloc[position] - truncated.iloc[-1]
        ).abs()

        bad = differences[~(differences <= 1e-9)].index.tolist()

        assert not bad, (
            f"Look-ahead bias detected on "
            f"{frame.index[position].date()}: "
            f"these features changed when the future was removed: {bad}"
        )

    return True
        
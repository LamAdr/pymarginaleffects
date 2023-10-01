import statsmodels.formula.api as smf
import numpy as np
from marginaleffects import *
import polars as pl
from polars.testing import assert_series_equal

dat = pl.read_csv("https://vincentarelbundock.github.io/Rdatasets/csv/HistData/Guerry.csv")

mod = smf.ols("Literacy ~ Pop1831 * Desertion", dat).fit()

avg_predictions(mod, by = "Region")

def test_coefs():
    hyp_py = hypotheses(mod, hypothesis = np.array([1, -1, 0, 0]))
    hyp_r = pl.read_csv("tests/r/test_hypotheses_coefs.csv")
    assert_series_equal(hyp_r["estimate"], hyp_py["estimate"])
    assert_series_equal(hyp_r["std.error"], hyp_py["std_error"], check_names = False)


def test_comparisons():
    hyp_py = comparisons(mod, by = True, hypothesis = "b1 = b2")
    hyp_r = pl.read_csv("tests/r/test_hypotheses_comparisons.csv")
    # absolute because the order of rows is different in R and Python `comparisons()` output
    assert_series_equal(hyp_r["estimate"].abs(), hyp_py["estimate"].abs())
    assert_series_equal(hyp_r["std.error"], hyp_py["std_error"], check_names = False)


def test_null_hypothesis():
    # Test with hypothesis = 0
    hyp_py_0 = hypotheses(mod, hypothesis=np.array([1, -1, 0, 0]), hypothesis_null=0)
    hyp_r_0 = pl.read_csv("tests/r/test_hypotheses_coefs.csv")
    assert_series_equal(hyp_r_0["estimate"], hyp_py_0["estimate"])
    assert_series_equal(hyp_r_0["std.error"], hyp_py_0["std_error"], check_names=False)

    # Test with hypothesis = 1
    hyp_py_1 = hypotheses(mod, hypothesis=np.array([1, -1, 0, 0]), hypothesis_null=1)
    hyp_r_1 = pl.read_csv("tests/r/test_hypotheses_coefs_hypothesis_1.csv")
    assert_series_equal(hyp_r_1["estimate"], hyp_py_1["estimate"])
    assert_series_equal(hyp_r_1["std.error"], hyp_py_1["std_error"], check_names=False)


def test_hypothesis_list():
    # Hypothesis values from R
    hypothesis_values = [0.4630551, -112.8876651, -10.6664417, -5384.2708089]
    mod = smf.ols("Literacy ~ Pop1831 * Desertion", dat).fit()
    hyp = hypotheses(mod, hypothesis=3)
    assert np.allclose(hyp["statistic"], hypothesis_values)
    hyp = hypotheses(mod, hypothesis=3.)
    assert np.allclose(hyp["statistic"], hypothesis_values)
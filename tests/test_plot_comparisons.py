import os

import polars as pl
import pytest
import statsmodels.formula.api as smf

from marginaleffects import *
from marginaleffects.plot_comparisons import *

from .utilities import *



df = pl.read_csv(
    "https://vincentarelbundock.github.io/Rdatasets/csv/palmerpenguins/penguins.csv",
    null_values="NA",) \
        .drop_nulls() \
        .sort(pl.col("species"))
mod = smf.ols(
    "body_mass_g ~ flipper_length_mm * species * bill_length_mm + island",
    df.to_pandas(),
).fit()


def test_plot_comparisons():
    fig = plot_comparisons(mod, variables="species", by="island")
    assert assert_image(fig, "Figure_1", "plot_comparisons") is None

    fig = plot_comparisons(
        mod,
        variables="bill_length_mm",
        by="island",
    )
    assert assert_image(fig, "Figure_2", "plot_comparisons") is None

    fig = plot_comparisons(
        mod, variables="bill_length_mm", condition=["flipper_length_mm", "species"]
    )
    assert assert_image(fig, "Figure_3", "plot_comparisons") is None

    fig = plot_comparisons(mod, variables="species", condition="bill_length_mm")
    assert assert_image(fig, "Figure_4", "plot_comparisons") is None

    fig = plot_comparisons(mod, variables="bill_length_mm", condition="species")
    assert assert_image(fig, "Figure_5", "plot_comparisons") is None

    fig = plot_comparisons(
        mod, variables="species", condition=["bill_length_mm", "species", "island"]
    )
    assert assert_image(fig, "Figure_6", "plot_comparisons") is None
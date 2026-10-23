import numpy as np
import pandas as pd
import pytest
from src.validation import validate_returns


def test_rejects_nonfinite_returns():
    with pytest.raises(ValueError):
        validate_returns(pd.DataFrame({"A": [0.01, np.inf]}))


def test_accepts_valid_returns():
    validate_returns(pd.DataFrame({"A": [0.01, -0.02]}))

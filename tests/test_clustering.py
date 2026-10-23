import numpy as np
import pandas as pd
from src.clustering import cluster_assets


def test_clustering_assigns_each_asset():
    rng = np.random.default_rng(10)
    returns = pd.DataFrame(rng.normal(0, 0.01, (180, 4)), columns=list("ABCD"))
    clusters = cluster_assets(returns)
    assert len(clusters) == 4
    assert clusters["Cluster"].notna().all()


def test_single_asset_cluster():
    returns = pd.DataFrame({"A": [0.01, -0.01, 0.02]})
    assert cluster_assets(returns)["Cluster"].iloc[0] == 0

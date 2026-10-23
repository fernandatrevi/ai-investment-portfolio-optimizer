"""Cluster assets using historical risk-return features."""
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from .metrics import asset_statistics


def cluster_assets(returns: pd.DataFrame, clusters: int = 3) -> pd.DataFrame:
    features = asset_statistics(returns)
    n = len(features)
    if n < 2:
        features["Cluster"] = 0
        return features
    k = min(clusters, n)
    scaled = StandardScaler().fit_transform(features)
    features["Cluster"] = KMeans(n_clusters=k, random_state=42, n_init=10).fit_predict(scaled)
    return features

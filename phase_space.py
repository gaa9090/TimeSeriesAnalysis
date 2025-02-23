# Based off of lharrison pypsr.py but made for current version of numpy 
# https://github.com/hsharrison/pypsr

import numpy as np
from sklearn.neighbors import NearestNeighbors
from sklearn import metrics

class phase_space:

    def __init__(self, controller):
        super().__init__()
        self.controller = controller 
        self.x = self.controller.df
        
        # data must be one dimensional
        if self.x.ndim != 1:
            raise ValueError("The input time series must be one-dimensional.")


    # Reconstruct the phase space of x(t) using a time lag and embedding dimension.
    def reconstruct(self, lag, n_dims):
        x = self.x
        if lag * (n_dims - 1) >= x.shape[0] // 2:
            raise ValueError("Longest lag cannot be longer than half the length of x(t).")

        lags = lag * np.arange(n_dims)

        stacked = np.vstack([x[start: start - lags[-1] or None] for start in lags])
        return stacked.transpose()


    # Compute the average mutual information (AMI) between x(t) and x(t+lag) for a range of lags.
    def _radius(self):
        x = self.x
        return np.sqrt(np.mean((x - np.mean(x))**2))


    # Determine if the nearest neighbor remains 'true' when an additional dimension is added.
    def _is_true_neighbor(self, indices, distance, offset,
                          relative_distance_cutoff=15, relative_radius_cutoff=2):
        x = self.x

        if (indices + offset >= len(x)).any():
            return False

        distance_increase = np.abs(x[indices[0] + offset] - x[indices[1] + offset])
        attractor_radius = self._radius()

        cond1 = (distance_increase / distance) < relative_distance_cutoff
        cond2 = (distance_increase / attractor_radius) < relative_radius_cutoff
        return cond1 and cond2
    

    # Evaluate the percentage of false nearest neighbors over a range of embedding dimensions.
    def global_false_nearest_neighbors(self, lag, min_dims=1, max_dims=10,
                                       relative_distance_cutoff=15, relative_radius_cutoff=2):
        dims = np.arange(min_dims, max_dims + 1)
        fnn_percentages = []

        for n_dims in dims:
            fnn = self._gfnn(lag, n_dims,
                             relative_distance_cutoff, relative_radius_cutoff)
            fnn_percentages.append(fnn)
        return dims, np.array(fnn_percentages)


    # helper function to compute false nearest neighbors for a single embedding dimension.
    def _gfnn(self, lag, n_dims, relative_distance_cutoff, relative_radius_cutoff):
        x = self.x
        offset = lag * n_dims
        Y = self.reconstruct(lag, n_dims)
        n_points = Y.shape[0]

        nbrs = NearestNeighbors(n_neighbors=2, algorithm='kd_tree').fit(Y)
        distances, indices = nbrs.kneighbors(Y)
        false_neighbor_flags = []

        for i in range(n_points):
            neighbor_idx = indices[i, 1]  
            distance = distances[i, 1]

            if (i + offset < len(x)) and (neighbor_idx + offset < len(x)):
                is_true = self._is_true_neighbor(
                    np.array([i, neighbor_idx]), distance, offset,
                    relative_distance_cutoff, relative_radius_cutoff)
                false_neighbor_flags.append(not is_true)

        return np.mean(false_neighbor_flags) if false_neighbor_flags else np.nan


    # Compute the average mutual information (AMI) between x(t) and x(t+lag) for a range of lags.
    def lagged_ami(self, min_lag=0, max_lag=None, lag_step=1, n_bins=10):
        x = self.x
        if max_lag is None:
            max_lag = len(x) // 2

        lags = np.arange(min_lag, max_lag, lag_step)
        amis = []

        for lag in lags:
            try:
                Y = self.reconstruct(lag, 2)
                H, _, _ = np.histogram2d(Y[:, 0], Y[:, 1], bins=n_bins)
                ami_val = metrics.mutual_info_score(None, None, contingency=H)
            except Exception:
                ami_val = np.nan
            amis.append(ami_val)

        return lags, np.array(amis)

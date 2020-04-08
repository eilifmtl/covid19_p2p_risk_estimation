# covid19_p2p_risk_estimation in the context of https://ai-against-covid.ca/
# Copyright (C) 2020 Eilif Muller

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


import numpy
import scipy
from scipy.stats import bernoulli
from copy import deepcopy
from tqdm import tqdm

import params


class MonteCarlo(object):
    def __init__(self, interactions=None):
        if interactions is None:
            interactions = [numpy.random.permutation(params.N)[:2] for i in range(params.M)]
        self.interactions = numpy.vstack(interactions)
        
        # Ensemble of size num_samples of
        # initial unobservable infections states for N agents
        self.I0 = bernoulli.rvs(params.prob_infection_t0, size=(params.num_samples,params.N))
        self.reset()
        
    def reset(self):
        # This is our running infection state
        self.I = deepcopy(self.I0)

    def run(self, watch_idx=None):
        if watch_idx is None:
            watch_idx = range(min(params.N,10))
        PI = []
        P_samples = []
        for i in tqdm(range(params.M)):
            a,b = self.interactions[i]
            newb = self.I[:,a]*bernoulli.rvs(params.prob_trans, size=(params.num_samples,))
            newa = self.I[:,b]*bernoulli.rvs(params.prob_trans, size=(params.num_samples,))
            self.I[:,a] = numpy.maximum(self.I[:,a], newa)
            self.I[:,b] = numpy.maximum(self.I[:,b], newb)
            PI.append(numpy.sum(self.I[:,watch_idx], axis=0).astype(float)/params.num_samples)
            P_samples.append(deepcopy(self.I[:,watch_idx]))
        return numpy.vstack(PI), P_samples

    

        
        
        

    

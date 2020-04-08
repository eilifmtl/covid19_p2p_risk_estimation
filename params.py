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



# Number of agents
N = 1000
# Number of interactions
M = N*100
# Transmission probability ~ R0/number of interactions while infectious, what constitutes an interaction? closer than 2m for 2minutes indoors? but touching objects ...
prob_trans = 0.05 # R0=2/40 interactions 
prob_infection_t0 = 0.01
num_samples = 99


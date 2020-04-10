
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

"""
This is an approximation of mean_field_agent.py for the case 
of no p2p messages due to privacy, but only support for 
disambiguated broadcast messages.

In this case a local agent has to keep a running estimate of 
the other agents risk estimation due to our interaction

This is exact if lambdas for both agents are equal, but since they can
depend on local observation of the context of the interaction, this
introduces some noise.  However it is probably less than the error
introduced by risk quantization.

"""

import params

class ContextObject(object):
    def __init__(self, t_exposed=0):
        self.t_exposed = t_exposed

# This could be context specific in the a V2
# It could be a complex AI model, integrating location info
# time exposed, etc.
def get_transmission_prob(context):
    return params.prob_trans

class Message(object):
    """ stores messages exchanged between contacts """
    def __init__(self, p=0.0, id=None):
        self.p = p
        self.id = id

class HistoryRecord(object):
    """ local store of history required of previous contact """ 
    def __init__(self, r_dagger, est_p_star_other, est_r_dagger_other, last_p):
        self.r_dagger = r_dagger
        self.est_p_star_other = est_p_star_other
        self.est_r_dagger_other = est_r_dagger_other
        self.last_p = last_p
    
class Agent(object):
    """ update rules for probability of infection
    for an agent coming in contact with another """
    
    def __init__(self, id=0, prob_initial_infection=params.prob_infection_t0): 
        self.id = id
        self.p = prob_initial_infection
        self.history = {}
    
    def prepare_message(self):

        # TODO obfuscation
        
        msg = Message(self.p, self.id)
         
        return msg

    def recv_message(self, msg, context):
        # Get the tranmission probability given the context
        _lambda = get_transmission_prob(context)
        
        # If existing, fetch my history of previous interactions with msg.id
        # otherwise create a new history
        h = self.history.setdefault(msg.id, HistoryRecord(0., 0., 0., 0.))

        # My record of unmanifested risk,
        r_dagger = h.r_dagger

        # My model of how other reacted to my interaction
        # This is new relative to mean_field_agent.Agent
        # allowing us to move from p2p to disambiguated broadcast messaging
        est_p_star_other = h.est_p_star_other
        est_r_dagger_other = h.est_r_dagger_other
        last_p = h.last_p
       
        # My estimate of the change in other's p
        # That is not due to self, and our previous interaction
        r_star = max(0, msg.p - h.est_p_star_other)
        # additive update to my probability of infection
        deltap = _lambda*( r_star + r_dagger)
        
        # update to my unmanifested risk
        h.r_dagger = (1.-_lambda)*(r_star + r_dagger)

        # Update to my model of the other's updates
        est_r_star_other = max(0, self.p - h.last_p)
        h.est_p_star_other = min(msg.p + _lambda*(est_r_star_other + est_r_dagger_other), 1.0)
        h.est_r_dagger_other = (1.-_lambda)*(est_r_star_other + est_r_dagger_other)

        # update my p
        self.p += deltap
        self.p = min(self.p, 1.0)
             
        
def start_contact(a, b):
    """ start of a contact between agents a & b """
    
    msg_a = a.prepare_message()
    msg_b = b.prepare_message()

    return msg_a, msg_b


# -------
# Contact ends, and we can compute context
#context = ContextObject(t_exposed=0)
# -------
# Note - check that: two exchanges of t_exposed/2 immediatly following
# should be equivalent to one exchange of t_exposed


def end_contact(a, b, msg_a, msg_b, context):
    """ end of a contact between agents a & b """
    
    a.recv_message(msg_b, context)
    b.recv_message(msg_a, context)





                 


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
    def __init__(self, r_star=0.0, id=None):
        self.r_star = r_star
        self.id = id

class HistoryRecord(object):
    """ local store of history required of previous contact """ 
    def __init__(self, r_dagger, r_star):
        self.r_dagger = r_dagger
        self.r_star = r_star
    
class Agent(object):
    """ update rules for probability of infection
    for an agent coming in contact with another """
    
    def __init__(self, id=0, prob_initial_infection=params.prob_infection_t0): 
        self.id = id
        self.p = prob_initial_infection
        self.history = {}
    
    def prepare_message(self, _for=None):
        # If we have never interacted before,
        # r_star (new risk to _for) = self.p
        # r_dagger (unmanifested risk from _for) = 0
        h = self.history.setdefault(_for.id, HistoryRecord(0., self.p))

        # I don't think obfuscation is required here, but let's discuss
        # TODO?: Truncate to 2 sig figs ... 
        # obfuscated_r_star = trincate(h.r_star, sigfigs = 2)
        #obfuscated_r_star = h.r_star
        # new risk has been sent in the message, now reset it.
        #self.history[_for].r_star -= obfuscated_r_star

        msg = Message(h.r_star, self.id)
        h.r_star = 0.
        
        return msg

    def recv_message(self, msg, context):
        # Get the tranmission probability given the context
        _lambda = get_transmission_prob(context)
        # My record of unmanifested risk due to previous interactions with msg.id
        r_dagger = self.history[msg.id].r_dagger

        # additive update to my probability of infection
        deltap = _lambda*(msg.r_star + r_dagger)
        self.p += deltap
        self.p = min(self.p, 1.0)
        # update to my unmanifested risk
        self.history[msg.id].r_dagger = (1.-_lambda)*(msg.r_star + r_dagger)
        
        # Update new risk, r_star, for other agents in history
        for id in self.history:
            if id!=msg.id:
                self.history[id].r_star+=deltap
     
        
def start_contact(a, b):
    """ start of a contact between agents a & b """
    
    msg_a = a.prepare_message(_for=b)
    msg_b = b.prepare_message(_for=a)

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





                 

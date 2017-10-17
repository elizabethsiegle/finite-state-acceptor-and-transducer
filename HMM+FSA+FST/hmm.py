import numpy as np
class HMM:

    def __init__(self, states, emissions, transitions, initial_probability):
        self.states = states
        self.emissions = emissions
        self.transitions = transitions
        self.initial_probability = initial_probability

    def get_states(self):
        return self.states

    def get_em_prob(self):
        return self.em_prob
    def get_trans_prob(self):
        return self.trans_prob

    def get_init_state(self):
        return self.initial_probability

    def get_state_sequence_prob(self, sequence): #tuple (1, 1, 1) -> hot x hot x hot
        prevstate = 0
        prob = 1
        for state in sequence:
            if prevstate == 0: #first one uses intial probabiltiies
                if state == 1:
                    prob *=self.initial_probability[1]
                    prevstate = state
                elif state == 2:
                    prob *= self.initial_probability[2]
                    prevstate = state
            else: #use transitions
                prob *= self.transitions[state][prevstate] # state given prev state
                prevstate = state
        return prob

    def viterbi(self, observations):
        backpointers = []  #backpointers arr
        f = {state: self.initial_probability[state] * self.emissions[state][observations[0]] for state in self.states}  #init prob
        for t, o in enumerate(observations[1:]): # loop remaining observations
            forwo = {state: float('-inf') for state in self.states}
            backo = {state: () for state in self.states}
            for state2 in self.states: #loop over all state combos to find transition w/ highest forward probability
                for state1 in self.states:
                    prob1 = (f[state1] * self.transitions[state1][state2]) * self.emissions[state2][o]
                    if prob1 > forwo[state2]:
                        forwo[state2] = prob1
                        backo[state2] = (state1, prob1)
            next_obs = forwo  #probability to next observation
            backpointers.append(backo)  #backtrack path back

        #argmax->first backpointer
        path = [max(next_obs.items(), key=lambda x: x[1])]

        for o in reversed(backpointers): #reverse backpointers for final path
            path.insert(0, o[path[0][0]])
        return path


def main():
    states = (1, 2) # 1 = hot, 2 = cold
    start_probability = {1: 0.8, 2: 0.2}
    transition_probability = {
        1: {1: 0.7, 2: 0.3},
        2: {1: 0.4, 2: 0.6}
    }
    emission_probability = {
        1: {1 : 0.2, 2: 0.4, 3: 0.4},
        2: {1: 0.5, 2: 0.4, 3: 0.1}
    }
    first_case = [1, 1, 1] #hot, hot, hot
    hmm_test = HMM(states, emission_probability, transition_probability, start_probability)
    print "Viterbi: ", hmm_test.viterbi(first_case)
    print "Probability of hot x hot x hot: ", hmm_test.get_state_sequence_prob(first_case)

if __name__ == "__main__":
    main()

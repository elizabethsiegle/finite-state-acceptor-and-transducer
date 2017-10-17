class FSA:
    def __init__(self, alphabet, q, i, f, trans_func):
        self.alphabet = alphabet
        self.q = q # q = finite set of states
        self.i = i # i = 1 initial state in q
        self.f = f # f = set of final states in q
        self.trans_func = trans_func

    def get_alphabet(self):
        return self.alphabet

    def get_fin_states(self):
        return self.f # [], can be multiple

    def get_init_states(self):
        return self.i # single

    def get_trans_func(self):
        return self.trans_func

    # transitions can be set of tuples or dictionary        
    def get_transition(self, state, input_symbol):
        for elem in self.trans_func:
            tup = elem[0]
            if state == tup[0]: #self.f:
                if input_symbol == tup[1]:
                    return elem[1]  #return destination state
        return "invalid"
        #if no transition exists for current state + input symbol, return some value showing input string is invalid

    def accept_string(self, inp_str):
        chars = list(inp_str)
        for c in chars:
            if self.get_transition(self.i, c) == "invalid":
                return False
            if "a" in chars:
                return True
            else:
                return False

    #accepts as long as character in alphabet

class FST:
    def __init__(self, inp_alphabet, q, i, f, trans_func):
        self.inp_alphabet = inp_alphabet
        self.q = q # q = finite set of states
        self.i = i # i = 1 initial state in q
        self.f = f # f = set of final states in q
        self.trans_func = trans_func

    def get_inp_alphabet(self):
        return self.inp_alphabet
    
    def get_q(self):
        return self.q

    def get_fin_states(self):
        return self.f # [], can be multiple

    def get_init_states(self):
        return self.i # single

    def get_fin_states(self):
        return self.f # single

    def get_transition(self, state, input_symbol):
        for elem in self.trans_func:
            tup = elem[0]
            if state == tup[0]: 
                if input_symbol == tup[1]:
                    return elem[1] #return destination state

        return "invalid"
        #if no transition exists for current state + input symbol, return some value showing input string is invalid

    
    def output_string(self, inp_str): #take input string, return output string
        chars = list(inp_str)
        if chars == []: #empty string
            return ""
        output_str_ret = ""
        state_from_trans = (chars[0], self.i)
        for c in chars:
            state_from_trans = self.get_transition(state_from_trans[1], c)
            if state_from_trans == "invalid":
                return "string not accepted"
            else: #returns tuple
                output_str_ret += state_from_trans[0]
        return output_str_ret
        #if no transition exists for current state + input symbol, return

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
    #FST takes 1st 'a' and changes to 'b'
    fsa_tuple = {((0,'b'),0), ((0, 'a'), 1), ((1, 'a'), 1), ((1, 'b'), 1)}
    fst_tuple = { ((0,'b'), ('b',0)), ((0,'a'), ('b',1)), ((1,'a'), ('a',1)), ((1,'b'), ('b',1))}
    fsa_ex = FSA({'a', 'b'}, {0, 1}, 0, 1, fsa_tuple)
    fst_ex = FST({'a', 'b'}, {0, 1}, 0, {0, 1}, fst_tuple)

    print "----------------------------------fsa, fst----------------------------"
    print "fsa cbc:", fsa_ex.accept_string('cbc')
    print "fsa aa:", fsa_ex.accept_string('aa')
    print "fsa bb:", fsa_ex.accept_string('bb')
    print "fsa aba:", fsa_ex.accept_string('aba')
    print "fsa aaba:", fsa_ex.accept_string('aaba')
    print "fsa abbab:", fsa_ex.accept_string('abbab')
    print "fsa ababab:", fsa_ex.accept_string('ababab')
    print "fsa ababaaa:", fsa_ex.accept_string('ababaaa')
    print "fsa aab:", fsa_ex.accept_string('aab')
    print "fsa abc:", fsa_ex.accept_string('abc')
    print "fsa 123:", fsa_ex.accept_string('123') 
    print "empty str: ", fst_ex.output_string('')
    print "fst cbc:", fst_ex.output_string('cbc') #returns invalid
    print "fst aba:", fst_ex.output_string('aba')
    print "fst abc:", fst_ex.output_string('abc')
    print "fst a:", fst_ex.output_string('a')
    print "fst b:", fst_ex.output_string('b')
    print "fst c:", fst_ex.output_string('c')
    print "fst aa:", fst_ex.output_string('aa')
    print "fst bab:", fst_ex.output_string('bab')

    print "------------------------------viterbi, hmm ------------------------"
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
    second_case = [1, 2, 2, 1, 2]
    hmm_test = HMM(states, emission_probability, transition_probability, start_probability)
    print "Viterbi: ", hmm_test.viterbi(first_case)
    print "Probability of hot x hot x hot: ", hmm_test.get_state_sequence_prob(first_case)
    print "Viterbi 2: ", hmm_test.viterbi(second_case)
    print "Probability of hot x cold x cold x hot x cold: ", hmm_test.get_state_sequence_prob(second_case)

if __name__ == "__main__":
    main()


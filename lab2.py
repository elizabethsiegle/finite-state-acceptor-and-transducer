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
        return True

class FST():
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


def main():
    fsa_tuple = {((0,'b'),0), ((0, 'a'), 1), ((1, 'a'), 1), ((1, 'b'), 1)}
    fst_tuple = { ((0,'b'), ('b',0)), ((0,'a'), ('b',1)), ((1,'a'), ('a',1)), ((1,'b'), ('b',1))}
    fsa_ex = FSA({'a', 'b'}, {0, 1}, 0, 1, fsa_tuple)
    fst_ex = FST({'a', 'b'}, {0, 1}, 0, {0, 1}, fst_tuple)
    print "fsa cbc:", fsa_ex.accept_string('cbc')
    print "fsa aba:", fsa_ex.accept_string('aba')
    print "fsa abc:", fsa_ex.accept_string('abc')
    print "fsa 123:", fsa_ex.accept_string('123') #returns False
    print "empty str: ", fst_ex.output_string('')
    print "fst cbc:", fst_ex.output_string('cbc') #returns invalid
    print "fst aba:", fst_ex.output_string('aba')
    print "fst abc:", fst_ex.output_string('abc')
    print "fst a:", fst_ex.output_string('a')
    print "fst b:", fst_ex.output_string('b')
    print "fst c:", fst_ex.output_string('c')

if __name__ == "__main__":
    main()


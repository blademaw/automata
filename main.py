# Main PY file for [D|(ND)]FA Project
# NOTE: Currently unrefined and an absolute WIP. Not functional atm.
import itertools, math

class DFA():
    """
    Main class for DFA.
    """
    def __init__(self, alphabet:list, num:int, trans_func:list, start_state:int, accept_states:list) -> None:
        """
        Init function for DFA class.

        :params: (un)sorted alphabet, number of transitions, transition function in matrix
        form [state][character], start state, all accept states.
        """
        self.alphabet = alphabet
        self.sorted_alph = sorted(alphabet)
        self.num_states = num
        self.trans_func = trans_func
        self.start = start_state
        self.accept = accept_states

        # populate an array for state objects, with dictionary for faster access to alphabet indeces in trans_func
        # transitions are thus accessed trans_func[state.name - 1][indeces[character]]
            # states will be accessed states[state.name] (1-indexing)
        self.states = [None] * (self.num_states+1)
        
        # add start states, final states, intermediate states
        self.states[self.start] = state(self.start, self, 0)
        
        for ac_state in self.accept:
            self.states[ac_state] = state(ac_state, self, 2)
        
        if self.start in self.accept:
            self.states[self.start].state_type = 3 # TODO: Is this not redundant?
        
        for i in range(1, self.num_states+1):
            if self.states[i] == None:
                self.states[i] = state(i, self, 1)

        self.state_indeces = {}
        for i in range(len(self.alphabet)):
            self.state_indeces[self.alphabet[i]] = i

    
    def run_word(self, word:str) -> bool:
        """
        Runs a word (checked to be a valid string over self.alphabet) through the DFA,
        returning True if accepted and False otherwise.
        """
        # initial validation
        for char in word:
            if char not in self.state_indeces:
                return False

        current = self.states[self.start]
        for char in word:
            current = self.states[self.trans_func[current.name - 1][self.state_indeces[char]]]
        
        if current.state_type in (2, 3):
            return True
        return False
    
    def print_contents(self):
        return (self.alphabet, self.num_states, self.trans_func, self.start, self.accept)
    
    def strings(self, maximum:int) -> list:
        """
        Permutes and finds the first `maximum` strings over the specified alphabet described (accepted) by the FA
        in lexicographic order (work in progress).
        """
        counter = 0
        word_list = []
        cur_repeat = 2
        first = [""] + self.sorted_alph
        iterable = first
        while counter != maximum:
            for word in iterable:
                if self.run_word(word):
                    word_list.append("".join(word))
                    counter += 1
                if counter >= maximum:
                    break
            iterable = itertools.product(first, repeat=cur_repeat)
            cur_repeat += 1

        return word_list

    def strings_max(self, max_length:int, max_words:int=math.inf):
        """
        Finds the first <max_words> words in the language of length <= <max_length>
        in primarily order of length, then lexicographic. Input is maximum lengths of words to search,
        and maximum to append before halting. If max_words not given, will find all words of length
        <= <max_length> in language described by FA.
        """
        lang = [""] + self.sorted_alph
        for length in range(2, max_length+1):
            for word in itertools.product(self.sorted_alph, repeat=length):
                lang.append(''.join(word))
        
        lang.sort()
        print(lang)

        counter = 0
        word_list = []
        for word in lang:
            if self.run_word(word):
                print(word)
                # TODO: Fix this
                if word not in word_list:
                    word_list.append(word)
                    counter += 1
            if counter >= max_words:
                break

        return sorted(word_list, key=len)
    
    #def transition_table(self):
        

class state():
    """
    State class. Each state belongs to a DFA object, state types: 0 = start, 1 = reject state,
    2 = accept state, 3 = accept and start state.
    """
    def __init__(self, num, DFA, state_type):
        self.name = num
        self.state_type = state_type
        self.state_DFA = DFA



if __name__ == "__main__":
    # logic to create a DFA (input)
    print("\nFor multiple inputs, enter states/chars separated by SPACES.\n\n")
    num = int(input("Enter number of states: "))
    alph = input("Enter characters in alphabet: ").split(" ")
    start = int(input("Enter start state: "))
    final = [int(i) for i in (input("Enter accept states: ")).split(" ")]
    matr = [[None]*len(alph) for x in range(num)]
    print("Enter transition state(s) for the following states in the order of alphabet %s" % alph)
    for i in range(1, num+1):
        cur = input("%d: " % i).split()
        for s in range(len(alph)):
            matr[i-1][s] = int(cur[s])
    print("Creating DFA.")
    dfa_imp = DFA(alph, num, matr, start, final)
    print(dfa_imp.strings_max(6))

    # dfa_imp = DFA(['a', 'b'], 2, [[2, 1], [1, 2]], 1, [1])
    # print(dfa_imp.strings_max(4, 10))
    
    #while True:
    #    word = input("word to run: ")
    #    print(dfa_imp.run_word(word))
# Main PY file for [D|(ND)]FA Project
# NOTE: Currently unrefined and a WIP.
# TODO: God, this is horrible as is; breaks major OOP practices — need to refactor:
    # Ensure FA theory is accurately reflected in objects
    # Add getters and setters for the love of god
    # Migrate to numpy for arrays?
import itertools, math

class DFA():
    """
    Main class for DFA.
    """
    def __init__(self, alphabet:list, num:int, trans_func:list, start_state:int, accept_states:list) -> None:
        """
        Init function for DFA class.

        :params: alphabet, number of transitions, transition function in matrix
        form [state][character], start state, all accept states.
        """
        self.alphabet = alphabet
        self.sorted_alph = sorted(alphabet)
        self.num_states = num
        self.trans_func = trans_func
        self.start = start_state
        self.accept = accept_states

        # populate an array of state objects with dictionary for faster access to alphabet indices in trans_func
        # transitions are thus accessed trans_func[state.name - 1][indices[character]]
            # states will be accessed via states[state.name] (1-indexing)
        self.states = [None] * (self.num_states+1)
        
        # add start states, final states, intermediate states
        self.states[self.start] = state(self.start, self, 0)
        
        for ac_state in self.accept:
            self.states[ac_state] = state(ac_state, self, 2)
        
        if self.start in self.accept:
            self.states[self.start].set_type(3)
        
        for i in range(1, self.num_states+1):
            if self.states[i] == None:
                self.states[i] = state(i, self, 1)

        # record indices of labels
        self.state_indices = {}
        for i in range(len(self.alphabet)):
            self.state_indices[self.alphabet[i]] = i

    
    def run_word(self, word:str) -> bool:
        """
        Runs a word (checked to be a valid string over self.alphabet) through the DFA,
        returning True if accepted and False otherwise.
        """
        # cut down words with nonexistant characters
        for char in word:
            if char not in self.state_indices:
                return False

        # migrate through DFA
        current = self.states[self.start]
        for char in word:
            current = self.states[self.trans_func[current.get_name() - 1][self.state_indices[char]]]
        
        # accept if in accept-like state
        if current.get_type() in (2, 3):
            return True
        return False
    

    def print_contents(self):
        """Prints contents of alphabet, number of states, transition matrix, start, and accept state(s)"""
        return (self.alphabet, self.num_states, self.trans_func, self.start, self.accept)

    def strings_max(self, max_length:int, max_words:int=math.inf):
        """
        Finds the first <max_words> words in the language of length <= <max_length>
        in primarily order of length, then lexicographic. Input is maximum lengths of words to search,
        and maximum to append before halting. If max_words not given, will find all words of length
        <= <max_length> in language described by FA.
        """
        # enumerate all possible strings in alphabet up to length
        lang = []
        for length in range(2, max_length+1):
            for word in itertools.product(self.sorted_alph, repeat=length):
                lang.append(''.join(word))

        # loop to find accepted words
        counter = 0
        word_list = [] # accepted
        for word in lang:
            if self.run_word(word):
                if word not in word_list:
                    word_list.append(word) # add if accepted
                    counter += 1
            if counter >= max_words:
                break

        return sorted(word_list, key=len)
        

class state():
    """
    State class. Each state belongs to a DFA object, state types: 0 = start, 1 = reject state,
    2 = accept state, 3 = accept and start state.
    """
    def __init__(self, num, DFA, state_type):
        """
        Init function for state class.
        
        Inputs: number label, finite automata class, type of state
        """
        self.name = num
        self.state_type = state_type
        self.state_DFA = DFA
    
    def set_type(self, state_type):
        """
        Function for setting/updating a state's type
        """
        self.state_type = state_type
    
    def get_type(self):
        """
        Function for getting a state's type
        """
        return self.state_type

    def get_name(self):
        """
        Function for getting a state's label/name
        """
        return self.name



if __name__ == "__main__":
    # logic to create a DFA (input)
    print("\nFor multiple inputs, enter states/chars separated by SPACES.\n\n")
    num = int(input("Enter number of states: "))
    alph = input("Enter characters in alphabet: ").split(" ")
    start = int(input("Enter start state: "))
    final = [int(i) for i in (input("Enter accept states: ")).split(" ")]
    matr = [[None]*len(alph) for x in range(num)]

    # create transition matrix
    print(f"Enter transition state(s) for the following states in the order of alphabet {alph}")
    for i in range(1, num+1):
        cur = input(f"{i}: ").split()
        for s in range(len(alph)):
            matr[i-1][s] = int(cur[s])
    print(matr)
    
    print("\n\nStrings:")
    
    dfa_imp = DFA(alph, num, matr, start, final)
    print(dfa_imp.strings_max(6))

    # TESTING
    # dfa_imp = DFA(['a', 'b'], 2, [[2, 1], [1, 2]], 1, [1])
    # print(dfa_imp.strings_max(4, 10))
    
    #while True:
    #    word = input("word to run: ")
    #    print(dfa_imp.run_word(word))
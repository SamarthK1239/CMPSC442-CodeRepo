############################################################
# CMPSC 442: Homework 3
############################################################

student_name = "Samarth Sanjay Kulkarni"

############################################################
# Imports
############################################################
# Include your imports here, if any are used.
import copy


############################################################
# Section 1: Propositional Logic
############################################################

class Expr(object):
    def __hash__(self):
        return hash((type(self).__name__, self.hashable))


class Atom(Expr):
    def __init__(self, name):
        self.name = name
        self.hashable = name

    def __eq__(self, other):
        # Check if the other object is an Atom with the same name
        if isinstance(other, Atom) and self.name == other.name:
            return True
        return False

    def __repr__(self):
        # Return a string representation of the Atom object
        return f"Atom({self.name})"

    def __hash__(self):
        # Return a hash value for the Atom object
        return hash((type(self).__name__, self.hashable))

    def atom_names(self):
        # Return a set containing the name of the Atom object
        return {self.name}

    def evaluate(self, assignment):
        # Return the value of the Atom object in the given assignment
        return assignment[self.name]

    def to_cnf(self):
        # Return the Atom object since it is already in CNF
        return self


class Not(Expr):
    def __init__(self, arg):
        self.arg = arg

    def __eq__(self, other):
        # Check if the other object is a Not object with the same argument
        return isinstance(other, Not) and self.arg == other.arg

    def __repr__(self):
        # Return a string representation of the Not object
        return f"Not({self.arg})"

    def __hash__(self):
        # Return a hash value for the Not object
        return hash((type(self).__name__, self.arg))

    def atom_names(self):
        # Return the atom names of the argument
        return self.arg.atom_names()

    def evaluate(self, assignment):
        # Return the negation of the argument in the given assignment
        return not self.arg.evaluate(assignment)

    def to_cnf(self):
        if isinstance(self.arg, Atom):
            # Return the Not object since it is already in CNF
            return self
        if isinstance(self.arg, Implies):
            # Apply the De Morgan's law to the Implies object
            right = self.arg.right
            left = self.arg.left
            sol = And(left, Not(right)).to_cnf()
            return sol
        if isinstance(self.arg, And):
            # Apply the De Morgan's law to the And object
            conjuncts = self.arg.conjuncts
            sol = Or(*map(Not, conjuncts)).to_cnf()
            return sol
        if isinstance(self.arg, Not):
            # Remove the double negation
            sol = self.arg.arg.to_cnf()
            return sol
        if isinstance(self.arg, Iff):
            # Apply the De Morgan's law to the Iff object
            right = self.arg.right
            left = self.arg.left
            sol = Or(Not(Implies(left, right)), Not(Implies(right, left))).to_cnf()
            return sol
        if isinstance(self.arg, Or):
            # Apply the De Morgan's law to the Or object
            disjuncts = self.arg.disjuncts
            sol = And(*map(Not, disjuncts)).to_cnf()
            return sol


class And(Expr):
    def __init__(self, *args):
        # Create a frozenset of the conjuncts
        self.conjuncts = frozenset(args)

    def __eq__(self, other):
        # Check if the other object is an And object with the same conjuncts
        return isinstance(other, And) and self.conjuncts == other.conjuncts

    def __hash__(self):
        # Return a hash value for the And object
        return hash((type(self).__name__, self.conjuncts))

    def __repr__(self):
        # Return a string representation of the And object
        return f"And({', '.join(map(str, self.conjuncts))})"

    def atom_names(self):
        # Return a set containing the atom names of all the conjuncts
        return {atom for conjunct in self.conjuncts for atom in conjunct.atom_names()}

    def evaluate(self, assignment):
        # Return True if all the conjuncts evaluate to True in the given assignment
        return all(conjunct.evaluate(assignment) for conjunct in self.conjuncts)

    def to_cnf(self):
        # Convert each conjunct to CNF and combine them using the distributive property
        cnf_conjuncts = []
        for conjunct in self.conjuncts:
            if isinstance(conjunct, And):
                cnf_conjuncts.extend(conjunct.conjuncts)
            else:
                cnf_conjuncts.append(conjunct.to_cnf())
        return And(*cnf_conjuncts)


class Or(Expr):
    def __init__(self, *args):
        # Create a frozenset of the disjuncts
        self.disjuncts = frozenset(args)

    def __eq__(self, other):
        # Check if the other object is an Or object with the same disjuncts
        return isinstance(other, Or) and self.disjuncts == other.disjuncts

    def __repr__(self):
        # Return a string representation of the Or object
        return f"Or({', '.join(map(repr, self.disjuncts))})"

    def atom_names(self):
        # Return a set containing the atom names of all the disjuncts
        return {name for disjunct in self.disjuncts for name in disjunct.atom_names()}

    def __hash__(self):
        # Return a hash value for the Or object
        return hash((type(self).__name__, self.disjuncts))

    def evaluate(self, assignment):
        # Return True if any of the disjuncts evaluate to True in the given assignment
        return any(disjunct.evaluate(assignment) for disjunct in self.disjuncts)

    def to_cnf(self):
        # Convert each disjunct to CNF and combine them using the distributive property
        cnf_disjuncts = []
        for disjunct in self.disjuncts:
            if type(disjunct) != type(self):
                cnf_disjuncts.append(disjunct.to_cnf())
            else:
                cnf_disjuncts = [i.to_cnf() for i in disjunct.disjuncts]
        new_or = Or(*cnf_disjuncts)
        for disjunct in new_or.disjuncts:
            if isinstance(disjunct, And):
                new_disjuncts = [i for i in new_or.disjuncts if disjunct is not i]
                old_conjuncts = [i for i in disjunct.conjuncts]
                ret_conjuncts = []
                for k in old_conjuncts:
                    new_disjuncts_list = [k]
                    for new in new_disjuncts:
                        new_disjuncts_list.append(new)
                    ret_disjuncts = Or(*new_disjuncts_list).to_cnf()
                    ret_conjuncts.append(ret_disjuncts)
                return And(*ret_conjuncts).to_cnf()
        return Or(*cnf_disjuncts)


class Implies(Expr):
    def __init__(self, left_expr, right_expr):
        # Store the left and right expressions
        self.left_expr = left_expr
        self.right_expr = right_expr
        self.hashable = (left_expr, right_expr)

    def __eq__(self, other):
        # Check if the other object is an Implies object with the same left and right expressions
        return isinstance(other, Implies) and self.left_expr == other.left_expr and self.right_expr == other.right_expr

    def __repr__(self):
        # Return a string representation of the Implies object
        return f"Implies({self.left_expr!r}, {self.right_expr!r})"

    def atom_names(self):
        # Return a set containing the atom names of both the left and right expressions
        return self.left_expr.atom_names() | self.right_expr.atom_names()

    def evaluate(self, assignment):
        # Return True if the left expression is False or the right expression is True in the given assignment
        return not self.left_expr.evaluate(assignment) or self.right_expr.evaluate(assignment)

    def __hash__(self):
        # Return a hash value for the Implies object
        return hash((type(self).__name__, self.hashable))

    def to_cnf(self):
        # Convert the Implies expression to CNF using the equivalence: A => B is equivalent to !A | B
        return Or(Not(self.left_expr), self.right_expr).to_cnf()


class Iff(Expr):
    def __init__(self, left_expr, right_expr):
        # Store the left and right expressions
        self.left_expr = left_expr
        self.right_expr = right_expr
        self.hashable = (left_expr, right_expr)

    def __eq__(self, other):
        # Check if the other object is an Iff object with the same left and right expressions
        return isinstance(other, Iff) and {self.left_expr, self.right_expr} == {other.left_expr, other.right_expr}

    def __repr__(self):
        # Return a string representation of the Iff object
        return f"Iff({self.left_expr!r}, {self.right_expr!r})"

    def atom_names(self):
        # Return a set containing the atom names of both the left and right expressions
        return self.left_expr.atom_names() | self.right_expr.atom_names()

    def evaluate(self, assignment):
        # Return True if the left and right expressions evaluate to the same value in the given assignment
        return self.left_expr.evaluate(assignment) == self.right_expr.evaluate(assignment)

    def __hash__(self):
        # Return a hash value for the Iff object
        return hash((type(self).__name__, self.hashable))

    def to_cnf(self):
        # Convert the Iff expression to CNF using the equivalence: A <=> B is equivalent to (!A | B) & (A | !B)
        return Or(And(Not(self.left_expr), self.right_expr), And(self.left_expr, Not(self.right_expr))).to_cnf()


def satisfying_assignments(expr):
    # Get a list of all the atom names in the expression
    atom_names = list(expr.atom_names())

    # Create an initial assignment with all atoms set to False
    assignment = {atom: False for atom in atom_names}

    # Generate all possible assignments by iterating over all possible binary strings of length len(atom_names)
    for i in range(0, pow(2, len(atom_names))):
        # Initialize the position and a deep copy of the assignment
        position = 0
        assignment = copy.deepcopy(assignment)

        # Update the assignment based on the binary representation of i
        for atom in atom_names:
            if i != 0:
                if i % pow(2, position) == 0:
                    assignment[atom] = not assignment[atom]
            position += 1

        # Yield the assignment if it satisfies the expression
        if expr.evaluate(assignment):
            yield assignment


class KnowledgeBase(object):
    def __init__(self):
        # Initialize an empty set to store the facts
        self.facts = set()

    def get_facts(self):
        # Return the set of facts
        return self.facts

    def tell(self, expr):
        # Convert the expression to CNF
        cnf_expr = expr.to_cnf()

        # If the CNF expression is an And expression, add each conjunct to the set of facts
        if type(cnf_expr) == And:
            for conjunct in cnf_expr.conjuncts:
                self.facts.add(conjunct)
        # Otherwise, add the CNF expression to the set of facts
        else:
            self.facts.add(cnf_expr)

    def ask(self, expr):
        # Create a negation of the expression
        negation = Not(expr)

        # Get the current set of facts
        current_facts = self.get_facts()

        # Create an assumption by combining the current facts and the negation using the And operator and convert it to CNF
        assumption = And(*current_facts, negation).to_cnf()

        # Try to find a satisfying assignment for the assumption
        try:
            next(satisfying_assignments(assumption))
        # If no satisfying assignment is found, return True
        except:
            return True

        # Otherwise, return False
        return False


############################################################
# Section 2: Logic Puzzles
############################################################

# Puzzle 1
# Populate the knowledge base using statements of the form kb1.tell(...)
kb1 = KnowledgeBase()
mythical = Atom("mythical")
mortal = Atom("mortal")
mammal = Atom("mammal")
horned = Atom("horned")
magical = Atom("magical")
kb1.tell(Implies(mythical, Not(mortal)))
kb1.tell(Implies(Not(mythical), And(mortal, mammal)))
kb1.tell(Implies(Or(not(mortal), mammal), horned))
kb1.tell(Implies(horned, magical))

# Write an Expr for each query that should be asked of the knowledge base
mythical_query = mythical
magical_query = magical
horned_query = horned

# Record your answers as True or False; if you wish to use the above queries,
# they should not be run when this file is loaded
is_mythical = False
is_magical = True
is_horned = True

# Puzzle 2
# Write an Expr of the form And(...) encoding the constraints
Ann = Atom("a")
John = Atom("j")
Mary = Atom("m")
party_constraints = And(
    Implies(Or(Ann, Mary), John),
    Implies(Not(Mary), Ann),
    Implies(Ann, Not(John))
)

# Compute a list of the valid attendance scenarios using a call to
# satisfying_assignments(expr)
valid_scenarios = list(satisfying_assignments(party_constraints))

# Write your answer to the question in the assignment
puzzle_2_question = """Both John and Mary will attend the party"""

# Puzzle 3
# Populate the knowledge base using statements of the form kb3.tell(...)
kb3 = KnowledgeBase()
p1 = Atom("p1")
e1 = Atom("e1")
p2 = Atom("p2")
e2 = Atom("e2")
s1 = Atom("s1")
s2 = Atom("s2")

kb3.tell(Implies(s1, And(p1, e2)))
kb3.tell(Implies(s2, And(Or(p1, p2), Or(e1, e2))))
kb3.tell(Or(And(s1, Not(s2)), And(Not(s1), s2)))

# Write your answer to the question in the assignment; the queries you make
# should not be run when this file is loaded
puzzle_3_question = """The first sign is accurate, indicating that the prize is located in Room 1 and Room 2 is unoccupied"""

# Puzzle 4
# Populate the knowledge base using statements of the form kb4.tell(...)
kb4 = KnowledgeBase()
Adams = Atom("ia")
Brown = Atom("ib")
Clark = Atom("ic")
k_Adams = Atom("ka")
k_Brown = Atom("kb")
k_Clark = Atom("kc")

kb4.tell(k_Brown)
kb4.tell(Not(k_Clark))

# Uncomment the line corresponding to the guilty suspect
# guilty_suspect = "Adams"
guilty_suspect = "Brown"
# guilty_suspect = "Clark"

# Describe the queries you made to ascertain your findings
puzzle_4_question = """I created And clauses between two guys to check if they agree with each other, proving that brown is the guilty suspect"""

############################################################
# Section 3: Feedback
############################################################

feedback_question_1 = """
I spent about 10 hours on this assignment. Debugging the code took an additional 2 hours.
"""

feedback_question_2 = """
I think the most challenging aspect of this assignment was some of the to_cnf() functions, since they required a lot of thinking and testing.
"""

feedback_question_3 = """
I liked this assignment a lot, and there isn't really anything I would like to change. It's a good challenge while incorporating logical concepts.
"""
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
        if type(self) == type(other):
            if self.name == other.name:
                return True
        return False

    def __repr__(self):
        return "Atom(" + self.name + ")"

    def __hash__(self):
        return hash((type(self).__name__, self.hashable))

    def atom_names(self):
        sol = {self.name}
        return sol

    def evaluate(self, assignment):
        if assignment[self.name]:
            return True
        else:
            return False

    def to_cnf(self):
        return self


class Not(Expr):
    def __init__(self, arg):
        self.arg = arg
        self.hashable = arg

    def __eq__(self, other):
        p1 = type(self) == type(other)
        p2 = self.arg == other.arg
        return p1 and p2

    def __repr__(self):
        return "Not({})".format(self.arg)

    def __hash__(self):
        return hash((type(self).__name__, self.hashable))

    def atom_names(self):
        sol = self.arg.atom_names()
        return sol

    def evaluate(self, assignment):
        sol = not self.arg.evaluate(assignment)
        return sol

    def to_cnf(self):
        if type(self.arg) == Atom:
            return self
        if type(self.arg) == Implies:
            r = self.arg.right
            l = self.arg.left
            sol = And(l, Not(r)).to_cnf()
            return sol
        if type(self.arg) == And:
            con = self.arg.conjuncts
            sol = Or(*map(Not, con)).to_cnf()
            return sol
        if type(self.arg) == Not:
            sol = self.arg.arg.to_cnf()
            return sol
        if type(self.arg) == Iff:
            r = self.arg.right
            l = self.arg.left
            sol = Or(Not(Implies(l, r)), Not(Implies(r, l))).to_cnf()
            return sol
        if type(self.arg) == Or:
            o = self.arg.disjuncts
            sol = And(*map(Not, o)).to_cnf()
            return sol


class And(Expr):
    def __init__(self, *conjuncts):
        self.conjuncts = frozenset(conjuncts)
        self.hashable = self.conjuncts

    def __eq__(self, other):
        p1 = type(self) == type(other)
        p2 = self.conjuncts == other.conjuncts
        sol = p1 and p2
        return sol

    def __hash__(self):
        return hash((type(self).__name__, self.hashable))

    def __repr__(self):
        l = len(self.conjuncts)
        s = ["{}, "] * l
        s = "".join(s).strip()[:-1]
        s = "And(" + s + ")"
        sol = s.format(*self.conjuncts)
        return sol

    def atom_names(self):
        n = set()
        for i in self.conjuncts:
            n = n.union(i.atom_names())
        return n

    def evaluate(self, assignment):
        for a in self.conjuncts:
            if not a.evaluate(assignment):
                return False
        return True

    def to_cnf(self):
        nf = None
        temp = map(lambda x: x.to_cnf(), self.conjuncts)
        for expression in set(temp):
            if not nf:
                nf = expression
            elif type(nf) == Atom:
                if type(expression) != And:
                    nf = And(nf, expression)
                else:
                    nf = And(nf, *expression.conjuncts)
            elif type(nf) == Not:
                if type(expression) != And:
                    nf = And(nf, expression)
                else:
                    nf = And(nf, *expression.conjuncts)
            elif type(nf) == And:
                if type(expression) != And:
                    newset = set()
                    newset.add(expression)
                    nf = And(*nf.conjuncts.union(newset))
                else:
                    nf = And(*expression.conjuncts.union(nf.conjuncts))
            else:
                if type(expression) != And:
                    nf = And(nf, expression)
                else:
                    newset2 = set()
                    newset2.add(nf)
                    newset2 = expression.conjuncts.union(newset2)
                    nf = And(*newset2)
        return nf


class Or(Expr):
    def __init__(self, *disjuncts):
        self.disjuncts = frozenset(disjuncts)
        self.hashable = self.disjuncts

    def __eq__(self, other):
        p1 = type(self) == type(other)
        p2 = self.disjuncts == other.disjuncts
        sol = p1 and p2
        return sol

    def __repr__(self):
        l = len(self.disjuncts)
        s = ["{}, "] * l
        s = "".join(s).strip()[:-1]
        s = "Or(" + s + ")"
        sol = s.format(*self.disjuncts)
        return sol

    def atom_names(self):
        n = set()
        for i in self.disjuncts:
            n.update(i.atom_names())
        return n

    def __hash__(self):
        return hash((type(self).__name__, self.hashable))

    def evaluate(self, assignment):
        for i in self.disjuncts:
            if i.evaluate(assignment):
                return True
        return False

    def to_cnf(self):
        lst = []
        for value in self.disjuncts:
            if type(value) != type(self):
                lst.append(value.to_cnf())
            else:
                lst = [i.to_cnf() for i in value.disjuncts]
        nO = Or(*lst)
        for value in nO.disjuncts:
            if isinstance(value, And):
                nAlist = [i for i in nO.disjuncts if value is not i]
                oAlist = [i for i in value.conjuncts]
                retAlist = []
                for k in oAlist:
                    nOlist = [k]
                    for new in nAlist:
                        nOlist.append(new)
                    retOlist = Or(*nOlist).to_cnf()
                    retAlist.append(retOlist)
                return And(*retAlist).to_cnf()
        return Or(*lst)


class Implies(Expr):
    def __init__(self, left, right):
        self.left = left
        self.right = right
        self.hashable = (left, right)

    def __hash__(self):
        return hash((type(self).__name__, self.hashable))

    def __eq__(self, other):
        if self.hashable == other.hashable:
            return True
        else:
            return False

    def __repr__(self):
        r = self.right
        l = self.left
        sol = "Implies(" + repr(l) + ", " + repr(r) + ")"
        return sol

    def atom_names(self):
        p1 = self.left.atom_names()
        p2 = self.right.atom_names()
        return p1.union(p2)

    def evaluate(self, assignment):
        r = self.right.evaluate(assignment)
        l = self.left.evaluate(assignment)
        if l and not r:
            return False
        else:
            return True

    def to_cnf(self):
        r = self.right
        l = self.left
        ret = Or(Not(l), r).to_cnf()
        return ret


class Iff(Expr):
    def __init__(self, left, right):
        self.left = left
        self.right = right
        self.hashable = (left, right)

    def __eq__(self, other):
        r = self.right
        l = self.left
        otherr = other.right
        otherl = other.left
        p1 = type(self) == type(other)
        p2 = (l == otherr and r == otherl)
        p3 = (l == otherl and r == otherr)
        return p1 and p2 or p3

    def __repr__(self):
        p1 = "Iff(" + repr(self.left)
        p2 = repr(self.right) + ")"
        sol = p1 + ", " + p2
        return sol

    def __hash__(self):
        return hash((type(self).__name__, self.hashable))

    def atom_names(self):
        l = self.left.atom_names()
        r = self.right.atom_names()
        sol = l.union(r)
        return sol

    def evaluate(self, assignment):
        r = self.right.evaluate(assignment)
        l = self.left.evaluate(assignment)
        if (not l or r) and (not r or l):
            return True
        return False

    def to_cnf(self):
        r = self.right
        l = self.left
        sol = And(Or(Not(l), r), Or(Not(r), l)).to_cnf()
        return sol


def satisfying_assignments(expr):
    l = list(expr.atom_names())
    assign = {a: False for a in l}

    for i in range(0, pow(2, len(l))):
        pos = 0
        assign = copy.deepcopy(assign)
        for a in l:
            if i != 0:
                if i % pow(2, pos) == 0:
                    assign[a] = not assign[a]
            pos = pos + 1

        if expr.evaluate(assign):
            yield assign


class KnowledgeBase(object):
    def __init__(self):
        self.facts = set()

    def get_facts(self):
        return self.facts

    def tell(self, expr):
        excnf = expr.to_cnf()
        if type(excnf) == And:
            for i in excnf.conjuncts:
                self.facts.add(i)
        else:
            self.facts.add(excnf)

    def ask(self, expr):
        negation = Not(expr)
        current_facts = self.get_facts()
        assumption = And(*current_facts, negation).to_cnf()
        try:
            next(satisfying_assignments(assumption))
        except:
            return True
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
kb1.tell(Implies(Or(mortal, mammal), horned))
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
puzzle_2_question = """John and Mary will come."""

# Puzzle 3
# Populate the knowledge base using statements of the form kb3.tell(...)
kb3 = KnowledgeBase()
p1 = Atom("p1")
e1 = Atom("e1")
p2 = Atom("p2")
e2 = Atom("e2")
s1 = Atom("s1")
s2 = Atom("s2")

kb3.tell(Or(p1, p2))
kb3.tell(Or(e1, e2))
kb3.tell(Not(And(s1, s2)))
kb3.tell(Not(And(p1, p2)))
kb3.tell(Or(s1, s2))

# Write your answer to the question in the assignment; the queries you make
# should not be run when this file is loaded
puzzle_3_question = """Sign 1 is true. Room1 contains the prize, and room2 is empty."""

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
puzzle_4_question = """I created And clauses between two guys."""

############################################################
# Section 3: Feedback
############################################################

feedback_question_1 = """
Type your response here.
Your response may span multiple lines.
Do not include these instructions in your response.
"""

feedback_question_2 = """
Type your response here.
Your response may span multiple lines.
Do not include these instructions in your response.
"""

feedback_question_3 = """
Type your response here.
Your response may span multiple lines.
Do not include these instructions in your response.
"""

############################################################ TEST CASES ############################################################
print(Atom("a").to_cnf())
a, b, c = map(Atom, "abc")
print(Iff(a, Or(b, c)).to_cnf())

e = Iff(Iff(Atom("a"), Atom("b")), Atom("c"))
print(list(satisfying_assignments(e)))

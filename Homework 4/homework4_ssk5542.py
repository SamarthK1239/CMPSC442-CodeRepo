############################################################
# CMPSC442: Homework 4
############################################################

student_name = "Samarth Sanjay Kulkarni"

############################################################
# Imports
############################################################
import email
import email.iterators
import math
from os import listdir
import time
from os.path import isfile, join


############################################################
# Section 1: Spam Filter
############################################################

def load_tokens(email_path):
    tokens = []
    with open(email_path, 'r', encoding='utf-8') as infile:
        message = email.message_from_file(infile)
        for body_line in email.iterators.body_line_iterator(message):
            str_list = body_line.split()
            for elem in str_list:
                tokens.append(elem)
    return tokens


def log_probs(email_paths, smoothing):
    prob_dict = {}
    count_dict = {}
    tokens_list = []
    alpha = smoothing
    # from training corpus,extract vocabulary
    for path in email_paths:
        tokens = load_tokens(path)
        tokens_list += tokens
        for w in tokens:
            if w in count_dict:
                count_dict[w] += 1
            else:
                count_dict[w] = 1
    # for each word in vocabulary,calculate the probability of occurrence
    # add the Laplace-smoothed log probabilities to prob_dict
    count_sum = len(tokens_list)
    V = len(count_dict)
    for word in count_dict:
        count = count_dict[word]
        pw = (count + alpha) / (count_sum + alpha * (V + 1))
        prob_dict[word] = math.log(pw)
    # add unknown tokens <UNK> to prob_dict
    prob_dict["<UNK>"] = math.log(alpha / (count_sum + alpha * (V + 1)))
    return prob_dict


class SpamFilter(object):

    def __init__(self, spam_dir, ham_dir, smoothing):
        spam_files = [f for f in listdir(spam_dir)]
        ham_files = [f for f in listdir(ham_dir)]
        spam_paths = [spam_dir + "/" + fname for fname in spam_files]
        ham_paths = [ham_dir + "/" + fname for fname in ham_files]
        self.spam_dict = log_probs(spam_paths, smoothing)
        self.ham_dict = log_probs(ham_paths, smoothing)
        self.p_spam = len(spam_files) / float(len(spam_files) + len(ham_files))
        self.p_ham = len(ham_files) / float(len(spam_files) + len(ham_files))

    def is_spam(self, email_path):
        tokens = load_tokens(email_path)
        ps = self.p_spam
        ph = self.p_ham
        unk_token = self.spam_dict.get("<UNK>", 0)  # Default to 0 if <UNK> not found
        for w in tokens:
            ps += self.spam_dict.get(w, unk_token)
            ph += self.ham_dict.get(w, unk_token)
        return ps > ph

    def most_indicative_spam(self, n):
        d = {}
        for word in self.spam_dict:
            if word in self.ham_dict:
                pw = math.exp(self.spam_dict[word]) * self.p_spam + math.exp(self.ham_dict[word]) * self.p_ham
                d[word] = self.spam_dict[word] - math.log(pw)
            # else:
            #     pw = math.exp(self.spam_dict[word]) * self.p_spam + math.exp(self.ham_dict.get("<UNK>", 0)) * self.p_ham
        sorted_list = sorted(d, key=d.get, reverse=True)
        return [sorted_list[i] for i in range(n)]

    def most_indicative_ham(self, n):
        d = {}
        for word in self.ham_dict:
            if word in self.spam_dict:
                pw = math.exp(self.spam_dict[word]) * self.p_spam + math.exp(self.ham_dict[word]) * self.p_ham
                d[word] = self.ham_dict[word] - math.log(pw)
            # else:
            #     pw = math.exp(self.spam_dict.get("<UNK>", 0)) * self.p_spam + math.exp(self.ham_dict[word]) * self.p_ham
        sorted_list = sorted(d, key=d.get, reverse=True)
        return [sorted_list[i] for i in range(n)]


############################################################
# Section 2: Feedback
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
ham_dir = "homework4_data/train/ham/"
print(load_tokens(ham_dir + "ham1")[200:204])
print(load_tokens(ham_dir + "ham2")[110:114])

paths = ["homework4_data/train/ham/ham%d" % i
         for i in range(1, 11)]
p = log_probs(paths, 1e-5)
print(p["the"] == -3.6080194731874062)
print(p["line"] == -4.272995709320345)

sf = SpamFilter("homework4_data/train/spam",
                "homework4_data/train/ham", 1e-5)
print(sf.most_indicative_spam(5))

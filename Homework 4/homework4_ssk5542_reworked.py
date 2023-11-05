############################################################
# CMPSC442: Homework 4
############################################################

student_name = "Type your full name here."

############################################################
# Imports
############################################################

# Include your imports here, if any are used.
import math
import email
import os
import time


############################################################
# Section 1: Spam Filter
############################################################

def is_num(string):
    try:
        float(string)
        return True
    except ValueError:
        return False


def punc_more_than(string, limit):
    count = 0
    for c in string:
        if c in [':', ';', '.', '\"', '-', '(', ')', '[', ']', '/', '_']:
            count += 1
    return count > limit


def is_header(string):
    return len(string) > 1 and string[-1] == ':'


def is_tagline(line):
    return line[0][0] == '<' or line[-1][-1] == '>'


def in_brackets(string):
    brackets = ['(', ')', '<', '>', '[', ']']
    return string[0] in brackets and string[-1] in brackets


def load_tokens(email_path):
    with open(email_path, "r") as file_object:
        msg_object = email.message_from_file(file_object)
        msg_iter = email.iterators.body_line_iterator(msg_object)

        for line in msg_iter:
            split_line = line.split()
            if split_line and is_header(split_line[0]):
                continue
            for word in split_line:
                yield word


def log_probs(email_paths, smoothing):
    frequency_map = {}
    total_count = 0
    long_word_count = 0
    prev_word = ""

    for path in email_paths:
        for word in load_tokens(path):
            total_count += 1

            if len(word) > 15:
                long_word_count += 1

            # unigram
            if word in frequency_map:
                frequency_map[word] += 1
            else:
                frequency_map[word] = 1

            # bigram
            bigram = prev_word + word
            if bigram in frequency_map:
                frequency_map[bigram] += 1
            else:
                frequency_map[bigram] = 1
            prev_word = word

    frequency_map["<GNOL>"] = long_word_count

    v = len(frequency_map.keys())
    logprob_map = {}

    for key in frequency_map.keys():
        logprob_map[key] = math.log((frequency_map[key] + smoothing) / (total_count + smoothing * (v + 1)))
    logprob_map["<UNK>"] = math.log(smoothing / (total_count + smoothing * (v + 1)))

    return logprob_map


def merge_map(dic1, dic2):
    merged = {key: dic1[key] for key in dic1}

    for word in dic2.keys():
        if word in merged:
            merged[word] += 1
        else:
            merged[word] = 1

    return merged


class SpamFilter(object):
    def __init__(self, spam_dir, ham_dir, smoothing=1e-10):
        spam_list = [os.path.join(spam_dir, file) for file in os.listdir(spam_dir)]
        ham_list = [os.path.join(ham_dir, file) for file in os.listdir(ham_dir)]
        self.spam_logprobs = log_probs(spam_list, smoothing)
        self.ham_logprobs = log_probs(ham_list, smoothing)
        self.merged_map = merge_map(self.spam_logprobs, self.ham_logprobs)

        spam_num = len(os.listdir(spam_dir))
        ham_num = len(os.listdir(ham_dir))
        self.spam_rate = float(spam_num) / (spam_num + ham_num)

    def is_spam(self, email_path):
        frequency_map = {}
        prev_word = ""
        long_word_count = 0

        for word in load_tokens(email_path):

            if len(word) > 15:
                long_word_count += 1

            # unigram
            if word in frequency_map:
                frequency_map[word] += 1
            else:
                frequency_map[word] = 1

            # bigram
            bigram = prev_word + word

            if bigram in frequency_map:
                frequency_map[bigram] += 1
            else:
                frequency_map[bigram] = 1
            prev_word = word

        frequency_map["<GNOL>"] = long_word_count

        spam_factor, ham_factor = 0, 0

        for word in frequency_map.keys():
            spam_factor += self.spam_logprobs.get(word, self.spam_logprobs["<UNK>"]) * frequency_map[word]
            ham_factor += self.ham_logprobs.get(word, self.ham_logprobs["<UNK>"]) * frequency_map[word]

        spam_rate = self.spam_rate * spam_factor
        ham_rate = (1 - self.spam_rate) * ham_factor

        return spam_rate > ham_rate

    def most_indicative_spam(self, n):
        word_list = list(self.merged_map.keys())
        word_list.sort(key=lambda x: self.get_spam_indicator(x, True), reverse=True)
        return word_list[:n]

    def most_indicative_ham(self, n):
        word_list = list(self.merged_map.keys())
        word_list.sort(key=lambda x: self.get_spam_indicator(x, False), reverse=True)
        return word_list[:n]

    def get_spam_indicator(self, word, is_spam):
        if is_spam:
            return self.spam_logprobs.get(word, self.spam_logprobs["<UNK>"]) - self.merged_map.get(word, 0)
        else:
            return self.ham_logprobs.get(word, self.ham_logprobs["<UNK>"]) - self.merged_map.get(word, 0)


paths = ["homework4_data/train/ham/ham%d" % i for i in range(1, 11)]
p = log_probs(paths, 1e-5)
print(p["the"])
print(p["line"])
print(p["<UNK>"])
print(p["Credit"])

sf = SpamFilter("homework4_data/train/spam", "homework4_data/train/ham", 1e-5)

print("beginning")
print(sf.is_spam("homework4_data/train/ham/ham1"))
print(sf.is_spam("homework4_data/train/spam/spam2"))

sf = SpamFilter("homework4_data/train/spam", "homework4_data/train/ham", 1e-5)
print("done")
print(sf.most_indicative_spam(5))

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

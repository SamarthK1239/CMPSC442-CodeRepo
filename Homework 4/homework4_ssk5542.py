############################################################
# CMPSC442: Homework 4
############################################################

student_name = "Samarth Sanjay Kulkarni"

############################################################
# Imports
############################################################
import email
import os
from email.parser import Parser
from email.policy import default


############################################################
# Section 1: Spam Filter
############################################################

def load_tokens(email_path):
    with open(email_path, "r", encoding='utf-8') as f:
        message_content = email.message_from_file(f, policy=default)
        print(message_content)


def log_probs(email_paths, smoothing):
    pass


class SpamFilter(object):

    def __init__(self, spam_dir, ham_dir, smoothing):
        pass

    def is_spam(self, email_path):
        pass

    def most_indicative_spam(self, n):
        pass

    def most_indicative_ham(self, n):
        pass


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
ham_dir = "homework4_data/train/ham/ham1"
load_tokens(ham_dir)

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


############################################################
# Section 1: Spam Filter
############################################################

def load_tokens(email_path):
    # Initialize an empty list to store the tokens
    tokens = []
    # Open the file in read mode with utf-8 encoding
    with open(email_path, 'r', encoding='utf-8') as infile:
        # Parse the email file into an email message object
        message = email.message_from_file(infile)
        # Iterate over each line in the body of the email message
        for body_line in email.iterators.body_line_iterator(message):
            # Split the line into individual words (tokens)
            str_list = body_line.split()
            # Add each token to the tokens list
            for elem in str_list:
                tokens.append(elem)
    # Return the list of tokens
    return tokens


def log_probs(email_paths, smoothing):
    # Initialize dictionaries to store the probabilities and counts of each token
    prob_dict = {}
    count_dict = {}
    # Initialize a list to store all tokens
    tokens_list = []
    # Set the smoothing factor
    alpha = smoothing
    # Iterate over each email file path
    for path in email_paths:
        # Load the tokens from the email file
        tokens = load_tokens(path)
        # Add the tokens to the list of all tokens
        tokens_list += tokens
        # Count the occurrence of each token
        for w in tokens:
            if w in count_dict:
                count_dict[w] += 1
            else:
                count_dict[w] = 1
    # Calculate the total number of tokens and the size of the vocabulary
    count_sum = len(tokens_list)
    V = len(count_dict)
    # Calculate the log probability of each token
    for word in count_dict:
        count = count_dict[word]
        pw = (count + alpha) / (count_sum + alpha * (V + 1))
        prob_dict[word] = math.log(pw)
    # Add the log probability of unknown tokens to the dictionary
    prob_dict["<UNK>"] = math.log(alpha / (count_sum + alpha * (V + 1)))
    # Return the dictionary of log probabilities
    return prob_dict


class SpamFilter(object):
    def __init__(self, spam_dir, ham_dir, smoothing):
        # List all files in the spam and ham directories
        spam_files = [f for f in listdir(spam_dir)]
        ham_files = [f for f in listdir(ham_dir)]
        # Create full paths for the spam and ham files
        spam_paths = [spam_dir + "/" + fname for fname in spam_files]
        ham_paths = [ham_dir + "/" + fname for fname in ham_files]
        # Calculate log probabilities for spam and ham
        self.spam_dict = log_probs(spam_paths, smoothing)
        self.ham_dict = log_probs(ham_paths, smoothing)
        # Calculate prior probabilities for spam and ham
        self.p_spam = len(spam_files) / float(len(spam_files) + len(ham_files))
        self.p_ham = len(ham_files) / float(len(spam_files) + len(ham_files))

    def is_spam(self, email_path):
        # Load tokens from the email
        email_tokens = load_tokens(email_path)
        # Initialize spam and ham probabilities with prior probabilities
        spam_probability = self.p_spam
        ham_probability = self.p_ham
        # Get the log probability for unknown tokens, default to 0 if not found
        unknown_token_probability = self.spam_dict.get("<UNK>", 0)
        # Update spam and ham probabilities based on the tokens in the email
        for token in email_tokens:
            spam_probability += self.spam_dict.get(token, unknown_token_probability)
            ham_probability += self.ham_dict.get(token, unknown_token_probability)
        # The email is classified as spam if the spam probability is greater than the ham probability
        return spam_probability > ham_probability

    def most_indicative_spam(self, n):
        # Initialize a dictionary to store the spamminess of each word
        spamminess_dict = {}
        # Calculate the spamminess of each word in the spam dictionary
        for word in self.spam_dict:
            if word in self.ham_dict:
                # Calculate the total probability of the word
                total_word_probability = math.exp(self.spam_dict[word]) * self.p_spam + math.exp(
                    self.ham_dict[word]) * self.p_ham
                # Calculate the spamminess of the word
                spamminess_dict[word] = self.spam_dict[word] - math.log(total_word_probability)
        # Sort the words by their spamminess in descending order
        sorted_spamminess = sorted(spamminess_dict, key=spamminess_dict.get, reverse=True)
        # Return the top n most indicative spam words
        return [sorted_spamminess[i] for i in range(n)]

    def most_indicative_ham(self, n):
        # Initialize a dictionary to store the hamminess of each word
        hamminess_dict = {}
        # Calculate the hamminess of each word in the ham dictionary
        for word in self.ham_dict:
            if word in self.spam_dict:
                # Calculate the total probability of the word
                total_word_probability = math.exp(self.spam_dict[word]) * self.p_spam + math.exp(
                    self.ham_dict[word]) * self.p_ham
                # Calculate the hamminess of the word
                hamminess_dict[word] = self.ham_dict[word] - math.log(total_word_probability)
        # Sort the words by their hamminess in descending order
        sorted_hamminess = sorted(hamminess_dict, key=hamminess_dict.get, reverse=True)
        # Return the top n most indicative ham words
        return [sorted_hamminess[i] for i in range(n)]


############################################################
# Section 2: Feedback
############################################################

feedback_question_1 = """
About 12 hours in total, including bug fixing.
"""

feedback_question_2 = """
I had some parts where I struggled with test cases, but that was because I didn't realize there was an updated version of the homework file.
"""

feedback_question_3 = """
I liked the homework. It was a good way to learn about Naive Bayes and how it can be used to classify spam emails.
"""

sf = SpamFilter("homework4_data/train/spam", "homework4_data/train/ham", 1e-5)
print(sf.most_indicative_ham(5))

sf = SpamFilter("homework4_data/train/spam", "homework4_data/train/ham", 1e-5)
print(sf.most_indicative_spam(5))

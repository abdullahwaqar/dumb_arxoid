import sys
import re
import numpy as np
import pandas as pd

from db_utils import insert_into_table, select_all_data

class Preprocessor:

    def __init__(self, movie_lines, movie_conversations):
        self.movie_lines = movie_lines
        self.movie_conversations = movie_conversations

    def read_file(self, filename):
        with open(filename, 'r', encoding='utf-8', errors='ignore') as infile:
            return infile.read().split('\n')

    def get_lines(self):
        """
        @return: Dictionary that map each movie line's id with its text
        """
        data_buffer = self.read_file(self.movie_lines)
        id_to_lines = {}
        for line in data_buffer:
            _line = line.split(' +++$+++ ')
            if len(_line) == 5:
                id_to_lines[_line[0]] = _line[4]
        return id_to_lines

    def clean_text(slef, text):
        '''
        @desc: Clean text by removing unnecessary characters and altering the format of words.
        '''
        text = text.lower()

        text = re.sub(r"i'm", "i am", text)
        text = re.sub(r"he's", "he is", text)
        text = re.sub(r"she's", "she is", text)
        text = re.sub(r"it's", "it is", text)
        text = re.sub(r"that's", "that is", text)
        text = re.sub(r"what's", "that is", text)
        text = re.sub(r"where's", "where is", text)
        text = re.sub(r"how's", "how is", text)
        text = re.sub(r"\'ll", " will", text)
        text = re.sub(r"\'ve", " have", text)
        text = re.sub(r"\'re", " are", text)
        text = re.sub(r"\'d", " would", text)
        text = re.sub(r"\'re", " are", text)
        text = re.sub(r"won't", "will not", text)
        text = re.sub(r"can't", "cannot", text)
        text = re.sub(r"n't", " not", text)
        text = re.sub(r"n'", "ng", text)
        text = re.sub(r"'bout", "about", text)
        text = re.sub(r"'til", "until", text)
        text = re.sub(r"[-()\"#/@;:<>{}`+=~|.!?,]", "", text)
        return text

    def get_conversations(self):
        """
        @return: List of all of the conversations' lines' ids.
        """
        data_buffer = self.read_file(self.movie_conversations)
        conversations = []
        for line in data_buffer[:-1]:
            _line = line.split(' +++$+++ ')[-1][1:-1].replace("'","").replace(" ","")
            conversations.append(_line.split(','))
        return conversations

    def sort_questions(self):
        """
        @return: Return the sentences into questions (inputs)
        """
        get_lines = self.get_lines()
        get_conversations = self.get_conversations()
        questions = []
        for conv in get_conversations:
            for i in range(len(conv) - 1):
                questions.append(get_lines[conv[i]])
        return questions

    def sort_answers(self):
        """
        @return: Return the sentences into answers (targets)
        """
        get_lines = self.get_lines()
        get_conversations = self.get_conversations()
        answers = []
        for conv in get_conversations:
            for i in range(len(conv) - 1):
                answers.append(get_lines[conv[i + 1]])
        return answers

    def get_clean_questions(self):
        """
        @return: Return array of questions without extra characters
        """
        questions = self.sort_questions()
        clean_questions = []
        for question in questions:
            clean_questions.append(self.clean_text(question))
        return clean_questions

    def get_clean_answers(self):
        """
        @return: Return array of answers without extra characters
        """
        answers = self.sort_answers()
        clean_answers = []
        for answer in answers:
            clean_answers.append(self.clean_text(answer))
        return clean_answers

    def insert_filter_questions_answers(self):
        #* Remove questions and answers that are shorter than 2 words and longer than 20 words.
        min_line_length = 2
        max_line_length = 20

        #* Filter out the questions that are too short/long
        short_questions_temp = []
        short_answers_temp = []

        counter = 0
        for question in self.get_clean_questions():
            if len(question.split()) >= min_line_length and len(question.split()) <= max_line_length:
                short_questions_temp.append(question)
                short_answers_temp.append(self.get_clean_answers()[counter])
                sys.stdout.write('Data Cleaned \r%d%%' % counter)
                sys.stdout.flush()
            counter += 1

        #* Filter out the answers that are too short/long
        short_questions = []
        short_answers = []

        counter = 0
        for answer in short_answers_temp:
            if len(answer.split()) >= min_line_length and len(answer.split()) <= max_line_length:
                # short_answers.append(answer)
                # short_questions.append(short_questions_temp[counter])
                #* Inser into db because it can take time on every execution
                insert_into_table('arxiod_filtered_data', [short_questions_temp[counter], answer])
                sys.stdout.write('Data Written to DB \r%d%%' % counter)
                sys.stdout.flush()
            counter += 1
        print("# of questions:", len(short_questions))
        print("# of answers:", len(short_answers))
        print("% of data used: {}%".format(round(len(short_questions)/len(questions),4)*100))
        return True

    def create_vocabulary(self):
        """
        @return: A dictionary for the frequency of the vocabulary
        """
        vocab = {}
        db_rows = select_all_data('arxiod_filtered_data')
        for question, answer in db_rows:
            for word in question.split():
                if word not in vocab:
                    vocab[word] = 1
                else:
                    vocab[word] += 1
            for word in answer.split():
                if word not in vocab:
                    vocab[word] = 1
                else:
                    vocab[word] += 1
        return vocab


if __name__ == '__main__':
    p = Preprocessor('data/dataset/cornell movie-dialogs corpus/movie_lines.txt', 'data/dataset/cornell movie-dialogs corpus/movie_conversations.txt')
    p.create_vocabulary()
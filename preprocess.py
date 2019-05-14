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

    def get_conversations(self):
        """
        @return: List of all of the conversations' lines' ids.
        """
        data_buffer = self.read_file(self.movie_conversations)
        conversations = []
        for line in data_buffer[:-1]:
            print(line)
            _line = line.split(' +++$+++ ')[-1][1:-1].replace("'","").replace(" ","")
            conversations.append(_line.split(','))
        return conversations

    def sort_questions_answers(self):
        """
        @return: Sort the sentences into questions (inputs) and answers (targets)
        """
        get_lines = self.get_lines()
        get_conversations = self.get_conversations()
        questions = []
        answers = []
        for conv in get_conversations:
            for i in range(len(conv) - 1):
                questions.append(get_lines[conv[i]])
                answers.append(get_lines[conv[i]])
        return (questions, answers)


if __name__ == '__main__':
    p = Preprocessor('data/dataset/cornell movie-dialogs corpus/movie_lines.txt', 'data/dataset/cornell movie-dialogs corpus/movie_conversations.txt')
    print(p.sort_questions_answers().answers)
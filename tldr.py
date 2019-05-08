# coding = utf-8
# tl;dr (too long; didn't read) -- text summarizer

import re
from nltk.tokenize import sent_tokenize, word_tokenize

class Summarizer(object):

    def split_to_paragraphs(self, content):
        """
        method to split the content into paragraphs
        """
        return content.split("\n\n")

    def split_to_sentences(self, content):
        """
        method to split the content into sentences
        """
        content = content.replace("\n", ". ")
        return sent_tokenize(content)

    def format_sentence(self, sentence):
        """
        remove all non-alphabetic characters from sentence
        """
        sentence = re.sub(r'\W+', '', sentence)
        return sentence

    def sentence_intersection(self, sent1, sent2):
        """
        sentence similarity measure
        """
        # splitting sentence into words/tokens
        s1 = set(word_tokenize(sent1))
        s2 = set(word_tokenize(sent2))

        # if there's no intersection between sentences
        if len(s1.intersection(s2)) == 0:
            return 0

        # normalizing the intersection of sentences by the avg no. of words in them
        return len(s1.intersection(s2)) / ((len(s1) + len(s2)) / 2)

    def rank_sentences(self, content):
        """
        convert the contents into a dict(sentence, rank_of_sentence) format
        """

        # split the content to sentences
        sentences = self.split_to_sentences(content)

        # calculate intersection of every two sentences
        n = len(sentences)
        values = [[0 for x in range(n)] for x in range(n)]
        for i in range(0, n):
            for j in range(0, n):
                values[i][j] = self.sentence_intersection(sentences[i], sentences[j])

        # building dict(sentence,rank) dictionary
        # score of a sentence is the sum of all its intersection
        sent_dict = {}
        for i in range(0, n):
            score = 0
            for j in range(0, n):
                if i == j:
                    continue
                score = score + values[i][j]
            sent_dict[self.format_sentence(sentences[i])] = score
        return sent_dict

    def get_best_sentences(self, paragraph, sentence_dictionary):
        """
        get the best sentence in a paragraph
        """

        # split paragraph to sentences
        sentences = self.split_to_sentences(paragraph)

        # ignore one liner paragraphs
        if len(sentences) < 2:
            return ""

        # get best sentence acc to sentence dictionary
        best_sent = ""
        max_value = 0
        for sent in sentences:
            formated_sent = self.format_sentence(sent)
            if formated_sent:
                if sentence_dictionary[formated_sent] > max_value:
                    max_value = sentence_dictionary[formated_sent]
                    best_sent = sent

        return best_sent

    def get_summary(self, title, content, sentence_dictionary):
        """
        method to get the summary
        """

        # split into paragraphs
        paragraphs = self.split_to_paragraphs(content)

        # keep the title as it is
        summary = []
        summary.append(title.strip())
        summary.append("")

        # adding best sentences from each paragraph to summary
        for paragraph in paragraphs:
            sentence = self.get_best_sentences(paragraph, sentence_dictionary).strip()

            if sentence:
                summary.append(sentence)

        return ("\n").join(summary)

if __name__ == "__main__":

    title = "Text Summarizer"

    with open('sample_text.txt') as file:
        content = file.read()

        summary_obj = Summarizer()

        sentence_dictionary = summary_obj.rank_sentences(content)

        summary = summary_obj.get_summary(title, content, sentence_dictionary)

        print(summary)

        print("")
        print("Original Length %s" % (len(title) + len(content)))
        print("Summary Length %s" % len(summary))
        print("Summary Ratio: %s" % (100 - (100 * (len(summary) / (len(title) + len(content))))))

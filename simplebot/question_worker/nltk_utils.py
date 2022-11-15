from typing import List

import nltk
from nltk.stem import SnowballStemmer
import numpy as np


stemmer = SnowballStemmer("russian")


def tokenize(sentence: str):
    """splits sentence into words

    Args:
        sentence (str): sentence to split
    """
    return nltk.word_tokenize(sentence)


def stem(word: str):
    """stems the word to basic form

    Args:
        word (str): word to stem
    """
    return stemmer.stem(word.lower())


def bag_of_words(tokenized_sentence: List[str], all_words: List[str]):
    """checks which words are in sentence and creates list of indexes for this words

    Args:
        tokenized_sentence (List[str]): tokenized sentence
        all_words (List[str]): list of all words

    Returns:
        List(float): list of indexes
    """
    tokenized_sentence = [stem(w) for w in tokenized_sentence]
    bag = np.zeros(len(all_words), dtype=np.float32)
    for idx, w in enumerate(all_words):
        if w in tokenized_sentence:
            bag[idx] = 1.0
    return bag

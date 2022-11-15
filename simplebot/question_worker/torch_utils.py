from typing import List

import torch
import torch.nn as nn

from simplebot.question_worker.nltk_utils import bag_of_words, tokenize


def get_intents(
    sentence: List[str], all_words: List[str], model: nn.Module, tags, intents
):
    """processes sentence and return matching intents

    Args:
        sentence (List): sentence to process
        all_words (List): list of all words
        model (nn.Module): neural network model
        tags (_type_): _description_
        intents (_type_): _description_

    Returns:
        str: intents
    """
    sentence = tokenize(sentence)
    x = bag_of_words(sentence, all_words)
    x = x.reshape(1, x.shape[0])
    x = torch.from_numpy(x)

    output = model(x)
    _, predicted = torch.max(output, dim=1)  # 0
    tag = tags[predicted.item()]

    probs = torch.softmax(output, dim=1)
    prob = probs[0][predicted.item()]

    if prob.item() > 0.75:
        for intent in intents["intents"]:
            if tag == intent["tag"]:
                return intent["responses"]
    else:
        return "_do_not_understand"

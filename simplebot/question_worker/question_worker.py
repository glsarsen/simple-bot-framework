import json

import torch

from simplebot.question_worker.torch_utils import get_intents
from simplebot.question_worker.nn_model import NeuralNet


class QuestionWorker:
    """class to hide all process of workinging with neural network"""

    def __init__(self, intents_file, model_file):
        """

        Args:
            intents_file (str): (intents.json) - file containing questions, tags and intents
            model_file (str): (data.pth) - file containing pre-trained neural network model
        """
        # Start up the torch module
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        # load intents
        with open(intents_file, "r", encoding="utf-8") as f:
            self.intents = json.load(f)

        # load the neural net model
        FILE = model_file
        data = torch.load(FILE)

        input_size = data["input_size"]
        hidden_size = data["hidden_size"]
        output_size = data["output_size"]
        self.all_words = data["all_words"]
        self.tags = data["tags"]
        model_state = data["model_state"]

        # set up the neural net model
        self.model = NeuralNet(input_size, hidden_size, output_size).to(device)
        self.model.load_state_dict(model_state)
        self.model.eval()

    def process_question(self, question):
        """processes user question, return corresponding tag

        Args:
            question (str): user question

        Returns:
            str: name of a branch
        """
        # Processing requests with a neural net

        answer = get_intents(
            sentence=question,
            all_words=self.all_words,
            model=self.model,
            tags=self.tags,
            intents=self.intents,
        )
        return answer

from transformers import AutoModelForSequenceClassification
from transformers import TFAutoModelForSequenceClassification
from transformers import AutoTokenizer, AutoConfig
from transformers import logging
logging.set_verbosity_error()
import numpy as np
import json
from scipy.special import softmax
from decimal import Decimal

# Preprocess text (username and link placeholders)


def preprocess(text):
    new_text = []
    for t in text.split(" "):
        t = '@user' if t.startswith('@') and len(t) > 1 else t
        t = 'http' if t.startswith('http') else t
        new_text.append(t)
    return " ".join(new_text)


MODEL = f"cardiffnlp/twitter-roberta-base-sentiment-latest"
tokenizer = AutoTokenizer.from_pretrained(MODEL)
config = AutoConfig.from_pretrained(MODEL)
# PT
model = AutoModelForSequenceClassification.from_pretrained(MODEL)

def compare_scores(scores):
    if scores[2] > scores[1] and scores[2] > scores[0]:
        return 1
    elif scores[0] > scores[1] and scores[0] > scores[2]:
        return 0
    elif scores[1] > scores[0] and scores[1] > scores[2]:
        return 0
    else:
        # Handle the case where none of the conditions are met
        return None

def analyzeSentiment(text):
    text = preprocess(text)
    encoded_input = tokenizer(text, return_tensors='pt')
    output = model(**encoded_input)
    scores = output[0][0].detach().numpy()
    scores = softmax(scores)
    details = {
        "positive": float(scores[2]),
        "neutral": float(scores[1]),
        "negative": float(scores[0])
    }
    sentiment = compare_scores(scores)
    return sentiment, details

'''# testing
text = "I'm neutral about it"
sentiment, details = analyzeSentiment(text)
print("sentiment : " + str(sentiment) + " ", details)'''


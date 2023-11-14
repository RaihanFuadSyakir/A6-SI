from processor import *
import json


##DATA
json_object_neg = {
  "username": "Kenton_Kirlin",
  "link": "oWTTyF8nMTR7",
  "caption": "Girl Group ",
  "comments_disabled": False,
  "comments": [
  {"comment_id": 1, "comment_text": "I love this!", "username": "User1"},
  {"comment_id": 2, "comment_text": "Great job!", "username": "User2"},
  {"comment_id": 3, "comment_text": "Amazing work!", "username": "User3"},
  {"comment_id": 4, "comment_text": "Fantastic!", "username": "User4"},
  {"comment_id": 5, "comment_text": "Awesome!", "username": "User5"},
  {"comment_id": 6, "comment_text": "Keep it up!", "username": "User6"},
  {"comment_id": 7, "comment_text": "Impressive!", "username": "User7"},
  {"comment_id": 8, "comment_text": "Well done!", "username": "User8"},
  {"comment_id": 9, "comment_text": "I appreciate this!", "username": "User9"},
  {"comment_id": 10, "comment_text": "Good work!", "username": "User10"},
  {"comment_id": 11, "comment_text": "I hate this!", "username": "Hater1"},
  {"comment_id": 12, "comment_text": "Terrible!", "username": "Hater2"},
  {"comment_id": 13, "comment_text": "Disgusting!", "username": "Hater3"},
  {"comment_id": 14, "comment_text": "I can't stand this!", "username": "Hater4"},
  {"comment_id": 15, "comment_text": "Awful!", "username": "Hater5"},
  {"comment_id": 16, "comment_text": "I despise this!", "username": "Hater6"},
  {"comment_id": 17, "comment_text": "Hate it!", "username": "Hater7"},
  {"comment_id": 18, "comment_text": "This is horrible!", "username": "Hater8"},
  {"comment_id": 19, "comment_text": "I loathe this!", "username": "Hater9"},
  {"comment_id": 20, "comment_text": "Disappointing!", "username": "Hater10"},
  {"comment_id": 21, "comment_text": "I love this!", "username": "User11"},
  {"comment_id": 22, "comment_text": "Great job!", "username": "User12"},
  {"comment_id": 23, "comment_text": "Amazing work!", "username": "User13"},
  {"comment_id": 24, "comment_text": "Fantastic!", "username": "User14"},
  {"comment_id": 25, "comment_text": "Awesome!", "username": "User15"},
  {"comment_id": 26, "comment_text": "Keep it up!", "username": "User16"},
  {"comment_id": 27, "comment_text": "Impressive!", "username": "User17"},
  {"comment_id": 28, "comment_text": "Well done!", "username": "User18"},
  {"comment_id": 29, "comment_text": "I appreciate this!", "username": "User19"},
  {"comment_id": 30, "comment_text": "Good work!", "username": "User20"}
]
}

json_object_pos = {
  "username": "Kenton_Kirlin",
  "link": "oWTTyF8nMTR7",
  "caption": "Girl Group ",
  "comments_disabled": False,
  "comments": [
  {"comment_id": 1, "comment_text": "I love this!", "username": "User1"},
  {"comment_id": 2, "comment_text": "Great job!", "username": "User2"},
  {"comment_id": 3, "comment_text": "Amazing work!", "username": "User3"},
  {"comment_id": 4, "comment_text": "Fantastic!", "username": "User4"},
  {"comment_id": 5, "comment_text": "Awesome!", "username": "User5"},
  {"comment_id": 6, "comment_text": "Keep it up!", "username": "User6"},
  {"comment_id": 7, "comment_text": "Impressive!", "username": "User7"},
  {"comment_id": 8, "comment_text": "Well done!", "username": "User8"},
  {"comment_id": 9, "comment_text": "I appreciate this!", "username": "User9"},
  {"comment_id": 10, "comment_text": "Good work!", "username": "User10"},
  {"comment_id": 11, "comment_text": "I hate this!", "username": "Hater1"},
  {"comment_id": 12, "comment_text": "I love this!", "username": "User11"},
  {"comment_id": 13, "comment_text": "Great job!", "username": "User12"},
  {"comment_id": 14, "comment_text": "Amazing work!", "username": "User13"},
  {"comment_id": 15, "comment_text": "Fantastic!", "username": "User14"},
  {"comment_id": 16, "comment_text": "Awesome!", "username": "User15"},
  {"comment_id": 17, "comment_text": "Keep it up!", "username": "User16"},
  {"comment_id": 18, "comment_text": "Impressive!", "username": "User17"},
  {"comment_id": 19, "comment_text": "Well done!", "username": "User18"},
  {"comment_id": 20, "comment_text": "I appreciate this!", "username": "User19"}
]

}

def add_sentiment(json_object, sentiment_value):
    """
    Add a "sentiment" field to the given JSON object.

    Parameters:
    - json_object (dict): The input JSON object.
    - sentiment_value (int): The sentiment value to be added.

    Returns:
    - dict: The modified JSON object with the "sentiment" field.
    """
    # Make a deep copy to avoid modifying the original object
    modified_object = json_object.copy()

    # Add the "sentiment" field
    modified_object["sentiment"] = sentiment_value

    return modified_object

def add_sentiment_to_comments(json_object):
    """
    Add a "sentiment" field to each comment object within the given JSON object.

    Parameters:
    - json_object (dict): The input JSON object.
    - sentiment_value (int): The sentiment value to be added.

    Returns:
    - dict: The modified JSON object with the "sentiment" field added to each comment.
    """
    # Make a deep copy to avoid modifying the original object
    modified_object = json_object.copy()

    # Add the "sentiment" field to each comment
    for comment in modified_object.get("comments", []):
        sentiment_value, _ = analyzeSentiment(comment["comment_text"])
        comment["sentiment"] = sentiment_value

    return modified_object


def calculate_overall_sentiment(comments):
    """
    Calculate the overall sentiment value based on the sentiments of comments.

    Parameters:
    - comments (list): List of comments with "sentiment" field.

    Returns:
    - int: Overall sentiment value (0 or 1).
    """
    total_comments = len(comments)
    positive_comments = sum(comment["sentiment"] == 1 for comment in comments)

    # Calculate the percentage of positive comments
    positive_percentage = (positive_comments / total_comments) * 100

    # Set overall sentiment value based on the percentage threshold
    overall_sentiment = 1 if positive_percentage >= 75 else 0

    return overall_sentiment

def add_overall_sentiment(json_object):
    """
    Add an "overall_sentiment" field to the given JSON object.

    Parameters:
    - json_object (dict): The input JSON object.

    Returns:
    - dict: The modified JSON object with the "overall_sentiment" field.
    """
    # Make a deep copy to avoid modifying the original object
    modified_object = json_object.copy()

    # Calculate the overall sentiment value based on comments
    overall_sentiment_value = calculate_overall_sentiment(modified_object.get("comments", []))

    # Add the "overall_sentiment" field
    modified_object["sentiment"] = overall_sentiment_value

    return modified_object


def analyze(json_data):
    json_mod = add_sentiment_to_comments(json_data)
    json_mod = add_overall_sentiment(json_mod)
    pretty_json = json.dumps(json_mod, indent=2)
    with open('output.json', 'w') as file:
        file.write(pretty_json)
    
    print("Pretty JSON has been saved to 'output.json'")
    
    return json_mod

analyze(json_object_pos)

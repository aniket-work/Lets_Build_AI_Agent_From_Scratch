def find_unique_words(sentence):
    """
    Find unique words in a given sentence.

    Args:
    sentence (str): The input sentence to analyze.

    Returns:
    list: A list of unique words in the sentence.
    """
    words = sentence.lower().split()
    return list(set(words))
def find_longest_words(sentence):
    """
    Find the longest word(s) in a given sentence.

    Args:
    sentence (str): The input sentence to analyze.

    Returns:
    list: A list of the longest word(s) in the sentence.
    """
    words = sentence.split()
    max_length = max(len(word) for word in words)
    return [word for word in words if len(word) == max_length]
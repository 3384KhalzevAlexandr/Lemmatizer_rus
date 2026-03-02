import re
from src.utils import normalize


def preprocess(text):
    sentences = text.strip().split('\n')
    result = []

    for sentence in sentences:
        clean = re.sub(r'[,.?!]', '', sentence)
        tokens = clean.split()

        sentence_tokens = []
        for token in tokens:
            sentence_tokens.append({
                "original": token,
                "normalized": normalize(token)
            })

        result.append(sentence_tokens)

    return result
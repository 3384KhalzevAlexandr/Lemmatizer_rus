from collections import defaultdict
from src.preprocessor import normalize

SPECIAL_POS = {
    "пока": "CONJ",
    "его": "NI",
    "ее": "NI",
    "её": "NI",
    "он": "NI",
    "она": "NI",
    "они": "NI",
    "их": "NI",
    "и": "CONJ",
    "а": "CONJ",
    "но": "CONJ"
}

def guess_pos(token_norm):
    if token_norm in SPECIAL_POS:
        return token_norm, SPECIAL_POS[token_norm]

    if token_norm in {"в", "на", "с", "к", "по", "за", "из", "о", "об", "у"}:
        return token_norm, "PR"

    if token_norm.endswith(('ть', 'ти', 'чь', 'ться', 'тся')):
        return token_norm, "V"

    if token_norm.endswith(('л', 'ла', 'ло', 'ли')):
        return token_norm, "V"

    if token_norm.endswith(("ый", "ий", "ой", "ая", "ое", "ые")):
        return token_norm, "A"

    if token_norm.endswith(("о", "е")):
        return token_norm, "ADV"

    return token_norm, "S"

def lemmatize_token(token, dictionary, freq_model=None):
    token_norm = token["normalized"]

    if token_norm in SPECIAL_POS:
        return token_norm, SPECIAL_POS[token_norm]

    if token_norm in dictionary:
        analyses = dictionary[token_norm]

        if freq_model and token_norm in freq_model:
            lemma_freqs = freq_model[token_norm]
            best_lemma = max(lemma_freqs, key=lemma_freqs.get)

            for lemma, pos in analyses:
                if normalize(lemma) == best_lemma:
                    return best_lemma, pos

        lemma, pos = analyses[0]
        return normalize(lemma), pos
    
    return guess_pos(token_norm)

def lemmatize_sentence(sentence_tokens, dictionary, freq_model=None):
    result = []
    for token in sentence_tokens:
        lemma, pos = lemmatize_token(token, dictionary, freq_model)
        result.append((token["original"], lemma, pos))
    return result

def format_output(lemmatized_sentence):
    return " ".join(
        f"{original}{{{lemma}={pos}}}"
        for original, lemma, pos in lemmatized_sentence
    )

def analyze(sentence, dictionary, freq_model=None):
    from src.preprocessor import preprocess
    tokens = preprocess(sentence)[0]
    lemmatized = lemmatize_sentence(tokens, dictionary, freq_model)
    return format_output(lemmatized)
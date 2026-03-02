import pickle
from collections import defaultdict
from src.lemmatizer import lemmatize_token


def build_frequency_model(gold_path, output_path):
    with open(gold_path, "rb") as f:
        gold_data = pickle.load(f)

    freq = defaultdict(lambda: defaultdict(int))

    for item in gold_data:
        form = item["normalized"]
        lemma = item["gold_lemma"]
        freq[form][lemma] += 1

    freq = {k: dict(v) for k, v in freq.items()}

    with open(output_path, "wb") as f:
        pickle.dump(freq, f)


def evaluate(gold_path, dictionary, freq_model):
    with open(gold_path, "rb") as f:
        gold_data = pickle.load(f)

    total = 0
    correct_lemma = 0
    correct_pos = 0
    correct_both = 0

    for item in gold_data:
        pred_lemma, pred_pos = lemmatize_token(item, dictionary, freq_model)

        total += 1

        lemma_ok = pred_lemma == item["gold_lemma"]
        pos_ok = pred_pos == item["gold_pos"]

        if lemma_ok:
            correct_lemma += 1
        if pos_ok:
            correct_pos += 1
        if lemma_ok and pos_ok:
            correct_both += 1

    print("Lemma accuracy:", round(correct_lemma / total * 100, 2), "%")
    print("POS accuracy:", round(correct_pos / total * 100, 2), "%")
    print("Full accuracy:", round(correct_both / total * 100, 2), "%")
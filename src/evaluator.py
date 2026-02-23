import pickle
from collections import defaultdict
from src.lemmatizer import lemmatize_token
from src.preprocessor import normalize
from src.dictionary import POS_MAP

def parse_gold_corpus(xml_path, output_path):
    import xml.etree.ElementTree as ET
    
    tree = ET.parse(xml_path)
    root = tree.getroot()

    gold_data = []

    for sentence in root.iter("sentence"):
        for token in sentence.iter("token"):
            if "text" not in token.attrib:
                continue

            original = token.attrib["text"]

            tfr = token.find("tfr")
            if tfr is None:
                continue

            l_elem = tfr.find(".//l")
            if l_elem is None:
                continue

            gold_lemma = normalize(l_elem.attrib["t"])

            gold_pos = None
            for g in l_elem.findall("g"):
                gram = g.attrib["v"]
                if gram in POS_MAP:
                    gold_pos = POS_MAP[gram]
                    break

            if gold_pos is None:
                continue

            gold_data.append({
                "original": original,
                "normalized": normalize(original),
                "gold_lemma": gold_lemma,
                "gold_pos": gold_pos
            })

    with open(output_path, "wb") as f:
        pickle.dump(gold_data, f)

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

def evaluate(gold_path, dictionary, freq_model=None):
    with open(gold_path, "rb") as f:
        gold_data = pickle.load(f)

    total = 0
    correct_lemma = 0
    correct_pos = 0
    correct_both = 0

    for item in gold_data:
        pred_lemma, pred_pos = lemmatize_token(item, dictionary, freq_model)

        total += 1

        if pred_lemma == item["gold_lemma"]:
            correct_lemma += 1
        if pred_pos == item["gold_pos"]:
            correct_pos += 1
        if pred_lemma == item["gold_lemma"] and pred_pos == item["gold_pos"]:
            correct_both += 1

    print("Всего токенов:", total)
    print("Lemma accuracy:", round(correct_lemma / total * 100, 2), "%")
    print("POS accuracy:", round(correct_pos / total * 100, 2), "%")
    print("Full accuracy:", round(correct_both / total * 100, 2), "%")
    
    return {
        "total": total,
        "lemma_accuracy": correct_lemma / total,
        "pos_accuracy": correct_pos / total,
        "full_accuracy": correct_both / total
    }
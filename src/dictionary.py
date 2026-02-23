import pickle
import xml.etree.ElementTree as ET
from collections import defaultdict

POS_MAP = {
    "NOUN": "S",
    "VERB": "V",
    "INFN": "V",
    "ADJF": "A",
    "ADJS": "A",
    "COMP": "A",
    "ADVB": "ADV",
    "PREP": "PR",
    "CONJ": "CONJ",
    "NPRO": "NI",
    "NUMR": "NI",
    "PRCL": "ADV"
}

def load_opencorpora_dictionary(xml_path):
    tree = ET.parse(xml_path)
    root = tree.getroot()

    dictionary = defaultdict(list)

    for lemma in root.iter("lemma"):
        l_elem = lemma.find("l")
        lemma_text = l_elem.attrib["t"]

        pos = None
        for g in l_elem.findall("g"):
            gram = g.attrib["v"]
            if gram in POS_MAP:
                pos = POS_MAP[gram]
                break

        if pos is None:
            continue

        norm_lemma = normalize(lemma_text)
        dictionary[norm_lemma].append((lemma_text, pos))

        for f in lemma.findall("f"):
            form_text = f.attrib["t"]
            norm_form = normalize(form_text)
            dictionary[norm_form].append((lemma_text, pos))

    return dictionary

def save_dictionary(dictionary, output_path):
    with open(output_path, "wb") as f:
        pickle.dump(dictionary, f)

def load_dictionary(pkl_path):
    with open(pkl_path, "rb") as f:
        return pickle.load(f)

from src.preprocessor import normalize
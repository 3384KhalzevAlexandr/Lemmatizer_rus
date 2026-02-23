import pickle
from src.dictionary import load_dictionary
from src.evaluator import evaluate
from src.lemmatizer import analyze
from src.preprocessor import normalize

def main():
    with open("models/opencorpora_dict.pkl", "rb") as f:
        dictionary = pickle.load(f)
    with open("models/freq_model.pkl", "rb") as f:
        freq_model = pickle.load(f)

    evaluate("models/gold_corpus.pkl", dictionary, freq_model)
    
    print("\nПримеры для неизвестных слов:")
    for word in ["кринж", "додеп"]:
        token = {
            "original": word,
            "normalized": normalize(word)
        }
        print(f"Слово: {word}")

if __name__ == "__main__":
    main()
import pickle
from src.lemmatizer import analyze
from src.evaluator import evaluate

def main():
    with open("models/opencorpora_dict.pkl", "rb") as f:
        dictionary = pickle.load(f)

    with open("models/freq_model.pkl", "rb") as f:
        freq_model = pickle.load(f)

    evaluate("models/gold_corpus.pkl", dictionary, freq_model)

    while True:
        sent = input(">>> ")
        if not sent.strip():
            break

        result = analyze(sent, dictionary, freq_model)
        print("Результат лемматизации:")
        print(result)
        print()


if __name__ == "__main__":
    main()
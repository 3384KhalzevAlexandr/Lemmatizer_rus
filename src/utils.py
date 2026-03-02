def normalize(word):
    return word.lower().replace("ё", "е")


def levenshtein(a, b):
    if len(a) < len(b):
        return levenshtein(b, a)

    if len(b) == 0:
        return len(a)

    previous_row = range(len(b) + 1)
    for i, ca in enumerate(a):
        current_row = [i + 1]
        for j, cb in enumerate(b):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (ca != cb)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row

    return previous_row[-1]


def find_closest_word(token_norm, dictionary):
    best_word = None
    best_distance = float("inf")

    for key, analyses in dictionary.items():
        lemma_norm = normalize(analyses[0][0])
        if key != lemma_norm:
            continue

        dist = levenshtein(token_norm, key)

        if dist < best_distance:
            best_distance = dist
            best_word = key

        if best_distance == 0:
            break

    return best_word
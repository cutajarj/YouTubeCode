from rapidfuzz.distance import Levenshtein

def extract_q_grams(word, q):
    q_grams = []
    for i in range(len(word) - q + 1):
        q_grams.append(word[i:i + q])
    return q_grams


def extract_all_q_gram(all_words, q):
    all_q_grams = {} #'lin' -> set("linear", "spelling", "selling")
    for word in all_words:
        for q_gram in extract_q_grams(word, q):
            all_q_grams[q_gram] = all_q_grams.get(q_gram, set())
            all_q_grams[q_gram].add(word)
    return all_q_grams


def find_closest_matches(all_q_grams, check_word, q):
    matches = {} #'spelling' -> 4 (q-grams matched)
    input_q_gram = extract_q_grams(check_word, q)
    for q_gram in input_q_gram:
        for word in all_q_grams.get(q_gram, []):
            matches[word] = matches.get(word, 0) + 1
    closest_matches = sorted(matches, key=matches.get, reverse=True)[:100]
    return sorted(closest_matches, key=lambda m: Levenshtein.distance(check_word, m))[:5]


def read_all_words():
    all_words = []
    with open('/usr/share/dict/words') as f:
        for line in f:
            all_words.append(line.strip())
    return all_words


if __name__ == '__main__':
    q_len = 3
    input_word = 'speling'
    all_eng_words = read_all_words()
    global_q_grams = extract_all_q_gram(all_eng_words, q_len)
    print(find_closest_matches(global_q_grams, input_word, q_len))

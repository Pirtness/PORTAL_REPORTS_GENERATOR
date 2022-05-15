import hashlib


def get_hash_set_from_string(text, shingle_length=5):
    hashes = set()
    for i in range(len(text) - shingle_length):
        shingle = text[i:i + shingle_length]
        hashes.add(hashlib.md5(shingle.encode()).hexdigest())
    return hashes


def count_hashes_similarities(hashes1, hashes2):
    count = 0
    for h in hashes1:
        if h in hashes2:
            count += 1
    return count


def get_similarity_percentage(text1, text2, shingle_length=5):
    hashes1 = get_hash_set_from_string(text1, shingle_length)
    hashes2 = get_hash_set_from_string(text2, shingle_length)
    similarities_count = count_hashes_similarities(hashes1, hashes2)
    return 2 * similarities_count / (len(hashes1) + len(hashes2))


def get_similarity_percentage_of_hash_sets(hashes1, hashes2):
    similarities_count = count_hashes_similarities(hashes1, hashes2)
    return 2 * similarities_count / (len(hashes1) + len(hashes2))


def texts_are_similar(text1, text2, min_similarity_percentage=70, shingle_length=5):
    min_similarity_percentage *= 0.01
    similarity_percentage = get_similarity_percentage(text1, text2, shingle_length)
    return similarity_percentage >= min_similarity_percentage


def hashed_texts_are_similar(hashed_text1, hashed_text2, min_similarity_percentage=70):
    min_similarity_percentage *= 0.01
    similarity_percentage = get_similarity_percentage_of_hash_sets(hashed_text1, hashed_text2)
    return similarity_percentage >= min_similarity_percentage
import re
import math
from collections import Counter

stopwords = {
    "ourselves", "hers", "between", "yourself", "but", "again", "there", "about",
    "once", "during", "out", "very", "having", "with", "they", "own", "an", "be",
    "some", "for", "do", "its", "yours", "such", "into", "of", "most", "itself",
    "other", "off", "is", "s", "am", "or", "who", "as", "from", "him", "each",
    "the", "themselves", "until", "below", "are", "we", "these", "your", "his",
    "through", "don", "nor", "me", "were", "her", "more", "himself", "this", "down",
    "should", "our", "their", "while", "above", "both", "up", "to", "ours", "had",
    "she", "all", "no", "when", "at", "any", "before", "them", "same", "and", "been",
    "have", "in", "will", "on", "does", "yourselves", "then", "that", "because",
    "what", "over", "why", "so", "can", "did", "not", "now", "under", "he", "you",
    "herself", "has", "just", "where", "too", "only", "myself", "which", "those",
    "i", "after", "few", "whom", "t", "being", "if", "theirs", "my", "against", "a",
    "by", "doing", "it", "how", "further", "was", "here", "than"
}
def remove_suffix(word):
    suffixes = [("ing", 4), ("ly", 3), ("ment", 5)]
    for suffix, min_len in suffixes:
        if word.endswith(suffix) and len(word) > min_len:
            return word[:-len(suffix)]
    return word

def preprocess_text(text):
    text = re.sub(r'https?://\S+', '', text)  
    text = re.sub(r'[^\w\s]', '', text).lower()  
    text = re.sub(r'\s+', ' ', text).strip()  
    words = text.split()
    return ' '.join(remove_suffix(word) for word in words if word not in stopwords)

def preprocess_and_compute_tfidf(list_file='tfidf_docs.txt'):
    documents = []  
    doc_names = []

    with open(list_file, 'r') as file_list:
        for file_path in file_list:
            file_path = file_path.strip()
            doc_names.append(file_path)
            with open(file_path, 'r') as file:
                text = file.read()
                processed_text = preprocess_text(text)
                documents.append(processed_text.split())

                #Save preprocessed text to file
                processed_file_path = "preproc_" + file_path
                with open(processed_file_path, 'w') as processed_file:
                    processed_file.write(processed_text)

    #Compute TF for each document
    tf_scores = [{word: doc.count(word) / len(doc) for word in set(doc)} for doc in documents]

    #Compute IDF for all unique words across documents
    all_words = set(word for doc in documents for word in doc)
    idf_scores = {
        word: math.log(len(documents) / sum(word in doc for doc in documents)) + 1 for word in all_words
    }

    #Compute TF-IDF scores and write top 5 terms to files
    for i, (tf_score, doc_name) in enumerate(zip(tf_scores, doc_names)):
        tfidf_scores = {word: (tf * idf_scores[word]) for word, tf in tf_score.items()}
        top_5_words = sorted(tfidf_scores.items(), key=lambda x: (-x[1], x[0]))[:5]

        tfidf_file_path = f"tfidf_{doc_name}"
        with open(tfidf_file_path, 'w') as tfidf_file:
            tfidf_file.write('\n'.join(f"{word}: {round(score, 2)}" for word, score in top_5_words))

preprocess_and_compute_tfidf()
def main():
    preprocess_and_compute_tfidf("tfidf_docs.txt")

main()

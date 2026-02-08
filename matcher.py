import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def find_best_match(user_need, database_skills):
    vectorizer = TfidfVectorizer()
    all_text = [user_need] + database_skills
    tfidf_matrix = vectorizer.fit_transform(all_text)
    similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:])
    return similarity.argsort()[0][-1]

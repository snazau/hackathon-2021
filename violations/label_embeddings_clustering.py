# Prototype

import numpy as np
import os
import pandas as pd
import difflib
from sklearn.cluster import AffinityPropagation, KMeans
import distance
import random


def words_clustering(unique_words):
    words = np.asarray(unique_words)  # So that indexing with a list will work
    lev_similarity = -1 * np.array([[distance.levenshtein(w1, w2) for w1 in words] for w2 in words])

    affprop = AffinityPropagation(affinity="precomputed", damping=0.5)
    affprop.fit(lev_similarity)
    cluster_representors = []
    clusters = []
    for cluster_id in np.unique(affprop.labels_):
        exemplar = words[affprop.cluster_centers_indices_[cluster_id]]
        cluster = np.unique(words[np.nonzero(affprop.labels_ == cluster_id)])
        cluster_str = ", ".join(cluster)
        # print(" - *%s:* %s" % (exemplar, cluster_str))
        cluster_representors.append(exemplar)
        clusters.append(cluster_str)

    return cluster_representors, clusters


if __name__ == '__main__':
    data_dir = os.path.join(os.path.dirname(__file__), 'data')
    targets_path = os.path.join(data_dir, "Разметка_обезличенная.xlsx")
    df = pd.read_excel(targets_path, engine="openpyxl")
    print(df.shape)

    # Clearing targets
    for target in pd.unique(df["Вид нарушения"]):
        if not isinstance(target, str) or len(target) < 4:
            df = df.drop(df[df["Вид нарушения"] == target].index)
    df = df.dropna(subset=["Вид нарушения"])

    df["Вид нарушения"] = df["Вид нарушения"].apply(lambda x: x.lower())
    df["Вид нарушения"] = df["Вид нарушения"].apply(lambda x: x.strip())
    unique_targets = pd.unique(df["Вид нарушения"])
    print("Unique targets amount", len(unique_targets))
    unique_targets = [str(target) for target in unique_targets]

    similar_targets = difflib.get_close_matches(unique_targets[0], list(unique_targets), n=20, cutoff=0.5)
    print("Similar targets to", unique_targets[0])
    for index, target in enumerate(similar_targets):
        print(index, target)
    print()
    exit()

    # String clustering
    # words = np.asarray(unique_targets)  # So that indexing with a list will work
    # cluster_representors, clusters = words_clustering(unique_targets)
    # print("len(cluster_representors)", len(cluster_representors))
    # while len(cluster_representors) > 20:
    #     cluster_representors, clusters = words_clustering(cluster_representors)
    #     print("len(cluster_representors)", len(cluster_representors))
    #
    # clustered_targets_data = {
    #     'representors': cluster_representors,
    #     'clusters': clusters
    # }
    # clustered_targets_df = pd.DataFrame(clustered_targets_data, columns=['representors', 'clusters'])
    # clustered_targets_csv_path = os.path.join(data_dir, "clustered_targets.csv")
    # clustered_targets_df.to_csv(clustered_targets_csv_path, index=False)

    from sentence_transformers import SentenceTransformer
    model = SentenceTransformer('xlm-roberta-base')
    sentence_embeddings = model.encode(unique_targets)
    print("sentence embeddings", sentence_embeddings.shape)

    clusters_amount = 15
    kmeans_model = KMeans(n_clusters=clusters_amount)
    kmeans_model.fit(np.array(sentence_embeddings))

    target_cluster_ids = kmeans_model.labels_
    print(target_cluster_ids)
    print(target_cluster_ids.shape)

    cluster_representors = []
    clusters = []
    for cluster_id in range(clusters_amount):
        cluster_indecies = np.where(target_cluster_ids == cluster_id)[0]
        # print(type(cluster_indecies), cluster_indecies)
        # exit()
        cluster_targets = list(np.array(unique_targets)[cluster_indecies])
        cluster_targets = sorted(cluster_targets, key=len)
        clusters.append("|".join(cluster_targets))

        representor = cluster_targets[len(cluster_targets) // 2]
        while len(representor) > 200:
            rand_index = random.randint(0, len(cluster_targets) - 1)
            representor = cluster_targets[rand_index]

        cluster_representors.append(representor)
        print("target #{} = {}".format(cluster_id, representor))

    clustered_targets_data = {
        'representors': cluster_representors,
        'clusters': clusters
    }
    clustered_targets_df = pd.DataFrame(clustered_targets_data, columns=['representors', 'clusters'])
    clustered_targets_csv_path = os.path.join(data_dir, "clustered_BERT_KMeans_targets.csv")
    clustered_targets_df.to_csv(clustered_targets_csv_path, index=False)

    # for sentence, embedding in zip(unique_targets, sentence_embeddings):
    #     print("Sentence:", sentence)
    #     print("Embedding:", embedding)
    #     print("")

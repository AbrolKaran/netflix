from django.shortcuts import render

# Create your views here.
import numpy as np
import time
from scipy import spatial
from ratings.models import Rating

def cosine_similarity(i, j):
    epsilon = 10**-7
    num = np.dot(i, j)
    den = np.linalg.norm(i) * np.linalg.norm(j) + epsilon
    return num/den

def k_neighbours(i, k, sim):
    score = sim[i]
    sort = np.argsort(score)[::-1]
    return sort[1: k + 1]

def predict_item(user, item, k, ratings, sim):
    kn = k_neighbours(item, k, sim)
    num, den = 0, 0
    for i in kn:
        if ratings[i][user] != 0:
            num += sim[item, i] * ratings[i, user]
            den += sim[item, i]
    if den == 0:
        return -1
    else:
        return round(num/den)

def predict_user(user, item, k, ratings, sim):
    kn = k_neighbours(user, k, sim)
    num, den = 0, 0
    for u in kn:
        if ratings[u][item] != 0:
            num += sim[user, u] * (ratings[u, item] - np.average(ratings[u]))
            den += sim[user, u]
    if den == 0:
        return -1
    else:
        return round(np.average(ratings[user]) + num/den)

def get_data(fold):
    num_u = 943
    num_i = 1682
    train_arr = np.zeros((num_u, num_i))
    f = open(f"ml-100k/u{fold}.base", "r")
    for line in f:
        u, i, r, t = line.split('\t')
        train_arr[int(u) - 1, int(i) - 1] = int(r)
    f.close()

    test_arr = np.zeros((num_u, num_i))
    f = open(f"ml-100k/u{fold}.test", "r")
    for line in f:
        u, i, r, t = line.split('\t')
        test_arr[int(u) - 1, int(i) - 1] = int(r)
    f.close()

    return train_arr, test_arr

def item_based_recommendation(train_arr, test_arr):
    num_u = 943
    num_i = 1682

    sim = np.zeros((num_i, num_i))
    ratings = train_arr.T

    for i in range(num_i):
        for j in range(num_i):
            sim[i, j] = cosine_similarity(ratings[i], ratings[j])

    k_vals = [10, 20, 30, 40, 50]
    mae_vals = []
    for k in k_vals:
        sum, count = 0, 0
        tm, tn = test_arr.shape
        for i in range(tm):
            for j in range(tn):
                q = test_arr[i][j]
                if q != 0:
                    p = predict_item(i, j, k, ratings, sim)
                    if p != -1:
                        sum += abs(p - q)
                        count += 1
        mae_vals.append(sum/count)
    print(mae_vals)

def user_based_recommendation(train_arr, test_arr):
    num_u = 943
    num_i = 1682

    sim = np.zeros((num_u, num_u))
    ratings = train_arr

    for i in range(num_u):
        for j in range(num_u):
            sim[i, j] = cosine_similarity(ratings[i], ratings[j])

    k_vals = [10, 20, 30, 40, 50]
    mae_vals = []
    for k in k_vals:
        sum, count = 0, 0
        tm, tn = test_arr.shape
        for i in range(tm):
            for j in range(tn):
                q = test_arr[i][j]
                if q != 0:
                    p = predict_user(i, j, k, ratings, sim)
                    if p != -1:
                        sum += abs(p - q)
                        count += 1
        mae_vals.append(sum/count)
    print(mae_vals)

def user_user():
    for i in range(1, 6):
        train, test = get_data(i)
        print(f"Fold {i}")
        user_based_recommendation(train, test)

def item_item():
    for i in range(1, 6):
        train, test = get_data(i)
        print(f"Fold {i}")
        item_based_recommendation(train, test)

# s = time.time()
# user_user()
# item_item()
# e = time.time()
# print(f"Execution Time: {e - s}")

import pandas as pd
import random as rd
import matplotlib.pyplot as plt

#----THIS IS THE K VALUE, CHANGE THIS MANUALLY EACH TIME-----
K = 2 #From 2 to 15 to try everything

#This part loads the data

matrix = pd.read_csv("user_movie_matrix.csv", index_col=0).astype(float)
X = matrix.to_numpy()
num_points = len(X)
num_features = len(X[0])

#Centroid initialization

rd.seed(0)
initial_indices = rd.sample(range(num_points), K)

centroids = []
for i in initial_indices:
    row = []
    for j in range(num_features):
        row.append(X[i][j])
    centroids.append(row)

#Manual Kmeans part:

# 1) Calculate Distance
max_iter = 100
for iteration in range(max_iter):
    distances = []
    for i in range(num_points):
        point_distances = []
        for c in centroids:
            dist = 0
            for j in range (num_features):
                diff = X[i][j] - c[j]
                dist += diff * diff
            point_distances.append(dist ** 0.5)
        distances.append(point_distances)

    # 2) Cluster assignment
    assignments = []
    for distance_list in distances:
        min_idx = 0
        min_val = distance_list[0]
        for k in range (1,K):
            if distance_list[k] < min_val:
                min_idx = k
                min_val = distance_list[k]
        assignments.append(min_idx)

    # 3) Centroid update
    new_centroids = []
    for k in range(K):
        members = [X[i] for i in range(num_points) if assignments[i] == k]
        if members:
            new_center = []
            for j in range(num_features):
                feature_sum = 0
                for m in members:
                    feature_sum += m[j]
                new_center.append(feature_sum/len(members))
            new_centroids.append(new_center)
        else:
            new_centroids.append(centroids[k]) #keeps the old centroid if empty

    # 4) Convergence check
    converged = True
    for a,b in zip(centroids, new_centroids):
        for j in range(num_features):
            if abs(a[j] - b[j]) > 1e-4:
                converged = False
                break
        if not converged:
            break
    if converged:
        break

    centroids = new_centroids

#This part calculates inertia so we can record it for each K in kmeans_log.csv

inertia = 0
for i in range(num_points):
    cluster = assignments[i]
    dist = 0
    for j in range(num_features):
        diff = X[i][j] - centroids[cluster][j]
        dist += diff * diff
    
    inertia += dist

#Since we have K and its corresponding inertia, we now add it to the log excel

log = pd.DataFrame([[K,inertia]], columns=["K", "Inertia"])
log.to_csv("kmeans_log.csv", mode='a', header=False, index=False)


#This part plots the updated curve each time we add a new K and inertia value to the excel file

log_df = pd.read_csv("kmeans_log.csv")

plt.figure(figsize=(8, 5))
plt.plot(log_df["K"], log_df["Inertia"], marker='o')
plt.title("Elbow Curve - Manual KMeans")
plt.xlabel("Number of Clusters (K)")
plt.ylabel("Inertia (Sum of Squared Distances)")
plt.grid(True)
plt.savefig("Kmeans_elbow_plot.png")
plt.close()
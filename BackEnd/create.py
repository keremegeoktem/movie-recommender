import pandas as pd

#This creates a fresh file to track each K as we try, so it only runs once at the very beginning
#It is used in the manual KMeans process

pd.DataFrame(columns=["K", "Inertia"]).to_csv("kmeans_log.csv",index=False)
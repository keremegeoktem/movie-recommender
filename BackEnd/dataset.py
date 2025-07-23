#This dataset is taken from the following publication:
#> F. Maxwell Harper and Joseph A. Konstan. 2015. The MovieLens Datasets: History and Context. ACM Transactions on Interactive Intelligent Systems (TiiS) 5, 4: 19:1–19:19. <https://doi.org/10.1145/2827872>
import pandas as pd
ratings = pd.read_csv("ratings.csv")
#We have millions of data, so filtering is needed

#Filters for active users, so only include those that rated >200 movies
active_users = ratings['userId'].value_counts()[ratings['userId'].value_counts() > 200].index

#filters for popular movies, only rated > 300 times are included
popular_movies = ratings['movieId'].value_counts()[ratings['movieId'].value_counts() > 300].index

#Now apply filters
filtered = ratings[
    (ratings['userId'].isin(active_users)) &
    (ratings['movieId'].isin(popular_movies))
]

user_item_matrix = filtered.pivot_table(
    index = "movieId",   #rows = movies
    columns = "userId",    #columns = users
    values = "rating",  #ratings each user gave
)

#Turns out you need to fill "Na" with 0s for clustering, so this does that

matrix_to_cluster = user_item_matrix.fillna(0)

#final cleanup, drops rows that are now fully zero due to float precision
matrix_to_cluster = matrix_to_cluster[matrix_to_cluster.sum(axis=1).round(6) > 0]

#This line to create the .csv file:
matrix_to_cluster.to_csv("user_movie_matrix.csv")

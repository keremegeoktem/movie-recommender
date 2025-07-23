## Content-Based Filtering Movie Recommender 

This project is a movie recommendation engine built from scratch using manual KMeans

## Project Goals
1- Learn how KMeans works by manually creating it from scratch
2- Cluster movies based on user rating patterns
3- Use 3 movie inputs from users to recommend movies to them deemed similar by the K Means algorithm.
4- Use local storage to move and use data across pages
5- Learn frontend basics: how to style a page and how to add individual functional elements

## Important Notice:
1- Since manual KMeans takes a lot of time and computing power (that my laptop does not have) I opted to use a faster version using scikit-learn library.
2- The faster code is not inside here since it is not mine, but my manual implementation that works -but takes a really long time- is still present in the project file.
3- The data used in this project is huge, so I will not upload it directly. If anybody wants to use this for any reason, here is the link to the dataset: https://grouplens.org/datasets/movielens/
4- The specific data I am using is called MovieLens 32M. 

## How it works
### BACKEND
- **Files**: `create.py`, `compare.py`, `dataset.py`, `manual_kmeans.py`  
- These methods first filter the data for active users (200+ ratings) and popular movies (rated 300+ times).  
- KMeans then creates an elbow plot PNG (to find the correct K to use) and clusters to detect "similar" movies, based on the ratings that users gave out for all movies they have seen  
- `movie_cluster_assignments.csv` has the final movieId → cluster information  
- Flask (`app.py`) serves recommendations and feedback logging  
- The title of the movies and the imdbIds can be found by downloading the dataset from the link above  

### FRONTEND
- **Pages**:  
  - `welcome.html`: The user is prompted to select a movie they have seen, and then press continue or reset their selection  
  - `page2.html`: The user then has 10 options from the cluster of the movie they chose. Selecting three is required to move ahead, and they have three resets until the page resets and takes them back to welcome.html. The assumption is that if someone can not find 3 out of 30 movies they have seen in one genre, they are not necessarily that involved with that genre  
  - `results.html`: After page2.html, the code logs the movies on page 2 that have been on the user's screen that they have not selected. If there are at least 10 movies, they are displayed on results.html for them to watch. If not, the rest is taken from the Excel. The start over button takes them to the beginning  

- The feedback button logs both the time/date and the feedback given in an Excel sheet named `feedback_log.csv` that the code also creates for the first time  

## Project Structure
movie_recommender_app  
│  
├── app.py  
├── .gitignore  
├── requirements.txt  
├── feedback_log.xlsx  
├── movie_cluster_assignments.csv  
│  
├── BackEnd/  
│   ├── dataset.py  
│   ├── create.py  
│   ├── compare.py  
│   ├── manual_kmeans.py  
│   ├── kmeans_elbow_plot.png  
│   └── kmeans_log.csv  
│  
├── static/  
│   ├── style.css  
│   └── script.js  
│  
├── templates/  
    ├── welcome.html  
    ├── page2.html  
    └── results.html 

## Example features include
1) Cluster-aware recommendations
2) scrollable and dynamic UI elements
3) Feedback logging with timestamps
4) Automatic reset if the user can not find three movies from the initial cluster chosen
5) IMDB links embedded in each result, taken from links.csv automatically using the pandas library

## About this project
This was my first project, so it was very simple and served as a personal test to see how much I could learn on my own free time. This project is intended for educational purposes only and is not intended for commercial use.

## Author
Kerem Ege Oktem
Github: [@keremegeoktem](https://github.com/keremegeoktem)

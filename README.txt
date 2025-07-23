----Content-Based Filtering Movie Recommender----

This project is a movie recommendation engine built from scratch using manual KMeans, without scikit-learn or any shortcuts

------ Project Goals -----
1- Learn how KMeans works by manually creating it from scratch
2- Cluster movies based on user ratings from a large dataset (attached in this folder)
3- Use 3 movie inputs from users to recommend movies to them deemed similar by the K Means algorithm.
4- Learn how local storage works in order to store and communicate data between pages
5- Learn frontend basics: how to style a page and how to add individual functional elements

Important Notice:
1- Since manual KMeans takes a lot of time and computing power (that my laptop does not have) I opted to use a faster version using scikit-learn library.
2- The faster code is not inside here since it is not mine, but my manual implementation that works -but takes a really long time- is still present in the project file.
3- The data used in this project is huge, so I will not upload it directly. If anybody wants to use this for any reason, here is the link to the dataset: https://grouplens.org/datasets/movielens/
4- The specific data I am using is called MovieLens 32M. 

----- How it works-----
1- BACKEND
    - Create.py, compare.py, dataset.py, and manual_kmeans.py all load, filter, and then prepare the excel sheet for the backend.
    - Using the ratings.cv as a base, it filtered to active users (200> ratings at least) and popular movies (rated at least 300 times)
    - KMeans then created an elbow plot png (to find the correct K to use) and clusters to detect "similar" movies, based on the ratings that users gave out for all movies they have seen
    - There is also links.csv, which has the imdb id of each title so that python can access them using pandas and build a bridge for each movie
2- FRONTEND
    - app.py is the middle-man, it utilizes the Flask class to communicate from the excel to jscript and html. 
    - In welcome.html, the user is prompted to select a movie they have seen, and then press continue or reset their selection
    - Pressing continue takes them to page2.html, in which they have 10 options now from the cluster of the movie they chose.
    - Selecting 3 is required to move ahead, and they have 3 resets until the page resets and takes them back to welcome.html
    - The assumption is that if someone can not find 3 out of 30 movies they have seen in one genre, they are not necessarily that involved with that genre
    - Finally, once 3 movies are entered and the user presses continue again, the code logs the movies that have been on the user's screen that they have not selected.
    - If there is at least 10 movies, they are displayed on results.html for them to watch.
    - If not, the rest is taken from the excel.
    - Start over button takes them to the beginning
    - The feedback button logs both the time/date and the feedback given in an excel sheet named feedback_log.csv that the code also creates for the first time

This was my first project, so it is very simple in nature and not overly complicated on the frontend side. I want to specialize on backend, so I just created a filler website with minimal elements.
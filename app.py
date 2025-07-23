from flask import Flask, render_template, jsonify, request
import pandas as pd
import random
from datetime import datetime
import os

app = Flask(__name__)

# Load and prepare the data
clusters_df = pd.read_csv("movie_cluster_assignments.csv")
movies_df = pd.read_csv("movies.csv")
links_df = pd.read_csv("BackEnd/links.csv", dtype={"imdbId": str})
links_df["movieId"] = links_df["movieId"].astype(int)
links_df["imdbId"] = links_df["imdbId"].astype(str)

# Ensure consistent data types
movies_df["movieId"] = movies_df["movieId"].astype(int)
clusters_df["MovieId"] = clusters_df["MovieId"].astype(int)

# Build the lookup dictionary for title and genre
movie_lookup = movies_df.set_index("movieId")[["title", "genres"]].to_dict(orient="index")

@app.route("/")
def welcome_page():
    return render_template("welcome.html")

@app.route("/get-random-movies")
def get_random_movies():
    result = []
    for cluster_id in clusters_df['Cluster'].unique():
        cluster_movies = clusters_df[clusters_df['Cluster'] == cluster_id]

        if not cluster_movies.empty:
            random_movie_id = int(random.choice(cluster_movies["MovieId"].tolist()))

            movie_info = movie_lookup.get(random_movie_id, {"title": "Unknown", "genres": "Unknown"})
            result.append({
                "movieId": random_movie_id,
                "title": movie_info["title"],
                "genres": movie_info["genres"]
            })

    return jsonify(result[:3])

#Page 2 Code Starts Here

@app.route("/page2")
def page2():
    return render_template("page2.html")

@app.route("/get-cluster-id/<movie_title>")
def get_cluster_id(movie_title):
    match = movies_df[movies_df["title"] == movie_title]
    movie_id = match.iloc[0]["movieId"]
    cluster_match = clusters_df[clusters_df["MovieId"] == movie_id]
    cluster_id = int(cluster_match.iloc[0]["Cluster"])
    return jsonify({"cluster_id":cluster_id})

@app.route("/get-cluster-movies/<int:cluster_id>")
def get_cluster_movies(cluster_id):
    cluster_movies = clusters_df[clusters_df["Cluster"] == cluster_id]
    movie_ids = cluster_movies["MovieId"].tolist()
    selected_title = request.args.get("exclude_title", "")
    excluded_id = None
    match = movies_df[movies_df["title"] == selected_title]

    if not match.empty:
        excluded_id = int(match.iloc[0]["movieId"])
        if excluded_id in movie_ids:
            movie_ids.remove(excluded_id)
    
    chosen_ids = random.sample(movie_ids, min(10, len(movie_ids)))
    result = []
    for mid in chosen_ids:
        info = movie_lookup.get(mid, {"title": "Unknown", "genres": "Unknown"})
        result.append({
            "movieId": mid,
            "title": info["title"],
            "genres": info["genres"]
        })
    return jsonify(result)
# Page 3 code starts here
@app.route("/results")
def show_results():
    return render_template("results.html")

@app.route("/get-recommendations", methods=["POST"])
def get_recommendations():
    try:
        data = request.get_json()
        selected_Titles = data.get("selectedMovies", [])
        skipped_Titles = data.get("skippedMovies", [])

        #This block will convert the ID of a movie into its name since they are in seperate excels
        selected_ids = movies_df[movies_df["title"].isin(selected_Titles)]["movieId"].tolist()
        skipped_ids = movies_df[movies_df["title"].isin(skipped_Titles)]["movieId"].tolist()

        #This line will get the cluster information from the selected movies
        cluster_ids = clusters_df[clusters_df["MovieId"].isin(selected_ids)]["Cluster"].unique()

        #Every movie that MIGHT get recommended is pulled from this cluster in this line
        candidate_ids = clusters_df[clusters_df["Cluster"].isin(cluster_ids)]["MovieId"].unique().tolist()

        #This removes the movieIds that the user has already seen
        seen_ids = set(selected_ids + skipped_ids)
        unseen_candidates = [mid for mid in candidate_ids if mid not in seen_ids]

        #Final list of recommendations
        recommendations = []

        #if there is less than 10 movies that the user skipped, then take more from the same cluster
        if len(skipped_ids) >= 10:
            final_ids = skipped_ids[:10]
        else:
            needed = 10 - len(skipped_ids)
            top_up_ids = random.sample(unseen_candidates, min(needed, len(unseen_candidates)))
            final_ids = skipped_ids + top_up_ids

        for mid in final_ids:
            info = movie_lookup.get(mid, {"title": "Unknown", "genres": "Unknown"})
            imdb_match = links_df[links_df["movieId"] == mid]
            imdb_id = imdb_match.iloc[0]["imdbId"] if not imdb_match.empty else None
            recommendations.append({
                "movieId": mid,
                "title": info["title"],
                "genres": info["genres"], 
                "imdbId": imdb_id
            })
        
        return jsonify(recommendations)
    
    
    except Exception as e:
        print("Error in /get-recommendations:", e)
        return jsonify({"status": "error", "message": str(e)}), 500

#Shared Across Pages 2 And 3
@app.route("/submit-feedback", methods=["POST"])
def submit_feedback():
    print("🟢 Feedback route hit")
    data = request.json
    feedback = data.get("feedback", "").strip()

    if not feedback:
        print("⚠️ Empty feedback submitted")
        return jsonify({"status": "error", "message": "No feedback provided"}), 400

    filepath = "feedback_log.xlsx"
    entry = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "feedback": feedback
    }

    try:
        if os.path.exists(filepath):
            print("📄 File exists — appending to Excel")
            df = pd.read_excel(filepath)
            df = pd.concat([df, pd.DataFrame([entry])], ignore_index=True)
        else:
            print("🆕 Creating new Excel file")
            df = pd.DataFrame([entry])

        df.to_excel(filepath, index=False)
        print("✅ Feedback saved")
        return jsonify({"status": "success"})
    except Exception as e:
        print(" Error saving feedback:", e)
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
let currentClusterId = null;
window.onload = function () {
    const bodyId = document.body.id;

    if (bodyId === "welcomePage") {
        // Page 1
        setTimeout(() => {
            document.getElementById("welcome").classList.add("shrink");
            document.getElementById("dragSection").style.display = "flex";
            refreshMovies();
        }, 2500);
    }

    else if (bodyId === "page2") {
        // Page 2
        setTimeout(() => {
            document.getElementById("welcome").classList.add("shrink");
            document.getElementById("dragSection").style.display = "flex";
        }, 2500);

        const movieTitle = localStorage.getItem("selectedMovie");
        if (movieTitle) {
            fetch(`/get-cluster-id/${encodeURIComponent(movieTitle)}`)
                .then(response => response.json())
                .then(data => {
                    const clusterId = data.cluster_id;
                    loadClusterMovies(clusterId);
                });
        }
    }

    else if (bodyId === "results") {
        const message = document.getElementById("resultsMessage");

        const siblings = Array.from(document.querySelectorAll(".results-container > *"))
            .filter(el => el !== message);
        siblings.forEach(el => el.classList.add("results-hidden"));

        setTimeout(() => {
            message.classList.add("fade-out");

            setTimeout(() => {
                siblings.forEach(el => {
                    el.classList.remove("results-hidden");
                    el.classList.add("results-visible");
                });
                
                message.remove();
                loadRecommendations();
            }, 2000); // matches fade-out duration
        }, 2500);
    }
};

async function refreshMovies() {
    try {
        const response = await fetch("/get-random-movies");
        const movies = await response.json();

        const movieElements = document.querySelectorAll(".movie");
        movies.forEach((movie, index) => {
            if (movieElements[index]) {
                movieElements[index].textContent = movie.title;
                movieElements[index].setAttribute("draggable", "true");
            }
        });

        setupDrag();
        setupDropZone();
    } catch (error) {
        console.error("Error fetching movies", error);
    }
}

function setupDrag() {
    const movies = document.querySelectorAll(".movie");

    movies.forEach(movie => {
        movie.addEventListener("dragstart", e => {
            e.dataTransfer.setData("text/plain", e.target.textContent);
        });
    });
}

function setupDropZone() {
    const dropZone = document.getElementById("drop-zone");
    const continueBtn = document.getElementById("continueBtn");

    dropZone.addEventListener("dragover", e => {
        e.preventDefault();
        dropZone.style.backgroundColor = "rgba(255, 255, 255, 0.2)";
    });

    dropZone.addEventListener("dragleave", () => {
        dropZone.style.backgroundColor = "rgba(255, 255, 255, 0.1)";
    });

    dropZone.addEventListener("drop", e => {
        e.preventDefault();
        const movieTitle = e.dataTransfer.getData("text/plain");
        dropZone.textContent = `Selected: ${movieTitle}`;
        continueBtn.disabled = false;
        continueBtn.classList.add("active");
        dropZone.style.backgroundColor = "rgba(255, 255, 255, 0.15)";

        document.querySelectorAll(".movie").forEach(m => m.classList.remove("selected"));
        document.querySelectorAll(".movie").forEach(m => {
            if (m.textContent === movieTitle) {
                m.classList.add("selected-movie");
            }
        });
    });
}

function resetSelection() {
    const dropZone = document.getElementById("drop-zone");
    const continueBtn = document.getElementById("continueBtn");

    dropZone.textContent = "Drop movie here";
    dropZone.style.backgroundColor = "rgba(255, 255, 255, 0.1)";
    continueBtn.disabled = true;
    continueBtn.classList.remove("active");

    document.querySelectorAll(".movie").forEach(m => m.classList.remove("selected-movie"));
}

function continuePage() {
    const selectedMovie = document.querySelector(".selected-movie").textContent;
    localStorage.setItem("selectedMovie", selectedMovie);
    window.location.href = "/page2";
}

// PAGE 2 SCRIPTS:

let refreshCount = 0;
const MAX_REFRESHES = 3;
let selectedMovies = new Set();
let skippedMovies = new Set();

async function loadClusterMovies(clusterId){
    currentClusterId = clusterId;
    selectedMovies.clear();

    const response = await fetch(`/get-cluster-movies/${clusterId}`);
    const movies = await response.json();

    const movieElements = document.querySelectorAll(".movie-2");

    movieElements.forEach((m, i) => {
        const movie = movies[i];
        if (m && movie) {
            m.textContent = movie.title;
            m.setAttribute("draggable", "true");
            m.classList.remove("selected-movie");
        } else {
            m.textContent = "";
            m.setAttribute("draggable", "false");
            m.classList.remove("selected-movie");
        }
    });

    movieElements.forEach((m,i) => {
        const movie = movies[i];
        if(m && movie){
            skippedMovies.add(movie.title);
        }
    });

    setupDragPage2();
    setupDropZonePage2();
}

function setupDragPage2(){
    const movies = document.querySelectorAll(".movie-2");

    movies.forEach(movie => {
        movie.addEventListener("dragstart", e => {
            e.dataTransfer.setData("text/plain", e.target.textContent);
        });
    });
}

function handleRefresh(clusterId){
    refreshCount++;
    if(refreshCount >= MAX_REFRESHES){
        window.location.href = "/";
        return;
    }

    loadClusterMovies(clusterId).then(() => {
        selectedMovies.clear();
        document.querySelectorAll(".drop-zone").forEach(zone => {
            const movie = zone.textContent.trim();
            if (movie && movie !== "Drop here") {
                selectedMovies.add(movie);
            }
        });

        if (selectedMovies.size === 3) {
            document.getElementById("continueBtn").disabled = false;
        } else {
            document.getElementById("continueBtn").disabled = true;
        }
    });
}

function setupDropZonePage2(){
    const continueBtn = document.getElementById("continueBtn");
    const dropZones = document.querySelectorAll(".drop-zone");

    dropZones.forEach(dropZone => {
        dropZone.addEventListener("dragover", e => {
            e.preventDefault();
            dropZone.style.backgroundColor = "rgba(255,255,255,0.2)";
        });

        dropZone.addEventListener("dragleave", () => {
            dropZone.style.backgroundColor = "rgba(255,255,255,0.1)";
        });

        dropZone.addEventListener("drop", e => {
            e.preventDefault();
            const movieTitle = e.dataTransfer.getData("text/plain");

            if(!selectedMovies.has(movieTitle) && dropZone.textContent === "Drop here"){
                selectedMovies.add(movieTitle);
                dropZone.textContent = movieTitle;
                dropZone.style.backgroundColor = "rgba(255,255,255,0.15)";

                document.querySelectorAll(".movie-2").forEach(m => {
                    if(m.textContent === movieTitle){
                        m.classList.add("selected-movie");
                    }
                });
            }

            skippedMovies.delete(movieTitle);

            if(selectedMovies.size === 3){
                continueBtn.disabled = false;
                continueBtn.classList.add("active");
            }
        })
    });
}

function resetDropZones(){
    selectedMovies.clear();

    document.querySelectorAll(".drop-zone").forEach(zone => {
        zone.textContent = "Drop here";
        zone.style.backgroundColor = "rgba(255,255,255,0.1)";
    });

    document.querySelectorAll(".movie-2").forEach(m => m.classList.remove("selected-movie"));

    const continueBtn = document.getElementById("continueBtn");
    continueBtn.disabled = true;
    continueBtn.classList.remove("active");
}

function submitSelections(){
    const selected = Array.from(selectedMovies);
    const skipped = Array.from(skippedMovies);
    localStorage.setItem("selectedMovies", JSON.stringify(selected));
    localStorage.setItem("skippedMovies", JSON.stringify(skipped));
    localStorage.setItem("refreshCount", refreshCount);
    window.location.href = "results";
}

function toggleFeedbackPopup() {
    const popup = document.getElementById("feedbackPopup");
    popup.style.display = popup.style.display === "block" ? "none" : "block";
}

function submitFeedback() {
    const feedbackElement = document.getElementById("feedbackText") || document.getElementById("feedbackBox");
    const statusMsg = document.getElementById("feedbackConfirmation") || document.getElementById("feedbackStatus");
    const feedback = feedbackElement.value.trim();

    if (!feedback) {
        statusMsg.textContent = "Please write something before submitting.";
        return;
    }

    fetch("/submit-feedback", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ feedback: feedback })
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === "success") {
            statusMsg.textContent = "Thanks for your feedback!";
            feedbackElement.value = "";
        } else {
            statusMsg.textContent = "There was a problem saving your feedback.";
        }
    })
    .catch(() => {
        statusMsg.textContent = "Could not connect to the server.";
    });
}


//PAGE 3 SCRIPTS

async function loadRecommendations(){
    const selectedMovies = JSON.parse(localStorage.getItem("selectedMovies") || "[]");
    const skippedMovies = JSON.parse(localStorage.getItem("skippedMovies") || "[]");

    try{
        const response = await fetch("/get-recommendations", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                selectedMovies: selectedMovies,
                skippedMovies: skippedMovies
            })
        });

        const recommendations = await response.json();
        const boxes = document.querySelectorAll(".recommendation-grid .movie-display");

        recommendations.forEach((movie, index) => {
            if (boxes[index]) {
                const fullText = `${movie.title} — ${movie.genres}`;
                const imdbUrl = `https://www.imdb.com/title/tt${movie.imdbId}`;
                boxes[index].innerHTML = `
                    <a href="${imdbUrl}" target="_blank" class="scroll-text">
                        ${fullText}
                    </a>`;
            }
        });
    }
    catch (error){
        console.error("Failed to load recommendations:", error);
    }
}
function goAgain() {
    window.location.href = "/";
}
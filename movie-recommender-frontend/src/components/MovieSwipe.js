import React, { useState, useEffect } from "react";
import { motion } from "framer-motion";

export default function MovieSwipe() {
  const [movies, setMovies] = useState([]);
  const [swipeHistory, setSwipeHistory] = useState([]);
  const [swipeMessage, setSwipeMessage] = useState(null);
  const userId = 1;

  const fetchRecommendations = () => {
    fetch(`http://127.0.0.1:8000/recommend/${userId}`)
      .then((res) => res.json())
      .then((data) => {
        if (!data || !Array.isArray(data.recommendations)) {
          console.warn("No valid recommendations returned from backend");
          setMovies([]);
          return;
        }

        const formatted = data.recommendations.map((movie, index) => ({
          id: index + 1,
          title: movie.title || "Untitled",
          genre: movie.genre || "Unknown",
          poster: movie.poster || "https://via.placeholder.com/500x750?text=No+Poster",
          year: movie.year || "N/A",
        }));

        setMovies(formatted);
      })
      .catch((err) => {
        console.error("Error fetching recommendations:", err);
        setMovies([]);
      });
  };

  const fetchSwipeHistory = () => {
    fetch(`http://127.0.0.1:8000/swipe-history?user_id=${userId}`)
      .then((res) => res.json())
      .then((data) => {
        if (!data || !Array.isArray(data.history)) {
          console.warn("No valid swipe history returned");
          return;
        }

        setSwipeHistory(data.history);
      });
  };

  useEffect(() => {
    fetchRecommendations();
    fetchSwipeHistory();
  }, []);

  const handleDragEnd = (event, info, movieId) => {
    let action = null;

    if (info.offset.x > 150) {
      setSwipeMessage("Liked ❤️");
      action = "like";
    } else if (info.offset.x < -150) {
      setSwipeMessage("Disliked ❌");
      action = "dislike";
    } else {
      setSwipeMessage(null);
      return;
    }

    const movie = movies.find((m) => m.id === movieId);
    fetch("http://127.0.0.1:8000/swipe/", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        user_id: userId,
        movie_title: movie.title,
        action,
      }),
    }).then(() => {
      fetchRecommendations();  // Auto-refresh
      fetchSwipeHistory();     // Update swipe history
    });

    setTimeout(() => {
      setSwipeMessage(null);
      setMovies((prev) => prev.filter((m) => m.id !== movieId));
    }, 800);
  };

  return (
    <div className="flex flex-col items-center justify-start min-h-screen overflow-y-auto p-4">
      <h1 className="text-3xl font-bold mb-4">Movie Recommender</h1>

      <div className="relative w-full max-w-md h-[450px]">
        {movies.map((movie) => (
          <motion.div
            key={movie.id}
            drag="x"
            dragConstraints={{ left: 0, right: 0 }}
            onDragEnd={(e, info) => handleDragEnd(e, info, movie.id)}
            whileTap={{ scale: 1.02 }}
            whileDrag={{ rotate: 2 }}
            className="absolute w-full h-[450px] bg-white rounded-3xl shadow-2xl overflow-hidden cursor-grab touch-none"
          >
            <img
              src={movie.poster}
              alt={movie.title}
              className="w-full h-full object-cover pointer-events-none select-none"
              draggable="false"
            />
            <div className="absolute bottom-0 left-0 right-0 bg-gradient-to-t from-black/80 to-transparent text-white p-4">
              <h2 className="text-xl font-bold">{movie.title}</h2>
              <p className="text-sm">{movie.genre} | {movie.year}</p>
            </div>
          </motion.div>
        ))}

        {/* 💬 No Recommendations Message */}
        {movies.length === 0 && (
          <div className="absolute top-1/2 left-1/2 -translate-x-1/2 text-center text-gray-600 font-medium">
            No more recommendations.<br />Try liking more movies or refresh.
          </div>
        )}
      </div>

      {/* 🔄 Refresh Button */}
      <button
        className="mt-5 px-4 py-2 bg-blue-600 text-white rounded-full hover:bg-blue-700 transition"
        onClick={fetchRecommendations}
      >
        🔄 Refresh Recommendations
      </button>

      {swipeMessage && (
        <div className="mt-6 px-6 py-2 bg-white rounded-full shadow-md text-xl font-bold text-center text-blue-600 animate-bounce border border-blue-300">
          {swipeMessage}
        </div>
      )}

      {swipeHistory.length > 0 && (
        <div className="mt-6 w-full max-w-md bg-white rounded-xl shadow-lg p-4">
          <h2 className="text-lg font-bold mb-2 text-center text-blue-700">Swipe History</h2>
          <ul className="space-y-1 text-sm text-gray-700 max-h-48 overflow-y-auto">
            {swipeHistory.map((entry, index) => (
              <li key={index} className="flex justify-between border-b pb-1">
                <span>{entry.movie_title}</span>
                <span className={entry.action === "like" ? "text-green-500" : "text-red-500"}>
                  {entry.action}
                </span>
              </li>
            ))}
          </ul>
        </div>
      )}
      <button
  onClick={() => {
    fetch(`http://127.0.0.1:8000/reset-history/${userId}`, {
      method: "DELETE",
    })
      .then((res) => res.json())
      .then((data) => {
        alert(data.message);
        setSwipeHistory([]);
        setMovies([]);  // Optionally clear movies too
      });
  }}
  className="mt-4 px-4 py-2 bg-red-600 text-white rounded-lg shadow-md hover:bg-red-700"
>
  Reset History
</button>

    </div>
  );
}

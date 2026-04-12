"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from recommender import load_songs, recommend_songs


def main() -> None:
    songs = load_songs("data/songs.csv") 

    # Taste profile: focused late-night coder — low energy, high acousticness, neutral valence
    # Critique note: energy (0.35) and acousticness (0.80) are the two features that most
    # clearly separate "chill lofi" from "intense rock". Rock scores ~0.91 energy / ~0.10
    # acousticness, so it will lose ~1.4 points on energy proximity and ~0.49 on acousticness
    # versus a lofi track — enough spread to rank them very differently even if genre doesn't match.
    # The profile is intentionally NOT locked to one genre so the system can surface a chill
    # jazz or ambient track alongside lofi if the vibe numbers are close.
    user_prefs = {
        "genre": "lofi",
        "mood": "chill",
        "energy": 0.35,
        "valence": 0.60,
        "danceability": 0.55,
        "acousticness": 0.80,
    }

    recommendations = recommend_songs(user_prefs, songs, k=5)

    print("\nTop recommendations:\n")
    for rec in recommendations:
        # You decide the structure of each returned item.
        # A common pattern is: (song, score, explanation)
        song, score, explanation = rec
        print(f"{song['title']} - Score: {score:.2f}")
        print(f"Because: {explanation}")
        print()


if __name__ == "__main__":
    main()

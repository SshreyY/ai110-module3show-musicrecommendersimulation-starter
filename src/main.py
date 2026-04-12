"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

try:
    from recommender import load_songs, recommend_songs
except ModuleNotFoundError:
    from src.recommender import load_songs, recommend_songs


def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"Loaded songs: {len(songs)}")

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

    print("\n" + "=" * 50)
    print("  Top Recommendations")
    print("=" * 50)
    for i, (song, score, explanation) in enumerate(recommendations, start=1):
        print(f"\n#{i}  {song['title']} by {song['artist']}")
        print(f"    Genre: {song['genre']} | Mood: {song['mood']}")
        print(f"    Score: {score:.2f} / 7.5")
        print("    Why:")
        for reason in explanation.split(", "):
            print(f"      - {reason}")
    print("\n" + "=" * 50)


if __name__ == "__main__":
    main()

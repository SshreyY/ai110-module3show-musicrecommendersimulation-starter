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


# --- User Profiles ---

PROFILES = {
    "High-Energy Pop": {
        "genre": "pop",
        "mood": "happy",
        "energy": 0.90,
        "valence": 0.85,
        "danceability": 0.85,
        "acousticness": 0.10,
    },
    "Chill Lofi": {
        # Critique note: energy (0.35) and acousticness (0.80) are the two features
        # that most clearly separate "chill lofi" from "intense rock". Rock scores
        # ~0.91 energy / ~0.10 acousticness, so it will lose ~1.4 pts on energy
        # proximity and ~0.49 on acousticness vs a lofi track — enough spread to
        # rank them very differently even when genre doesn't match.
        "genre": "lofi",
        "mood": "chill",
        "energy": 0.35,
        "valence": 0.60,
        "danceability": 0.55,
        "acousticness": 0.80,
    },
    "Deep Intense Rock": {
        "genre": "rock",
        "mood": "intense",
        "energy": 0.92,
        "valence": 0.40,
        "danceability": 0.60,
        "acousticness": 0.08,
    },
    # Edge case: high energy but explicitly calm/chill mood — the system should
    # surface songs that are physically energetic (gym-style) yet tagged as chill,
    # which barely exist in the catalog. Watch whether energy or mood wins.
    "Conflicted Vibe (high energy + chill mood)": {
        "genre": "ambient",
        "mood": "chill",
        "energy": 0.88,
        "valence": 0.65,
        "danceability": 0.75,
        "acousticness": 0.50,
    },
}


def run_profile(profile_name: str, user_prefs: dict, songs: list) -> None:
    recommendations = recommend_songs(user_prefs, songs, k=5)

    print("\n" + "=" * 54)
    print(f"  Profile: {profile_name}")
    print("=" * 54)
    for i, (song, score, explanation) in enumerate(recommendations, start=1):
        print(f"\n#{i}  {song['title']} by {song['artist']}")
        print(f"    Genre: {song['genre']} | Mood: {song['mood']}")
        print(f"    Score: {score:.2f} / 7.5")
        print("    Why:")
        for reason in explanation.split(", "):
            print(f"      - {reason}")
    print("=" * 54)


def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"Loaded songs: {len(songs)}")

    for profile_name, user_prefs in PROFILES.items():
        run_profile(profile_name, user_prefs, songs)


if __name__ == "__main__":
    main()

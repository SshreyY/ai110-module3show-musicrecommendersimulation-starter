# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name

**VibeFinder 1.0**

---

## 2. Intended Use

VibeFinder 1.0 suggests songs from a small catalog based on a user's stated genre preference, mood preference, and four numeric "vibe" sliders (energy, valence, danceability, and acousticness). It is designed for classroom exploration of how content-based recommender systems work — not for production use. The system assumes the user already knows what they want and can express it in numbers; it makes no attempt to learn from listening history or feedback.

---

## 3. How the Model Works

Imagine you tell a friend: "I want something chill, acoustic, low energy, lofi." Your friend scans their playlist and mentally checks each song against what you said. The closer a song matches your description, the more likely they are to suggest it.

VibeFinder works the same way. Each song in the catalog has a set of labels — genre, mood — and a set of numbers that describe how it sounds (energy, how positive it feels, how danceable it is, how acoustic it is). The user's profile has the same information: a preferred genre, a preferred mood, and target numbers.

For each song, the system computes a score out of 7.5:
- Genre and mood are checked as exact matches. Get the right genre and you earn 2.0 points; right mood earns 1.5 points.
- For the numeric features, the system measures how far the song is from your target and awards points based on closeness. A song that exactly matches your energy target earns the full 1.5 points; one that's far away earns close to zero.

All the points are added up, songs are sorted from highest to lowest, and the top results are returned.

---

## 4. Data

The catalog contains 18 songs stored in `data/songs.csv`. The original starter dataset had 10 songs covering pop, lofi, rock, synthwave, jazz, ambient, and indie pop. I added 8 more songs to cover genres that were missing: folk, hip-hop, r&b, classical, country, metal, reggae, and electronic.

Mood labels represented: happy, chill, intense, relaxed, focused, moody, nostalgic, confident, romantic, melancholic, angry, energetic.

Despite the expansion, the dataset skews toward Western popular music styles. There is nothing representing K-pop, Afrobeats, Latin, or classical Indian music. Most songs were assigned numeric attributes by hand based on my perception of how those genres typically sound, which means the numbers reflect one person's taste and cultural frame of reference. A user whose idea of "high energy" is a salsa track would likely get poor results.

---

## 5. Strengths

The system works best for users who have a clear, consistent taste profile — someone who knows they want lofi and chill and low energy will get excellent results. Library Rain scored 7.44/7.5 for the Chill Lofi profile, and every song in the top 3 genuinely felt appropriate for that vibe.

The scoring logic is fully transparent: every point contribution is printed alongside the recommendation so the user can see exactly why a song ranked where it did. This is a strength real-world systems often lack — Spotify does not explain why it put a song in your Discover Weekly.

The proximity scoring (1 − |difference|) also allows the system to surface cross-genre discoveries. Spacewalk Thoughts (ambient) appeared in the Chill Lofi top 5 because its audio numbers were close enough to the lofi profile, even without a genre match. A pure genre-filter system would have missed it.

---

## 6. Limitations and Bias

**Categorical weight trap.** Genre (weight 2.0) and mood (weight 1.5) together can contribute up to 3.5 out of 7.5 points — nearly half the total score — through a binary on/off match. This means a song that perfectly matches your genre and mood label but sounds nothing like what you actually want (wrong energy, wrong acousticness) can still outscore a song that matches your audio preferences nearly perfectly but belongs to a slightly different genre. The Conflicted Vibe experiment exposed this directly: Spacewalk Thoughts (energy 0.28) won over songs with energy 0.88 simply because its genre and mood labels matched.

**Small catalog bias.** With only 18 songs and 14 distinct genres, several genres have exactly one representative. A user who wants rock will always see Storm Runner at #1, regardless of how well it actually matches their numeric preferences. There is no competition within the genre to surface a better fit.

**Cold-start problem.** The system has no default profile and cannot learn from behavior. A new user who does not know what "valence 0.6" means will fill in arbitrary numbers and get arbitrary results. Real recommenders solve this by observing a few plays before asking for explicit preferences.

**No diversity enforcement.** The ranking rule always picks the top N closest songs, which means a user with a popular-genre preference can get five nearly identical songs at the top. There is no mechanism to spread results across moods, tempos, or sub-genres.

**Hand-coded attributes reflect one perspective.** All numeric values in songs.csv were assigned by me based on how I perceive those genres. Someone from a different cultural background might rate the same songs very differently, and those users would get worse recommendations.

---

## 7. Evaluation

I tested four distinct user profiles:

- **High-Energy Pop** (genre=pop, mood=happy, energy=0.90): Sunrise City ranked #1 as expected. The surprise was Rooftop Lights landing #2 despite being "indie pop" — its happy mood match plus close energy was enough to beat Gym Hero's genre match without a mood match. This showed mood weight (1.5) can compensate for a genre miss in the right conditions.

- **Chill Lofi** (genre=lofi, mood=chill, energy=0.35): Library Rain at 7.44/7.5 — the closest thing to a perfect match in the catalog. Results felt genuinely right. The only mild surprise was Focus Flow (#3) despite a mood mismatch (focused ≠ chill), which raised a question about whether "focused" and "chill" should really be treated as completely different.

- **Deep Intense Rock** (genre=rock, mood=intense, energy=0.92): Storm Runner locked #1 automatically. This exposed the small catalog bias — with only one rock song, the system has no choice but to recommend it first regardless of numeric fit.

- **Conflicted Vibe / edge case** (genre=ambient, mood=chill, energy=0.88): The clearest bias signal. Spacewalk Thoughts (energy 0.28) won over genuinely high-energy songs because genre+mood labels outweighed a 0.60 energy gap. A real recommender would not recommend a soft ambient track to someone who asked for high-energy music.

I also ran a weight shift experiment (genre 1.0, energy 3.0) and observed that Neon Pulse entered the top 3 for the Conflicted Vibe profile with a perfect energy score, confirming the system responds predictably to weight changes. Categorical lock-in was reduced but not eliminated.

---

## 8. Future Work

- **Soft genre similarity:** Instead of a binary genre match, use a genre similarity matrix (e.g., lofi and ambient are closer than lofi and metal) so cross-genre discoveries are rewarded proportionally.
- **Minimum numeric thresholds:** Require that energy proximity clears a minimum bar before categorical bonuses are added — this would fix the Conflicted Vibe case where a mismatched song wins on labels alone.
- **Catalog diversity enforcement:** After scoring, apply a diversity pass that ensures the top 5 results span at least 3 different moods or genres, preventing five nearly identical songs from dominating the list.
- **Implicit feedback loop:** Track which recommendations the user skips or replays and adjust weights over time, moving from a static profile to a learned one.
- **Richer dataset:** Expand to 100+ songs with more balanced genre and mood representation, including non-Western music styles, and use standardized audio features from an API rather than hand-coded values.

---

## 9. Personal Reflection

Building this made me realize how much of a recommender's behavior is determined before any user ever touches it — by the weights you choose, the features you include, and the data you collect. I assumed genre would be a reasonable anchor for recommendations, but the Conflicted Vibe experiment showed that anchoring too hard on a label can completely override what the user actually described in numbers. The system was technically doing what I told it to do; the problem was that I told it the wrong thing.

It also changed how I think about Spotify and similar apps. When Discover Weekly surfaces a song I love, it's not magic — it's a much larger version of the same weighted proximity math, trained on millions of users instead of one hand-coded profile. But it still has the same fundamental tensions: do you trust the label, or the audio signal? Do you reward familiarity, or push for discovery? Those are design choices that reflect values, not just math.

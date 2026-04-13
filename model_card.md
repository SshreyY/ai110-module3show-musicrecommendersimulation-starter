# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name

**VibeFinder 1.0**

---

## 2. Intended Use and Non-Intended Use

This is a learning tool. It is meant to show how a content-based recommender works by letting you see how weights, labels, and proximity scores combine to rank songs. It is good for classroom demos and for experimenting with what happens when you change a weight.

It is not for real music discovery. 18 songs is not a catalog. The numbers were hand-coded by one person based on one cultural frame of reference. Do not use this to make actual recommendations to real users and do not treat it as a model for how Spotify or any production system actually works.

---

## 3. How the Model Works

Imagine you tell a friend: "I want something chill, acoustic, low energy, lofi." Your friend scans their playlist and mentally checks each song against what you said. The closer a song matches your description, the more likely they are to suggest it.

VibeFinder works the same way. Each song has labels (genre and mood) and a set of numbers that describe how it sounds: energy, how positive it feels, how danceable it is, how acoustic it is. The user's profile has the same information: a preferred genre, a preferred mood, and target numbers.

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

The system works best when the user has a clear consistent taste. Someone who wants lofi, chill, and low energy will get good results. Library Rain scored 7.44/7.5 for the Chill Lofi profile and all three top results felt like the right picks.

Every point contribution is printed next to each recommendation so you can see exactly why a song ranked where it did. Spotify does not do that. You have no idea why a song ended up in your Discover Weekly.

The proximity math also lets the system find songs outside the user's genre if the audio numbers are close enough. Spacewalk Thoughts (ambient) showed up in the Chill Lofi top 5 because its energy and acousticness were close to the lofi profile even though the genre did not match. A system that only filtered by genre would have skipped it.

---

## 6. Limitations and Bias

**Categorical weight trap.** Genre (weight 2.0) and mood (weight 1.5) together are 3.5 out of 7.5 points, almost half the total. A song can match your genre and mood labels but sound nothing like what you want and still win. The Conflicted Vibe experiment showed this clearly. Spacewalk Thoughts (energy 0.28) beat genuinely high-energy songs because its labels matched even though the audio was completely off.

**Small catalog bias.** With 18 songs across 14 genres, some genres have only one song. A user who wants rock will always get Storm Runner at #1 no matter what their numeric preferences are because there is nothing else to compete with it.

**Cold-start problem.** The system has no default profile and cannot learn from behavior. A new user who does not know what "valence 0.6" means will fill in arbitrary numbers and get arbitrary results. Real recommenders solve this by observing a few plays before asking for explicit preferences.

**No diversity enforcement.** The ranking rule always picks the top N closest songs, which means a user with a popular-genre preference can get five nearly identical songs at the top. There is no mechanism to spread results across moods, tempos, or sub-genres.

**Hand-coded attributes reflect one perspective.** All numeric values in songs.csv were assigned by me based on how I perceive those genres. Someone from a different cultural background might rate the same songs very differently, and those users would get worse recommendations.

---

## 7. Evaluation

I tested four distinct user profiles:

- **High-Energy Pop** (genre=pop, mood=happy, energy=0.90): Sunrise City ranked #1 as expected. The surprise was Rooftop Lights landing #2 as an indie pop track. Its happy mood match plus close energy was enough to beat Gym Hero even though Gym Hero had the genre match. That showed mood weight (1.5) can make up for a genre miss.

- **Chill Lofi** (genre=lofi, mood=chill, energy=0.35): Library Rain scored 7.44/7.5. Results felt right. The only unexpected one was Focus Flow at #3 despite its mood being "focused" not "chill." It got there on genre plus numeric proximity, which made me wonder if focused and chill should really score the same as a miss.

- **Deep Intense Rock** (genre=rock, mood=intense, energy=0.92): Storm Runner took #1 automatically. There is only one rock song in the catalog so the system has no choice. The numeric fit does not matter here.

- **Conflicted Vibe / edge case** (genre=ambient, mood=chill, energy=0.88): Spacewalk Thoughts (energy 0.28) won even though the user wanted high energy. Genre and mood gave it 3.5 points upfront and the energy gap could not overcome that. A real recommender would not give a soft ambient track to someone who asked for high energy.

I also ran a weight shift experiment (genre 1.0, energy 3.0) and observed that Neon Pulse entered the top 3 for the Conflicted Vibe profile with a perfect energy score, confirming the system responds predictably to weight changes. Categorical lock-in was reduced but not eliminated.

---

## 8. Future Work

- **Soft genre similarity:** Instead of a binary genre match, use a similarity matrix. Lofi and ambient would score something like 0.8 instead of 0. Lofi and metal would stay near 0. That would fix the Conflicted Vibe case where a song wins on labels even though the audio is completely wrong.
- **Minimum energy threshold:** A song should not be able to win a high-energy query purely on label points. Add a floor so that if your energy is too far off, the label bonus does not count.
- **Bigger catalog:** 18 songs is not enough to test anything real. 100 or more songs with actual audio features from an API instead of numbers I made up would make results much more meaningful.
- **Feedback loop:** Let the system track what the user skips or replays and adjust over time. Right now it gives the same answer forever with no way to correct itself.

---

## 9. Personal Reflection

The biggest thing I learned was from the Conflicted Vibe profile. I set energy to 0.88 but genre to ambient and mood to chill, basically contradicting myself. I expected weird results. What I did not expect was that Spacewalk Thoughts with an energy of 0.28 would beat genuinely high energy songs just because its genre and mood labels matched. The system did exactly what I told it to do. The problem was that I told it the wrong thing. That is when it clicked for me that bias in a system is not always a bug. Sometimes it is just the design you chose.

Using Claude to help build this was useful but I had to check everything myself. Claude was good at explaining why something happened in terms of the math but it could not run the code so I verified every output in the terminal before writing anything down. It was more like a thinking partner than a source of truth.

What surprised me most was how real the results felt even though the algorithm is just subtraction and multiplication. When Library Rain scored 7.44 out of 7.5 for the Chill Lofi profile it felt like a genuinely good pick, not like math. I did not expect something that simple to feel that intentional.

If I kept going I would fix the genre binary first. Instead of a song getting 0 or 2 points I would make lofi and ambient score something like 0.8 since they are close but not the same genre. That one change would fix the Conflicted Vibe problem. After that I would expand the catalog to 100 or more songs using real audio features from an API instead of numbers I made up.

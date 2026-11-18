# Reusable prompt: product intro video

Paste the prompt below into Claude Code, opened in the project you want the video for.
Fill in the few `[BRACKETS]`. Anything you leave out, Claude works out from the project.

---

Use this project as context. Read the source, README and CLAUDE.md to learn what the product does, who it is for, and its look and feel (colors, fonts, components). Also follow the conventions in https://github.com/jperezdelcerro-qontigo/claude-config.

Make a [30-45] second product intro video for [PRODUCT URL, or "the app in this folder"].

Scenes (adapt the details to what this product actually does):
* Scene 1: Text animation hook. A question or pain point the audience relates to. [Optional: exact text]
* Scene 2: Show the old, painful way of solving this problem. Use a browser window or app mockup. Keep it simple and recognizable, with 2-3 concrete frustrations.
* Scene 3: Introduce the product. Show the core action a new user takes first, using the real UI.
* Scene 4: Show the product working. A loading or processing state, then the key output appearing. The user performs the main action, with a signature animation.
* Scene 5: Show the result. A confirmation screen with the details that make the outcome tangible.
* Scene 6: Show where the result goes (e.g. Teams, email, calendar), real-life usage of the outcome, and a timeline of next steps.
* Scene 7: Text animation closing. Product name plus a three-word tagline.

Voiceover ([TONE, e.g. upbeat, friendly]): 5 short lines, one breath each (8-15 words), covering: the hook, a welcome with the value proposition, three benefit phrases, the timing or next step, and a call to action. [Optional: exact lines]

Use the look and feel of the product for all UI components. Colors, fonts, and style must match it. If the site isn't reachable, take them from the project's CSS.
Keep transitions smooth and fast-paced throughout.

Keep `video/SCRIPT.md` as the editable written script of the video (scenes, timing, voiceover) and update it with every change.

---

## Notes

- 7 scenes in 30-45 s is about 4-6 s each. Merge scenes if you need more breathing room.
- Scene 2 works best with pain points your audience already knows.
- If the product isn't public, describe its style (hex colors, font names, mood) in the prompt.
- Optional exact texts: add them in quotes next to the scene or voiceover line you want to control.

## Example: skillsMatch (original brief)

Same prompt, with the brackets filled in:

* Product: https://pages.simhub.simcorp.com/JOSP/learning-match/
* Hook: "Want to learn a new skill, but don't know who to ask?"
* Old way: a coworker scrolls a long company directory and an endless Teams chat, types "does anyone know how to...?" and gets no replies.
* Core action: open the app, fill in the skills you can teach, pick what you want to learn in Browse.
* Working: "Finding your match..." loading, colleague cards slide in, "Propose a swap" in My swaps, a matching animation links two profiles.
* Result: "It's a match!" with two people side by side, the skill each teaches the other, and a weekly 1-hour slot added to the calendar.
* Where it goes: notification in Teams and email, the two colleagues meeting and swapping roles, timeline Kick off, 8 weeks of sessions, Showcase in Week 8.
* Closing: "skillsMatch. Learn. Teach. Grow."
* Voiceover (upbeat, friendly):
  1. "What if you could learn the skills you've always wanted... from someone right here in our office?"
  2. "Welcome to skillsMatch, where you teach what you know and learn what you need."
  3. "One hour a week. Two-way learning. Real growth."
  4. "Eight weeks, starting this October. Kick off is next week."
  5. "Find your match. Grow together."

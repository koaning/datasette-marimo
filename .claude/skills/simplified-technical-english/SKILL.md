---
name: simplified-technical-english
description: >-
  Write or revise documentation in Simplified Technical English (ASD-STE100), a
  controlled-language standard for clear, unambiguous technical writing. Use when
  the user asks to simplify, tighten, or review docs (README, guides, comments,
  API docs) for clarity, or names "STE" / "Simplified Technical English" / "plain
  technical English". Applies the STE writing rules and reports what changed.
---

# Simplified Technical English (STE)

Simplified Technical English (ASD-STE100) is a controlled language for technical
documentation. It exists to make text easy to understand for every reader,
including non-native speakers and machine translators, by removing ambiguity and
needless variation.

Apply these rules when you write new documentation or revise existing text.

## Core writing rules

**Sentences**
- Keep procedural (instruction) sentences to 20 words or fewer.
- Keep descriptive (explanatory) sentences to 25 words or fewer.
- Write one instruction per sentence. Put each separate step in its own sentence.
- Start an instruction with the verb (the command). Example: "Run the tests."

**Voice and tense**
- Use the active voice. Do not use the passive voice.
  - Not: "The database is downloaded by the plugin."
  - Use: "The plugin downloads the database."
- Use the simple present tense where you can.

**Words**
- Use one word for one meaning, and one meaning for one word. Do not use a second
  word for the same idea.
- Use approved, common words. Replace difficult words with simple ones:
  - "utilize" → "use", "in order to" → "to", "prior to" → "before",
    "additional" → "more", "leverage" → "use", "commence" → "start".
- Keep technical terms and proper names (for example: Datasette, SQLite, CSV,
  JSON, PyPI, uv). Consistent technical terms are correct STE.
- Do not use slang, idioms, or jargon that is not necessary.

**Articles and grammar**
- Keep the articles "a", "an", and "the". Do not drop them to save space.
- Do not make long noun clusters. Use three words maximum in a row of nouns.
  Break longer clusters with prepositions ("the row limit for the CSV export").

**Structure**
- Keep paragraphs short: six sentences maximum.
- Use a vertical (bulleted or numbered) list for a sequence of steps or a set of
  related items. Numbered lists are for steps in order.
- Put the condition before the action. Example: "If the database is immutable,
  the plugin shows the download link."

## How to apply this skill

1. Read the target text once for meaning. Do not change what it says, only how it
   says it.
2. Revise sentence by sentence against the rules above. Split long sentences.
   Change passive to active. Replace difficult words. Remove repeated ideas.
3. Keep every fact, command, URL, and code block exactly correct. STE clarifies
   language; it must not change technical meaning.
4. Keep the document's existing structure (headings, code fences, tables) unless
   a change makes it clearer.
5. After the revision, give the user a short report: list the main rule types you
   applied (for example: "shortened 4 long sentences, removed passive voice in 3
   places, replaced 5 difficult words"). Note anything you left unchanged on
   purpose, such as technical terms.

## What NOT to change
- Code, commands, URLs, file paths, and configuration keys.
- Product and technology names.
- The technical accuracy of any statement.

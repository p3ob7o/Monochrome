#!/usr/bin/env python3
"""
Zinsser Agent

Reviews markdown drafts through William Zinsser's On Writing Well principles
and creates GitHub issues for feedback. Runs only once per draft.
"""

import json
import os
import subprocess
import sys
from pathlib import Path

import anthropic


ZINSSER_PROMPT = """You are a non-interactive editing agent for Monochrome.blog. You take a blog-post draft as input, analyze it through William Zinsser's On Writing Well principles (clarity, simplicity, humanity, unity, and relentless cutting), and return feedback only.

Context assumptions (always true):
- The draft is a blog post for Monochrome.blog.
- The audience is existing followers: mostly photographers or people passionate about photography.
- Readers may be technically competent, but the writing should avoid tech jargon and "gear-speak" unless essential.
- Draft length varies; your default bias is to shorten wherever meaning is not lost, and conserve where cutting would reduce meaning.
- You must preserve meaning, intent, and the author's original tone of voice at all costs.

Your role:
- You do not ask questions.
- You do not rewrite, rephrase, or provide corrected sentences/paragraphs.
- You provide feedback only, one point at a time.
- You may be ruthless about clutter, vagueness, self-indulgence, and weak structure, but never at the expense of meaning, intent, or tone.
- Your notes are addressed to the author (the post writer).

Operating principles (Zinsser-style):

1. Clarity above all
   - Identify any sentence/paragraph whose meaning isn't instantly clear to an attentive reader.
   - Flag ambiguity, mushy abstractions, and imprecise claims.
   - Prefer the concrete over the general; call out where specifics would sharpen meaning.

2. Strip the clutter (without changing meaning)
   - Hunt for: filler, throat-clearing, clichés, inflated phrasing, needless qualifiers, redundant pairs, and bureaucratic language.
   - Point out where a phrase can be cut because it adds no information or voice.
   - Treat jargon as clutter unless it is essential to the point.

3. Enforce unity
   - Identify the controlling idea (what the post is really about) and test every paragraph against it.
   - Flag detours, tangents, and "interesting but not this post" material.
   - Call out sections where the post feels like two posts stitched together.

4. Respect voice; avoid performance
   - Preserve the author's tone and cadence.
   - Flag moments that feel like posturing, apology, over-explaining, or writing to impress.
   - Encourage plainspoken confidence: say what you mean, directly.

5. Structure for reader attention
   - Evaluate the lead: does it earn attention quickly, or does it warm up too long?
   - Check progression: each paragraph should move the reader forward (claim → support → implication).
   - Flag weak transitions, repetition, and endings that drift or fade.

6. Prefer the particular
   - Identify where selective, vivid details would clarify or persuade.
   - Flag places where the draft lists facts/ideas without showing why they matter.

Safety rails:
- Never recommend changes that alter the author's meaning, intent, or voice.
- If cutting risks meaning loss, recommend tightening by removing only redundancies or by reorganizing instead.

Return your response as a JSON array of feedback notes. Each note should follow this structure:
[
    {{
        "title": "<2-6 words capturing the issue>",
        "anchor": "<short excerpt from draft, max ~25 words, to locate the issue>",
        "why_it_matters": "<1-3 sentences, reader-focused explanation>",
        "action": "<what to change, cut, move, or clarify - without proposing exact sentences>",
        "principle": "<one of: Clarity | Clutter | Unity | Voice | Structure | Particulars>"
    }}
]

Provide 3-7 feedback notes, ordered by impact (highest-impact first). The highest-impact issues are usually: unclear controlling idea, cluttered lead, or structural drift.

Here is the draft to review:

---
{draft_content}
---

Respond with only the JSON array, no additional text."""


def read_draft(filepath: str) -> str:
    """Read the markdown draft file."""
    with open(filepath, "r", encoding="utf-8") as f:
        return f.read()


def has_already_reviewed(filename: str) -> bool:
    """Check if Zinsser has already reviewed this file."""
    result = subprocess.run(
        [
            "gh", "issue", "list",
            "--label", "zinsser",
            "--label", filename,
            "--state", "all",  # Check both open and closed
            "--json", "number",
        ],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        return False

    issues = json.loads(result.stdout)
    return len(issues) > 0


def get_zinsser_review(draft_content: str) -> list[dict]:
    """Send draft to Claude API and get Zinsser-style feedback."""
    client = anthropic.Anthropic()

    message = client.messages.create(
        model="claude-opus-4-20250514",
        max_tokens=3000,
        messages=[
            {
                "role": "user",
                "content": ZINSSER_PROMPT.format(draft_content=draft_content)
            }
        ]
    )

    response_text = message.content[0].text

    # Parse JSON response
    try:
        return json.loads(response_text)
    except json.JSONDecodeError:
        # Try to extract JSON array from the response
        start = response_text.find("[")
        end = response_text.rfind("]") + 1
        if start != -1 and end > start:
            return json.loads(response_text[start:end])
        raise ValueError(f"Could not parse JSON from response: {response_text}")


def create_issue(title: str, body: str, labels: list[str]) -> None:
    """Create a GitHub issue using gh CLI."""
    cmd = [
        "gh", "issue", "create",
        "--title", title,
        "--body", body,
    ]
    for label in labels:
        cmd.extend(["--label", label])

    subprocess.run(cmd, check=True)


def ensure_labels_exist(labels: list[str]) -> None:
    """Ensure all required labels exist in the repository."""
    for label in labels:
        subprocess.run(
            ["gh", "label", "create", label, "--force"],
            capture_output=True
        )


def create_feedback_issue(filename: str, note: dict) -> None:
    """Create a single Zinsser feedback issue."""
    title = f"[Zinsser] {filename}: {note['title']}"

    body = f"""## Principle: {note['principle']}

### Anchor
> {note['anchor']}

### Why It Matters
{note['why_it_matters']}

### Action
{note['action']}
"""

    labels = ["zinsser", "feedback", filename, note["principle"].lower()]
    ensure_labels_exist(labels)
    create_issue(title, body, labels)
    print(f"Created feedback issue: {title}")


def main():
    if len(sys.argv) != 2:
        print("Usage: python zinsser.py <path-to-draft.md>")
        sys.exit(1)

    filepath = sys.argv[1]
    filename = Path(filepath).name

    if not os.path.exists(filepath):
        print(f"Error: File not found: {filepath}")
        sys.exit(1)

    # Check if already reviewed (one pass only)
    if has_already_reviewed(filename):
        print(f"Zinsser has already reviewed {filename}. Skipping (one pass only).")
        sys.exit(0)

    print(f"Reading draft: {filepath}")
    draft_content = read_draft(filepath)

    print("Sending to Claude for Zinsser review...")
    notes = get_zinsser_review(draft_content)

    print(f"Received {len(notes)} feedback notes")

    # Create feedback issues
    for note in notes:
        create_feedback_issue(filename, note)

    print("Zinsser review complete!")


if __name__ == "__main__":
    main()

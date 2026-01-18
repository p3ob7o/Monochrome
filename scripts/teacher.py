#!/usr/bin/env python3
"""
Teacher Agent

Reviews markdown drafts as an AP English teacher and creates GitHub issues
for grades and feedback.
"""

import json
import os
import subprocess
import sys
from pathlib import Path

import anthropic


REVIEW_PROMPT = """You are an AP English teacher grading a student's writing draft.
Review this draft and provide a grade and detailed feedback.

Grade on a 0-100 scale using these criteria:
- Thesis clarity and strength (20 points)
- Organization and structure (20 points)
- Evidence and support (20 points)
- Analysis and critical thinking (20 points)
- Language, style, and mechanics (20 points)

Return your response as JSON with this exact structure:
{{
    "grade": <number 0-100>,
    "summary": "<2-3 sentence overall assessment>",
    "breakdown": {{
        "thesis": {{"score": <0-20>, "comment": "<brief comment>"}},
        "organization": {{"score": <0-20>, "comment": "<brief comment>"}},
        "evidence": {{"score": <0-20>, "comment": "<brief comment>"}},
        "analysis": {{"score": <0-20>, "comment": "<brief comment>"}},
        "language": {{"score": <0-20>, "comment": "<brief comment>"}}
    }},
    "feedback": [
        {{
            "title": "<brief 5-10 word description>",
            "category": "<thesis|organization|evidence|analysis|language>",
            "issue": "<specific problem identified>",
            "suggestion": "<actionable improvement recommendation>",
            "example": "<optional: example from the text or suggested revision>"
        }}
    ]
}}

Provide 3-5 feedback items, each focused on a single, specific, actionable improvement.
Be constructive but honest. If the writing is strong, focus on refinements rather than major issues.

Here is the draft to review:

---
{draft_content}
---

Respond with only the JSON, no additional text."""


def read_draft(filepath: str) -> str:
    """Read the markdown draft file."""
    with open(filepath, "r", encoding="utf-8") as f:
        return f.read()


def get_review(draft_content: str) -> dict:
    """Send draft to Claude API and get structured review."""
    client = anthropic.Anthropic()

    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=2000,
        messages=[
            {
                "role": "user",
                "content": REVIEW_PROMPT.format(draft_content=draft_content)
            }
        ]
    )

    response_text = message.content[0].text

    # Parse JSON response
    try:
        return json.loads(response_text)
    except json.JSONDecodeError:
        # Try to extract JSON from the response if it has extra text
        start = response_text.find("{")
        end = response_text.rfind("}") + 1
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
        # Try to create label, ignore if it already exists
        subprocess.run(
            ["gh", "label", "create", label, "--force"],
            capture_output=True
        )


def create_grade_issue(filename: str, review: dict) -> None:
    """Create the grade issue with overall assessment."""
    grade = review["grade"]
    summary = review["summary"]
    breakdown = review["breakdown"]

    title = f"[Teacher] {filename}: {grade}/100"

    body = f"""## Grade: {grade}/100

### Summary
{summary}

### Breakdown

| Category | Score | Comment |
|----------|-------|---------|
| Thesis | {breakdown['thesis']['score']}/20 | {breakdown['thesis']['comment']} |
| Organization | {breakdown['organization']['score']}/20 | {breakdown['organization']['comment']} |
| Evidence | {breakdown['evidence']['score']}/20 | {breakdown['evidence']['comment']} |
| Analysis | {breakdown['analysis']['score']}/20 | {breakdown['analysis']['comment']} |
| Language | {breakdown['language']['score']}/20 | {breakdown['language']['comment']} |
"""

    labels = ["teacher", "grade", filename]
    ensure_labels_exist(labels)
    create_issue(title, body, labels)
    print(f"Created grade issue: {title}")


def create_feedback_issues(filename: str, review: dict) -> None:
    """Create individual feedback issues for each improvement point."""
    for item in review["feedback"]:
        title = f"[Teacher] {filename}: {item['title']}"

        body = f"""## Category: {item['category'].title()}

### Issue
{item['issue']}

### Suggestion
{item['suggestion']}
"""
        if item.get("example"):
            body += f"""
### Example
{item['example']}
"""

        labels = ["teacher", "feedback", filename, item["category"]]
        ensure_labels_exist(labels)
        create_issue(title, body, labels)
        print(f"Created feedback issue: {title}")


def main():
    if len(sys.argv) != 2:
        print("Usage: python teacher.py <path-to-draft.md>")
        sys.exit(1)

    filepath = sys.argv[1]
    filename = Path(filepath).name

    if not os.path.exists(filepath):
        print(f"Error: File not found: {filepath}")
        sys.exit(1)

    print(f"Reading draft: {filepath}")
    draft_content = read_draft(filepath)

    print("Sending to Claude for review...")
    review = get_review(draft_content)

    grade = review["grade"]
    print(f"Grade received: {grade}/100")

    # Always create grade issue
    create_grade_issue(filename, review)

    # Create feedback issues only if grade < 85
    if grade < 85:
        print(f"Grade below 85, creating {len(review['feedback'])} feedback issues...")
        create_feedback_issues(filename, review)
    else:
        print("Grade 85 or above, skipping individual feedback issues.")

    print("Review complete!")


if __name__ == "__main__":
    main()

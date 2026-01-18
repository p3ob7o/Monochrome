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
        model="claude-opus-4-20250514",
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


def find_existing_grade_issue(filename: str) -> int | None:
    """Find existing grade issue for a file by labels."""
    result = subprocess.run(
        [
            "gh", "issue", "list",
            "--label", "teacher",
            "--label", "grade",
            "--label", filename,
            "--state", "open",
            "--json", "number",
        ],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        return None

    issues = json.loads(result.stdout)
    if issues:
        return issues[0]["number"]
    return None


def find_existing_feedback_issues(filename: str) -> list[dict]:
    """Find existing feedback issues for a file."""
    result = subprocess.run(
        [
            "gh", "issue", "list",
            "--label", "teacher",
            "--label", "feedback",
            "--label", filename,
            "--state", "open",
            "--json", "number,title,body",
        ],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        return []

    return json.loads(result.stdout)


def update_issue_title(issue_number: int, new_title: str) -> None:
    """Update an issue's title."""
    subprocess.run(
        ["gh", "issue", "edit", str(issue_number), "--title", new_title],
        check=True,
    )


def add_comment_to_issue(issue_number: int, body: str) -> None:
    """Add a comment to an existing issue."""
    subprocess.run(
        ["gh", "issue", "comment", str(issue_number), "--body", body],
        check=True,
    )


def add_label_to_issue(issue_number: int, label: str) -> None:
    """Add a label to an existing issue."""
    ensure_labels_exist([label])
    subprocess.run(
        ["gh", "issue", "edit", str(issue_number), "--add-label", label],
        check=True,
    )


COMPARE_FEEDBACK_PROMPT = """Given a new feedback item and a list of existing feedback issues, determine:
1. Is this feedback essentially the same as an existing issue? → "duplicate"
2. Is this feedback related to (but different from) an existing issue? → "related" + issue number
3. Is this feedback entirely new? → "new"

New feedback:
- Title: {title}
- Category: {category}
- Issue: {issue}
- Suggestion: {suggestion}

Existing issues:
{existing_issues}

Respond with ONLY JSON, no other text: {{"action": "duplicate" | "related" | "new", "related_issue": <number or null>}}"""


def compare_feedback(
    new_feedback: dict, existing_issues: list[dict]
) -> tuple[str, int | None]:
    """Use Claude to compare new feedback against existing issues."""
    # Format existing issues for the prompt
    existing_str = ""
    for issue in existing_issues:
        existing_str += f"\n- Issue #{issue['number']}: {issue['title']}\n  Body: {issue['body'][:500]}...\n"

    client = anthropic.Anthropic()
    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=200,
        messages=[
            {
                "role": "user",
                "content": COMPARE_FEEDBACK_PROMPT.format(
                    title=new_feedback["title"],
                    category=new_feedback["category"],
                    issue=new_feedback["issue"],
                    suggestion=new_feedback["suggestion"],
                    existing_issues=existing_str,
                ),
            }
        ],
    )

    response_text = message.content[0].text

    try:
        result = json.loads(response_text)
        return (result["action"], result.get("related_issue"))
    except (json.JSONDecodeError, KeyError):
        # Default to "new" if we can't parse the response
        print(f"Warning: Could not parse comparison response, treating as new")
        return ("new", None)


def format_grade_body(review: dict) -> str:
    """Format the grade issue body."""
    grade = review["grade"]
    summary = review["summary"]
    breakdown = review["breakdown"]

    return f"""## Grade: {grade}/100

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


def create_grade_issue(filename: str, review: dict) -> None:
    """Create a new grade issue."""
    grade = review["grade"]
    title = f"[Teacher] {filename}: {grade}/100"
    body = format_grade_body(review)

    labels = ["teacher", "grade", filename]
    if grade >= 90:
        labels.append("zinsser-ready")
    ensure_labels_exist(labels)
    create_issue(title, body, labels)
    print(f"Created grade issue: {title}")


def handle_grade_issue(filename: str, review: dict) -> None:
    """Handle grade issue - update existing or create new."""
    existing_issue = find_existing_grade_issue(filename)
    grade = review["grade"]

    if existing_issue:
        # Update existing issue
        new_title = f"[Teacher] {filename}: {grade}/100"
        body = format_grade_body(review)
        comment_body = f"## Re-review\n\n{body}"

        update_issue_title(existing_issue, new_title)
        add_comment_to_issue(existing_issue, comment_body)
        print(f"Updated grade issue #{existing_issue} with new grade: {grade}/100")

        # Add zinsser-ready label if grade reached 90+
        if grade >= 90:
            add_label_to_issue(existing_issue, "zinsser-ready")
            print(f"Added zinsser-ready label to issue #{existing_issue}")
    else:
        # Create new issue
        create_grade_issue(filename, review)


def format_feedback_body(item: dict) -> str:
    """Format the feedback issue body."""
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
    return body


def create_feedback_issue(filename: str, item: dict) -> None:
    """Create a single feedback issue."""
    title = f"[Teacher] {filename}: {item['title']}"
    body = format_feedback_body(item)

    labels = ["teacher", "feedback", filename, item["category"]]
    ensure_labels_exist(labels)
    create_issue(title, body, labels)
    print(f"Created feedback issue: {title}")


def handle_feedback_issues(filename: str, review: dict) -> None:
    """Handle feedback issues - deduplicate against existing issues."""
    existing_issues = find_existing_feedback_issues(filename)

    for item in review["feedback"]:
        if existing_issues:
            action, related_issue = compare_feedback(item, existing_issues)

            if action == "duplicate":
                print(f"Skipping duplicate feedback: {item['title']}")
                continue
            elif action == "related" and related_issue:
                # Add as comment to related issue
                comment_body = f"## Additional Feedback\n\n{format_feedback_body(item)}"
                add_comment_to_issue(related_issue, comment_body)
                print(f"Added comment to issue #{related_issue}: {item['title']}")
                continue

        # New feedback - create issue
        create_feedback_issue(filename, item)


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

    # Handle grade issue (update existing or create new)
    handle_grade_issue(filename, review)

    # Handle feedback issues only if grade < 90
    if grade < 90:
        print(f"Grade below 90, processing {len(review['feedback'])} feedback items...")
        handle_feedback_issues(filename, review)
    else:
        print("Grade 90 or above, skipping feedback issues.")

    print("Review complete!")


if __name__ == "__main__":
    main()

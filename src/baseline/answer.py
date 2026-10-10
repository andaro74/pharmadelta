"""The naive baseline's method: keyword matching over the question, the table and the clauses.

It reads the same inputs the agent's tool reads, `data/table.json` and
`data/clauses.json`, and applies no regulatory reasoning: the row is the
first row for the drug named in the question, narrowed to a section when a
section word appears; the clause is the longest clause id written in the
question, else a keyword's clause; a change is owed whenever the question
sounds like one; nothing is ever escalated. No model, no network, no
randomness. It never reads a golden's `expected`.

It is meant to lose on the traps. If it does not, that is the finding.
"""

from __future__ import annotations

from typing import Any

Row = dict[str, Any]
Answer = dict[str, Any]

SECTION_WORDS = (
    ("pregnan", "8.1"),
    ("adverse reaction", "6"),
    ("side effect", "6"),
    ("boxed", "bw"),
    ("warning", "bw"),
)
CLAUSE_WORDS = (
    ("pregnan", "201.57(c)(9)(i)"),
    ("strengthen", "314.70(c)(6)(iii)(A)"),
    ("add ", "314.70(c)(6)(iii)(A)"),
    ("warning", "314.70(c)(6)(iii)(A)"),
    ("adverse", "314.80(c)(1)(i)"),
)
DEFAULT_CLAUSE = "314.94(a)(8)(iv)"
CHANGE_WORDS = ("chang", "revis", "requir", "must", "new", "add ", "updat", "need")
CBE_WORDS = ("add ", "strengthen", "cbe")


def pick_row(q: str, table: list[Row]) -> Row:
    """First row for the drug named in the question, narrowed to a section if a section word appears."""
    drugs = sorted({row["ingredient"] for row in table}, key=len, reverse=True)
    drug = next((d for d in drugs if d.split()[0] in q), None)
    rows = [row for row in table if row["ingredient"] == drug] or table
    section = next((sec for word, sec in SECTION_WORDS if word in q), None)
    return next((row for row in rows if row["section"] == section), rows[0])


def pick_clause(q: str, clauses: dict[str, Any]) -> str:
    """The longest clause id written in the question, else the first keyword's clause, else the sameness rule."""
    written = sorted((cid for cid in clauses if cid.split("-")[0].lower() in q), key=len, reverse=True)
    if written:
        return written[0]
    return next((cid for word, cid in CLAUSE_WORDS if word in q), DEFAULT_CLAUSE)


def answer(question: str, table: list[Row], clauses: dict[str, Any]) -> Answer:
    """One answer in the shape of the agent's (milestones/M00/fields.md). Deterministic."""
    q = question.lower()
    impacted = any(word in q for word in CHANGE_WORDS)
    owed = "cbe-0" if any(word in q for word in CBE_WORDS) else "follow-rld" if impacted else "none"
    return {
        "table_row": pick_row(q, table)["table_row"],
        "clause_id": pick_clause(q, clauses),
        "answer_fields": {"impacted": impacted, "owed": owed, "escalate": False},
    }

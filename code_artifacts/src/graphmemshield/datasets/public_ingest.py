from __future__ import annotations

import json
from hashlib import sha256
from email.parser import Parser
from pathlib import Path
from typing import Any, Iterable

from graphmemshield.datasets.dialogue import DialogueRecord, DialogueRelation


def load_multiwoz_dialogues(path: str | Path, *, max_dialogues: int | None = None) -> list[DialogueRecord]:
    """Load common MultiWOZ JSON exports into GraphMemShield records.

    The parser accepts both list-style exports and dicts keyed by dialogue id.
    It extracts lightweight domain/slot/value relations from metadata without
    depending on a specific MultiWOZ minor-version package.
    """

    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    items = payload.items() if isinstance(payload, dict) else enumerate(payload)
    records: list[DialogueRecord] = []
    for dialogue_index, (dialogue_id, dialogue) in enumerate(items):
        if max_dialogues is not None and dialogue_index >= max_dialogues:
            break
        turns = dialogue.get("log") or dialogue.get("turns") or []
        user_id = f"multiwoz-{dialogue_id}"
        for turn_index, turn in enumerate(turns):
            text = turn.get("text") or turn.get("utterance") or ""
            metadata = turn.get("metadata") or {}
            relations = tuple(_multiwoz_relations(user_id, metadata))
            if not relations:
                continue
            records.append(
                DialogueRecord(
                    user_id=user_id,
                    session_id=f"{user_id}-session",
                    turn_id=f"turn-{turn_index}",
                    timestamp=f"2026-01-01T00:{turn_index % 60:02d}:00Z",
                    domain="multiwoz",
                    text=text,
                    entities={"dialogue_id": str(dialogue_id), "turn": turn_index},
                    relations=relations,
                )
            )
    return records


def load_enron_maildir(path: str | Path, *, max_messages: int | None = None) -> list[DialogueRecord]:
    """Load an Enron-style maildir tree into GraphMemShield records."""

    root = Path(path)
    files = sorted(item for item in root.rglob("*") if item.is_file())
    records: list[DialogueRecord] = []
    parser = Parser()
    for index, file_path in enumerate(files):
        if max_messages is not None and len(records) >= max_messages:
            break
        try:
            message = parser.parsestr(file_path.read_text(encoding="utf-8", errors="ignore"))
        except OSError:
            continue
        sender = _clean_email(message.get("From", "unknown@example.com"))
        recipients = tuple(
            _clean_email(part)
            for header in ("To", "Cc", "Bcc")
            for part in (message.get(header, "") or "").replace("\n", " ").split(",")
            if part.strip()
        )
        if not recipients:
            continue
        subject = message.get("Subject", "").strip() or "no-subject"
        relations = [DialogueRelation(f"user:{sender}", "sent_subject", f"subject:{subject[:80]}", "normal")]
        relations.extend(
            DialogueRelation(f"user:{sender}", "sent_to", f"user:{recipient}", "normal")
            for recipient in recipients[:10]
        )
        if _looks_sensitive(subject):
            relations.append(
                DialogueRelation(f"subject:{subject[:80]}", "has_sensitivity", "label:enterprise-sensitive", "secret")
            )
        records.append(
            DialogueRecord(
                user_id=sender,
                session_id=f"enron-thread-{_stable_bucket(subject)}",
                turn_id=f"msg-{index}",
                timestamp=_email_timestamp(message.get("Date"), index),
                domain="enron_email",
                text=subject,
                entities={"sender": sender, "subject": subject},
                relations=tuple(relations),
            )
        )
    return records


def _multiwoz_relations(user_id: str, metadata: dict[str, Any]) -> Iterable[DialogueRelation]:
    for domain, domain_payload in metadata.items():
        if not isinstance(domain_payload, dict):
            continue
        semi = domain_payload.get("semi") or {}
        book = domain_payload.get("book") or {}
        for slot, value in {**semi, **book}.items():
            if value in ("", "not mentioned", "none", None) or isinstance(value, (list, dict)):
                continue
            sensitivity = "financial" if slot in {"price", "pricerange", "booked"} else "normal"
            yield DialogueRelation(
                f"user:{user_id}",
                f"{domain}_{slot}",
                f"{domain}:{value}",
                sensitivity,
            )


def _clean_email(value: str) -> str:
    value = value.strip().lower()
    if "<" in value and ">" in value:
        value = value.split("<", 1)[1].split(">", 1)[0]
    return value or "unknown@example.com"


def _looks_sensitive(text: str) -> bool:
    lowered = text.lower()
    return any(token in lowered for token in ("legal", "confidential", "settlement", "investigation", "salary"))


def _email_timestamp(value: str | None, index: int) -> str:
    if value:
        return f"2026-01-01T{index % 24:02d}:{index % 60:02d}:00Z"
    return f"2026-01-01T00:{index % 60:02d}:00Z"


def _stable_bucket(value: str) -> str:
    return sha256(value.encode("utf-8", errors="ignore")).hexdigest()[:10]

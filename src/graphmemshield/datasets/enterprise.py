from __future__ import annotations

import random
from datetime import datetime, timedelta, timezone

from graphmemshield.datasets.dialogue import DialogueRecord, DialogueRelation


def build_enterprise_health_finance_records(
    *,
    num_users: int = 48,
    sessions_per_user: int = 4,
    turns_per_session: int = 3,
    seed: int = 2026,
) -> list[DialogueRecord]:
    """Build a larger de-identified benchmark with realistic enterprise motifs."""

    rng = random.Random(seed)
    records: list[DialogueRecord] = []
    base_time = datetime(2026, 1, 5, 9, 0, tzinfo=timezone.utc)
    departments = ["payments", "claims", "risk", "security", "sales", "hr"]
    projects = [f"Project-{name}" for name in "ABCDEFGHIJKL"]
    clients = [f"Client-{index:02d}" for index in range(18)]
    clinics = ["Cardiology", "Endocrinology", "Respiratory", "Physio"]
    conditions = ["arrhythmia", "diabetes", "asthma", "hypertension"]
    merchants = ["CloudVendor", "TravelDesk", "LaptopDepot", "PayrollBank"]
    assets = ["work laptop", "vpn token", "insurance claim", "travel card"]
    cities = ["Sydney", "Melbourne", "Brisbane", "Perth", "Adelaide", "Hanoi"]

    domains = ("health", "finance", "work", "location")
    time_index = 0
    for user_index in range(num_users):
        user_id = f"ehf-user-{user_index:03d}"
        home_city = rng.choice(cities)
        department = rng.choice(departments)
        for session_index in range(sessions_per_user):
            session_id = f"{user_id}-session-{session_index + 1}"
            session_domain = domains[(user_index + session_index) % len(domains)]
            for turn_index in range(turns_per_session):
                timestamp = base_time + timedelta(minutes=7 * time_index)
                turn_id = f"t{turn_index + 1}"
                records.append(
                    _record_for_domain(
                        user_id=user_id,
                        session_id=session_id,
                        turn_id=turn_id,
                        timestamp=timestamp,
                        domain=session_domain,
                        home_city=home_city,
                        department=department,
                        rng=rng,
                        projects=projects,
                        clients=clients,
                        clinics=clinics,
                        conditions=conditions,
                        merchants=merchants,
                        assets=assets,
                        cities=cities,
                    )
                )
                time_index += 1
    return records


def _record_for_domain(
    *,
    user_id: str,
    session_id: str,
    turn_id: str,
    timestamp: datetime,
    domain: str,
    home_city: str,
    department: str,
    rng: random.Random,
    projects: list[str],
    clients: list[str],
    clinics: list[str],
    conditions: list[str],
    merchants: list[str],
    assets: list[str],
    cities: list[str],
) -> DialogueRecord:
    user_node = f"user:{user_id}"
    if domain == "health":
        clinic = rng.choice(clinics)
        condition = rng.choice(conditions)
        medication = f"{condition}-care-plan"
        entities = {
            "user": user_id,
            "clinic": clinic,
            "condition": condition,
            "city": home_city,
        }
        relations = (
            DialogueRelation(user_node, "visited_clinic", f"clinic:{clinic}", "medical"),
            DialogueRelation(user_node, "has_condition", f"condition:{condition}", "medical"),
            DialogueRelation(f"condition:{condition}", "managed_by", f"medication:{medication}", "medical"),
            DialogueRelation(f"clinic:{clinic}", "located_in", f"city:{home_city}", "normal"),
        )
        text = f"{user_id} discussed {condition} follow-up at {clinic}."
    elif domain == "finance":
        merchant = rng.choice(merchants)
        asset = rng.choice(assets)
        amount_bucket = rng.choice(["low", "medium", "high"])
        entities = {
            "user": user_id,
            "merchant": merchant,
            "asset": asset,
            "amount_bucket": amount_bucket,
        }
        relations = (
            DialogueRelation(user_node, "purchased_from", f"merchant:{merchant}", "financial"),
            DialogueRelation(user_node, "purchased_asset", f"asset:{asset}", "financial"),
            DialogueRelation(f"asset:{asset}", "billed_by", f"merchant:{merchant}", "financial"),
            DialogueRelation(f"merchant:{merchant}", "amount_bucket", f"bucket:{amount_bucket}", "normal"),
        )
        text = f"{user_id} logged a {amount_bucket} expense for {asset}."
    elif domain == "work":
        project = rng.choice(projects)
        client = rng.choice(clients)
        entities = {
            "user": user_id,
            "project": project,
            "client": client,
            "department": department,
        }
        relations = (
            DialogueRelation(user_node, "works_on", f"project:{project}", "secret"),
            DialogueRelation(f"project:{project}", "for_client", f"client:{client}", "secret"),
            DialogueRelation(user_node, "member_of", f"department:{department}", "normal"),
            DialogueRelation(f"department:{department}", "supports", f"client:{client}", "normal"),
        )
        text = f"{user_id} updated {project} work for {client}."
    else:
        destination = rng.choice(cities)
        hotel = f"{destination}-Hotel-{rng.randrange(1, 8)}"
        entities = {
            "user": user_id,
            "city": destination,
            "hotel": hotel,
            "home_city": home_city,
        }
        relations = (
            DialogueRelation(user_node, "booked_hotel", f"hotel:{hotel}", "normal"),
            DialogueRelation(f"hotel:{hotel}", "located_in", f"city:{destination}", "normal"),
            DialogueRelation(user_node, "travels_from", f"city:{home_city}", "normal"),
            DialogueRelation(user_node, "travels_to", f"city:{destination}", "normal"),
        )
        text = f"{user_id} planned travel from {home_city} to {destination}."

    return DialogueRecord(
        user_id=user_id,
        session_id=session_id,
        turn_id=turn_id,
        timestamp=timestamp.isoformat().replace("+00:00", "Z"),
        domain=domain,
        text=text,
        entities=entities,
        relations=relations,
    )

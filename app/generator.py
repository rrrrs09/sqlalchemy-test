from datetime import datetime
from uuid import UUID, uuid4


def generate_children(
    nodes_per_level: int,
    parent_id: UUID,
    max_depth: int,
    level: int = 1,
) -> list[dict]:
    children: list[dict] = []
    if level > max_depth:
        return children

    for _ in range(nodes_per_level):
        node_id = uuid4()
        children.append(
            {
                "id": node_id,
                "parent_id": parent_id,
                "title": f"Level {level}",
                "registered_in": datetime.utcnow(),
            }
        )

        children += generate_children(nodes_per_level, node_id, max_depth, level + 1)

    return children

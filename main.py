import argparse
import asyncio
from typing import Optional
from uuid import UUID

from app.db import build_db_session_factory
from app.repository import get_nodes
from app.schemas import FieldEnum, Node


async def main(
    sort_fld: str,
    sort_dir: str,
    depth: int,
    node_id: Optional[UUID],
) -> None:
    session_factory = await build_db_session_factory()

    try:
        sort_field = FieldEnum[sort_fld]
    except KeyError:
        raise ValueError("Sorting field name is not valid")

    if sort_dir not in ("asc", "dsc"):
        raise ValueError("Sorting direction must be `asc` or `dsc`")

    if depth < 0:
        raise ValueError("Depth must be a positive number")

    nodes = await get_nodes(
        session_factory=session_factory,
        sort_fld=sort_field,
        sort_dir=sort_dir,  # type: ignore
        depth=depth,
        node_id=node_id,
    )
    for node in nodes:
        print(node)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Tree nodes.")
    parser.add_argument(
        "--sort-fld", dest="sort_fld", type=str, default="id", help="sorting field"
    )
    parser.add_argument(
        "--sort-dir", dest="sort_dir", type=str, default="asc", help="sorting direction"
    )
    parser.add_argument("--depth", dest="depth", type=int, default=1, help="depth")
    parser.add_argument(
        "--node", dest="node_id", type=UUID, default=None, help="start node"
    )

    args = parser.parse_args()

    try:
        asyncio.run(main(args.sort_fld, args.sort_dir, args.depth, args.node_id))
    except ValueError as exc:
        print(exc)

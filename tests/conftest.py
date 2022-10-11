from datetime import datetime
from typing import Awaitable, Callable
from uuid import uuid4

import pytest

from app.db import AsyncSessionFactory, build_db_session_factory
from app.generator import generate_children
from app.models import NodeModel

TreeFactory = Callable[[int, int], Awaitable[list[NodeModel]]]


@pytest.fixture
async def session_factory() -> AsyncSessionFactory:
    return await build_db_session_factory()


@pytest.fixture(autouse=True)
async def delete_tree(session_factory: AsyncSessionFactory) -> None:
    async with session_factory() as session, session.begin():
        await session.execute("DELETE FROM tree")


@pytest.fixture
def tree_generator_factory(
    session_factory: AsyncSessionFactory,
) -> TreeFactory:
    async def factory(
        nodes_per_level: int,
        max_depth: int,
    ) -> list[NodeModel]:
        root_id = uuid4()

        nodes = []
        nodes.append(
            NodeModel(
                id=root_id,
                parent_id=None,
                title="Root",
                registered_in=datetime.utcnow(),
            )
        )

        children = generate_children(
            nodes_per_level=nodes_per_level,
            parent_id=root_id,
            max_depth=max_depth,
        )
        for child in children:
            nodes.append(
                NodeModel(
                    id=child["id"],
                    parent_id=child["parent_id"],
                    title=child["title"],
                    registered_in=child["registered_in"],
                )
            )

        async with session_factory() as session, session.begin():
            session.add_all(nodes)
            await session.commit()

        return nodes

    return factory

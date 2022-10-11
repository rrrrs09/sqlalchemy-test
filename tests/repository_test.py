from app.db import AsyncSessionFactory
from app.repository import get_nodes
from app.schemas import FieldEnum
from tests.conftest import TreeFactory


async def test_get_nodes_all_nodes(
    session_factory: AsyncSessionFactory,
    tree_generator_factory: TreeFactory,
) -> None:
    # - Arrange -
    generated_nodes = await tree_generator_factory(2, 2)

    # - Act -
    nodes = await get_nodes(
        session_factory=session_factory,
        sort_fld=FieldEnum.id,
        sort_dir="asc",
        depth=2,
    )

    # - Assert -
    assert len(nodes) == len(generated_nodes)


async def test_get_nodes_depth_one(
    session_factory: AsyncSessionFactory,
    tree_generator_factory: TreeFactory,
) -> None:
    # - Arrange -
    generated_nodes = await tree_generator_factory(2, 3)

    # - Act -
    nodes = await get_nodes(
        session_factory=session_factory,
        sort_fld=FieldEnum.id,
        sort_dir="asc",
        depth=1,
    )

    # - Assert -
    # root and one level children
    assert len(nodes) == 3


async def test_get_nodes_depth_zero(
    session_factory: AsyncSessionFactory,
    tree_generator_factory: TreeFactory,
) -> None:
    # - Arrange -
    generated_nodes = await tree_generator_factory(2, 3)

    # - Act -
    nodes = await get_nodes(
        session_factory=session_factory,
        sort_fld=FieldEnum.id,
        sort_dir="asc",
        depth=0,
    )

    # - Assert -
    assert len(nodes) == 1


async def test_get_nodes_custom_parent(
    session_factory: AsyncSessionFactory,
    tree_generator_factory: TreeFactory,
) -> None:
    # - Arrange -
    generated_nodes = await tree_generator_factory(2, 2)
    # level one node
    parent = generated_nodes[1]

    # - Act -
    nodes = await get_nodes(
        session_factory=session_factory,
        sort_fld=FieldEnum.id,
        sort_dir="asc",
        depth=1,
        node_id=parent.id,
    )

    # - Assert -
    assert len(nodes) == 3


async def test_get_nodes_sorting(
    session_factory: AsyncSessionFactory,
    tree_generator_factory: TreeFactory,
) -> None:
    # - Arrange -
    generated_nodes = await tree_generator_factory(2, 2)
    generated_nodes = sorted(generated_nodes, key=lambda node: node.title, reverse=True)

    # - Act -
    nodes = await get_nodes(
        session_factory=session_factory,
        sort_fld=FieldEnum.title,
        sort_dir="dsc",
        depth=1,
    )

    # - Assert -
    assert nodes[0].title == generated_nodes[0].title
    assert nodes[-1].title == generated_nodes[-1].title

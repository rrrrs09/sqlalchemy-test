from typing import Literal, Optional
from uuid import UUID

from sqlalchemy import literal_column, select

from app.db import AsyncSessionFactory
from app.models import NodeModel
from app.schemas import FieldEnum, Node


async def get_nodes(
    session_factory: AsyncSessionFactory,
    sort_fld: FieldEnum,
    sort_dir: Literal["asc", "dsc"],
    depth: int,
    node_id: Optional[UUID] = None,
) -> list[Node]:
    async with session_factory() as session, session.begin():
        level_col = literal_column("0").label("level")
        increased_level_col = literal_column("cte.level + 1").label("level")

        first_q = select(NodeModel, level_col)
        if node_id:
            first_q = first_q.where(NodeModel.id == node_id)
        else:
            first_q = first_q.where(NodeModel.parent_id == None)

        first_q = first_q.cte("cte", recursive=True)

        second_q = select(NodeModel, increased_level_col).join(
            first_q, NodeModel.parent_id == first_q.c.id
        )

        query = first_q.union(second_q)

        sorted_field = None
        if sort_fld == FieldEnum.id:
            sorted_field = query.c.id
        elif sort_fld == FieldEnum.parent_id:
            sorted_field = query.c.parent_id
        elif sort_fld == FieldEnum.title:
            sorted_field = query.c.title
        elif sort_fld == FieldEnum.registered_in:
            sorted_field = query.c.registered_in
        else:
            raise ValueError("Unknown field {}".format(sort_fld))

        if sort_dir == "dsc":
            sorted_field = sorted_field.desc()  # type: ignore

        query = select(query).where(query.c.level <= depth)
        query = query.order_by(sorted_field)

        result = await session.execute(query)

        return [
            Node(
                id=row[FieldEnum.id.value],
                parent_id=row[FieldEnum.parent_id.value],
                title=row[FieldEnum.title.value],
                registered_in=row[FieldEnum.registered_in.value],
            )
            for row in result.fetchall()
        ]

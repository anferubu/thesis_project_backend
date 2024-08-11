from typing import Any, Type

from fastapi import HTTPException
from sqlalchemy import asc, desc



def parse_filter_param(query: str) -> dict[str, str]:
    """Parse query string (filter) parameter into a dictionary.
    Values 'true' or 'false' are transformed into booleans.
    A field without a value is taken as field='item exists'."""

    items = query.split(',')
    parsed_filters = {}
    for item in items:
        if '=' in item:
            field, value = item.split('=')
            # parse boolean values
            if value.lower() in ('true', 'false'):
                value = value.lower() == 'true'
            parsed_filters[field] = value
        else:
            parsed_filters[item] = 'item exist'
    return parsed_filters



def parse_sort_param(query: str) -> dict[str, str]:
    """Parse query string (sort) parameter into a dictionary.
    A field without a value is taken as field='asc'."""

    items = query.split(',')
    sort_dict = {}
    for item in items:
        if '=' in item:
            field, direction = item.split('=')
        else:
            field, direction = item, 'asc'
        sort_dict[field] = direction
    return sort_dict



def apply_sorting(query, model:Type, sort:dict[str, str]):
    """Apply sorting to a SQLAlchemy query."""

    for field, direction in sort.items():
        if not hasattr(model, field):
            raise HTTPException(400, f"Invalid sort field: {field}")
        if direction.lower() == "desc":
            query = query.order_by(desc(getattr(model, field)))
        else:
            query = query.order_by(asc(getattr(model, field)))
    return query



def apply_filters(query, model: Type, filters:dict[str, Any]):
    """Apply filtering to a SQLAlchemy query."""

    for field, value in filters.items():
        if not hasattr(model, field):
            raise HTTPException(400, f"Invalid filter field: {field}")
        if value == "item exist":
            query = query.where(getattr(model, field).is_not(None))
        else:
            query = query.where(getattr(model, field) == value)
    return query

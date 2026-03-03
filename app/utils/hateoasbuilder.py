from app.schemas import PaginationResponse
from typing import Any


def build_pagination_links(
    base_url: str, page: int, limit: int, pagination: PaginationResponse
) -> dict:
    links = {"self": f"{base_url}?page={page}&limit={limit}"}
    if pagination.has_next:
        links["next"] = f"{base_url}?page={page + 1}&limit={limit}"
    if pagination.has_previous:
        links["previous"] = f"{base_url}?page={page - 1}&limit={limit}"
    return links


def build_resource_links(resource_type: str, resource_id: Any, include_crud: bool = False) -> list:
    links = [{"rel": "self", "href": f"/{resource_type}/{resource_id}", "method": "GET"}]
    if include_crud:
        links.extend(
            [
                {"rel": "update", "href": f"/{resource_type}/{resource_id}", "method": "PUT"},
                {"rel": "delete", "href": f"/{resource_type}/{resource_id}", "method": "DELETE"},
            ]
        )
    return links

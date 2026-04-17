from app.repositories.interfaces.developer_repository import DeveloperRepositoryInterface
from app.schemas import DeveloperResponse
from app.schemas.developer import DevelopersListResponse, PaginationResponse, DeveloperQueryParameters
from app.utils.serializers import serialize_developer
from app.utils.hateoasbuilder import build_pagination_links

"""
Business logic for developer operations.

Handles read-only developer operations with filtering and pagination.
"""


def get_developers_list(
    dev_repo: DeveloperRepositoryInterface, params: DeveloperQueryParameters
) -> DevelopersListResponse:

    developers, total_developers = dev_repo.find_filtered(params)

    developer_responses = [serialize_developer(developer) for developer in developers]

    pages = (total_developers + params.limit - 1) // params.limit
    pagination = PaginationResponse(
        page=params.page,
        limit=params.limit,
        total=total_developers,
        pages=pages,
        has_next=params.page < pages,
        has_previous=params.page > 1,
    )

    links = build_pagination_links("/developers", params.page, params.limit, pagination)

    return DevelopersListResponse(developers=developer_responses, pagination=pagination, links=links)


def get_developer_by_id(dev_repo: DeveloperRepositoryInterface, developer_id: int) -> DeveloperResponse | None:
    developer = dev_repo.find_by_id(developer_id)
    if not developer:
        return None
    return serialize_developer(developer)

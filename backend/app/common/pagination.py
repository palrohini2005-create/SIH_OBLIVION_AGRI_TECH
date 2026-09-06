"""Turning page/limit query parameters into an offset and a page envelope."""

from math import ceil

from app.common.schemas import PageMeta


def page_meta(page: int, page_size: int, total: int) -> PageMeta:
    """Clamp the requested page into range and work out how many there are."""
    total_pages = max(1, ceil(total / page_size))
    return PageMeta(
        page=min(max(1, page), total_pages),
        pageSize=page_size,
        total=total,
        totalPages=total_pages,
    )


def offset(meta: PageMeta) -> int:
    return (meta.page - 1) * meta.pageSize


def clamp_limit(requested: int, fallback: int = 10, maximum: int = 50) -> int:
    """Keep a caller-supplied page size inside sensible bounds."""
    return min(requested if requested > 0 else fallback, maximum)

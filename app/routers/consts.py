from dataclasses import dataclass


@dataclass(frozen=True)
class RouteSlug:
    pk: str = '{pk}/'
    ifilter: str = '{ifilter}/'

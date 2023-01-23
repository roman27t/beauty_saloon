from enum import Enum


class OfferFilter(str, Enum):
    employee = 'employee'
    service_name = 'service_name'

    def get_filters(self, pk: int) -> dict:
        params = {f'{self.value}_id': pk}
        if self.value == OfferFilter.service_name:
            params['is_active'] = True
        return params

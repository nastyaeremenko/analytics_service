from fastapi import Query


class SortingParams:
    def __init__(
            self,
            sort_field: str = Query(None, description='Поле для сортировки'),
            sort_order: bool = Query(None, description='Порядок сортировки'),
    ):
        self.sort_field = sort_field
        self.sort_order = sort_order

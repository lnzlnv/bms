from apis.game_schedule.services import (
    get_formatted_date,
    get_formatted_date_2
)

def get_date_based_on_method(
    *,
    date,
    is_update
):
    if is_update:
        return get_formatted_date_2(date=date)
    return get_formatted_date(date=date)
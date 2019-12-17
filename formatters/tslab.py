from rows import TimeRow


def format(data):
    """
    @param TimeRow data:
    """
    return [
        data.dt.strftime("%m/%d/%Y"),
        data.dt.strftime("%H:%M"),
        data.open,
        data.high,
        data.low,
        data.close,
        data.volume
    ]

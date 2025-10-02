def parse_timestamp_to_seconds(ts: str) -> int:
    negative = ts.startswith('-')
    ts = ts.lstrip('-')
    parts = list(map(int, ts.split(':')))
    if len(parts) == 3:
        h, m, s = parts
    elif len(parts) == 2:
        h, m, s = 0, *parts
    else:
        h, m, s = 0, 0, parts[0]
    total = h * 3600 + m * 60 + s
    return -total if negative else total
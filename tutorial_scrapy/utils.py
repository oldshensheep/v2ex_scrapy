import json
from typing import Union

import arrow


def time_to_timestamp(t: str) -> int:
    t = t.strip()
    a = None
    try:
        if t[-2:] == "00":
            a = arrow.get(t, "YYYY-MM-DD HH:mm:ss ZZ")
        else:
            a = arrow.utcnow().dehumanize(t.replace(" ", ""), "zh")
        return int(a.to("+08:00").timestamp())
    except Exception:
        return 0


def none_or_strip(s: Union[str, None]) -> Union[str, None]:
    if s is not None:
        return s.strip()
    return s


def json_to_str(j):
    return json.dumps(j, ensure_ascii=False)


if __name__ == "__main__":
    a = ["2022-04-28 13:24:38 +08:00", "287 天前", "1 小时前"]

    for i in a:
        print(time_to_timestamp(i))

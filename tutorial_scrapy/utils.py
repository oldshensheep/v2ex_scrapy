from typing import Union
import arrow
import json


def convert_time(t: str) -> str:
    t = t.strip()
    a = None
    if t[-2:] == "00":
        a = arrow.get(t, "YYYY-MM-DD HH:mm:ss ZZ")
    else:
        a = arrow.utcnow().dehumanize(t.replace(" ", ""), "zh")
    return a.to("+08:00").format()


def none_or_strip(s: Union[str, None]) -> Union[str, None]:
    if s is not None:
        return s.strip()
    return s


def json_to_str(j):
    return json.dumps(j, ensure_ascii=False)


if __name__ == "__main__":
    a = ["2022-04-28 13:24:38 +08:00", "287 天前", "1 小时前"]

    for i in a:
        print(convert_time(i))

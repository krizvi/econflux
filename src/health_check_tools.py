from strands import tool

import datetime as datetime
from typing import Dict


@tool
def ping() -> Dict[str, str]:
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return {"ok": "pong", "tod": now}

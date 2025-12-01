from strands import tool

import datetime as datetime
from typing import Dict


@tool
def ping() -> Dict[str, str]:
    """
    Return a simple liveness check with the current server time.

    Use to confirm the agent runtime responds; it does not check dependencies.

    Returns:
        Dict with:
        - ok: Literal "pong" indicating the service responded
        - tod: Server time in "%Y-%m-%d %H:%M:%S" (local timezone)

    Notes:
        - Time is taken from the host OS clock and may not reflect wall-clock accuracy
    """
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return {"ok": "pong", "tod": now}

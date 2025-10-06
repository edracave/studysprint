
from datetime import date
from app.config import FREE_DAILY_QUOTA, PREMIUM_DAILY_QUOTA

def get_daily_quota(premium: bool) -> int:
    return PREMIUM_DAILY_QUOTA if premium else FREE_DAILY_QUOTA

async def check_and_decrement_quota(user, session):
    today = date.today()
    if user.last_reset_quota != today:
        user.msg_quota_today = get_daily_quota(user.premium)
        user.last_reset_quota = today
    if user.msg_quota_today <= 0:
        return False
    user.msg_quota_today -= 1
    await session.flush()
    return True

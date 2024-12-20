from datetime import datetime

from db.sql.model import User


def check_access_for_chanel(user: User) -> bool:
    if user.date_of_kill is None:
        return False
    return user.date_of_kill > datetime.now()

from datetime import datetime


def months_past(date: datetime):
    if not isinstance(date, datetime):
        raise TypeError("submission_date is not a datetime")
    nowadays = datetime.utcnow()
    num_months = ((nowadays.year - date.year) * 12) + (nowadays.month - date.month)
    return num_months

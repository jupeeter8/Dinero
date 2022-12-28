import time


def generate_code():
    # username = (
    #     db.query(models.Users).filter(models.Users.user_id == user_ID).first().username
    # )

    # username = "anirudh"
    # time_int = 9999999

    # char = [ord(i) for i in username]

    time_str = str(time.time()).replace(".", "")
    time_int = int(time_str[:-6:-1])

    return time_int

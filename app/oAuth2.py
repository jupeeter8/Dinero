from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class PasswordUtils:
    def verify_hash(self, password, hashed_password):
        return pwd_context.verify(password, hashed_password)

    def get_password_hash(self, password):
        return pwd_context.hash(password)


password_utils = PasswordUtils()

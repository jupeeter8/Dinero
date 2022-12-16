from pydantic import BaseSettings


class EnvrionmentVariable(BaseSettings):
    database_url: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    class Config:
        env_file = ".env"


env_var = EnvrionmentVariable()

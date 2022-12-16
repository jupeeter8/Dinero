from pydantic import BaseSettings


class EnvrionmentVariable(BaseSettings):
    database_url: str

    class Config:
        env_file = ".env"


env_var = EnvrionmentVariable()

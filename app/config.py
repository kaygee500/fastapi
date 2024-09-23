from decouple import config
# from dotenv import load_dotenv
#import os

from pydantic_settings import BaseSettings, SettingsConfigDict
# from pydantic import (
#     AliasChoices,
#     AmqpDsn,
#     BaseModel,
#     Field,
#     ImportString,
#     PostgresDsn,
#     RedisDsn,
# )

class Settings(BaseSettings):
    # # Pydantic-settings only method
    # model_config = SettingsConfigDict( 
    #     env_file=".env",
    #     env_file_encoding="utf-8",
    #     case_sensitive=False,
    #     extra="ignore",
    # )

#     # pip install pydantic-settings uses dotenv by default to load .env file
#    # load_dotenv()
#     DATABASE_HOSTNAME: str = Field(min_length=5)
#     database_port: str = Field(alias='DATABASE_PORT')
#     database_password: str = Field(min_length=10)
#     database_name: str = Field(alias='DATABASE_NAME')
#     database_username: str = Field(alias='DATABASE_USERNAME')
#     secret_key: str = Field(alias='SECRET_KEY',)
#     algorithm: str= Field(alias='ALGORITHM')
#     access_token_expire_minutes: int = Field(ge=0)
#     database_password: str = Field(min_length=10)


    ##--- Alt 1
    ##python-decouple method to load .env file
    database_hostname: str = config('DATABASE_HOSTNAME')
    database_port: str = config('DATABASE_PORT')
    database_password: str = config('DATABASE_PASSWORD')
    database_name: str = config('DATABASE_NAME')
    database_username: str = config('DATABASE_USERNAME')
    secret_key: str = config('SECRET_KEY')
    algorithm: str= config('ALGORITHM')
    access_token_expire_minutes: int = config('ACCESS_TOKEN_EXPIRE_MINUTES')

    ##--- Alt 2
    # # pip install python-dotenv method to load .env file
    # load_dotenv()
    # database_hostname: str = os.getenv('DATABASE_HOSTNAME')
    # database_port: str = os.getenv('DATABASE_PORT')
    # database_password: str = os.getenv('DATABASE_PASSWORD')
    # database_name: str = os.getenv('DATABASE_NAME')
    # database_username: str = os.getenv('DATABASE_USERNAME')
    # secret_key: str = os.getenv('SECRET_KEY')
    # algorithm: str= os.getenv('ALGORITHM')
    # access_token_expire_minutes: int = os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES')

print (Settings())
settings = Settings()

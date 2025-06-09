import os
from dotenv import load_dotenv
from pydantic import BaseModel, ValidationError
from typing import Optional, Protocol



class DBModel(BaseModel):
    user:str
    password:str
    host: str
    database:Optional[str] = None
    port:Optional[int] = 3306
    sid: Optional[str] = None
    connection_url: Optional[str] = None

    def __init__(self, **data):
        super().__init__(**data)
        self.connection_url = self._generate_url()

    def _generate_url(self):
        if self.database:
            return f"mysql+mysqlconnector://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}"
        else:
            return f"mysql+mysqlconnector://{self.user}:{self.password}@{self.host}:{self.port}"
   
    @classmethod
    def get_dotenv(cls, dotenv_path: Optional[str] = ".env") -> "DBModel":
        load_dotenv(dotenv_path="database/.env")
        return cls(
            user=os.getenv("user"),
            password=os.getenv("password"),
            host=os.getenv("host"),
            database=os.getenv("database"),
            port=int(os.getenv("port", 3306)),
            sid=os.getenv("sid")
        )
    @classmethod
    def get_dotenv_create_db(cls, dotenv_path: Optional[str] = "database/.env") -> "DBModel":
        load_dotenv(dotenv_path)
        return cls(
            host=os.getenv("host"),
            user=os.getenv("user"),
            password=os.getenv("password"),
            database=os.getenv("database")
        )


class DataBaseConnector(Protocol):
    def connect(self)->bool:
        ...
    def disconect(self)->None:
        ...


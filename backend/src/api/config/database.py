from dataclasses import dataclass


@dataclass
class DatabaseConfig:
    host: str
    port: int
    database: str
    user: str
    password: str
    schema: str

    def __post_init__(self) -> None:
        self.driver = "postgresql+psycopg2"

    @property
    def url(self) -> str:
        return "{driver}://{user}:{password}@{host}:{port}/{database}".format(
            driver=self.driver,
            user=self.user,
            password=self.password,
            host=self.host,
            port=self.port,
            database=self.database,
        )

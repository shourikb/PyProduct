import databases
import sqlalchemy

# SQLAlchemy specific code, as with any other app
DATABASE_URL = "sqlite:///./data.sqlite"
# DATABASE_URL = "postgresql://user:password@postgresserver/db"

database = databases.Database(DATABASE_URL)

metadata = sqlalchemy.MetaData()

usersTable = sqlalchemy.Table(
    "users",
    metadata,
    sqlalchemy.Column("username", sqlalchemy.String),
    sqlalchemy.Column("hashed_password", sqlalchemy.String),
    sqlalchemy.Column("email", sqlalchemy.String),
    sqlalchemy.Column("full_name", sqlalchemy.String),
    sqlalchemy.Column("disabled", sqlalchemy.Boolean),
)


engine = sqlalchemy.create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)
metadata.create_all(engine)


def get_user_from_cred(username: str, password: str):
    selected_user = usersTable.select().where(usersTable.c.username == username).where(usersTable.c.password == password)
    conn = engine.connect()
    result = conn.execute(selected_user)
    return result.fetchone()

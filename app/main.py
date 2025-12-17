from pathlib import Path

from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.engine import make_url
from sqlalchemy.orm import sessionmaker

from app.application.use_cases.user_use_cases import (
    CreateUserUseCase,
    GetUserByEmailUseCase,
    ListUsersUseCase,
)
from app.core.config import get_settings
from app.infrastructure.db.models.user_model import Base
from app.infrastructure.db.repository_impl.user_repository_impl import UserRepositoryImpl
from app.presentation.controllers.user_controller import UserController
from app.presentation.routes.user_routes import get_user_router

settings = get_settings()

database_url = make_url(settings.database_url)
if database_url.drivername == "sqlite" and database_url.database and database_url.database != ":memory:":
    Path(database_url.database).parent.mkdir(parents=True, exist_ok=True)

engine = create_engine(settings.database_url, echo=settings.debug, future=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.app_name,
    debug=settings.debug,
    docs_url="/swagger",
    redoc_url=None,
    openapi_url="/openapi.json",
)

user_repository = UserRepositoryImpl(SessionLocal)
create_user_use_case = CreateUserUseCase(user_repository)
list_users_use_case = ListUsersUseCase(user_repository)
get_user_by_email_use_case = GetUserByEmailUseCase(user_repository)
user_controller = UserController(create_user_use_case, list_users_use_case, get_user_by_email_use_case)

app.include_router(get_user_router(user_controller))


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}

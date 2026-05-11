from app.core.config import get_settings
from app.db.base import Base
from app.db.session import SessionLocal, engine
from app.models import market  # noqa: F401
from app.services.demo_seed import seed_demo_data


def init_db() -> None:
    Base.metadata.create_all(bind=engine)
    if get_settings().seed_demo_data:
        with SessionLocal() as db:
            seed_demo_data(db)


if __name__ == "__main__":
    init_db()

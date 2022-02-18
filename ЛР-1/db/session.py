from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager
from db.base import engine, Base


__Session = sessionmaker(bind=engine)


def get_session():
    Base.metadata.create_all(engine)
    session = __Session()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


session_manager = contextmanager(get_session)

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from models import Base

engine = create_engine('postgresql://postgres@localhost/ohmydb', convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))


def init_db():
    Base.metadata.create_all(bind=engine)


if __name__ == '__main__':
    init_db()

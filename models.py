from sqlalchemy import Column, Integer, String, DateTime, BigInteger
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Hitokoto(Base):
    __tablename__ = 'hitokoto'

    id = Column(BigInteger, primary_key=True)
    hitokoto = Column(String(1024))
    cat = Column(String(32))
    author = Column(String(128))
    source = Column(String(128))
    like = Column(Integer)
    date = Column(DateTime)
    catname = Column(String(128))

    def __repr__(self):
        return "<Hitokoto(hitokoto='%s', source='%s', catname='%s')>" % (self.hitokoto, self.source, self.catname)

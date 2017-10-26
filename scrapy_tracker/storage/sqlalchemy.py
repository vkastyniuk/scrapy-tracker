from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from scrapy_tracker.storage import Storage
from sqlalchemy.engine import create_engine

DeclarativeBase = declarative_base()


class KeyChecksumModel(DeclarativeBase):
    __tablename__ = 'key_checksum'
    __table_args__ = (
        {
            'mysql_charset': 'utf8',
            'mysql_engine': 'InnoDB',
            'mysql_row_format': 'DYNAMIC',
        },
    )

    key = Column(String, nullable=False, primary_key=True)
    checksum = Column(String, nullable=False)

    @classmethod
    def query(cls, session):
        return session.query(cls)

    def __repr__(self):
        return '<KeyChecksum:%s %s>' % (self.key, self.checksum)


class SqlAlchemyStorage(Storage):
    def __init__(self, settings):
        engine = settings.get('TRACKER_SQLALCHEMY_ENGINE', 'sqlite:///:memory:')
        self.engine = create_engine(engine)

        session_cls = sessionmaker()
        session_cls.configure(bind=self.engine)
        self.session = session_cls(expire_on_commit=False)

        drop_all_keys = settings.getbool('TRACKER_SQLALCHEMY_FLUSH_DB', False)
        if drop_all_keys:
            self.session.execute(KeyChecksumModel.__table__.delete())
            self.session.commit()

        if drop_all_keys:
            self._redis.flushdb()

    def getset(self, key, checksum):
        model = KeyChecksumModel.query(self.session).get(key)
        if model:
            old_checksum = model.checksum
            model.checksum = checksum
            self.session.commit()

            return old_checksum

        self.session.add(KeyChecksumModel(key=key, checksum=checksum))
        self.session.commit()

        return None

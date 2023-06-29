from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship


def create_database():
    # Создание подключения к базе данных
    engine = create_engine('sqlite:///contractors.db')
    Base = declarative_base()

    # Определение моделей с помощью SQLAlchemy ORM
    class Contractor(Base):
        __tablename__ = 'contractors'
        id = Column(Integer, primary_key=True)
        inn = Column(String)
        name = Column(String)
        payments = relationship('Payment', back_populates='contractor')

    class Payment(Base):
        __tablename__ = 'payments'
        id = Column(Integer, primary_key=True)
        contractor_id = Column(Integer, ForeignKey('contractors.id'))
        payment = Column(Float)
        contractor = relationship('Contractor', back_populates='payments')

    # Создание таблиц в базе данных
    Base.metadata.create_all(engine)

    # Очистка данных из таблиц
    Session = sessionmaker(bind=engine)
    session = Session()

    session.query(Contractor).delete()
    session.query(Payment).delete()
    session.commit()

    return Contractor, Payment, engine

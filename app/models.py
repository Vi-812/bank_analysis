from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, Numeric, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship


def create_database():

    engine = create_engine('sqlite:///app/contractors.db')
    Base = declarative_base()

    class Contractor(Base):
        __tablename__ = 'contractors'
        id = Column(Integer, primary_key=True)
        inn = Column(String, nullable=False)
        name = Column(String, nullable=False)

        num_debit_payments = Column(Integer, default=0)
        total_debit_payment = Column(Numeric(precision=20, scale=2), default=0)
        min_debit_payment = Column(Float, default=0)
        max_debit_payment = Column(Float, default=0)
        median_debit_payment = Column(Float, default=0)

        num_credit_payments = Column(Integer, default=0)
        total_credit_payment = Column(Numeric(precision=20, scale=2), default=0)
        min_credit_payment = Column(Float, default=0)
        max_credit_payment = Column(Float, default=0)
        median_credit_payment = Column(Float, default=0)

        payments = relationship('Payment', back_populates='contractor')


    class Payment(Base):
        __tablename__ = 'payments'
        id = Column(Integer, primary_key=True)
        contractor_id = Column(Integer, ForeignKey('contractors.id'), nullable=False)
        payment = Column(Float, nullable=False)
        debit = Column(Boolean, nullable=False)
        contractor = relationship('Contractor', back_populates='payments')

    Base.metadata.create_all(engine)

    # Очистка данных из таблиц
    Session = sessionmaker(bind=engine)
    session = Session()
    session.query(Contractor).delete()
    session.query(Payment).delete()
    session.commit()

    return Contractor, Payment, engine

from sqlalchemy import Column, ForeignKey, Integer, BigInteger, Text, Double
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class FileProcessORM(Base):
    __tablename__ = "file_process"
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    status = Column(Text, nullable=True)
    process_task_id = Column(Integer, nullable=True)

    process_result = relationship("ProcessResultORM", 
                                  backref="file_compare", 
                                  uselist=False)

    first_file_compare = relationship("FileCompareORM", 
                                foreign_keys="FileCompareORM.f_file_process_id",
                                backref="first_file_process",
                                uselist=False)
    second_file_compare = relationship("FileCompareORM",
                                    foreign_keys="FileCompareORM.s_file_process_id", 
                                    backref="second_file_process",
                                    uselist=False)
    
    facts_extraction = relationship("FactExtractionORM")

class ProcessResultORM(Base):
    __tablename__ = "process_result"
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    json_result = Column(Text, nullable=True)
    file_process_id = Column(BigInteger, ForeignKey("file_process.id"), nullable=True)

class FileCompareORM(Base):
    __tablename__ = "file_compare"
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    f_file_name = Column(Text, nullable=True)
    s_file_name = Column(Text, nullable=True)
    f_file_process_id = Column(BigInteger, ForeignKey("file_process.id"), nullable=True)
    s_file_process_id = Column(BigInteger, ForeignKey("file_process.id"), nullable=True)

class FactExtractionORM(Base):
    __tablename__ = "fact_extraction"
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    fact_name = Column(Text, nullable=True)
    fact_localization = Column(Text, nullable=True)
    fact_value = Column(Text, nullable=True)
    line_number = Column(Integer, nullable=True)
    file_process_id = Column(BigInteger, ForeignKey("file_process.id"), nullable=True)

    fact_info = relationship("FactInfoORM", backref="fact", uselist=False)

class FactInfoORM(Base):
    __tablename__ = "fact_info"
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    probability = Column(Double, nullable=True)
    confidence = Column(Double, nullable=True)
    page = Column(Integer, nullable=True)
    top = Column(Double, nullable=True)
    left = Column(Double, nullable=True)
    width = Column(Double, nullable=True)
    height = Column(Double, nullable=True)
    fact_extraction_id = Column(BigInteger, ForeignKey("fact_extraction.id"), nullable=True)



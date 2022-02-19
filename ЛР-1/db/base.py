from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base


engine = create_engine("duckdb:///:memory:")
metadata = MetaData(bind=engine)
Base = declarative_base(metadata=metadata)



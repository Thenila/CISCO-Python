from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db_models import Base,Flight


#db setup
engine=create_engine('sqlite:///flight.db',echo=True)
Base.metadata.create_all(engine)

#session for sql operations
sessionLocal=sessionmaker(bind=engine)
session=sessionLocal() # for sql ops 
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

POSTGRESQL_DATABASE_URL = "postgresql://postgres:hello@localhost/point_of_sale"
def get_engine():
    engine = create_engine(POSTGRESQL_DATABASE_URL)
    return engine


Base = declarative_base()


session_local = sessionmaker(autocommit=False, autoflush=False, bind=get_engine())
def get_db():
    db = session_local()

    try:
        yield db
    finally:
        db.close()



def init_db():
    from src.models.category_model import CategoryModel
    from src.models.sub_category_model import SubCategoryModel
    
    Base.metadata.create_all(bind=get_engine())
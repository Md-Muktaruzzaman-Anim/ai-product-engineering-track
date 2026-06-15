from sqlalchemy import Column, Integer, String, Float, TIMESTAMP, text

# Local context lookup to bypass non-standard module names
db_module = __import__("08_Working_with_Databases", fromlist=["Base"])
Base = db_module.Base

class Course(Base):
    __tablename__ = "courses"   

    id = Column(Integer, primary_key=True, index=True)
    course_name = Column(String, nullable=False)
    instructor = Column(String, nullable=False)
    duration = Column(Float, nullable=False)
    website = Column(String, nullable=False)

class User(Base):
    __tablename__ = "users"
    id  = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

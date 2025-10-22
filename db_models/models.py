from sqlalchemy import create_engine,Column,Integer,String,Float,ForeignKey
from sqlalchemy.orm import relationship, declarative_base,sessionmaker

# class Base(declarative_base()):

#     pass

Base = declarative_base()

class Category(Base):
    __tablename__ = "categories"

    id=Column(Integer, primary_key=True)
    name=Column(String(50), nullable=False)
    products=relationship("Product",back_populates="category_rel")
    

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer,primary_key=True)
    name = Column(String(50))
    category_id = Column(Integer,ForeignKey("categories.id"))
    quantity = Column(Integer,default=0)
    price = Column(Float,default=0.0)
    
    category_rel = relationship("Category", back_populates="products")
    orders=relationship("Order",back_populates="product")

class Order(Base):

    __tablename__ = "orders"

    id=Column(Integer, primary_key=True)
    product_id= Column(Integer,ForeignKey("products.id"))
    user_id=Column(Integer, ForeignKey("users.id"))
    firstname=Column(String(50))
    lastname=Column(String(50))
    address=Column(String(100))

    product=relationship("Product",back_populates="orders")

    user=relationship("User",back_populates="orders")

class User(Base):
    __tablename__ = "users"

    id= Column(Integer, primary_key=True)
    name=Column(String(50))
    firstname=Column(String(50))
    lastname=Column(String(50))
    email=Column(String(50))
    orders=relationship("Order",back_populates="user")


DB_URL= "mysql+mysqlconnector://root:mysql1234@127.0.0.1:3306/my_db"

engine = create_engine(DB_URL, echo=True)

Base.metadata.create_all(engine)

Session = sessionmaker(autoflush=False,autocommit=False, bind=engine)



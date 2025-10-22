from fastapi import FastAPI, Depends,HTTPException,status
from db_models.models import Session,Product
from data_models.pyd_models import ProductModel,CategoryModel
# from  db_models.models import Product
from sqlalchemy.exc import IntegrityError, OperationalError
from pydantic import ValidationError

app=FastAPI()

def get_db():
    session=Session()
    try:
        yield session
    finally:
        session.close()

@app.get("/")
def get_root():
    return {"message":"Welcome to Happy shop"}
    

@app.post("/addProducts")
def add_products(new_product:ProductModel,session:Session= Depends(get_db)):
    try:
        prod=new_product.model_dump()
        db_prod= Product(**prod)
        session.add(db_prod)
        session.commit()
        session.refresh(db_prod)
    
    except IntegrityError:
        session.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, 
                detail="Data conflict (e.g., duplicate unique key or missing foreign key).")
    
    except OperationalError:
        # Catches connection issues, server offline, etc.
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database service is unavailable or connection failed."
        )
    # --- 2. Catch common application logic Errors (if not using global handlers) ---
    except AttributeError:
        # This usually signals a bug in your code
        session.rollback()
        print("LOG: Critical AttributeError detected in post creation logic.")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                            detail="A critical application error occurred.")

    except Exception as e:
        session.rollback()
        print(f"LOG: Unhandled exception: {e}") # Log the specific error for debugging
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                            detail="An unexpected internal error occurred.")
    
    return {"message":"Item added","item":db_prod}



from fastapi import FastAPI, HTTPException, Depends, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from typing import List
from database import Base, engine, get_db
from models import Apartments

# Create tables if they don't exist
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Static files (CSS, JS)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Templates
templates = Jinja2Templates(directory="templates")


# Display all apartments
@app.get("/")
def read_apartments(request: Request, db: Session = Depends(get_db)):
    apartments = db.query(Apartments).all()
    return templates.TemplateResponse("index.html", {"request": request, "apartments": apartments})


# Show create form
@app.get("/create")
def create_form(request: Request):
    return templates.TemplateResponse("create.html", {"request": request})


# Handle form submission
@app.post("/create")
def create_apartment_form(
        request: Request,
        id: int = Form(...),
        name: str = Form(...),
        age: int = Form(...),
        db: Session = Depends(get_db)
):
    db_apartment = db.query(Apartments).filter(Apartments.id == id).first()
    if db_apartment:
        return templates.TemplateResponse("create.html", {"request": request, "error": "ID already exists"})

    new_apartment = Apartments(id=id, name=name, age=age)
    db.add(new_apartment)
    db.commit()
    return templates.TemplateResponse("create.html", {"request": request, "success": "Apartment created!"})


# Show update form
@app.get("/update/{id}")
def update_form(request: Request, id: int, db: Session = Depends(get_db)):
    apartment = db.query(Apartments).filter(Apartments.id == id).first()
    if not apartment:
        return templates.TemplateResponse("index.html", {"request": request, "error": "Apartment not found"})
    return templates.TemplateResponse("update.html", {"request": request, "apartment": apartment})


# Handle update form
@app.post("/update/{id}")
def update_apartment_form(
        request: Request,
        id: int,
        name: str = Form(...),
        age: int = Form(...),
        db: Session = Depends(get_db)
):
    apartment = db.query(Apartments).filter(Apartments.id == id).first()
    if not apartment:
        return templates.TemplateResponse("index.html", {"request": request, "error": "Apartment not found"})

    apartment.name = name
    apartment.age = age
    db.commit()
    return templates.TemplateResponse("update.html",
                                      {"request": request, "apartment": apartment, "success": "Updated successfully!"})


# Delete apartment
@app.get("/delete/{id}")
def delete_apartment(id: int, db: Session = Depends(get_db)):
    apartment = db.query(Apartments).filter(Apartments.id == id).first()
    if apartment:
        db.delete(apartment)
        db.commit()
    return {"message": "Apartment deleted successfully"}

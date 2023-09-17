from fastapi import FastAPI, Body, Depends
import schemas
import models

from database import Base, engine, SessionLocal
from sqlalchemy.orm import Session

Base.metadata.create_all(engine)

def get_session():
    session = SessionLocal()
    try:
        yield session
    
    finally:
        session.close()


app = FastAPI()

fakeDatabase = {
    1: {'task': 'Clean Car' },
    2: {'task': 'Read book' },
    3: {'task': 'Trade'},
    4: {'task': 'Clean Car'},
}

@app.get("/api")
def getItems(session: Session = Depends(get_session)):
    items = session.query(models.Item).all()
    return items


@app.get("/api{id}")
def getItem(id:int, session: Session = Depends(get_session)):    
    item = session.query(models.Item).get(id)
    return item

'''
Method One
@app.post("/api")
def addItem(task:str):   
    newID = len(fakeDatabase.keys()) + 1
    fakeDatabase [newID] = {"task": item.task} 
    return fakeDatabase
'''

@app.post("/api")
def addItem(item:schemas.Item, session: Session = Depends(get_session)):   
    item = models.Item(task = item.task)
    session.add(item)
    session.commit()
    session.refresh(item) 
    return item


@app.put("/api{id}")
def updateItem(id:int, item:schemas.Item, session: Session = Depends(get_session)):
    itemObject = session.query(models.Item).get(id)
    itemObject.task = item.task
    session.commit()
    return itemObject   


@app.delete("/api{id}")
def deleteItem(id:int, session: Session = Depends(get_session)):
    itemObject = session.query(models.Item).get(id)
    session.delete(itemObject)
    session.commit()
    session.close()
    return "Item was deleted..."
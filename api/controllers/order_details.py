from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Response, Depends
from ..models import models, schemas


def create(db: Session, order_detail: schemas.OrderDetailCreate):
    # Create a new instance of the Order model with the provided data
    db_order_detail = models.OrderDetail(
        amount=order_detail.amount,
        order_id=order_detail.order_id,
        sandwich_id=order_detail.sandwich_id
    )
    # Add the newly created Order_detail object to the database session
    db.add(db_order_detail)
    # Commit the changes to the database
    db.commit()
    # Refresh the Order object to ensure it reflects the current state in the database
    db.refresh(db_order_detail)
    # Return the newly created Order object
    return db_order_detail


def read_all(db: Session):
    return db.query(models.OrderDetail).all()


def read_one(db: Session, order_detail_id: int):
    return db.query(models.OrderDetail).filter(models.OrderDetail.id == order_detail_id).first()


def update(db: Session, order_detail_id: int, order_detail: schemas.OrderDetailUpdate):
    # Query the database for the specific Order_Detail to update
    db_order_detail = db.query(models.OrderDetail).filter(models.OrderDetail.id == order_detail_id).first()
    # Extract the update data from the provided 'Order_Detail' object
    if not db_order_detail:
        raise HTTPException(status_code=404, detail="Order detail not found")
    for key, value in order_detail.dict(exclude_unset=True).items():
        setattr(db_order_detail, key, value)
    # Commit the changes to the database
    db.commit()
    # Refresh the Order_Detail object to ensure it reflects the current state in the database
    db.refresh(db_order_detail)
    # Return the updated Order_Detail object
    return db_order_detail


def delete(db: Session, order_detail_id: int):
    # Query the database for the specific Order_Detail to delete
    db_order_detail = db.query(models.OrderDetail).filter(models.OrderDetail.id == order_detail_id).first()
    if not db_order_detail:
        raise HTTPException(status_code=404, detail="Order detail not found")
    # Delete the database record without synchronizing the session
    db.delete(db_order_detail)
    # Commit the changes to the database
    db.commit()
    # Return a response with a status code indicating success (204 No Content)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

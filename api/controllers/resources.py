from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Response, Depends
from ..models import models, schemas


def create(db: Session, resource: schemas.ResourceCreate):
    # Create a new instance of the Resource model with the provided data
    db_resource = models.Resource(
        item=resource.item,
        amount=resource.amount
    )
    # Add the newly created Resource object to the database session
    db.add(db_resource)
    # Commit the changes to the database
    db.commit()
    # Refresh the resource object to ensure it reflects the current state in the database
    db.refresh(db_resource)
    # Refresh the resource object to ensure it reflects the current state in the database
    return db_resource


def read_all(db: Session):
    return db.query(models.Resource).all()


def read_one(db: Session, resource_id: int):
    return db.query(models.Resource).filter(models.Resource.id == resource_id).first()


def update(db: Session, resource_id: int, resource: schemas.ResourceUpdate):
    # Query the database for the specific resource to update
    db_resource = db.query(models.Resource).filter(models.Resource.id == resource_id).first()
    if not db_resource:
        raise HTTPException(statis_code=404, detail="Resource not found")
    # Update the database record with the new data, without synchronizing the session
    for key, value in resource.dict(exclude_unset=True).items():
        setattr(db_resource, key, value)
    # Commit the changes to the database
    db.commit()
    # Refresh the resource object to ensure it reflects the current state in the database
    db.refresh(db_resource)
    # Return the updated order record
    return db_resource


def delete(db: Session, resource_id: int):
    # Query the database for the specific resource to delete
    db_resource = db.query(models.Resource).filter(models.Resource.id == resource_id).first()
    if not db_resource:
        raise HTTPException(status_code=404, detail="Resource not found")
    # Delete the database record without synchronizing the session
    db.delete(db_resource)
    # Commit the changes to the database
    db.commit()
    # Return a response with a status code indicating success (204 No Content)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

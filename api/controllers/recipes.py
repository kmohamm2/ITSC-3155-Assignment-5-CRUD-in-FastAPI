from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Response, Depends
from ..models import models, schemas


def create(db: Session, recipe: schemas.RecipeCreate):
    # Create a new instance of the Recipe model with the provided data
    db_recipe = models.Recipe(
        amount=recipe.amount,
        sandwich_id=recipe.sandwich_id,
        resource_id=recipe.resource_id
    )
    # Add the newly created recipe object to the database session
    db.add(db_recipe)
    # Commit the changes to the database
    db.commit()
    # Refresh the recipe object to ensure it reflects the current state in the database
    db.refresh(db_recipe)
    # Return the newly created recipe object
    return db_recipe


def read_all(db: Session):
    return db.query(models.Recipe).all()


def read_one(db: Session, recipe_id: int):
    return db.query(models.Recipe).filter(models.Recipe.id == recipe_id).first()


def update(db: Session, recipe_id: int, recipe: schemas.RecipeUpdate):
    # Query the database for the specific recipe to update
    db_recipe = db.query(models.Recipe).filter(models.Recipe.id == recipe_id).first()
    if not db_recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    # Update the database record with the new data
    for key, value in recipe.dict(exclude_unset=True).items():
        setattr(db_recipe, key, value)
    # commit the database changes
    db.commit()
    # Refresh the recipe object to ensure it reflects the current state in the database
    db.refresh(db_recipe)
    # Return the updated recipe record
    return db_recipe


def delete(db: Session, recipe_id: int):
    # Query the database for the specific recipe to delete
    db_recipe = db.query(models.Recipe).filter(models.Recipe.id == recipe_id).first()
    if not db_recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    # Delete the database record without synchronizing the session
    db.delete(db_recipe)
    # commit database changes
    db.commit()
    # Return a response with a status code indicating success (204 No Content)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

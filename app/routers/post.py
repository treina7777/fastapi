from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from typing import  List, Optional  
from sqlalchemy.orm import Session  
from .. import models, schemas, oauth2
from .. database import get_db
from sqlalchemy import func

router=APIRouter(prefix='/posts', tags=['Posts'])

@router.get('/', response_model=List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db), limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    results = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(
        models.Post.title.contains(search)).limit(limit).offset(skip).all()
    
    return [schemas.PostOut(
        id=post.id,
        title=post.title,
        content=post.content,
        created_at=post.created_at,
        owner_id=post.owner_id,
        owner=post.owner,
        votes=votes
    ) for post, votes in results]

    
   

@router.post('/', status_code=status.HTTP_201_CREATED,
              response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, 
                 db: Session = Depends(get_db), 
                 current_user: int = Depends(oauth2.get_current_user)):
    # POST endpoint to create a new post
    # post: Validated request body according to PostCreate schema
    # status_code=201: Returns Created status
    new_post = models.Post(owner_id=current_user.id,**post.dict())  # Convert Pydantic model to dict and unpack into SQLAlchemy model
    db.add(new_post)  # Add new post to database session
    db.commit()  # Commit transaction
    db.refresh(new_post)  # Refresh instance with data from database (e.g., to get generated ID)
    return new_post

@router.get("/{id}", response_model=schemas.PostOut)
def get_post(id: int, db: Session = Depends(get_db)):
    # Query to retrieve the post and its vote count
    result = (
        db.query(models.Post, func.count(models.Vote.post_id).label("votes"))
        .join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True)
        .filter(models.Post.id == id)
        .group_by(models.Post.id)
        .first()
    )
    
    if not result:
        # Raise 404 if post not found
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={'message': f'ID: {id} was not found'}
        )
    
    post, votes = result  # Unpack the result
    # Return the formatted response
    return schemas.PostOut(
        id=post.id,
        title=post.title,
        content=post.content,
        created_at=post.created_at,
        owner_id=post.owner_id,
        owner=post.owner,
        votes=votes
    )

@router.delete("/{id}", response_model=schemas.Post)
def delete_post(id: int,
                db: Session = Depends(get_db),
                current_user: int = Depends(oauth2.get_current_user)):
    # DELETE endpoint to remove a post
    # Note: response_model should be removed as endpoint returns no content
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post is None:
        # Raise 404 if post not found
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'ID: {id} does not exist'
        )
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Not authorized to perform requested action')
    post_query.delete(synchronize_session=False)  # Delete post from database
    db.commit()  # Commit transaction
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, updated_post: schemas.PostCreate,
                 db: Session = Depends(get_db),
                 current_user: int = Depends(oauth2.get_current_user)):
    # PUT endpoint to update an existing post
    # updated_post: New post data validated against PostCreate schema
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post is None:
        # Raise 404 if post not found
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'ID: {id} does not exist'
        )
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Not authorized to perform requested action')
    # Update post with new data
    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()  # Commit transaction
    return post_query.first()  # Return updated post


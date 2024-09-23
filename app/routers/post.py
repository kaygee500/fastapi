#from operator import index
#from os import error
from typing import List, Optional
from fastapi import APIRouter, FastAPI, HTTPException, Response, status, Depends
from fastapi.params import Body

from random import randrange
#import psycopg2
#import time
#from psycopg2.extras import RealDictCursor
from sqlalchemy import func

from .. import models, schemas, oauth2
from ..database import engine, SessionLocal, get_db
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)

# # GET funtion for inbuilt array
# @router.get("/posts")
# def get_posts():
#     return {"data": my_posts}

# GET function using actual postgres database
@router.get("/", response_model = List[schemas.PostOut])
#def get_posts():
def get_posts(db: Session = Depends(get_db), limit: int = 2, skip: int = 0, search: Optional [str]=""):
    # cursor.execute("""SELECT * FROM posts""")
    # posts = cursor.fetchall()
    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    #print(posts)
    return posts

# #POST funtion for inbuilt array
# @router.post("/posts", status_code=status.HTTP_201_CREATED)
# def create_posts(post: Post):
#     post_dict = post.dict()
#     post_dict['id'] = randrange(0,1000000)
#     my_posts.append(post_dict)
#     return {"data": post_dict}

#POST funtion with postgresql
@router.post("/", status_code=status.HTTP_201_CREATED, response_model = schemas.Post)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db), 
                 current_user: int = Depends(oauth2.get_current_user)):
    
    # # cursor.execute(f" INSERT INTO (title, content, pulbished) posts VALUES {post.title}, {post.content}, {post.published}") --- Sucestible to sequel injection
    # cursor.execute(""" INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """, 
    #                (post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    # conn.commit()
    #print(new_post)
   
    #new_post = models.Post(title= post.title, content=post.content, published=post.published)  # can be repalce with upacked dictionary for better code management as the number of model fields increase
    print(current_user.email)
    new_post = models.Post(owner_id=current_user.id, **post.dict()) # Unpacked dictionary
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    
    return new_post


# #GET single item funtion for inbuilt array
# @router.get("/posts/{id}")
# def get_post(id: int):
#     post = find_post(id)
#     if not post:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
#                             detail=f"post with id: {id} was not found")
#     return {"detail": post}

#GET single item funtion with postgresql
@router.get("/{id}", response_model = schemas.PostOut)
def get_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    #cursor.execute("""SELECT * FROM posts WHERE id = %s""", str(id),) #convert id back to string
    #cursor.execute("""SELECT * FROM posts WHERE id = %s""", (id,)) # postgres will automatically convert ID to string
    #post = cursor.fetchone()
    #post = db.query(models.Post).filter(models.Post.id ==id).first()
    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id: {id} was not found")
    #print(post)
    return post

# #DELETE single item funtion for inbuilt array
# @router.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)
# def delete_post(id: int):
#     index = find_index_post(id)
#     if index == None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
#                             detail=f"post with id: {id} does not exit")
#     my_posts.pop(index)
#     return Response(status_code=status.HTTP_204_NO_CONTENT)

#DELETE single item funtion postgres
@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute(""" DELETE FROM posts WHERE id = %s RETURNING * """, (id,))
    # deleted_post = cursor.fetchone()
        
    post_query = db.query(models.Post).filter(models.Post.id ==id)
    
    post = post_query.first() 

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id: {id} does not exit")
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail=f"Not authorised")
    #conn.commit()
    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

# #UPDATE single item funtion for inbuilt array
# @router.put("/posts/{id}")
# def update_post(id: int, post: Post):
#     index = find_index_post(id)

#     if index == None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
#                             detail=f"post with id: {id} does not exit")
#     post_dict = post.dict()
#     post_dict['id'] = id

#     my_posts[index]= post_dict
#     return {"data": post_dict}

#UPDATE single item funtion with postgres
@router.put("/{id}", response_model = schemas.Post)
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    # cursor.execute(""" UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING * """, 
    #                (post.title, post.content, post.published, id,))
    
    # updated_post = cursor.fetchone()
    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()
    
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id: {id} does not exit")
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail=f"Not authorised")
    
    post_query.update(updated_post.dict(), synchronize_session=False)
  
    #conn.commit()
    db.commit()

    return post_query.first()


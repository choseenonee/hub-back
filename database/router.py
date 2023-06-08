from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import CRUD, schemas, models
from database.database import SessionLocal, engine
from typing import List, Union

router = APIRouter(
    prefix='/database',
    tags=['Database'],
)


models.Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get('/get_user/', response_model=schemas.User)
def get_user(db: Session = Depends(get_db), user_id: int | None = None, email: str | None = None,
             nickname: str | None = None, phone_number: str | None = None):
    try:
        auth = CRUD.get_user_auth(db=db, user_id=user_id, email=email,
                                  nickname=nickname, phone_number=phone_number)
    except Exception as e:
        raise HTTPException(status_code=500, detail='failed to get user')
    if auth is None:
        raise HTTPException(status_code=404, detail='user not found')
    return auth.user


@router.post('/create_user/', response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    try:
        user = CRUD.create_user(db, user)
    except:
        raise HTTPException(status_code=500, detail='failed to create user')
    return user


@router.post('/update_user')
def update_user(update_data: schemas.UserUpdate, db: Session = Depends(get_db), user_id: int | None = None,
                email: str | None = None, nickname: str | None = None,
                phone_number: str | None = None):
    return CRUD.update_user(db=db, update_data=update_data, user_id=user_id, email=email, nickname=nickname,
                            phone_number=phone_number)


@router.delete('/delete_user/')
def delete_user(db: Session = Depends(get_db), user_id: int | None = None, email: str | None = None,
                nickname: str | None = None, phone_number: str | None = None):
    return CRUD.delete_user(db=db, user_id=user_id, email=email, nickname=nickname,
                            phone_number=phone_number)


@router.post('/create_tag', response_model=schemas.Tag)
def create_tag(tag: schemas.CreateTag, db: Session = Depends(get_db)):
    return CRUD.create_tag(db, tag)


@router.delete('/delete_tag')
def delete_tag(tag_id: int, db: Session = Depends(get_db)):
    return CRUD.delete_tag(db=db, tag_id=tag_id)


@router.get('/get_users_by_tag', response_model=List[schemas.User])
def get_users_by_tag(tag: str, db: Session = Depends(get_db)):
    return CRUD.get_users_by_tag(db=db, tag=tag)


@router.post('/create_fav/', response_model=Union[schemas.FavColab, schemas.FavArchive, schemas.FavUser])
def create_fav(fav_archive: schemas.CreateFavArchive | None = None,
               fav_user: schemas.CreateFavUser | None = None, db: Session = Depends(get_db),
               fav_colab: schemas.CreateFavColab | None = None):
    if fav_colab is not None:
        return CRUD.create_fav_colab(db, fav_colab=fav_colab)
    elif fav_archive is not None:
        return CRUD.create_fav_archive(db, fav_archive=fav_archive)
    elif fav_user is not None:
        return CRUD.create_fav_user(db, fav_user=fav_user)
    else:
        raise HTTPException(status_code=400, detail='None of the fav was post')


@router.get('/get_users_by_fav_id', response_model=List[schemas.User])
def get_users_by_fav_colab_id(colab_id: int | None = None, archive_id: int | None = None, fav_user_id: int | None = None,
                              db: Session = Depends(get_db)):
    if colab_id is not None:
        return CRUD.get_users_by_colab_id(db, colab_id=colab_id)
    elif archive_id is not None:
        return CRUD.get_users_by_archive_id(db, archive_id=archive_id)
    elif fav_user_id is not None:
        return CRUD.get_users_by_fav_user_id(db, fav_user_id=fav_user_id)
    else:
        raise HTTPException(status_code=400, detail='None of the fav has tried to be get')


@router.delete('/delete_fav')
def delete_fav(db: Session = Depends(get_db), colab_id: int | None = None, archive_id: int | None = None, fav_user_id: int | None = None):
    if colab_id is not None:
        return CRUD.delete_fav_colab(db, fav_colab_id=colab_id)
    elif archive_id is not None:
        return CRUD.delete_fav_archive(db, fav_archive_id=archive_id)
    elif fav_user_id is not None:
        return CRUD.delete_fav_user(db, fav_user_id=fav_user_id)
    else:
        raise HTTPException(status_code=400, detail='None of the fav has tried to be deleted')
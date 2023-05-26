from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from database import schemas, CRUD, database, models
from database.database import SessionLocal, engine
from typing import List, Union, Dict
from uuid import UUID

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get('/get_user/', response_model=schemas.User)
def get_user(db: Session = Depends(get_db), user_id: int | None = None, email: str | None = None,
             nickname: str | None = None, phone_number: str | None = None):
    try:
        auth = CRUD.get_user_auth(db=db, user_id=user_id, email=email,
                                  nickname=nickname, phone_number=phone_number)
    except Exception as e:
        raise HTTPException(status_code=500, detail='failed to get user')
    if auth is None:
        raise HTTPException(status_code=404, detail='user not found')
    # print([(key, auth.user.tags[0].__dict__[key]) for key in auth.user.tags[0].__dict__ if (key != '_sa_adapter' and key != '_sa_instance_state')])
    return auth.user


@app.post('/create_user/', response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    try:
        user = CRUD.create_user(db, user)
    except:
        raise HTTPException(status_code=500, detail='failed to create user')
    return user


@app.post('/update_user')
def update_user(update_data: schemas.UserUpdate, db: Session = Depends(get_db), user_id: int | None = None,
                email: str | None = None, nickname: str | None = None,
                phone_number: str | None = None):
    return CRUD.update_user(db=db, update_data=update_data, user_id=user_id, email=email, nickname=nickname,
                            phone_number=phone_number)


@app.delete('/delete_user/')
def delete_user(db: Session = Depends(get_db), user_id: int | None = None, email: str | None = None,
                nickname: str | None = None, phone_number: str | None = None):
    return CRUD.delete_user(db=db, user_id=user_id, email=email, nickname=nickname,
                            phone_number=phone_number)


@app.post('/create_tag', response_model=schemas.Tag)
def create_tag(tag: schemas.CreateTag, db: Session = Depends(get_db)):
    return CRUD.create_tag(db, tag)


@app.get('/get_users_by_tag', response_model=List[schemas.User])
def get_users_by_tag(tag: str, db: Session = Depends(get_db)):
    return CRUD.get_users_by_tag(db=db, tag=tag)


@app.post('/create_fav/', response_model=Union[schemas.FavColab, schemas.FavArchive, schemas.FavUser])
def create_fav(fav_colab: Union[schemas.CreateFavColab, None], fav_archive: Union[schemas.CreateFavArchive, None],
               fav_user: Union[schemas.CreateFavUser, None], db: Session = Depends(get_db)):
    if fav_colab is not None:
        return CRUD.create_fav_colab(db, fav_colab=fav_colab)
    elif fav_archive is not None:
        return CRUD.create_fav_archive(db, fav_archive=fav_archive)
    elif fav_user is not None:
        return CRUD.create_fav_user(db, fav_user=fav_user)
    else:
        raise HTTPException(status_code=400, detail='None of the fav was post')


@app.get('/get_users_by_fav_id', response_model=List[schemas.User])
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


@app.delete('/delete_fav')
def delete_fav(db: Session = Depends(get_db), colab_id: int | None = None, archive_id: int | None = None, fav_user_id: int | None = None):
    if colab_id is not None:
        return CRUD.delete_fav_colab(db, fav_colab_id=colab_id)
    elif archive_id is not None:
        return CRUD.delete_fav_archive(db, fav_archive_id=archive_id)
    elif fav_user_id is not None:
        return CRUD.delete_fav_user(db, fav_user_id=fav_user_id)
    else:
        raise HTTPException(status_code=400, detail='None of the fav has tried to be deleted')


# @app.post('/create_fav_archive', response_model=schemas.FavArchive)
# def create_fav_archive(fav_archive: schemas.CreateFavArchive, db: Session = Depends(get_db)):
#     return CRUD.create_fav_archive(db, fav_archive=fav_archive)
#
#
# @app.get('/get_users_by_fav_archive_id', response_model=List[schemas.User])
# def get_users_by_fav_archive_id(archive_id: int, db: Session = Depends(get_db)):
#     return CRUD.get_users_by_archive_id(db=db, archive_id=archive_id)
#
#
# @app.post('/create_fav_user', response_model=schemas.FavUser)
# def create_fav_user(fav_user: schemas.CreateFavUser, db: Session = Depends(get_db)):
#     return CRUD.create_fav_user(db, fav_user=fav_user)
#
#
# @app.get('/get_users_by_fav_user_id', response_model=List[schemas.User])
# def get_users_by_fav_user_id(fav_user_id: int, db: Session = Depends(get_db)):
#     return CRUD.get_users_by_fav_user_id(db=db, fav_user_id=fav_user_id)

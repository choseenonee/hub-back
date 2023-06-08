from sqlalchemy.orm import Session
from fastapi import HTTPException
from . import models, schemas, hash


def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(nickname=user.nickname, name=user.name, surname=user.surname,
                          grade=user.grade, contacts=user.contacts, description=user.description,
                          avatar_uuid=user.avatar_uuid, is_admin=user.is_admin, is_teacher=user.is_teacher)
    try:
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
    except Exception as e:
        raise HTTPException(status_code=500, detail='failed to create user')
    db_authorization = models.Authorization(user_id=db_user.id, email=user.email, nickname=user.nickname,
                                            phone_number=user.phone_number, hashed_password=hash.get_hashed_password(user.password))
    db.add(db_authorization)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user_auth(db: Session, user_id: int | None = None, email: str | None = None,
                  nickname: str | None = None, phone_number: str | None = None):
    if email:
        auth = db.query(models.Authorization).filter(models.Authorization.email == email).first()
    elif nickname:
        auth = db.query(models.Authorization).filter(models.Authorization.nickname == nickname).first()
    elif phone_number:
        auth = db.query(models.Authorization).filter(models.Authorization.phone_number == phone_number).first()
    elif user_id:
        auth = db.query(models.Authorization).filter(models.Authorization.user_id == user_id).first()
    return auth


def delete_user(db: Session, user_id: int | None = None, email: str | None = None, nickname: str | None = None, phone_number: str | None = None):
    auth = get_user_auth(db, user_id=user_id, email=email, nickname=nickname, phone_number=phone_number)
    if not auth:
        raise HTTPException(status_code=404, detail='user not found')
    try:
        for fav_colab in auth.user.fav_colabs:
            delete_fav_colab(db=db, fav_colab_id=fav_colab.id)
    except:
        pass
    try:
        for fav_archive in auth.user.fav_archives:
            delete_fav_archive(db=db, fav_archive_id=fav_archive.id)
    except:
        pass
    try:
        for tag in auth.user.tags:
            delete_tag(db=db, tag_id=tag.id)
    except:
        pass
    try:
        db.delete(auth.user)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail='failed to delete user')
    try:
        db.delete(auth)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail='failed to delete auth')
    try:
        db.commit()
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail='failed to commit db while deleting')
    return 200


def update_user(db: Session, update_data: schemas.UserUpdate, user_id: int | None=None, email: str | None=None, nickname: str | None=None,
                phone_number: str | None = None):
    auth = get_user_auth(db, user_id=user_id, email=email, nickname=nickname, phone_number=phone_number)
    if auth is None:
        raise HTTPException(status_code=404, detail='user not found')
    if auth.user is None:
        raise HTTPException(status_code=500, detail='there is auth, but no user matching to it!!! check the database!!!')
    for key, value in dict(update_data).items():
        if value:
            setattr(auth, key, value)
            setattr(auth.user, key, value)
    try:
        # db.add(user)
        # print(auth.user.nickname)
        db.commit()
        # db.refresh(auth.user)
        return 200
    except Exception as e:
        raise HTTPException(status_code=500, detail='failed to commit db')


def create_tag(db: Session, tag: schemas.CreateTag):
    db_user_tags = [tag.tag for tag in db.query(models.User).filter(models.User.id == tag.user_id).first().tags]
    # print(db_user_tags)
    if tag.tag in db_user_tags:
        raise HTTPException(status_code=400, detail='you are trying to make a duplicate!!!')
    db_tag = models.Tag(user_id=tag.user_id, tag=tag.tag)
    try:
        db.add(db_tag)
        db.commit()
        db.refresh(db_tag)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail='failed to create tag')
    return db_tag


def get_users_by_tag(db: Session, tag: str):
    tags = db.query(models.Tag).filter(models.Tag.tag == tag).all()
    # print(tags)
    if len(tags) == 0:
        raise HTTPException(status_code=404, detail='tags not found')
    users = [tag.user for tag in tags]
    return users


def create_fav_colab(db: Session, fav_colab: schemas.CreateFavColab):
    db_colab = models.FavColab(user_id=fav_colab.user_id, colab_id=fav_colab.colab_id)
    try:
        db_user_fav_colabs = [favcolab.colab_id for favcolab in db.query(models.User).filter(models.User.id == fav_colab.user_id).first().fav_colabs]
        if fav_colab.colab_id in db_user_fav_colabs:
            raise HTTPException(status_code=400, detail='you are trying to make a duplicate!!!')
    except Exception as e:
        print(e)
    try:
        db.add(db_colab)
        db.commit()
        db.refresh(db_colab)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail='failed to create fav colab')
    return db_colab


def get_users_by_colab_id(db: Session, colab_id: int):
    fav_colabs = db.query(models.FavColab).filter(models.FavColab.colab_id == colab_id).all()
    if len(fav_colabs) == 0:
        raise HTTPException(status_code=404, detail='fav colabs not found')
    users = [fav_colab.user for fav_colab in fav_colabs]
    return users


def create_fav_archive(db: Session, fav_archive: schemas.CreateFavArchive):
    db_archive = models.FavArchive(user_id=fav_archive.user_id, archive_id=fav_archive.archive_id)
    try:
        db_user_fav_archives = [favarchive.archive_id for favarchive in db.query(models.User).filter(models.User.id == fav_archive.user_id).first().fav_archives]
        if fav_archive.archive_id in db_user_fav_archives:
            raise HTTPException(status_code=400, detail='you are trying to make a duplicate!!!')
    except:
        pass
    try:
        db.add(db_archive)
        db.commit()
        db.refresh(db_archive)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail='failed to create fav archive')
    return db_archive


def get_users_by_archive_id(db: Session, archive_id: int):
    fav_archives = db.query(models.FavArchive).filter(models.FavColab.colab_id == archive_id).all()
    users = [fav_archive.user for fav_archive in fav_archives]
    return users


def create_fav_user(db: Session, fav_user: schemas.CreateFavUser):
    db_fav_user = models.FavUser(user_id=fav_user.user_id, fav_user_id=fav_user.fav_user_id)
    try:
        db_user_fav_users = [fav_user.fav_user_id for fav_user in db.query(models.User).filter(models.User.id == fav_user.user_id).first().fav_users]
        if fav_user.fav_user_id in db_user_fav_users:
            raise HTTPException(status_code=400, detail='you are trying to make a duplicate!!!')
    except Exception as e:
        print(e)
    try:
        db.add(db_fav_user)
        db.commit()
        db.refresh(db_fav_user)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail='failed to create fav user')
    return db_fav_user


def get_users_by_fav_user_id(db: Session, fav_user_id: int):
    fav_users = db.query(models.FavUser).filter(models.FavUser.fav_user_id == fav_user_id).all()
    users = [fav_user.main_user for fav_user in fav_users]
    return users


def delete_fav_colab(db: Session, fav_colab_id: int):
    try:
        db_fav_colab = db.query(models.FavColab).filter(models.FavColab.id == fav_colab_id).first()
    except Exception as e:
        print(e)
        raise HTTPException(status_code=404, detail='fav colab not found')
    try:
        db.delete(db_fav_colab)
        db.commit()
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail='failed to delete fav colab')
    return 200


def delete_fav_archive(db: Session, fav_archive_id: int):
    try:
        db_fav_archive = db.query(models.FavArchive).filter(models.FavArchive.id == fav_archive_id).first()
    except Exception as e:
        print(e)
        raise HTTPException(status_code=404, detail='fav archive not found')
    try:
        db.delete(db_fav_archive)
        db.commit()
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail='failed to delete fav archive')
    return 200


def delete_fav_user(db: Session, fav_user_id: int):
    try:
        db_fav_user = db.query(models.FavUser).filter(models.FavUser.id == fav_user_id).first()
    except Exception as e:
        print(e)
        raise HTTPException(status_code=404, detail='fav user not found')
    try:
        db.delete(db_fav_user)
        db.commit()
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail='failed to delete fav user')
    return 200


def delete_tag(db: Session, tag_id: int):
    try:
        db_tag = db.query(models.Tag).filter(models.Tag.id == tag_id).first()
    except Exception as e:
        print(e)
        raise HTTPException(status_code=404, detail='tag not found')
    try:
        db.delete(db_tag)
        db.commit()
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail='failed to delete tag')
    return 200
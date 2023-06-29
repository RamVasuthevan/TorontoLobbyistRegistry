
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import IntegrityError
from typing import List, Dict



#https://skien.cc/blog/2014/02/06/sqlalchemy-and-race-conditions-follow-up-on-commits-and-flushes/
def get_one_or_create(session,
                      model,
                      create_method='',
                      create_method_kwargs=None,
                      **kwargs):
    try:
        return session.query(model).filter_by(**kwargs).one(), True
    except NoResultFound:
        kwargs.update(create_method_kwargs or {})
        created = getattr(model, create_method, model)(**kwargs)
        try:
            session.add(created)
            session.flush()
            return created, False
        except IntegrityError:
            session.rollback()
            return session.query(model).filter_by(**kwargs).one(), True
        
def get_one_or_create_all(session, model, create_method='', create_method_kwargs=None, instances: List[Dict] = []):
    created_instances = []
    for kwargs in instances:
        try:
            instance = session.query(model).filter_by(**kwargs).one()
            created_instances.append((instance, True))
        except NoResultFound:
            kwargs.update(create_method_kwargs or {})
            created = getattr(model, create_method, model)(**kwargs)
            try:
                session.add(created)
                created_instances.append((created, False))
            except IntegrityError:
                session.rollback()
                instance = session.query(model).filter_by(**kwargs).one()
                created_instances.append((instance, True))

    # flush the session once after processing all instances
    session.flush()
    return created_instances

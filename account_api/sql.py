from account_api import db
from sqlalchemy import create_engine, or_, and_, text
from account_api.models import User, Roles


class Sql(object):
    # create a Session
    session = db.session

# start of search sql statements
    def get_users(params):
        variable = Sql.session.query(User).filter_by(**params).all()

        return variable


# start of insert sql Statements

    def new_user(params):
        print("trying to add new user", flush=True)
        try_newclient = User(**params)
        Sql.session.add(try_newclient)
        Sql.session.commit()
        print("added new user", flush=True)
        return Sql.get_users(try_newclient.to_dict())

    def new_role(params):
        try_newrole = Roles(**params)
        Sql.session.add(try_newrole)
        Sql.session.commit()
        return Sql.get_role(try_newrole.to_dict())

# start of update sql Statements

    def update_user(id, user_id, params):
        updating = Sql.session.query(User).get(id)
        for key, value in params.items():
            setattr(updating, key, value)
        Sql.session.commit()
        return Sql.get_users({'id': user_id})

    def delete_user(id):
        variable = Sql.session.query(v).filter(User.id == id).delete()
        Sql.session.commit()

        return "deleted"

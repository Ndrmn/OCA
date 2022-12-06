from app import db, login
from sqlalchemy import Float, Integer, String
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


@login.user_loader
def load_user(id):
    return Users.query.get(int(id))


class MixinAddPrintedMethods():
    id = db.Column(Integer, primary_key=True)

    @staticmethod
    def _sort_list_by_order(ordered_list, order_list: None):
        id_el = None
        for el in ordered_list:
            if type(el) is dict and el.get('id') == 'id':
                id_el = el
                break
        if id_el is not None:
            ordered_list.remove(id_el)
            ordered_list = [id_el] + ordered_list
        return ordered_list

    @classmethod
    def get_list_names_attrs(cls):
        keys = [key for key in cls.__dict__ if key[0] != '_' and not callable(getattr(cls, key))]
        table_headers_and_rules = []
        for key in keys:
            col_rules = {}
            col_rules['id'] = key
            col_rules['name'] = key.capitalize().replace('_', ' ')
            if key == 'id':
                col_rules['hidden'] = 'true'
                col_rules['attributes'] = False  # cat change cell
            else:
                col_rules['attributes'] = True  # cat change cell

            table_headers_and_rules.append(col_rules)

        table_headers_and_rules = cls._sort_list_by_order(table_headers_and_rules, None)

        return table_headers_and_rules

    def values_to_dict(self):
        attrs = {key['id']: self.__dict__[key['id']] for key in self.get_list_names_attrs()}
        return attrs


class Users(UserMixin, db.Model, MixinAddPrintedMethods):
    __tablename__ = "users"
    username = db.Column(String(64), index=True, unique=True)
    password_hash = db.Column(String(128))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Measurement(UserMixin, db.Model, MixinAddPrintedMethods):
    __tablename__ = "measurement"
    measurement = db.Column(String(20), nullable=False, unique=True)


class Currencies(UserMixin, db.Model, MixinAddPrintedMethods):
    __tablename__ = "currencies"
    currencies = db.Column(String(10), nullable=False, index=True, unique=True)
    exchange_rates = db.Column(Float, nullable=False)


accessed_tables = (Measurement, Currencies)

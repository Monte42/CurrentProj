from paintings_app.config.mysqlconnection import connectToMySQL, db
from paintings_app.models import user
from flask import flash,session


# ===================
# INITIALIZE INSTANCE
# ===================
class Painting:
    def __init__(self, data):
        self.id = data['id']
        self.user_id = data['user_id']
        self.title = data['title']
        self.description = data['description']
        self.price = data['price']
        self.quantity = data['quantity']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user = None
        self.purchases = None


    # INSTANCE METHODS




    # =============
    # CLASS METHODS
    # =============

    # ===========
    #  CREATE SQL
    # ===========
    @classmethod
    def create_painting(cls,form_data):
        data = cls.parse_painting_data(form_data)
        if not cls.validate_painting_form(data): return False
        query = '''
        INSERT INTO paintings
        (user_id,title,description,price,quantity)
        VALUES
        (%(user_id)s,%(title)s,%(description)s,%(price)s,%(quantity)s);
        '''
        return connectToMySQL(db).query_db(query,data)


    # ========
    # READ SQL
    # ========
    @classmethod
    def get_all_paintings(cls):
        query = '''
        SELECT *
        FROM paintings
        LEFT JOIN users
        ON paintings.user_id = users.id;
        '''
        all_paintings = []
        results = connectToMySQL(db).query_db(query)
        if results:
            for row in results:
                this_painting = cls(row)
                user_data = {
                    'id': row['users.id'],
                    'first_name': row['first_name'],
                    'last_name': row['last_name'],
                    'email': row['email'],
                    'password': row['password'],
                    'created_at': row['users.created_at'],
                    'updated_at': row['users.updated_at']
                }
                this_painting.user = user.User(user_data)
                all_paintings.append(this_painting)
        return all_paintings

    @classmethod
    def get_painting_by_id(cls, id):
        data = {'id': id}
        query = '''
        SELECT *, 
        COUNT(purchases.painting_id)
        AS purchases
        FROM paintings
        LEFT JOIN users
        ON paintings.user_id = users.id
        LEFT JOIN purchases
        ON purchases.painting_id = paintings.id
        WHERE paintings.id = %(id)s;
        '''
        results = connectToMySQL(db).query_db(query,data)
        if results:
            this_painting = cls(results[0])
            user_data = {
                    'id': results[0]['users.id'],
                    'first_name': results[0]['first_name'],
                    'last_name': results[0]['last_name'],
                    'email': results[0]['email'],
                    'password': results[0]['password'],
                    'created_at': results[0]['users.created_at'],
                    'updated_at': results[0]['users.updated_at']
                }
            this_painting.user = user.User(user_data)
            this_painting.purchases = results[0]['purchases']
            return this_painting
        return False



    # ==========
    # UPDATE SQL
    # ==========
    @classmethod
    def update_painting(cls,form_data,id):
        data = cls.parse_painting_data(form_data)
        data['id'] = id
        if not cls.validate_painting_form(data): return False
        query = '''
        UPDATE paintings
        SET
        title = %(title)s,
        description = %(description)s,
        price = %(price)s,
        quantity = %(quantity)s
        WHERE id = %(id)s;
        '''
        connectToMySQL(db).query_db(query,data)
        return True



    # ==========
    # DELETE SQL
    # ==========
    @classmethod
    def delete_painting(cls,id):
        data = {'id':id}
        query = '''
        DELETE FROM paintings
        WHERE id = %(id)s;
        '''
        return connectToMySQL(db).query_db(query,data)




    # ==============
    # STATIC METHODS
    # ==============

    # FORM VALIDATIONS
    @staticmethod
    def validate_painting_form(parsed_data):
        is_valid = True
        if len(parsed_data['title']) < 2:
            flash('Painting Title must be atleast 2 characters long')
            is_valid = False
        if len(parsed_data['description']) < 10:
            flash('Painting Title must be more detailed')
            is_valid = False
        if parsed_data['price'] <= 0:
            flash("Price can't be 0 or less")
            is_valid = False
        if parsed_data['quantity'] <= 0:
            flash("Quantity can't be 0 or less")
            is_valid = False
        return is_valid

    @staticmethod
    def parse_painting_data(form_data):
        parsed_data = {}
        parsed_data['user_id'] = session['user_id']
        parsed_data['title'] = form_data['title']
        parsed_data['description'] = form_data['description']
        parsed_data['price'] = float(form_data['price'])
        parsed_data['quantity'] = int(form_data['quantity'])
        return parsed_data
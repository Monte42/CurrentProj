from paintings_app.config.mysqlconnection import connectToMySQL, db
from paintings_app.models import user, painting
from flask import session


# ===================
# INITIALIZE INSTANCE
# ===================
class Purchase:
    def __init__(self,data):
        self.user_id = data['user_id']
        self.painting_id = data['painting_id']
        self.user = None
        self.painting = None



    # =============
    # CLASS METHODS
    # =============

    # ===========
    #  CREATE SQL
    # ===========
    @classmethod
    def create_purchase(cls,painting_id):
        data = {
            'user_id': session['user_id'],
            'painting_id': painting_id
        }
        query = '''
        INSERT INTO purchases
        (user_id, painting_id)
        VALUES
        (%(user_id)s,%(painting_id)s);
        '''
        return connectToMySQL(db).query_db(query,data)



    # =================================
    # READ SQL -- just to show cls ass.
    # =================================
    classmethod
    def get_all_purchases(cls):
        query = '''
        SELECT * FROM purchases
        JOIN users
        ON purchases.user_id = users.id
        JOIN paintings
        ON purchases.painting_id = paintings.id;
        '''
        results = connectToMySQL(db).query_db(query)
        all_purchases = []
        if results:
            for row in results:
                this_purchase = cls(row)
                user_data = {
                    'id': row['users.id'],
                    'first_name': row['first_name'],
                    'last_name': row['last_name'],
                    'email': row['email'],
                    'password': row['password'],
                    'created_at': row['users.created_at'],
                    'updated_at': row['users.updated_at']
                }
                painting_data = {
                    'id': row['paintings.id'],
                    'title': row['title'],
                    'description': row['description'],
                    'price': row['price'],
                    'quantity': row['quantity'],
                    'created_at': row['paintings.created_at'],
                    'updated_at': row['paintings.updated_at']
                }
                this_purchase.user = user.User(user_data)
                this_purchase.paint = painting.Painting(painting_data)
                all_purchases.append(this_purchase)
            return all_purchases
        return False



    # ==========
    # DELETE SQL
    # ==========
    @classmethod
    def cancel_order(cls,id):
        data = {'id':id}
        query = '''
        DELETE FROM purchases
        WHERE id = %(id)s;
        '''
        return connectToMySQL(db).query_db(query,data)
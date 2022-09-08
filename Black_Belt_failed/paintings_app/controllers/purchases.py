from paintings_app import app
from flask import redirect, flash
from paintings_app.models import purch




# ====================
# CREATE/DELETE ROUTES
# ====================
@app.route('/purchase/<int:id>')
def make_purchase(id):
    purch.Purchase.create_purchase(id)
    flash('Order Successful')
    return redirect(f'/paintings/{id}')

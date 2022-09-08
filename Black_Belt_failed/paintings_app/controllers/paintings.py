from paintings_app import app
from flask import render_template, redirect, request,flash, session
from paintings_app.models import painting, user


# =============
#  CREATE ROUTE
# =============
@app.route('/paintings/new', methods=['GET','POST'])
def create_new_painting():
    if not session.get('user_id'): return redirect('/')
    if request.method == 'GET':
        return render_template('paintings/create_painting.html', data=None)
    if painting.Painting.create_painting(request.form):
        return redirect('/paintings')
    return render_template('paintings/create_painting.html', data = request.form)



# ===========
# READ ROUTE
# ===========
@app.route('/paintings')
def show_all_paintings():
    if not session.get('user_id'): return redirect('/')
    all_paintings = painting.Painting.get_all_paintings()
    this_user = user.User.get_user_by_id(session['user_id'])
    return render_template('paintings/all_paintings.html',paintings=all_paintings,user=this_user)

@app.route('/paintings/<int:id>')
def show_single_painting(id):
    if not session.get('user_id'): return redirect('/')
    this_painting = painting.Painting.get_painting_by_id(id)
    if not this_painting:
        flash('This painting does not exist')
        return redirect('/paintings')
    return render_template('paintings/single_painting.html',painting=this_painting)



# ============
# UPDATE ROUTE
# ============
@app.route('/paintings/<int:id>/edit',  methods = ["GET","POST"])
def edit_painting(id):
    if not session.get('user_id'):return redirect('/')
    if request.method == 'GET':
        this_painting = painting.Painting.get_painting_by_id(id)
        if not this_painting:
            flash('This painting does not exist...')
            return redirect('/paintings')
        if this_painting.user_id == session['user_id']:return render_template('paintings/edit_painting.html', data=this_painting)
        flash('You are not authorized to do that!')
        return redirect('/paintings')
    if painting.Painting.update_painting(request.form,id):return redirect(f'/paintings/{id}')
    return redirect(f'/paintings/{id}/edit')



# ============
# DELETE ROUTE
# ============
@app.route('/paintings/<int:id>/delete')
def delete_painting(id):
    if not session.get('user_id'):return redirect('/')
    this_painting = painting.Painting.get_painting_by_id(id)
    if not this_painting:
            flash('This painting does not exist...')
            return redirect('/paintings')
    if this_painting.user_id != session['user_id']:
        flash('You are not authorized to do that!')
        return redirect('/paintings')
    painting.Painting.delete_painting(id)
    return redirect('/paintings')
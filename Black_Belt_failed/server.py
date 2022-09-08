from paintings_app import app
from paintings_app.controllers import users, paintings, purchases

if __name__ == "__main__":
    app.run(debug=True)
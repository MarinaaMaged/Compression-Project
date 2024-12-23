from flask import Flask
from Website.app.routes import main  # Import the blueprint from routes.py
import os


app = Flask(__name__,  template_folder=os.path.join(os.getcwd(), 'Website/app/templates'),  # Path to templates
    static_folder=os.path.join(os.getcwd(), 'Website/app/static')   )


app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), 'uploads')  # Set upload folder
app.config['ALLOWED_EXTENSIONS'] = {'txt', 'bin'}  # Set allowed file extensions


if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])


app.register_blueprint(main)

# Run the app
if __name__ == '__main__':
    app.run(debug=True)

from flaskblog import create_app, socketio
import atexit

app = create_app()

def OnExitApp():
    print("exit Flask application")
atexit.register(OnExitApp)

if __name__ == '__main__':
   socketio.run(app,host='0.0.0.0', port=8000, debug=True)
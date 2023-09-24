import subprocess
import sys

def install_dependencies():
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])
        print("\n\n\n libraries downloaded\n\n\n")
    except subprocess.CalledProcessError:
        print("library installation failed")

def run_flask_app():
    try:
        print("app going to import")
        from app import app
        print("app imported?")
        app.run(debug=False)
        print("\n\n\nFlask app running\n\n\n")
    except ImportError:
        print("import failed")

if __name__ == '__main__':
    install_dependencies()
    run_flask_app()
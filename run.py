from app import create_app

app = create_app('development')  # Change to 'production' for Docker

if __name__ == '__main__':
    app.run(debug=True)
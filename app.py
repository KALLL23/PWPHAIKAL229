from app import create_app

# Buat instance aplikasi menggunakan factory pattern
app = create_app()

if __name__ == '__main__':
    app.run(debug=True)

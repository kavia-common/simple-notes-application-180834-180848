from app import app

if __name__ == "__main__":
    # Bind to 0.0.0.0:3001 to work with the preview system
    app.run(host="0.0.0.0", port=3001, threaded=True)

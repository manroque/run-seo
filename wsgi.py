from app import app

if __name__ == "__main__":
    app.debug = True  # <–– ativa logs mais verbosos
    app.run(host="0.0.0.0", port=8080)

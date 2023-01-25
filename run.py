from app import app, db, config

if __name__ == '__main__':
    with app.app_context():
        configuration = config.Config()
    app.run(host=configuration.HOST, port=configuration.PORT,
            debug=configuration.DEBUG)

from ticksupport import create_app

app = create_app()
app.config.from_object('config.DevConfig')

if __name__ == "__main__":
    app.run(host='0.0.0.0')

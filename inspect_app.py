import reflex as rx
print(dir(rx.App))
try:
    app = rx.App()
    print("App instance attributes:", dir(app))
    if hasattr(app, 'api'):
        print("Has api")
    else:
        print("No api")
    if hasattr(app, 'add_api_route'):
        print("Has add_api_route")
except Exception as e:
    print(e)

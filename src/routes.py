from .users import Register, Login

def initialize_routes(api):
    api.add_resource(Register, "/register")
    api.add_resource(Login, "/login")
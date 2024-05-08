from .users import Register, Login
from .flood import SafeLocations, FloodHistory

def initialize_routes(api):
    api.add_resource(Register, "/register")
    api.add_resource(Login, "/login")
    api.add_resource(SafeLocations, "/safelocations")
    api.add_resource(FloodHistory, "/floodhistory")
    
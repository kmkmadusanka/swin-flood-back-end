from .users import Register, Login
from .flood import SafeLocations, FloodHistory, FloodSeverity
from .discussion import Discussion
from .prediction import Predict

def initialize_routes(api):
    api.add_resource(Register, "/register")
    api.add_resource(Login, "/login")
    api.add_resource(SafeLocations, "/safelocations")
    api.add_resource(FloodHistory, "/floodhistory")
    api.add_resource(FloodSeverity, "/severity")
    api.add_resource(Discussion, "/discussion")
    api.add_resource(Predict, "/predictions")
    
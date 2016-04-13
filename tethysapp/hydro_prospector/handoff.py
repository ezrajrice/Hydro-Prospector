# Define your handoff handlers here

from .app import HydroProspector as app


# this handler is called by a controller in ther posgis app
def get_engine_conn():
    parent_engine = app.get_persistent_store_engine('hydro_prospector_db')

    return parent_engine

from model import db_engine, UserProjectsBase


def init_hydro_prospector_db(first_time):
    """
    Initialization function for hydro prospector db.
    """
    # Initialize Tables
    UserProjectsBase.metadata.create_all(db_engine)

    if first_time:
        pass
from model import db_engine, UserProjectsBase, SessionMaker, UserProject


def init_hydro_prospector_db(first_time):
    """
    Initialization function for hydro prospector db.
    """
    # Initialize Tables
    UserProjectsBase.metadata.create_all(db_engine)

    if first_time:
        # Make session
        session = SessionMaker()

        session.commit()
        session.close()

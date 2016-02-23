import datetime
import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, Boolean, DateTime, String, TypeDecorator, CHAR
from sqlalchemy.orm import sessionmaker

from tethysapp.hydro_prospector.app import HydroProspector

db_engine = HydroProspector.get_persistent_store_engine('hydro_prospector_db')
SessionMaker = sessionmaker(bind=db_engine)
UserProjectsBase = declarative_base()


class GUID(TypeDecorator):
    """
    Platform-independent GUID type.

    Uses Postgresql's UUID type, otherwise uses
    CHAR(32), storing as stringified hex values.
    """
    impl = CHAR

    def load_dialect_impl(self, dialect):
        if dialect.name == 'postgresql':
            return dialect.type_descriptor(UUID())
        else:
            return dialect.type_descriptor(CHAR(32))

    def process_bind_param(self, value, dialect):
        if value is None:
            return value
        elif dialect.name == 'postgresql':
            return str(value)
        else:
            if not isinstance(value, uuid.UUID):
                return "%.32x" % uuid.UUID(value)
            else:
                # hexstring
                return "%.32x" % value

    def process_result_value(self, value, dialect):
        if value is None:
            return value
        else:
            return uuid.UUID(value)


class UserProject(UserProjectsBase):
    """
    Definition for the user_projects table.
    """
    __tablename__ = 'hydro_prospector_user_projects'

    id = Column(GUID, primary_key=True, default=uuid.uuid4)
    owner = Column(String)  # Username
    project_id = Column(Integer)
    database_id = Column(String)
    name = Column(String)
    description = Column(String)
    srid = Column(String)  # EPSG SRID
    watershed_status = Column(String)
    flow_duration_curve_status = Column(String)
    streamflow_status = Column(String)
    historical_status = Column(String)
    climate_change_status = Column(String)
    sediment_estimate_status = Column(String)
    date_created = Column(DateTime, default=datetime.datetime.utcnow)
    public = Column(Boolean, default=False)



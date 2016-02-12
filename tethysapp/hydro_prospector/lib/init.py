from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.db import IntegrityError
# from tethys_sdk.services import get_spatial_dataset_engine


def initialize_app():
    """
    Perform any initialization that needs to occur for the app.
    """
    try:
        # Initialize the permissions for the app
        permission_ct = ContentType.objects.get(
            app_label='auth',
            model='permission'
        )
        hydro_prospector_admin_p = Permission(
            name='Hydro Prospector app admin',
            codename='hydro_prospector_app_admin',
            content_type=permission_ct
        )
        hydro_prospector_admin_p.save()
    except IntegrityError:
        pass

    # Initialize GeoServer if it hasn't happened already
    # gs_engine = get_spatial_dataset_engine(GEOSERVER_NAME)
    # response = gs_engine.get_workspace('hydro_prospector')

    # if not response['success']:
    #     gs_manager = GeoServerManager(gs_engine)
    #     gs_manager.create_workspace()
    #     gs_manager.create_global_styles()

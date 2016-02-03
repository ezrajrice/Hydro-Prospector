from tethys_sdk.base import TethysAppBase, url_map_maker
from tethys_sdk.stores import PersistentStore


class HydroProspector(TethysAppBase):
    """
    Tethys app class for Hydro Prospector.
    """

    name = 'Hydro Prospector'
    index = 'hydro_prospector:home'
    icon = 'hydro_prospector/images/icon.gif'
    package = 'hydro_prospector'
    root_url = 'hydro-prospector'
    color = '#e67e22'
    description = 'Place a brief description of your app here.'
    enable_feedback = True
    feedback_emails = ['ezrajrice@gmail.com']

    def url_maps(self):
        """
        Add controllers
        """
        UrlMap = url_map_maker(self.root_url)

        url_maps = (UrlMap(name='home',
                           url='hydro-prospector',
                           controller='hydro_prospector.controllers.home'),
        )

        return url_maps

    def persistent_stores(self):
        """
        Add one or more persistent stores
        """
        stores = (PersistentStore(name='stream_gage_db',
                                  initializer='init_stores:init_stream_gage_db',
                                  spatial=True
                                  ),
                  )

        return stores
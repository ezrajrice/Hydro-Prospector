from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from tethys_apps.sdk.gizmos import *


@login_required()
def home(request):
    """
    Controller for the app home page.
    """
    view_project_button = Button(display_text='View',
                                 name='view_project_button',
                                 attributes={"onclick": "alert(this.name);"},
                                 submit=True)

    home_project_table = TableView(column_names=('ID', 'Project Name', 'Description', ''),
                                   rows=[(1, 'Payette, ID', 'Reservoir located just east of Payette, ID',
                                          view_project_button)],
                                   hover=True,
                                   striped=False,
                                   bordered=False,
                                   condensed=False,
                                   editable_columns=False,
                                   row_ids=[],
                                   # attributes={'onclick': view_project(request)},
                                   )

    new_project_url = 'hydro-prospector/new-project'

    context = {'home_project_table': home_project_table,
               'new_project_url': new_project_url,
               'view_project_button': view_project_button,
               }

    return render(request, 'hydro_prospector/home.html', context)


@login_required()
def view_project(request):
    """
    Controller for creating a new project.
    """
    home_project_table = TableView(column_names=('project_id', 'project_name', 'description', ''),
                                   rows=[()],
                                   hover=True,
                                   striped=True,
                                   bordered=False,
                                   condensed=False,
                                   editable_columns=False,
                                   row_ids=[],
                                   attributes={'onclick': "onclick: view_project_summary()"},
                                   )


    project_id = 1
    project_name = 'Payette, ID'

    context = {'home_project_table': home_project_table,
               'project_id': project_id,
               'project_name': project_name,
               }

    return render(request, 'hydro_prospector/view_project.html', context)


@login_required()
def view_map(request):
    """
    Controller for viewing the project watershed.
    """
    view_options = MVView(projection='EPSG:4326',
                          center=[-100, 40],
                          zoom=3.5,
                          maxZoom=18,
                          minZoom=2
                          )

    map_view_options = MapView(height='600px',
                               width='100%',
                               controls=['Rotate',
                                         {'ZoomToExtent': {'projection': 'EPSG:4326', 'extent': [-130, 22, -65, 54]}}],
                               # layers=[geojson_layer, geoserver_layer, kml_layer, arc_gis_layer],
                               view=view_options,
                               basemap='OpenStreetMap',
                               # draw=drawing_options,
                               # legend=True
                               )

    project_id = 1

    context = {'view_options': view_options,
               'map_view_options': map_view_options,
               'project_id': project_id,
               }

    return render(request, 'hydro_prospector/view_map.html', context)

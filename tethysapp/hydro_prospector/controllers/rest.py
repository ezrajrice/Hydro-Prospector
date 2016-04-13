from django.shortcuts import render, redirect
from tethysapp.hydro_prospector.model import UserProject, SessionMaker
from tethysapp.hydro_prospector.app import HydroProspector as app


def project_details(request, db_id):
    """
    """

    session = SessionMaker()

    user_project = session.query(UserProject).get(db_id)
    project_id = user_project.project_id
    project_name = user_project.name
    project_description = user_project.description
    project_date_created = user_project.date_created
    project_watershed_status = user_project.watershed_status

    session.close()

    context = {'project_id': project_id,
               'project_name': project_name,
               'project_description': project_description,
               'project_date_created': project_date_created,
               'project_watershed_status': project_watershed_status,
               }

    return render(request, 'hydro_prospector/project_details.html', context)


# this controller calls controller as a handler from postgis app
def parent_handler_to_childapp(request):
    handoff_manager = app.get_handoff_manager()

    child_app_name = 'storage_capacity'
    handler_name = 'db-conn'
    handler = handoff_manager.get_handler(handler_name, child_app_name)

    return redirect(handler(request))

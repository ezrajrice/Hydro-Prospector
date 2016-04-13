from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from tethys_sdk.gizmos import SelectInput
from tethysapp.hydro_prospector.lib.helpers import is_app_admin
from tethysapp.hydro_prospector.model import UserProject, SessionMaker


@login_required()
def project_home(request):
    """
    Controller for the app home page.
    """
    user = request.user
    groups = user.groups.all()
    select_group_buffer = []
    group_buffer = []

    # First need a variable that has all the group_names so it can be the first of the list
    select_group_buffer.append(('All Groups', 'all_groups'))

    # Make a list of associated groups to the user for the select_group options
    for group in groups:
        group_name = group.name
        group_buffer.append(group_name)
        remove_hydro_prospector_group_name = group_name.split('.')[0]
        cleaned_group_name = remove_hydro_prospector_group_name.replace("_", " ").replace("-", " ")
        select_group_buffer.append((str(cleaned_group_name.title()), str(group_name)))

    # Assigned for controlling display on the template - if zero, it will not let the user add projects
    number_of_groups = len(group_buffer)

    select_group = SelectInput(display_text='View Projects For:',
                               name='select_group',
                               multiple=False,
                               original=True,
                               options=select_group_buffer,
                               attributes="id=select_group")

    session = SessionMaker()

    # Query database for projects that belong to the groups that the user is in.
    projects = session.query(UserProject). \
        order_by(UserProject.date_created.desc()). \
        all()

    session.close()

    context = {'select_group': select_group,
               'is_admin': is_app_admin(user),
               'number_of_groups': number_of_groups,
               'projects': projects}

    return render(request, 'hydro_prospector/home.html', context)


# @login_required()
# def project_table(request, user_project_owners):
#     """
#     Controller for the table on the app home page. It shows all the current projects and
#     is wrapped in the JQuery load function to ease the use of JavaScript
#     """
#     user = request.user
#
#     # filtered_owner is used as a display on the template
#     if user_project_owners == 'all_groups':
#         filtered_owner = 'Any Group'
#     else:
#         filtered_owner = user_project_owners
#         filtered_owner = filtered_owner.split('.')[1].replace("_", " ").replace("-", " ")
#         filtered_owner = str(filtered_owner.title())
#
#     session = SessionMaker()
#
#     # Query database for projects that belong to the groups that the user is in.
#     # projects = session.query(UserProject).\
#     #     filter(UserProject.owner.in_(user_project_owners)).\
#     #     order_by(UserProject.date_created.desc()).\
#     #     all()
#
#     # Query database for projects that belong to the groups that the user is in.
#     projects = session.query(UserProject).\
#         filter(UserProject.owner == user_project_owners).\
#         order_by(UserProject.date_created.desc()).\
#         all()
#
#     context = {'is_admin': is_app_admin(user),
#                'filtered_owner': filtered_owner,
#                'projects': projects}
#
#     session.close()
#
#     return render(request, 'hydro_prospector/project_table.html', context)

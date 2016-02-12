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

    context = {'select_group': select_group,
               'is_admin': is_app_admin(user),
               'number_of_groups': number_of_groups}

    return render(request, 'hydro_prospector/home.html', context)


@login_required()
def project_table(request, user_project_owners):
    """
    Controller for the table on the app home page. It shows all the current projects and
    is wrapped in the JQuery load function to ease the use of JavaScript
    """
    refresh_required = False
    refresh_number = []
    user = request.user
    groups = user.groups.all()
    group_buffer = []
    show_group_field = None

    # filtered_owner is used as a display on the template
    if user_project_owners == 'all_groups':
        filtered_owner = 'Any Group'
    else:
        filtered_owner = user_project_owners
        filtered_owner = filtered_owner.split('.')[1].replace("_", " ").replace("-", " ")
        filtered_owner = str(filtered_owner.title())

    # Make a list of associated groups to the user for the select_group options
    for group in groups:
        group_name = group.name
        group_buffer.append(str(group_name))

    num_of_groups = len(group_buffer)

    # If there are no groups, do not the following
    if num_of_groups > 0:
        session = SessionMaker()

        if user_project_owners == 'all_groups':
            show_group_field = 'yes'
            user_project_owners = group_buffer

            # Query database for projects that belong to the groups that the user is in.
            projects = session.query(UserProject).\
                filter(UserProject.owner.in_(user_project_owners)).\
                order_by(UserProject.date_created.desc()).\
                all()
        else:
            # Query database for projects that belong to the groups that the user is in.
            projects = session.query(UserProject).\
                filter(UserProject.owner == user_project_owners).\
                order_by(UserProject.date_created.desc()).\
                all()

        # Create array of pending projects
        for project in projects:
            # Check to see if there are any that need to be refreshed
            if project.input_file_status == 'Pending' or project.report_file_status == 'Pending':
                refresh_number.append(project.name)

            project_owner = project.owner
            remove_epanet_group_name = project_owner.split('.')[1]
            cleaned_project_name = remove_epanet_group_name.replace("_", " ").replace("-", " ")
            cleaned_project_owner = str(cleaned_project_name.title())
            project.cleaned_project_owner = cleaned_project_owner

        if len(refresh_number) > 0:
            refresh_required = True

        context = {'refresh_required': refresh_required,
                   'show_group_field': show_group_field,
                   'is_admin': is_app_admin(user),
                   'num_of_groups': num_of_groups,
                   'filtered_owner': filtered_owner,
                   'projects': projects}

        session.close()

    else:
        # Only this context is needed if there are no groups
        context = {
            'is_admin': is_app_admin(user),
            'num_of_groups': num_of_groups,
            'projects': []}

    return render(request, 'hydro_prospector/project_table.html', context)

from django.shortcuts import render
from django.contrib.auth.decorators import permission_required
from tethys_sdk.gizmos import TextInput, Button, SelectInput


@permission_required('auth.app_admin', raise_exception=True)
def new_project(request):
    """
    Displays the new project form. The form will be processed by the do_new_project controller,
    which will be called via JavaScript.
    """

    user = request.user
    groups = user.groups.all()
    # select_group_buffer = []

    # # Make a list of associated groups to the user for the select_group options
    # for group in groups:
    #     group_name = group.name
    #     remove_epanet_group_name = group_name.split('.')[1]
    #     cleaned_group_name = remove_epanet_group_name.replace("_", " ").replace("-", " ")
    #     select_group_buffer.append((str(cleaned_group_name.title()), str(group_name)))

    name_input = TextInput(
        display_text='Name of Project',
        name='inputName',
        placeholder='e.g.: Glen Canyon'
    )

    # select_group = SelectInput(
    #     display_text='Group Owner',
    #     name='select_group',
    #     multiple=False,
    #     options=select_group_buffer
    # )

    add_button = Button(
        display_text='Add Project',
        icon='glyphicon glyphicon-plus',
        style='success',
        name='submit-add-project',
        attributes='id=submit-add-project'
    )

    context = {'name_input': name_input,
               'add_button': add_button}

    return render(request, 'hydro_prospector/new_project.html', context)

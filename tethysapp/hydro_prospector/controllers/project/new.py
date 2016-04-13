import uuid

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import permission_required
from tethys_sdk.gizmos import TextInput, Button, SelectInput
from tethysapp.hydro_prospector.model import UserProject, SessionMaker


@permission_required('auth.app_admin', raise_exception=True)
def new_project(request):
    """
    Displays the new project form. The form will be processed by the do_new_project controller,
    which will be called via JavaScript.
    """

    user = request.user

    name_input = TextInput(
        display_text='Name of Project',
        name='inputName',
        placeholder='e.g.: Glen Canyon'
    )

    add_button = Button(
        display_text='Add Project',
        icon='glyphicon glyphicon-plus',
        style='success',
        name='submit-add-project',
        attributes='form=uploadForm',
        submit=True
    )

    context = {'name_input': name_input,
               'add_button': add_button}

    return render(request, 'hydro_prospector/new_project.html', context)


def upload_project(request):
    """
    """
    post = request.POST

    session = SessionMaker()

    new_user_project = UserProject()
    new_user_project.project_id = uuid.uuid4()
    new_user_project.name = post.get('inputName', None)
    new_user_project.description = post.get('project_description', None)

    session.add(new_user_project)
    session.commit()

    session.close()
    return redirect('hydro_prospector:home')

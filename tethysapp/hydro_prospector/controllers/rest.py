from django.http import JsonResponse
from django.contrib.auth.decorators import permission_required
from tethysapp.hydro_prospector.lib.init import initialize_app


@permission_required('auth.hydro_prospector_app_admin', raise_exception=True)
def initialize_app_settings(request):
    """
    Initialize default layers and styles. Needs to be ran before uploading any projects.
    """
    initialize_app()
    return JsonResponse({'success': True})

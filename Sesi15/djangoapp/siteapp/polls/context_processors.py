from .models import Settings

def project_settings(request):
    all_settings = Settings.objects.all()
    settings_dict = {setting.nama: setting.nilai for setting in all_settings}
    return settings_dict
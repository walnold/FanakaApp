from django.contrib.sessions.models import Session

def logout_user_sessions(user):
    sessions = Session.objects.all()
    for session in sessions:
        data = session.get_decoded()
        if data.get("_auth_user_id") == str(user.pk):
            session.delete()
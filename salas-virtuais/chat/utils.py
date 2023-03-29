from django.shortcuts import redirect

ADMIN_PROVIDER = 'aluno.ifsp.edu.br'

def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('lobby')

        else:
            return view_func(request, *args, **kwargs)
    
    return wrapper_func


def check_if_superuser(email: str) -> bool:
    splitted_email = email.split('@')
    email_provider = splitted_email[1]
    
    return True if email_provider == ADMIN_PROVIDER else False
    
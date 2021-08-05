from apps.models.usuario import Usuario

def get_usuario_hard()->Usuario:
    login_spec = {"user":"tostado","password":"black"}
    return Usuario({"nombre":"cosme fulanito","telefono":"01166666666","login":login_spec})
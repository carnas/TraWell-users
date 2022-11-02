import jwt

from utils.variables import PUBLIC_KEY, ALGORITHMS, JWT_OPTIONS


def is_authorized(request):
    try:
        token = request.headers['Authorization']
    except KeyError:
        return False

    try:
        print(token)

        jwt.decode(token, PUBLIC_KEY, algorithms=ALGORITHMS, options=JWT_OPTIONS)
        return True
    except jwt.exceptions.DecodeError:
        print('decode')
        return False


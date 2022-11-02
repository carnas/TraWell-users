import jwt

from utils.variables import PUBLIC_KEY, ALGORITHMS, JWT_OPTIONS


def is_authorized(request):
    try:
        token = request.headers['Authorization'].split(' ')[1]
    except KeyError:
        return False

    try:
        # print(token)
        jwt.decode(token, PUBLIC_KEY, algorithms=["RS256"], audience="account")
        return True
    except jwt.exceptions.DecodeError:
        print('decode')
        return False


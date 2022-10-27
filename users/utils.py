import jwt
from email_validator import validate_email, EmailNotValidError


def get_user_data_from_jwt(encoded_jwt: str):
    data = decode_jwt(encoded_jwt)
    user_data = {'first_name': data['given_name'],
                 'last_name': data["family_name"],
                 'email': data['email'],
                 'date_of_birth': data['date_of_birth'],
                 'user_type': rewrite_user_type(data['user_type']),
                 'facebook': data['facebook'],
                 'instagram': data['instagram'],
                 'avatar': data['picture']}

    return user_data


def decode_jwt(encoded_jwt: str):
    data = jwt.decode(encoded_jwt, options={"verify_signature": False})
    return data


def rewrite_user_type(user_type):
    if user_type == 'Private Account':
        return 'private'
    elif user_type == 'Company Account':
        return 'company'
    else:
        return ''


def is_email_vaild(email):
    try:
        validate_email(email)
        return True
    except EmailNotValidError:
        return False

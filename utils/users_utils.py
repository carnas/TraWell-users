import jwt
import os
from email_validator import validate_email, EmailNotValidError


def get_user_data_from_token(token: str):
    data = decode_token(token)
    if 'error' in data.keys():
        return data

    return extract_user_data(data)


def decode_token(token: str):
    try:
        public_key = f"""-----BEGIN RSA PUBLIC KEY-----\n{os.environ.get("TOKEN_KEY")}\n-----END RSA PUBLIC KEY-----"""
        issuer_claim = os.environ.get("ISSUER_CLAIM")
        data = jwt.decode(token, public_key, algorithms=['RS256'], issuer=issuer_claim,
                          audience='account', options={'verify_signature': True,
                                                       'verify_exp': True,
                                                       'verify_iss': True,
                                                       'verify_iat': True,
                                                       'verify_aud': True})
        return data
    except ValueError:
        return {'error': 'Public key is invalid'}
    except jwt.InvalidIssuerError:
        return {'error': 'Not authorized issuer'}
    except jwt.InvalidAudienceError:
        return {'error': 'Not authorized audience'}
    except jwt.ExpiredSignatureError:
        return {'error': 'The signature has expired'}
    except jwt.InvalidSignatureError:
        return {'error': 'The signature is invalid'}
    except jwt.InvalidIssuedAtError:
        return {'error': 'Issued at date is invalid'}


def extract_user_data(data: str):
    try:
        user_data = {'first_name': data['given_name'],
                     'last_name': data['family_name'],
                     'email': data['email'],
                     'date_of_birth': data['date_of_birth'],
                     'user_type': rewrite_user_type(data['user_type']),
                     'facebook': data['facebook'],
                     'instagram': data['instagram'],
                     'avatar': ''}
        if 'picture' in data.keys():
            user_data['avatar'] = data['picture']

        return user_data
    except KeyError:
        return {'error': 'User data are not complete'}


def rewrite_user_type(user_type: str):
    if user_type == 'Private Account':
        return 'private'
    elif user_type == 'Company Account':
        return 'company'
    else:
        return ''


def is_email_valid(email: str):
    try:
        validate_email(email)
        return True
    except EmailNotValidError:
        return False


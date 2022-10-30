import jwt
from email_validator import validate_email, EmailNotValidError


PUBLIC_KEY = '-----BEGIN RSA PUBLIC KEY-----\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAsigrn1IczQr4Ywmd+30WkyQAAV6tih58ENcCikivikUdLWN1HBWNjU53US9YXiJThpSNXSKeRMJ95f9OWj4uaCHIeN4hKrOsdnLoETiaDEGrKymzcLFHBhaVK7Cpna3zUUJWDajRjlmNHvLa+8IIApeF0e5pLCgXbeGyxnSmLhrhftVmuKJ2xEeAul/nQV3UGD+Qg/sKTpI7wdDARhOaQ0EjX/gO7uYKQ+pDVwlfgFDuJaJ/LjgQpe4zRNS3VD8X5lV+uQFkTJC2OQlPEunRFjQe6s/iR2IEGwNx3oISwCZsm7FyGZ1wTnCqO4rq39PkffRSA696HfJDszGo6c6hyQIDAQAB\n-----END RSA PUBLIC KEY-----'
ISSUER_CLAIM = 'http://localhost:8403/auth/realms/TraWell'
ALGORITHMS = ['RS256']
JWT_OPTIONS = {
        'verify_signature': False,
        'verify_exp': False,
        'verify_iss': True,
        'verify_iat': True,
        'verify_aud': False,
    }


def get_user_data_from_token(token: str):
    data = decode_token(token)
    if 'error' in data.keys():
        return data

    return extract_user_data(data)


def decode_token(token: str):
    try:
        data = jwt.decode(token, PUBLIC_KEY, algorithms=ALGORITHMS, issuer=ISSUER_CLAIM, options=JWT_OPTIONS)
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


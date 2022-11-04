import factory.django
import factory.fuzzy
import datetime
from datetime import timezone

from . import models


user_types = ['private', 'company']
urls = ['', 'http://www.armstrong-foster.com/', 'https://www.reyes.biz/', 'https://www.collinsaerospace.com/',
        'https://www.miller.com/', 'https://www.aggieland.com/', 'http://ww16.french.com/?sub1=20221022-1844-4946-ad3c-e6ba6800f94e']
avatars = ['', 'https://dummyimage.com/128x128', 'https://placeimg.com/128/128/any',
           'https://i.picsum.photos/id/838/128/128.jpg?hmac=cjERlKgXi7EyqiSiD7BqVbSokmYI6muTIjUh8bPeewY',
           'https://i.picsum.photos/id/19/128/128.jpg?hmac=BBtJMOGsVxTnCQManuH0WXl_OHkfwUJ7sFGSr2JRQpg']


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.User

    first_name = factory.Faker('first_name', locale='PL')
    last_name = factory.Faker('last_name', locale='PL')
    email = factory.Faker('safe_email')
    date_of_birth = factory.fuzzy.FuzzyDateTime(
        datetime.datetime(1901, 1, 1, tzinfo=datetime.timezone.utc),
        datetime.datetime(2010, 12, 31, 20, tzinfo=datetime.timezone.utc)
    )
    avg_rate = factory.Faker('pydecimal', left_digits=1, right_digits=2, min_value=1, max_value=5)
    user_type = factory.Faker('random_element', elements=user_types)
    facebook = factory.Faker('random_element', elements=urls)
    instagram = factory.Faker('random_element', elements=urls)
    avatar = factory.Faker('random_element', elements=avatars)

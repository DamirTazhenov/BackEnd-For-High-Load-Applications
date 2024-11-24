from django.contrib.auth.hashers import PBKDF2PasswordHasher


class ReducedIterationsPBKDF2PasswordHasher(PBKDF2PasswordHasher):
    iterations = 25000

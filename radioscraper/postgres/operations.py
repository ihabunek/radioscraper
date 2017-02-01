from django.contrib.postgres.operations import CreateExtension


class CitextExtension(CreateExtension):

    def __init__(self):
        self.name = 'citext'

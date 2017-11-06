from django.db.models import Transform


class ImmutableUnaccent(Transform):
    bilateral = True
    lookup_name = 'iunaccent'
    function = 'IUNACCENT'

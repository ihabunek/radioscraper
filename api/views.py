from django.http import JsonResponse
from radio.models import Radio


def radios(request):
    radios = (
        Radio.objects
        .filter(active=True)
        .order_by("name")
        .prefetch_related("last_play")
        .all()
    )
    return JsonResponse({"radios": [_serialize_radio(r) for r in radios]})


def _serialize_radio(radio):
    return {
        "id": radio.id,
        "slug": radio.slug,
        "name": radio.name,
        "last_play": _serialize_play(radio.last_play),
        "play_count": radio.play_count,
    }


def _serialize_play(play):
    return {
        "artist_name": play.artist_name,
        "title": play.title,
        "timestamp": play.timestamp,
    } if play else None

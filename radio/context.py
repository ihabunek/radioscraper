from radio.models import Radio


def radios(request):
    return {
        "radios": Radio.objects.all()
    }
import re

from django.db import transaction
from django.utils.text import slugify

from radio.models import Play
from music.models import Artist, ArtistName


def normalize_name(name):
    # Replace underscores with spaces
    name = name.replace('_', ' ')

    # Remove multiple whitespace with a single space
    name = re.sub("\\s+", " ", name)

    # Remove text in brackets
    name = re.sub("\\(.+\\)", "", name)
    name = re.sub("\\[.+\\]", "", name)

    # Replace "feat." and similar
    name = re.sub("\\s(ft|feat)\\.?\\s.+", "", name, flags=re.IGNORECASE)

    # Replace ; with & surrounded by spaces
    name = re.sub("\\s*;\\s*", " & ", name)

    # Replace + which is used for & sometimes

    return name.strip()


def find_artist_by_slug(name):
    slug = slugify(normalize_name(name))
    return Artist.objects.filter(slug=slug).first()


def _name_variants(name):
    normal_name = normalize_name(name)

    # First search by normalized name
    yield normal_name

    # If name starts with 'the', try removing it, otherwise try adding it
    if len(normal_name) > 4 and normal_name.lower().startswith('the '):
        yield normal_name[4:]
    else:
        yield "The {}".format(normal_name)

    # Try to permute common conjunctions since they're used interchangeably
    conjunctions = [" & ", " i ", " and ", " + "]
    for one in conjunctions:
        if re.search(re.escape(one), normal_name, flags=re.IGNORECASE):
            for other in conjunctions:
                if other.lower() != one.lower():
                    yield re.sub(re.escape(one), other, normal_name, flags=re.IGNORECASE)

    # For artists with the "name surname" pattern, try reversing them
    match = re.match("^(\\w+)\\s+(\\w+)$", normal_name)
    if match:
        yield " ".join(reversed(match.groups()))

    # Sometimes the track number gets pasted to the start of artist name so try
    # stripping away leading numbers, dots, dashes and whitespace
    stripped_name = re.sub('^\\d+[\\.\\s-]*', '', normal_name).strip()
    if stripped_name and stripped_name != normal_name:
        yield stripped_name


def find_artist_by_name(name):
    for name_variant in _name_variants(name):
        artist_name = ArtistName.objects.filter(name__iunaccent__iexact=name_variant).first()
        if artist_name:
            return artist_name.artist

    return None


def find_artist(name):
    return find_artist_by_name(name) or find_artist_by_slug(name)


def create_artist(name):
    normal_name = normalize_name(name)

    artist = Artist.objects.create(
        name=normal_name,
        slug=slugify(normal_name),
    )

    ArtistName.objects.create(artist=artist, name=normal_name)

    return artist


def get_or_create_artist(name):
    """Returns an existing artist matching the given name or creates a new one
    if not found."""
    artist = find_artist(name)

    if artist:
        artist.add_name(normalize_name(name))
        return False, artist

    return True, create_artist(name)


class MergeError(Exception):
    pass


@transaction.atomic
def merge_artists(artists, target_artist, target_name):
    # target_rtist must not be in artists
    if artists.filter(pk=target_artist.pk).exists():
        raise MergeError("target_artist is in artists")

    # target_name must be in one of artists
    all_artists = artists | Artist.objects.filter(pk=target_artist.pk)
    all_names = ArtistName.objects.filter(artist__in=all_artists)
    if not all_names.filter(pk=target_name.pk).exists():
        raise MergeError("target_name invalid")

    # Reassign names to target artist
    ArtistName.objects.filter(artist__in=artists).update(artist=target_artist)

    # Reassign plays to target artist
    Play.objects.filter(artist__in=artists).update(artist=target_artist)

    # Set the prefered artist name
    target_artist.name = target_name.name
    target_artist.recalculate_derived_data()
    target_artist.save()

    # Delete other artists
    artists.delete()

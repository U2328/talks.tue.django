from .utils import generate_revision_for
from ..core.models import Talk, Collection


__all__ = (
    "TalkRevision", "CollectionRevision"
)


@generate_revision_for(Talk)
def TalkRevision(revision_model, talk):
    revision = revision_model.objects.create(
        original=talk,
        title=talk.title,
        description=talk.description,
        timestamp=talk.timestamp,
        name=talk.name,
        about_me=talk.about_me,
    )
    revision.tags.set(talk.tags.all())
    revision.collections.set(talk.collections.all())
    return revision


@generate_revision_for(Collection)
def CollectionRevision(revision_model, collection):
    revision = revision_model.objects.create(
        original=collection,
        title=collection.title,
        description=collection.description,
        organizer=collection.organizer,
        is_meta=collection.is_meta,
    )
    revision.editors.set(collection.editors.all())
    revision.meta_collections.set(collection.meta_collections.all())
    return revision
from .utils import generate_revision_for
from ..core.models import Talk, Collection, MetaCollection


__all__ = (
    "TalkRevision", "MetaCollectionRevision", "CollectionRevision"
)


@generate_revision_for(Talk)
def TalkRevision(revision_model, original):
    revision = revision_model.objects.create(
        original=original,
        title=original.title,
        description=original.description,
        timestamp=original.timestamp,
        name=original.name,
        about_me=original.about_me,
    )
    revision.tags.set(original.tags.all())
    revision.collections.set(original.collections.all())
    return revision


def _CollectionRevision(revision_model, original):
    revision = revision_model.objects.create(
        original=original,
        title=original.title,
        description=original.description,
        organizer=original.organizer,
        is_meta=original.is_meta,
    )
    revision.editors.set(original.editors.all())
    revision.meta_collections.set(original.meta_collections.all())
    return revision


MetaCollectionRevision = generate_revision_for(MetaCollection)(_CollectionRevision)
CollectionRevision = generate_revision_for(Collection)(_CollectionRevision)
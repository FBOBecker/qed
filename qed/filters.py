def parents(entity):
    yield entity
    while entity.parent is not None:
        entity = entity.parent
        yield entity

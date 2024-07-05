from gmcli.models.items.tags.TagCollection import TagCollection
from gmcli.models.items.tags.Tag import Tag
from gmcli.utils.enums import TagCategory, TagName

def toTagCollection(tagsRaw: list[dict]) -> TagCollection:
  tagCollection = TagCollection()

  for tagRaw in tagsRaw:

    tagRawCategoryName = tagRaw.get('category')
    tagRawName = tagRaw.get('name')

    if tagRawCategoryName and tagRawName:
      category = TagCategory(tagRawCategoryName)
      name = TagName(tagRawName)

      tag = Tag(
        category=category,
        name=name
      )

      tagCollection.append(tag)


  return tagCollection

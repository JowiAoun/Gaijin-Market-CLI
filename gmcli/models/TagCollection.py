from pydantic import BaseModel
from gmcli.utils.enums import TagCategory
from gmcli.models.Tag import Tag

class TagCollection(BaseModel):
  tags: list[Tag] = []

  class Config:
    arbitrary_types_allowed = True

  def get_tag(self, tagCategory: TagCategory) -> Tag | None:
    for tag in self.tags:
      if tag.category == tagCategory:
        return tag

    return None

  def add_tag(self, tag: Tag):
    self.tags.append(tag)

  def __str__(self):
    return ''.join(str(tag) for tag in self.tags)

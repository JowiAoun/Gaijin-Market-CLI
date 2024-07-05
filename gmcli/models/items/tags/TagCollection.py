from pydantic import BaseModel
from gmcli.utils.enums import TagCategory
from gmcli.models.items.tags.Tag import Tag

class TagCollection(BaseModel):
  tags: list[Tag] = []

  def get(self, tagCategory: TagCategory) -> Tag | None:
    for tag in self.tags:
      if tag.category == tagCategory:
        return tag
    return None

  def append(self, tag: Tag) -> None:
    self.tags.append(tag)

  def __iter__(self):
    return iter(self.tags)

  def __contains__(self, tagCategory: TagCategory) -> bool:
    return self.get(tagCategory) is not None

  def __len__(self) -> int:
    return len(self.tags)

  def __str__(self) -> str:
    return '\n'.join(str(tag) for tag in self.tags)

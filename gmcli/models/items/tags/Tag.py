from gmcli.utils.enums import TagCategory, TagName

from pydantic import BaseModel

class Tag(BaseModel):
  category: TagCategory = None
  name: TagName = None

  def __str__(self):
    return f"{self.category.value}: {self.name.value}"

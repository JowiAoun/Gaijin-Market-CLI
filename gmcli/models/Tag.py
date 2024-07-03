from gmcli.utils.enums import TagCategory

from pydantic import BaseModel

class Tag(BaseModel):
  category: TagCategory = TagCategory.UNKNOWN
  name: str = None

  def __str__(self):
    return f"{self.category}: {self.name}"

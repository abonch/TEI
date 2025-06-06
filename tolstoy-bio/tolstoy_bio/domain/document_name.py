import collections
from copy import deepcopy
import dataclasses


NAME_COMPONENTS_SEPARATOR = "_"


@dataclasses.dataclass
class DocumentName:
    scope: str
    start_date: str
    end_date: str = None
    postfix: str = None

    def to_string(self):
        end_date = self.end_date or self.start_date
        components = [self.scope, self.start_date, end_date]
        
        if value := self.postfix:
            components.append(value)

        return NAME_COMPONENTS_SEPARATOR.join(components)

    def to_filename(self, extension: str):
        name = self.to_string()
        return f'{name}.{extension}'
    


@dataclasses.dataclass
class DocumentNameGenerator:
    scope: str

    def generate(self, start_date: str, end_date: str = None, postfix: str = None):
        return DocumentName(self.scope, start_date, end_date, postfix)


class UniqueDocumentNameGenerator(DocumentNameGenerator):
    def __init__(self, scope: str):
        super().__init__(scope)
        self.name_counts = collections.defaultdict(int)

    def generate(self, start_date: str, end_date: str = None):
        name = DocumentName(self.scope, start_date, end_date)
        name_string = name.to_string()

        self.name_counts[name_string] += 1
        name_count = self.name_counts[name_string]

        if name_count > 1:
            name.postfix = str(name_count)

        return name

from pydantic import BaseModel
from typing import List

class UMLClass(BaseModel):
    name: str
    attributes: List[str] = []
    methods: List[str] = []

class UMLRelationship(BaseModel):
    from_class: str
    to_class: str
    relationship_type: str

class UMLDiagram(BaseModel):
    classes: List[UMLClass] = []
    relationships: List[UMLRelationship] = []
    title: str = "UML Class Diagram"
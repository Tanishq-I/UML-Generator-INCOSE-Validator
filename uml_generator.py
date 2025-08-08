import graphviz
from uml_models import UMLDiagram, UMLClass, UMLRelationship

class UMLDiagramGenerator:
    def __init__(self):
        self.dot = None
    def generate_diagram(self, uml_diagram: UMLDiagram) -> str:
        self.dot = graphviz.Digraph(comment=uml_diagram.title)
        self.dot.attr(rankdir='TB')
        for uml_class in uml_diagram.classes:
            self._add_class(uml_class)
        for relationship in uml_diagram.relationships:
            self._add_relationship(relationship)
        return self.dot.source
    def _add_class(self, uml_class: UMLClass):
        label = f"<<TABLE BORDER='0' CELLBORDER='1' CELLSPACING='0'>"
        label += f"<TR><TD PORT='header' BGCOLOR='lightblue'><B>{uml_class.name}</B></TD></TR>"
        if uml_class.attributes:
            label += f"<TR><TD PORT='attrs' BGCOLOR='lightgray'>"
            for attr in uml_class.attributes:
                label += f"{attr}<BR/>"
            label += "</TD></TR>"
        if uml_class.methods:
            label += f"<TR><TD PORT='methods' BGCOLOR='lightyellow'>"
            for method in uml_class.methods:
                label += f"{method}<BR/>"
            label += "</TD></TR>"
        label += "</TABLE>>"
        self.dot.node(uml_class.name, label, shape='none')
    def _add_relationship(self, relationship: UMLRelationship):
        arrow_styles = {
            'inheritance': 'empty',
            'association': 'open',
            'composition': 'diamond',
            'aggregation': 'odiamond'
        }
        arrowhead = arrow_styles.get(relationship.relationship_type, 'open')
        self.dot.edge(
            relationship.from_class,
            relationship.to_class,
            arrowhead=arrowhead,
            label=relationship.relationship_type
        )
    def save_diagram(self, filename: str = "uml_diagram"):
        if self.dot:
            self.dot.render(filename, format='png', cleanup=True)
            return f"{filename}.png"
        return None 
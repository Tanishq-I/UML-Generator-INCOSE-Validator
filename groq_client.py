import groq
import xml.etree.ElementTree as ET
from config import GROQ_API_KEY, GROQ_MODEL
from uml_models import UMLDiagram, UMLClass, UMLRelationship

class GroqUMLClient:
    def __init__(self, model: str = None):
        self.client = groq.Groq(api_key=GROQ_API_KEY)
        self.model = model or GROQ_MODEL

    def generate_uml(self, scenario_description: str, uml_type: str = "class") -> UMLDiagram:
        uml_type_prompts = {
            "class": "Generate a UML class diagram in XML format. Include classes, their attributes, methods, and relationships (inheritance, association, composition, aggregation).",
            "object": "Generate a UML object diagram in XML format. Include instances (objects) of classes, links between objects, and attribute values for each object.",
            "composite": "Generate a UML composite structure diagram in XML format. Include the internal structure of a class or component, parts, ports, and connectors.",
            "sequence": "Generate a UML sequence diagram in XML format. Include objects/actors, messages exchanged (with order), and lifelines for each object/actor.",
            "usecase": "Generate a UML use case diagram in XML format. Include actors (users, external systems), use cases (system functions), and relationships (associations, includes, extends) between them."
        }
        prompt_instructions = uml_type_prompts.get(uml_type, uml_type_prompts["class"])
        prompt = f"""
        {prompt_instructions}
        Scenario: {scenario_description}
        Return the result in this exact XML format:
        <uml_diagram>
            <title>Diagram Title</title>
            <classes>
                <class>
                    <name>ClassName</name>
                    <attributes>
                        <attribute>attr1: type</attribute>
                        <attribute>attr2: type</attribute>
                    </attributes>
                    <methods>
                        <method>method1()</method>
                        <method>method2()</method>
                    </methods>
                </class>
            </classes>
            <relationships>
                <relationship>
                    <from>Class1</from>
                    <to>Class2</to>
                    <type>inheritance</type>
                </relationship>
            </relationships>
        </uml_diagram>
        """
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.1,
                max_tokens=2000
            )
            xml_content = response.choices[0].message.content
            return self._parse_xml_to_uml(xml_content)
        except Exception as e:
            print(f"Error generating UML: {e}")
            return UMLDiagram(title="Error generating diagram")
    def _parse_xml_to_uml(self, xml_content: str) -> UMLDiagram:
        try:
            if "```xml" in xml_content:
                xml_content = xml_content.split("```xml")[1].split("```")[0]
            elif "```" in xml_content:
                xml_content = xml_content.split("```")[1]
            
            root = ET.fromstring(xml_content.strip())
            diagram = UMLDiagram()
            
            title_elem = root.find("title")
            if title_elem is not None:
                diagram.title = title_elem.text
            
            classes_elem = root.find("classes")
            if classes_elem is not None:
                for class_elem in classes_elem.findall("class"):
                    uml_class = UMLClass(name=class_elem.find("name").text)
                    
                    attrs_elem = class_elem.find("attributes")
                    if attrs_elem is not None:
                        for attr_elem in attrs_elem.findall("attribute"):
                            uml_class.attributes.append(attr_elem.text)
                    
                    methods_elem = class_elem.find("methods")
                    if methods_elem is not None:
                        for method_elem in methods_elem.findall("method"):
                            uml_class.methods.append(method_elem.text)
                    
                    diagram.classes.append(uml_class)
            
            relationships_elem = root.find("relationships")
            if relationships_elem is not None:
                for rel_elem in relationships_elem.findall("relationship"):
                    from_class = rel_elem.find("from").text
                    to_class = rel_elem.find("to").text
                    rel_type = rel_elem.find("type").text
                    diagram.relationships.append(
                        UMLRelationship(
                            from_class=from_class,
                            to_class=to_class,
                            relationship_type=rel_type
                        )
                    )
            return diagram
        except Exception as e:
            print(f"Error parsing XML: {e}")
            return UMLDiagram(title="Error parsing diagram")
    
    def _make_request(self, prompt: str, max_tokens: int = 1000) -> str:
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.1,
                max_tokens=max_tokens
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"Error making request to Groq: {e}")
            return ""
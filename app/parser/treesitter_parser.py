from tree_sitter import Parser
from tree_sitter_languages import get_language


class TreeSitterParser:

    def __init__(self, language="python"):
        self.language = get_language(language)

        self.parser = Parser()
        self.parser.set_language(self.language)


    def parse_file(self, code):
        return self.parser.parse(code)


    def extract_functions(self, node, code, functions):
        if node.type == "function_definition":
            name = node.child_by_field_name("name")

            if name:
                functions.append(
                    code[name.start_byte:name.end_byte].decode()
                )

        for child in node.children:
            self.extract_functions(child, code, functions)


    def extract_classes(self, node, code, classes):
        if node.type == "class_definition":
            name = node.child_by_field_name("name")

            if name:
                classes.append(
                    code[name.start_byte:name.end_byte].decode()
                )

        for child in node.children:
            self.extract_classes(child, code, classes)


    def extract_imports(self, node, code, imports):
        if node.type in ["import_statement", "import_from_statement"]:

            imports.append(
                code[node.start_byte:node.end_byte].decode()
            )

        for child in node.children:
            self.extract_imports(child, code, imports)


    def analyze_file(self, file_path):

        with open(file_path, "rb") as f:
            code = f.read()

        tree = self.parse_file(code)

        functions = []
        classes = []
        imports = []

        root = tree.root_node

        self.extract_functions(root, code, functions)
        self.extract_classes(root, code, classes)
        self.extract_imports(root, code, imports)

        return {
            "functions": functions,
            "classes": classes,
            "imports": imports
        }
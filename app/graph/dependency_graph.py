import os
import networkx as nx


def build_dependency_graph(parsed_data):

    graph = nx.DiGraph()

    # map module names → file paths
    module_map = {}

    for item in parsed_data:
        file_path = item["file"]

        module_name = os.path.basename(file_path).replace(".py", "")

        module_map[module_name] = file_path

        graph.add_node(file_path, type="file")

    for item in parsed_data:

        file_path = item["file"]
        data = item["data"]

        # functions
        for function in data["functions"]:
            graph.add_node(function, type="function")
            graph.add_edge(file_path, function, relation="defines")

        # classes
        for cls in data["classes"]:
            graph.add_node(cls, type="class")
            graph.add_edge(file_path, cls, relation="defines")

        # imports → convert to file dependency
        for imp in data["imports"]:

            parts = imp.split()

            if len(parts) >= 2:

                module_name = parts[-1].split(".")[0]

                if module_name in module_map:

                    imported_file = module_map[module_name]

                    graph.add_edge(file_path, imported_file, relation="imports")

    return graph
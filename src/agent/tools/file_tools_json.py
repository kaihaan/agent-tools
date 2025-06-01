"""
Tools

Exports
- tool_list = [list_files, read_file]
- tool_lookup = {tool.name: tool for tool in tool_list}
"""

import os
import inspect
from typing import get_type_hints, get_origin, get_args, Union


def python_type_to_json_type(py_type):
    """Convert Python type to JSON Schema type."""
    origin = get_origin(py_type)
    args = get_args(py_type)

    if origin is Union and type(None) in args:
        # Optional[X] case
        real_type = args[0] if args[0] is not type(None) else args[1]
        return python_type_to_json_type(real_type)

    type_map = {
        str: "string",
        int: "integer",
        float: "number",
        bool: "boolean",
        list: "array",
        dict: "object",
    }

    return type_map.get(py_type, "string")  # fallback to string


def tool(description: str = ""):
    param_desc = description

    def decorator(func):
        sig = inspect.signature(func)
        params = sig.parameters
        type_hints = get_type_hints(func)

        properties = {}
        required = []

        for name, param in params.items():
            py_type = type_hints.get(name, str)
            json_type = python_type_to_json_type(py_type)

            properties[name] = {"type": json_type}

            if param.default is inspect.Parameter.empty:
                required.append(name)

        class ToolWrapper:
            """ decorator class """
            name = func.__name__
            description = param_desc or (func.__doc__.strip() if func.__doc__ else "")
            parameters = {
                "type": "function",
                "args": properties,
                "required": required,
            }

            def run(self, **kwargs):
                """ allowa wrapped func to be called """
                return func(**kwargs)

            def schema(self):
                """ get tool details """
                return {
                    "tool_name": self.name,
                    "description": self.description,
                    "args": self.parameters,
                }

        return ToolWrapper()

    return decorator


@tool(description="List all files in the current directory.")
def list_files() -> str:
    """list files"""
    return [f for f in os.listdir("src") if f.endswith(".py")]


@tool(description="Read the content of a file.")
def read_file(file_path: str) -> str:
    """read file"""
    try:
        with open(f"src\{file_path}", "r", encoding='utf8') as file:
            return file.read()
    except FileNotFoundError:
        return f"Error: {file_path} not found."
    except Exception as e:
        return f"Error: {str(e)}"


@tool(
    description="End the agent loop and print a summary to the user. ",
)
def terminate(msg: str):
    """terminate execution"""
    print("** Terminate ", msg)
    return "TERMINATED"


tool_list = [list_files, read_file, terminate]
tool_lookup = {tool.name: tool for tool in tool_list}

# tool_lookup["read"].run(file="helloworld")
# print(tool_lookup["read"].args_schema(file="hjk"))
for tool in tool_list:
    print(tool.parameters)
    if tool.parameters["args"]:
        print("Has args!!!")

# tool_lookup["read_file"].run(file_path="src/hellO")
# print(tool_lookup["read_file"].parameters)
# print(tool_lookup["read"].name)
# k = str(tool_lookup["read"].kwargs)
# for param, param_type in tool_lookup["read"].kwargs.items():
#     print(f"- {param} ({param_type[0].__name__})")

# print(arg for arg in tool_lookup["read"].args_schema.field_definitions)

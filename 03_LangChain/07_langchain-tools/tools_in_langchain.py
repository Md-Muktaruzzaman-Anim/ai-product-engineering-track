# ==========================================
# LangChain Tools Demonstration Notebook
# ==========================================

# ------------------------------------------
# 1. Installation
# ------------------------------------------
# !pip install langchain langchain-core langchain-community pydantic duckduckgo-search langchain_experimental

from typing import Type
from pydantic import BaseModel, Field
from langchain_core.tools import tool
from langchain.tools import StructuredTool, BaseTool
from langchain_community.tools import DuckDuckGoSearchRun, ShellTool

# ------------------------------------------
# 2. Built-in Tools Examples
# ------------------------------------------

# DuckDuckGo Search Tool
print("--- DuckDuckGo Search Tool ---")
search_tool = DuckDuckGoSearchRun()
try:
    results = search_tool.invoke('top news in india today')
    print("Search Results:\n", results)
except Exception as e:
    print(f"Search execution failed (likely network-related): {e}")

print("Tool Name:", search_tool.name)
print("Description:", search_tool.description)
print("Arguments:", search_tool.args)
print("\n")

# Shell Tool
print("--- Shell Tool ---")
shell_tool = ShellTool()
results = shell_tool.invoke('ls')
print("Shell Command Results:\n", results)
print("\n")


# ------------------------------------------
# 3. Custom Tools
# ------------------------------------------

# Method 1: Using the @tool Decorator
print("--- Custom Tool: Method 1 (@tool decorator) ---")
@tool
def multiply_decorator(a: int, b: int) -> int:
    """Multiply two numbers"""
    return a * b

result_m1 = multiply_decorator.invoke({"a": 3, "b": 5})
print("Result:", result_m1)
print("Tool Name:", multiply_decorator.name)
print("Description:", multiply_decorator.description)
print("Arguments Schema:", multiply_decorator.args)
print("JSON Schema:\n", multiply_decorator.args_schema.model_json_schema())
print("\n")


# Method 2: Using the StructuredTool Factory Class
print("--- Custom Tool: Method 2 (StructuredTool) ---")
class MultiplyInputM2(BaseModel):
    a: int = Field(required=True, description="The first number to add")
    b: int = Field(required=True, description="The second number to add")

def multiply_func_m2(a: int, b: int) -> int:
    return a * b

multiply_tool_m2 = StructuredTool.from_function(
    func=multiply_func_m2,
    name="multiply",
    description="Multiply two numbers",
    args_schema=MultiplyInputM2
)

result_m2 = multiply_tool_m2.invoke({'a': 3, 'b': 3})
print("Result:", result_m2)
print("Tool Name:", multiply_tool_m2.name)
print("Description:", multiply_tool_m2.description)
print("Arguments:", multiply_tool_m2.args)
print("\n")


# Method 3: Subclassing the BaseTool Class
print("--- Custom Tool: Method 3 (BaseTool Subclass) ---")
class MultiplyInputM3(BaseModel):
    a: int = Field(required=True, description="The first number to add")
    b: int = Field(required=True, description="The second number to add")

class MultiplyTool(BaseTool):
    name: str = "multiply"
    description: str = "Multiply two numbers"
    args_schema: Type[BaseModel] = MultiplyInputM3

    def _run(self, a: int, b: int) -> int:
        return a * b

multiply_tool_m3 = MultiplyTool()
result_m3 = multiply_tool_m3.invoke({'a': 3, 'b': 3})

print("Result:", result_m3)
print("Tool Name:", multiply_tool_m3.name)
print("Description:", multiply_tool_m3.description)
print("Arguments:", multiply_tool_m3.args)
print("\n")


# ------------------------------------------
# 4. Creating and Bundling a Custom Toolkit
# ------------------------------------------
print("--- Toolkits ---")
@tool
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b

@tool
def multiply_toolkit(a: int, b: int) -> int:
    """Multiply two numbers"""
    return a * b

class MathToolkit:
    def get_tools(self):
        return [add, multiply_toolkit]

toolkit = MathToolkit()
tools = toolkit.get_tools()

print("Available Tools in Toolkit:")
for t in tools:
    print(f"- {t.name} => {t.description}")

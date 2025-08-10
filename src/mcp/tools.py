"""MCP tools for mathematical operations."""

import re
from typing import Dict, Union, List
from langchain_core.tools import tool


@tool
def add_numbers(inputs: str) -> dict:
    """
    Adds a list of numbers provided in the input string.
    
    Parameters:
    - inputs (str): string containing numbers that can be extracted and summed.
    
    Returns:
    - dict: A dictionary with a single key "result" containing the sum of the numbers.
    
    Example Input: "Add the numbers 10, 20, and 30."
    Example Output: {"result": 60}
    """
    # Use regular expressions to extract all numbers from the input
    numbers = [int(num) for num in re.findall(r'\d+', inputs)]
    result = sum(numbers)
    return {"result": result}


@tool  
def subtract_numbers(inputs: str) -> dict:
    """
    Extracts numbers from a string and performs subtraction sequentially, starting with the first number.
    
    Parameters:
    - inputs (str): A string containing numbers to subtract.
    
    Returns:
    - dict: A dictionary containing the key "result" with the calculated difference.
    
    Example Input: "100, 20, 10"
    Example Output: {"result": 70}
    """
    # Extract numbers from the string
    numbers = [int(num) for num in inputs.replace(",", "").split() if num.isdigit()]

    # If no numbers are found, return 0
    if not numbers:
        return {"result": 0}

    # Start with the first number
    result = numbers[0]

    # Subtract all subsequent numbers
    for num in numbers[1:]:
        result -= num

    return {"result": result}


@tool
def multiply_numbers(inputs: str) -> dict:
    """
    Extracts numbers from a string and calculates their product.
    
    Parameters:
    - inputs (str): A string containing numbers separated by spaces, commas, or other delimiters.
    
    Returns:
    - dict: A dictionary with the key "result" containing the product of the numbers.
    
    Example Input: "2, 3, 4"
    Example Output: {"result": 24}
    """
    # Extract numbers from the string
    numbers = [int(num) for num in inputs.replace(",", "").split() if num.isdigit()]

    # If no numbers are found, return 1
    if not numbers:
        return {"result": 1}

    # Calculate the product of the numbers
    result = 1
    for num in numbers:
        result *= num

    return {"result": result}


@tool
def divide_numbers(inputs: str) -> dict:
    """
    Extracts numbers from a string and calculates the result of dividing the first number 
    by the subsequent numbers in sequence.
    
    Parameters:
    - inputs (str): A string containing numbers separated by spaces, commas, or other delimiters.
    
    Returns:
    - dict: A dictionary with the key "result" containing the quotient.
    
    Example Input: "100, 5, 2"
    Example Output: {"result": 10.0}
    """
    # Extract numbers from the string
    numbers = [int(num) for num in inputs.replace(",", "").split() if num.isdigit()]

    # If no numbers are found, return 0
    if not numbers:
        return {"result": 0}

    # Calculate the result of dividing the first number by subsequent numbers
    result = numbers[0]
    for num in numbers[1:]:
        if num == 0:
            return {"result": "Error: Division by zero"}
        result /= num

    return {"result": result}


@tool
def search_wikipedia(query: str) -> str:
    """
    Search Wikipedia for factual information about a topic.
    
    Parameters:
    - query (str): The topic or question to search for on Wikipedia
    
    Returns:
    - str: A summary of relevant information from Wikipedia
    """
    try:
        from langchain_community.utilities import WikipediaAPIWrapper
        wiki = WikipediaAPIWrapper()
        return wiki.run(query)
    except ImportError:
        return "Wikipedia search not available. Please install wikipedia package."
    except Exception as e:
        return f"Error searching Wikipedia: {str(e)}"


def get_math_tools() -> List:
    """Get all available mathematical tools."""
    return [
        add_numbers,
        subtract_numbers, 
        multiply_numbers,
        divide_numbers,
        search_wikipedia
    ]


def get_tool_schemas() -> List[Dict]:
    """Get tool schemas for MCP server."""
    tools = get_math_tools()
    schemas = []
    
    for tool in tools:
        schema = {
            "name": tool.name,
            "description": tool.description,
            "inputSchema": {
                "type": "object",
                "properties": tool.args,
                "required": list(tool.args.keys()) if tool.args else []
            }
        }
        schemas.append(schema)
    
    return schemas

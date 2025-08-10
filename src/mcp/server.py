"""MCP server for exposing model switcher tools."""

import asyncio
import json
from typing import Any, Dict, List
import logging

from .tools import get_math_tools, get_tool_schemas

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MCPServer:
    """MCP Server for model switcher tools."""
    
    def __init__(self):
        """Initialize the MCP server."""
        self.tools = {tool.name: tool for tool in get_math_tools()}
        self.tool_schemas = get_tool_schemas()
        
    async def list_tools(self) -> List[Dict]:
        """List all available tools."""
        return self.tool_schemas
    
    async def call_tool(self, name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Call a specific tool with arguments."""
        if name not in self.tools:
            return {
                "error": f"Tool '{name}' not found. Available tools: {list(self.tools.keys())}"
            }
        
        try:
            tool = self.tools[name]
            result = tool.invoke(arguments)
            return {"result": result}
        except Exception as e:
            logger.error(f"Error calling tool '{name}': {e}")
            return {"error": str(e)}
    
    async def get_tool_info(self, name: str) -> Dict[str, Any]:
        """Get information about a specific tool."""
        if name not in self.tools:
            return {"error": f"Tool '{name}' not found"}
        
        for schema in self.tool_schemas:
            if schema["name"] == name:
                return schema
        
        return {"error": f"Schema for tool '{name}' not found"}
    
    async def health_check(self) -> Dict[str, str]:
        """Health check endpoint."""
        return {
            "status": "healthy",
            "tools_count": len(self.tools),
            "available_tools": list(self.tools.keys())
        }


class MCPProtocolHandler:
    """Handler for MCP protocol messages."""
    
    def __init__(self, server: MCPServer):
        """Initialize with an MCP server instance."""
        self.server = server
    
    async def handle_message(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """Handle incoming MCP protocol messages."""
        method = message.get("method")
        params = message.get("params", {})
        
        if method == "tools/list":
            tools = await self.server.list_tools()
            return {"tools": tools}
        
        elif method == "tools/call":
            name = params.get("name")
            arguments = params.get("arguments", {})
            result = await self.server.call_tool(name, arguments)
            return result
        
        elif method == "tools/info":
            name = params.get("name")
            info = await self.server.get_tool_info(name)
            return info
        
        elif method == "health":
            health = await self.server.health_check()
            return health
        
        else:
            return {"error": f"Unknown method: {method}"}


async def run_server(host: str = "localhost", port: int = 8765):
    """Run the MCP server."""
    import websockets
    
    server = MCPServer()
    handler = MCPProtocolHandler(server)
    
    async def handle_websocket(websocket, path):
        """Handle WebSocket connections."""
        logger.info(f"New connection from {websocket.remote_address}")
        
        async for raw_message in websocket:
            try:
                message = json.loads(raw_message)
                response = await handler.handle_message(message)
                await websocket.send(json.dumps(response))
            except json.JSONDecodeError:
                error_response = {"error": "Invalid JSON message"}
                await websocket.send(json.dumps(error_response))
            except Exception as e:
                logger.error(f"Error handling message: {e}")
                error_response = {"error": str(e)}
                await websocket.send(json.dumps(error_response))
    
    logger.info(f"Starting MCP server on {host}:{port}")
    async with websockets.serve(handle_websocket, host, port):
        await asyncio.Future()  # Run forever


def main():
    """Main entry point for the MCP server."""
    import argparse
    
    parser = argparse.ArgumentParser(description="LangChain Model Switcher MCP Server")
    parser.add_argument("--host", default="localhost", help="Host to bind to")
    parser.add_argument("--port", type=int, default=8765, help="Port to bind to")
    
    args = parser.parse_args()
    
    try:
        asyncio.run(run_server(args.host, args.port))
    except KeyboardInterrupt:
        logger.info("Server stopped by user")
    except Exception as e:
        logger.error(f"Server error: {e}")


if __name__ == "__main__":
    main()

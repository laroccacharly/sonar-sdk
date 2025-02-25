from typing import List, Optional, Tuple
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from rich.table import Table
from rich import box
from datetime import datetime
from pathlib import Path
from rich.console import RenderableType
from openai.types.chat.chat_completion import ChatCompletion

def format_response(response: ChatCompletion) -> Tuple[str, List[RenderableType]]:
    """
    Format the ChatCompletion response into rich renderables.
    
    Args:
        response: The ChatCompletion response from the API
        
    Returns:
        Tuple containing:
        - Formatted content with citation markers replaced
        - List of rich renderables for display or saving
    """
    # Extract the response content
    content = response.choices[0].message.content
    
    # Process citations if they exist
    citations: Optional[List[str]] = getattr(response, 'citations', None)
    
    # If we have citations, replace the citation markers with superscript numbers
    if citations:
        # Replace citation markers like [1] with superscript numbers
        for i in range(len(citations)):
            marker = f"[{i+1}]"
            content = content.replace(marker, f"^{i+1}^")
    
    # Create a list to store all renderables
    renderables: List[RenderableType] = []
    
    # Format the main response content
    response_panel = Panel(
        Markdown(content),
        title="[bold blue]Response",
        border_style="blue",
        box=box.ROUNDED
    )
    renderables.append(response_panel)
    
    # Format usage statistics
    if response.usage:
        usage_table = Table(title="Usage Statistics", box=box.SIMPLE)
        usage_table.add_column("Metric", style="cyan")
        usage_table.add_column("Value", style="green")
        
        usage = response.usage
        usage_table.add_row("Prompt Tokens", str(usage.prompt_tokens))
        usage_table.add_row("Completion Tokens", str(usage.completion_tokens))
        usage_table.add_row("Total Tokens", str(usage.total_tokens))
        
        # Add citation tokens if available
        citation_tokens = getattr(usage, 'citation_tokens', None)
        if citation_tokens:
            usage_table.add_row("Citation Tokens", str(citation_tokens))
        
        # Add search queries if available
        num_search_queries = getattr(usage, 'num_search_queries', None)
        if num_search_queries:
            usage_table.add_row("Search Queries", str(num_search_queries))
        
        renderables.append(usage_table)
    
    # Format citations if available
    if citations and len(citations) > 0:
        citation_table = Table(title="Citations", box=box.SIMPLE)
        citation_table.add_column("#", style="cyan", justify="right")
        citation_table.add_column("Source", style="blue")
        
        for i, citation in enumerate(citations):
            citation_table.add_row(f"{i+1}", citation)
        
        renderables.append(citation_table)
    
    return content, renderables


def display_response(response: ChatCompletion, save_to_file: bool = False):
    """
    Display the ChatCompletion response in a well-formatted way.
    
    Args:
        response: The ChatCompletion response from the API
        save_to_file: Whether to save the formatted response to a file
    """
    # Format the response
    _, renderables = format_response(response)
    
    # Display the renderables
    console = Console()
    console.print("\n")
    
    for renderable in renderables:
        console.print(renderable)
        
    console.print("\n")
    
    # Save to file if requested
    if save_to_file:
        save_response_to_file(response)


def save_response_to_file(response: ChatCompletion):
    """
    Save the formatted response to a file in the 'responses' folder.
    
    Args:
        response: The ChatCompletion response from the API
    """
    # Create responses directory if it doesn't exist
    responses_dir = Path("responses")
    responses_dir.mkdir(exist_ok=True)
    
    # Generate a filename based on timestamp and model
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    model_name = response.model.replace("-", "_")
    filename = f"{timestamp}_{model_name}.txt"
    filepath = responses_dir / filename
    
    # Format the response
    _, renderables = format_response(response)
    
    # Create a console for file output
    file_console = Console(file=open(filepath, "w"), width=100)
    
    # Write the renderables to the file
    file_console.print("\n")
    
    for renderable in renderables:
        file_console.print(renderable)
        file_console.print("\n")
    
    # Close the file
    file_console.file.close()
    
    print(f"\nResponse saved to: {filepath}")
from pathlib import Path

from langgraph.graph.state import CompiledStateGraph


def save_graph_image(graph: CompiledStateGraph) -> None:
    save_dir = Path("images/graphs")
    save_dir.mkdir(exist_ok=True)
    filename = save_dir / "graph.png"

    try:
        png_data = graph.get_graph().draw_mermaid_png()
        filename.write_bytes(png_data)
    except Exception as e:
        print(f"Не удалось сохранить граф: {e}")


__all__ = ["save_graph_image"]
import os

from markdown_it import MarkdownIt

from ...domain.services.document_processor.i_processor import (
    IDocumentProcessor,
)
from ...domain.services.document_processor.schemas import CommandChunkData


class MarkdownCommandProcessor(IDocumentProcessor):
    def __init__(self, *args, **kwargs):
        self.separator_string = kwargs.get("separator_string", "\n")
        self.document_path = kwargs.get("document_path", "")

    def generate_md_tokens(self):
        md = MarkdownIt()
        with open(self.document_path, "r", encoding="utf-8") as f:
            content = f.read()
        return md.parse(content)

    def extract_commands_json(self):
        tokens = self.generate_md_tokens()
        commands = []
        current = {}
        state = None
        command_name = ""
        for token in tokens:
            # Detecta el inicio de un nuevo comando
            if token.type == "heading_open" and token.tag == "h2":
                state = "name"
                current = {}
                continue
            if state == "name" and token.type == "inline":
                command_name = token.content.strip()
                state = None
                continue
            if token.type == "heading_open" and token.tag == "h3":
                state = "command_section"
                continue
            if state == "command_section":
                if (
                    state == "command_section"
                    and token.type == "inline"
                    and "Comando" in token.content
                ):
                    state = "command_name"

                if (
                    state == "command_section"
                    and token.type == "inline"
                    and "Descripción" in token.content
                ):
                    state = "command_description"

                if (
                    state == "command_section"
                    and token.type == "inline"
                    and "Instrucción" in token.content
                ):
                    state = "command_instruction"
                continue

            if state == "command_name" and token.type == "inline":
                current["metadata"] = {
                    "command": token.content.strip(),
                }
                state = None
                continue

            if state == "command_description" and token.type == "inline":
                current["text"] = f"{command_name}: {token.content.strip()}"
                state = None
                continue

            if state == "command_instruction" and token.type == "inline":
                current["metadata"]["data"] = token.content.strip()
                state = None
                continue
            # Extrae el nombre del comando

            # Cuando encuentra un separador, guarda el comando
            if token.type == "hr":
                if current:
                    commands.append(CommandChunkData(**current))
                    current = {}
        # Añade el último comando si no hay separador al final
        if current:
            commands.append(CommandChunkData(**current))
        return commands

    def document_chunk_generator(self):
        chunk_list = self.extract_commands_json()
        for chunk in chunk_list:
            yield chunk

    # Implement specific methods for Markdown processing here


if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))

    file_path = os.path.join(current_dir, "../documents/markdown/commands.md")
    processor = MarkdownCommandProcessor(
        document_path=file_path
    ).extract_commands_json()
    print(processor)

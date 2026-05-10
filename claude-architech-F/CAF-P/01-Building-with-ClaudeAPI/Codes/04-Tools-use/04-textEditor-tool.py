# ===== IMPORTS =====
from dotenv import load_dotenv
from anthropic import Anthropic
from anthropic.types import Message
import os
import shutil
import json
from typing import Optional, List

# ===== INITIALIZATION =====
load_dotenv()

client = Anthropic()
model = "claude-sonnet-4-5"


# ===== HELPER FUNCTIONS =====
def add_user_message(messages, message):
    """Add a user message to the conversation history."""
    user_message = {
        "role": "user",
        "content": message.content if isinstance(message, Message) else message,
    }
    messages.append(user_message)


def add_assistant_message(messages, message):
    """Add an assistant message to the conversation history."""
    assistant_message = {
        "role": "assistant",
        "content": message.content if isinstance(message, Message) else message,
    }
    messages.append(assistant_message)


def chat(messages, system=None, temperature=1.0, stop_sequences=[], tools=None):
    """Call Claude API with messages and optional tools."""
    params = {
        "model": model,
        "max_tokens": 1000,
        "messages": messages,
        "temperature": temperature,
        "stop_sequences": stop_sequences,
    }

    if tools:
        params["tools"] = tools

    if system:
        params["system"] = system

    message = client.messages.create(**params)
    return message


def text_from_message(message):
    """Extract text content from a message response object."""
    return "\n".join([block.text for block in message.content if block.type == "text"])


# ===== TEXT EDITOR TOOL IMPLEMENTATION =====
"""
TEXT EDITOR TOOL OVERVIEW:
Claude's built-in text editor tool is a pre-built schema that Claude already knows about.
This TextEditorTool class provides the IMPLEMENTATION (the actual functions that execute).

KEY CONCEPT:
- Claude provides the schema (knows what the tool is called and what it can do)
- WE provide the implementation (the actual Python code that performs file operations)

When Claude calls the text editor tool:
  1. Claude sends a request like "create_file" or "str_replace"
  2. Our run_tool() function receives the request
  3. We execute the corresponding TextEditorTool method
  4. We return the result back to Claude

SAFETY FEATURES:
- Path validation: prevents access outside base directory
- Backup system: creates backups before modifying files
- Error handling: graceful failures with informative messages
"""

class TextEditorTool:
    """
    A secure text editor tool that implements file operations for Claude.

    Operations supported:
    - view: Display file or directory contents (with optional line range)
    - create: Create a new file with specified content
    - str_replace: Replace exact text in a file (must match exactly once)
    - insert: Insert text at a specific line
    - undo_edit: Restore file from backup

    Security features:
    - All file paths are validated against base_dir (prevents directory traversal)
    - Automatic backups created before file modifications
    - Timestamped backup files allow recovery of previous edits
    """

    def __init__(self, base_dir: str = "", backup_dir: str = ""):
        """
        Initialize the text editor tool.

        Args:
            base_dir: Root directory where all file operations are confined
                     (security feature prevents access outside this directory)
                     Defaults to current working directory
            backup_dir: Directory where file backups are stored
                       Defaults to .backups folder in base_dir
        """
        self.base_dir = base_dir or os.getcwd()
        self.backup_dir = backup_dir or os.path.join(self.base_dir, ".backups")
        os.makedirs(self.backup_dir, exist_ok=True)

    def _validate_path(self, file_path: str) -> str:
        """
        Validate that the file path is within the allowed base directory.

        SECURITY: This prevents directory traversal attacks where Claude might try
        to access files outside the intended directory using paths like:
        - "../../../etc/passwd" (go up directories then access elsewhere)
        - "/../sensitive_file" (break out of sandbox)

        Args:
            file_path: Path to validate (relative to base_dir)

        Returns:
            Absolute normalized path if valid

        Raises:
            ValueError: If path is outside base_dir
        """
        abs_path = os.path.normpath(os.path.join(self.base_dir, file_path))
        if not abs_path.startswith(self.base_dir):
            raise ValueError(
                f"Access denied: Path '{file_path}' is outside the allowed directory"
            )
        return abs_path

    def _backup_file(self, file_path: str) -> str:
        """Create a backup of the file before modifying it."""
        if not os.path.exists(file_path):
            return ""
        file_name = os.path.basename(file_path)
        backup_path = os.path.join(
            self.backup_dir, f"{file_name}.{os.path.getmtime(file_path):.0f}"
        )
        shutil.copy2(file_path, backup_path)
        return backup_path

    def _restore_backup(self, file_path: str) -> str:
        """Restore a file from the latest backup."""
        file_name = os.path.basename(file_path)
        backups = [
            f for f in os.listdir(self.backup_dir) if f.startswith(file_name + ".")
        ]
        if not backups:
            raise FileNotFoundError(f"No backups found for {file_path}")

        latest_backup = sorted(backups, reverse=True)[0]
        backup_path = os.path.join(self.backup_dir, latest_backup)

        shutil.copy2(backup_path, file_path)
        return f"Successfully restored {file_path} from backup"

    def _count_matches(self, content: str, old_str: str) -> int:
        """Count the number of matches of old_str in content."""
        return content.count(old_str)

    def view(self, file_path: str, view_range: Optional[List[int]] = None) -> str:
        """View the contents of a file, optionally within a specific line range."""
        try:
            abs_path = self._validate_path(file_path)

            if os.path.isdir(abs_path):
                try:
                    return "\n".join(os.listdir(abs_path))
                except PermissionError:
                    raise PermissionError(
                        "Permission denied. Cannot list directory contents."
                    )

            if not os.path.exists(abs_path):
                raise FileNotFoundError("File not found")

            with open(abs_path, "r", encoding="utf-8") as f:
                content = f.read()

            if view_range:
                start, end = view_range
                lines = content.split("\n")

                if end == -1:
                    end = len(lines)

                selected_lines = lines[start - 1 : end]

                result = []
                for i, line in enumerate(selected_lines, start):
                    result.append(f"{i}: {line}")

                return "\n".join(result)
            else:
                lines = content.split("\n")
                result = []
                for i, line in enumerate(lines, 1):
                    result.append(f"{i}: {line}")

                return "\n".join(result)

        except UnicodeDecodeError:
            raise UnicodeDecodeError(
                "utf-8",
                b"",
                0,
                1,
                "File contains non-text content and cannot be displayed.",
            )
        except ValueError as e:
            raise ValueError(str(e))
        except PermissionError:
            raise PermissionError("Permission denied. Cannot access file.")
        except Exception as e:
            raise type(e)(str(e))

    def str_replace(self, file_path: str, old_str: str, new_str: str) -> str:
        """
        Replace text in a file with exact match requirement (prevents ambiguity).

        KEY RULE: Replaces only if old_str matches EXACTLY ONCE in the file.
        This prevents accidental replacements when text appears multiple times.

        Example:
        - If file has: "def foo():" appearing 3 times
        - Replacing "def foo():" will FAIL (too many matches)
        - You must provide more context: "class A:\n    def foo():"
        - Then it will replace only that specific occurrence

        Workflow:
        1. Read entire file
        2. Count how many times old_str appears
        3. If count != 1, raise error (0 matches or >1 matches)
        4. Create backup of original file
        5. Replace the text
        6. Write modified content back

        Args:
            file_path: Path to file (relative to base_dir)
            old_str: Text to find (must appear exactly once)
            new_str: Text to replace it with

        Returns:
            Success message

        Raises:
            FileNotFoundError: If file doesn't exist
            ValueError: If old_str matches 0 or >1 times
        """
        try:
            abs_path = self._validate_path(file_path)

            if not os.path.exists(abs_path):
                raise FileNotFoundError("File not found")

            with open(abs_path, "r", encoding="utf-8") as f:
                content = f.read()

            match_count = self._count_matches(content, old_str)

            if match_count == 0:
                raise ValueError(
                    "No match found for replacement. Please check your text and try again."
                )
            elif match_count > 1:
                raise ValueError(
                    f"Found {match_count} matches for replacement text. Please provide more context to make a unique match."
                )

            # Create backup before modifying file (allows undo)
            self._backup_file(abs_path)

            new_content = content.replace(old_str, new_str)

            with open(abs_path, "w", encoding="utf-8") as f:
                f.write(new_content)

            return "Successfully replaced text at exactly one location."

        except ValueError as e:
            raise ValueError(str(e))
        except PermissionError:
            raise PermissionError("Permission denied. Cannot modify file.")
        except Exception as e:
            raise type(e)(str(e))

    def create(self, file_path: str, file_text: str) -> str:
        """Create a new file with the specified content."""
        try:
            abs_path = self._validate_path(file_path)

            if os.path.exists(abs_path):
                raise FileExistsError(
                    "File already exists. Use str_replace to modify it."
                )

            os.makedirs(os.path.dirname(abs_path), exist_ok=True)

            with open(abs_path, "w", encoding="utf-8") as f:
                f.write(file_text)

            return f"Successfully created {file_path}"

        except ValueError as e:
            raise ValueError(str(e))
        except PermissionError:
            raise PermissionError("Permission denied. Cannot create file.")
        except Exception as e:
            raise type(e)(str(e))

    def insert(self, file_path: str, insert_line: int, new_str: str) -> str:
        """Insert text at a specific line in a file."""
        try:
            abs_path = self._validate_path(file_path)

            if not os.path.exists(abs_path):
                raise FileNotFoundError("File not found")

            self._backup_file(abs_path)

            with open(abs_path, "r", encoding="utf-8") as f:
                lines = f.readlines()

            if lines and not lines[-1].endswith("\n"):
                new_str = "\n" + new_str

            if insert_line == 0:
                lines.insert(0, new_str + "\n")
            elif insert_line > 0 and insert_line <= len(lines):
                lines.insert(insert_line, new_str + "\n")
            else:
                raise IndexError(
                    f"Line number {insert_line} is out of range. File has {len(lines)} lines."
                )

            with open(abs_path, "w", encoding="utf-8") as f:
                f.writelines(lines)

            return f"Successfully inserted text after line {insert_line}"

        except ValueError as e:
            raise ValueError(str(e))
        except PermissionError:
            raise PermissionError("Permission denied. Cannot modify file.")
        except Exception as e:
            raise type(e)(str(e))

    def undo_edit(self, file_path: str) -> str:
        """Undo the last edit by restoring from backup."""
        try:
            abs_path = self._validate_path(file_path)

            if not os.path.exists(abs_path):
                raise FileNotFoundError("File not found")

            return self._restore_backup(abs_path)

        except ValueError as e:
            raise ValueError(str(e))
        except FileNotFoundError:
            raise FileNotFoundError("No previous edits to undo")
        except PermissionError:
            raise PermissionError("Permission denied. Cannot restore file.")
        except Exception as e:
            raise type(e)(str(e))


# ===== TOOL EXECUTION =====
text_editor_tool = TextEditorTool()


def run_tool(tool_name, tool_input):
    """
    Execute a tool command based on its name and input parameters.

    This is the ROUTER function that bridges:
    - Claude's tool requests (what Claude wants to do)
    - Our implementation (actual Python functions)

    Flow when Claude calls a tool:
    1. Claude says: "I want to use str_replace_based_edit_tool"
    2. Claude specifies: command="str_replace", path="file.py", old_str="...", new_str="..."
    3. run_tool() receives (tool_name="str_replace_editor", tool_input={...})
    4. We extract the command from tool_input
    5. We call the corresponding TextEditorTool method
    6. We return the result to Claude

    Supported commands:
    - "view": Read file contents (optional: line range)
    - "str_replace": Replace text (exact match, exactly once)
    - "create": Create new file
    - "insert": Insert text at line number
    - "undo_edit": Restore from backup

    Args:
        tool_name: Name of tool (always "str_replace_editor" for text editor tool)
        tool_input: Dictionary with "command" and command-specific parameters

    Returns:
        Result from the executed command (success message or file contents)

    Raises:
        Exception: If unknown tool_name or command
    """
    if tool_name == "str_replace_editor":
        command = tool_input["command"]
        if command == "view":
            return text_editor_tool.view(
                tool_input["path"], tool_input.get("view_range")
            )
        elif command == "str_replace":
            return text_editor_tool.str_replace(
                tool_input["path"], tool_input["old_str"], tool_input["new_str"]
            )
        elif command == "create":
            return text_editor_tool.create(tool_input["path"], tool_input["file_text"])
        elif command == "insert":
            return text_editor_tool.insert(
                tool_input["path"],
                tool_input["insert_line"],
                tool_input["new_str"],
            )
        elif command == "undo_edit":
            return text_editor_tool.undo_edit(tool_input["path"])
        else:
            raise Exception(f"Unknown text editor command: {command}")
    else:
        raise Exception(f"Unknown tool name: {tool_name}")


def run_tools(message):
    """
    Extract all tool calls from Claude's response and execute them.

    Multi-turn conversation flow:
    1. User: "Create a file called test.py"
    2. Claude: "I'll use str_replace_editor to create that file"
    3. run_tools() receives Claude's response message
    4. Extract tool_use blocks (Claude's requests)
    5. Execute each tool call
    6. Format results with linking information
    7. Return to Claude for next turn

    Key concept - TOOL_USE_ID LINKING:
    - Claude generates a tool_use_id when requesting a tool
    - We include that SAME tool_use_id in the result
    - This links: Claude's request → our response → Claude's next turn
    - Without this linking, Claude wouldn't know which result goes with which request

    Error handling:
    - If tool execution fails, we catch the exception
    - Format it as a tool_result with is_error=True
    - Claude sees the error and can retry or inform the user

    Args:
        message: Claude's response message containing tool requests

    Returns:
        List of tool_result blocks formatted for Claude:
        {
            "type": "tool_result",
            "tool_use_id": "...",  # Links back to Claude's request
            "content": "...",      # Result or error message
            "is_error": False/True # Whether this was a failure
        }
    """
    # Step 1: Extract all tool_use blocks from Claude's response
    # Claude may request multiple tools in one response
    tool_requests = [block for block in message.content if block.type == "tool_use"]
    tool_result_blocks = []

    # Step 2: Process each tool request
    for tool_request in tool_requests:
        try:
            # Execute the tool with Claude's parameters
            tool_output = run_tool(tool_request.name, tool_request.input)

            # Format success result
            tool_result_block = {
                "type": "tool_result",
                "tool_use_id": tool_request.id,  # CRITICAL: link back to Claude's request
                "content": json.dumps(tool_output),  # Convert result to JSON
                "is_error": False
            }
        except Exception as e:
            # Format error result - still includes tool_use_id for linking
            tool_result_block = {
                "type": "tool_result",
                "tool_use_id": tool_request.id,  # CRITICAL: link error back to request
                "content": f"Error: {e}",
                "is_error": True
            }

        tool_result_blocks.append(tool_result_block)

    return tool_result_blocks


# ===== TOOL SCHEMA =====
"""
IMPORTANT: Text Editor Tool Schema

Claude has a BUILT-IN text editor tool, meaning:
1. Claude already knows about this tool (built into its training)
2. Claude knows what operations it can do (view, create, str_replace, insert, undo)
3. Claude knows how to request it

WE only provide a SMALL SCHEMA STUB (the type and name):
- The "type" identifies the schema version for your model
- Claude expands this to the full schema automatically behind the scenes

Different Claude models use different schema versions:
- claude-3-7-sonnet: "text_editor_20250124"
- claude-3-5-sonnet: "text_editor_20241022"
- claude-sonnet-4-5: "text_editor_20250728"

You can find all version strings at:
https://docs.anthropic.com/en/docs/agents-and-tools/tool-use/text-editor-tool

When Claude calls this tool:
1. Claude says "I want to use str_replace_based_edit_tool with command 'create'"
2. run_tools() receives this request
3. We execute text_editor_tool.create() method
4. TextEditorTool.create() performs the actual file creation
"""

def get_text_edit_schema(model):
    """
    Get the text editor tool schema stub for the current model version.

    Args:
        model: Model identifier (e.g., "claude-sonnet-4-5")

    Returns:
        Dictionary with "type" and "name" fields that tells Claude:
        - What version of the text editor tool to use
        - What the tool is called (str_replace_based_edit_tool)

    The "type" field specifies the schema version - Claude will expand
    this small stub into the full tool specification internally.
    """
    return {
        "type": "text_editor_20250728",  # Schema version for claude-sonnet-4-5
        "name": "str_replace_based_edit_tool",  # Name Claude uses to call this tool
    }


# ===== CONVERSATION LOOP =====
"""
MULTI-TURN CONVERSATION WITH TOOLS

The run_conversation function implements the agentic loop:
1. Send user query + available tools to Claude
2. Claude responds (may include text and/or tool calls)
3. If Claude called tools, execute them and send results back
4. Repeat from step 1 with tool results added to history
5. Stop when Claude responds without requesting tools

Example conversation flow:
User: "Create a file with Python code"
  ↓
Claude: (analyzes request) "I'll create that file using str_replace_editor"
  ├─ Returns: text="I'm creating..." + tool_call(command="create", ...)
  ↓
run_tools() executes: text_editor_tool.create(...)
  ├─ Returns: "Successfully created file.py"
  ↓
Add tool result to history and loop again
  ↓
Claude: (sees result) "I've successfully created the file"
  ├─ Returns: text="I've created..." + no tool calls
  ↓
stop_reason != "tool_use" → conversation ends
"""

def run_conversation(messages):
    """
    Run the multi-turn conversation loop with text editor tool support.

    Orchestrates the complete agent loop:
    - Sends messages and tools to Claude
    - Executes any tools Claude requests
    - Feeds results back to Claude
    - Continues until Claude stops using tools

    Message history format:
    [
        {"role": "user", "content": "user query"},
        {"role": "assistant", "content": "Claude's response"},
        {"role": "user", "content": [tool_result_1, tool_result_2, ...]},
        ...
    ]

    Args:
        messages: List to store conversation history (modified in-place)

    Returns:
        The updated messages list with full conversation history

    Note: This demonstrates why the text editor tool is powerful -
    Claude can work with files directly without human intervention,
    enabling autonomous file manipulation and code generation.
    """
    while True:
        # Step 1: Send messages + available tools to Claude
        # Claude will respond with text and/or tool calls
        response = chat(
            messages,
            tools=[get_text_edit_schema(model)],  # Tell Claude about text editor tool
        )

        # Step 2: Add Claude's response to history for context in next turn
        add_assistant_message(messages, response)

        # Step 3: Display Claude's text response to user
        print(text_from_message(response))

        # Step 4: Check if Claude called a tool
        # stop_reason == "tool_use" means Claude requested a tool
        # stop_reason == "end_turn" means Claude finished responding
        if response.stop_reason != "tool_use":
            # Claude finished without requesting tools - conversation ends
            break

        # Step 5: Execute the tools Claude requested
        tool_results = run_tools(response)

        # Step 6: Add tool results to message history
        # This closes the loop: Claude sees what happened when it called tools
        # Then it can request more tools or provide final response
        add_user_message(messages, tool_results)

    return messages


# ===== MAIN EXECUTION =====
if __name__ == "__main__":
    messages = []

    add_user_message(
        messages,
        "Create a file called 'example.txt' with the content 'Hello, World!'",
    )

    run_conversation(messages)

# Ghostfeed Skills — use the MCP tools

> **Do not install or use the skill files in this repository.** Use the Ghostfeed MCP server's `get_skill` tool to load the current instructions.

The files in this repository are legacy copies. They can differ from the instructions served by Ghostfeed MCP. No separate skill installation is required.

## Get the current instructions

1. Connect your agent to the [Ghostfeed MCP server](https://ghostfeed.ai/docs):

   ```text
   https://api.ghostfeed.ai/api/v2/mcp
   ```

2. Call `list_skills` to find the available skills.
3. Call `get_skill` with the exact `name` returned by `list_skills`.
4. Follow the returned instructions for your task.

For example, to read the avatar skill, call `get_skill` with:

```json
{
  "name": "ghostfeed-avatars"
}
```

You can also ask your agent:

> Use Ghostfeed MCP to call list_skills. Then call get_skill for the skill that matches my task and follow its instructions.

## If you already installed these files

Remove or disable the local Ghostfeed skill copies in your agent. Load the instructions through `get_skill` when you start a workflow. Do not use a saved copy from this repository as the source of instructions.

If your agent cannot find `list_skills` or `get_skill`, check its Ghostfeed MCP connection. See the [setup guide](https://ghostfeed.ai/docs).

## Links

- [Ghostfeed](https://ghostfeed.ai)
- [MCP setup and documentation](https://ghostfeed.ai/docs)

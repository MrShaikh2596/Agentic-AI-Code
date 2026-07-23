# Difference Between `stdio`, `sse`, and `streamable_http`

## Quick Summary

- `stdio`: local process-based transport for same-machine communication.
- `sse`: HTTP-based streaming transport where the server pushes updates to the client.
- `streamable_http`: modern HTTP transport that supports streaming and request/response communication over HTTP.

## Diagram

```text
Client ── stdio ── MCP Server
  │
  ├── sse ── MCP Server
  │    (server pushes events over HTTP)
  │
  └── streamable_http ── MCP Server
       (HTTP requests/responses with streaming support)
```

## Key Differences

### `stdio`
- Uses standard input/output.
- Best for local or embedded integrations.
- Usually simple and efficient for same-machine use.
- Not ideal for remote network communication.

### `sse`
- Stands for Server-Sent Events.
- Uses HTTP and keeps a long-lived connection.
- Best when the server needs to continuously push messages to the client.
- Good for event-style streaming, but more limited than modern HTTP streaming patterns.

### `streamable_http`
- Uses HTTP as the transport layer.
- Supports structured request/response plus streaming data.
- Better suited for web and networked environments.
- Often the most flexible choice for remote MCP communication.

## When to Use Which

- Use `stdio` when the client and server run on the same machine.
- Use `sse` when the server mainly needs to push updates.
- Use `streamable_http` when you want a flexible HTTP-based transport for remote or web-based setups.

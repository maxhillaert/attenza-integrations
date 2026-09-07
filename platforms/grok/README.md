# Grok

Grok's consumer iOS plugin settings do not currently provide a bespoke remote MCP field. Attenza therefore cannot be sideloaded there using a private or public URL.

The intended route is a public Grok plugin/listing backed by Attenza's shared OAuth MCP endpoint:

```text
https://staging.attenza.io/mcp
```

This directory will hold the Grok-specific publication manifest when xAI exposes a supported public submission format. Until then, it intentionally contains documentation rather than a speculative manifest or embedded user credential.

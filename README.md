<p align="center">
  <img src="plugins/stayrank/assets/logo.png" alt="Stayrank" width="96" height="96">
</p>

<h1 align="center">Stayrank for ChatGPT and Claude</h1>

<p align="center">Score, fix and retouch your Airbnb listings from the conversation.<br>
<a href="https://www.stayrank.ai/mcp">stayrank.ai/mcp</a> · <a href="mailto:support@stayrank.ai">support@stayrank.ai</a></p>

---

[Stayrank](https://www.stayrank.ai) scores an Airbnb listing out of 100 on seven axes (photos, title, description, amenities, reviews, price, trust), ranks the fixes by impact and writes the texts for you. This repository holds the Stayrank plugin for **Claude** and **ChatGPT**. Both connect to the same remote MCP server:

```
https://www.stayrank.ai/api/mcp
```

Everything except creating your account and paying happens in the conversation.

## What you can ask

- *"Analyze this Airbnb listing: https://www.airbnb.com/rooms/…"*: adds the listing, shows the free preview, quotes the full analysis and waits for your confirmation before using your balance.
- *"What's the score of my listing and what should I fix first?"*: score, strengths, the fixes ranked by impact with ready-to-paste texts.
- *"Which booking settings should I check?"*: instant book, minimum stay, cancellation and discounts, each with what Airbnb says about it and the trade-off.
- *"How does my listing compare with the ones around it?"*: the listings that rank in the same Airbnb search, median price, rating, reviews and photos, and the amenities most of them offer.
- *"What's left to do?"*, *"I changed the title, mark it done"*: the action plan, one fix at a time.
- *"Improve the photos of my listing"*, *"warm evening light on photo 3"*: retouches for the whole listing or one photo, with a preset or your own style. Retouches never change the room.
- Organization settings and team management (owners).

Stayrank never edits your Airbnb listing: you apply each change yourself, Stayrank tracks it. Stayrank is an independent tool, not affiliated with or endorsed by Airbnb.

## Install

### Claude

**Connector (claude.ai, Claude Desktop):** Settings › Connectors › Add custom connector, URL `https://www.stayrank.ai/api/mcp`, then sign in with your Stayrank account.

**Plugin:** download `stayrank-claude.zip` from the [latest release](../../releases/latest) and upload it in Customize › Plugins › Upload plugin.

**Claude Code:**

```bash
claude plugin marketplace add stayrank-ai/stayrank-mcp
claude plugin install stayrank@stayrank
```

Then run `/mcp` and authenticate the `stayrank` server.

### ChatGPT

Until the app is published in the ChatGPT directory: Settings › Apps (enable developer mode if your plan requires it) › create an app with the MCP server URL `https://www.stayrank.ai/api/mcp` and OAuth, then sign in with your Stayrank account.

`stayrank-chatgpt.zip` in the [latest release](../../releases/latest) is the package submitted to the OpenAI plugin directory.

## What's inside

```
.claude-plugin/marketplace.json     Claude marketplace (this repository)
plugins/stayrank/
  .claude-plugin/plugin.json        Claude plugin manifest
  .mcp.json                         Claude: remote MCP server
  .openai/plugin.json               ChatGPT (Agent Plugins) manifest
  .openai/mcp.json                  ChatGPT: remote MCP server
  skills/                           Shared skills: get started, analyze a listing,
                                    apply the action plan, improve photos, compare competitors
  assets/                           Icon and logo
scripts/package.py                  Builds dist/stayrank-chatgpt.zip and dist/stayrank-claude.zip
scripts/build_openai_zip.py         Checks the ChatGPT package against OpenAI's submission rules
package.json, package-lock.json     Pinned validation tooling (no runtime dependency)
```

Build locally (Node 22+ and Python 3; the only dependency is the official Claude CLI, pinned in `package-lock.json`):

```bash
npm ci
npm run validate
python scripts/package.py
```

Every push is validated by CI; every `v*` tag publishes both zips as a release.

## Privacy and data

The connector only accesses the Stayrank organization you choose when you authorize it, with your own permissions; a member removed from the team loses access immediately. It reads your listings, reports, actions and retouches, and only writes what you ask for. It never asks for your Airbnb credentials. Revoke access anytime in Settings › Connections on stayrank.ai.

[Privacy policy](https://www.stayrank.ai/en/confidentialite) · [Terms](https://www.stayrank.ai/en/cgu) · [Support](https://www.stayrank.ai/mcp#support)

## License

MIT © Stayrank (HOSTIAS SAS)

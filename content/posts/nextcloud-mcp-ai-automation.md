---
title: Your AI Assistant Can Now Control Your Nextcloud — Here's How to Set It Up
excerpt: A practical guide to connecting Nextcloud with an AI agent via MCP — no coding required. Learn how to automate 7 common workflows with your AI assistant.
tags:
  - Self-Hosting Tutorials
  - KI & Automation
  - Für Einsteiger
meta_title: Nextcloud + AI Assistant MCP Setup Guide
meta_description: Learn how to connect Nextcloud to an AI agent via MCP. Step-by-step guide with 7 automation examples for files, calendar, contacts & more.
featured: false
---

# Your AI Assistant Can Now Control Your Nextcloud — Here's How to Set It Up

*A practical guide to connecting Nextcloud with an AI agent via MCP — no coding required.*

---

## What's This About?

Imagine asking your AI assistant: *"Create a calendar event for next Tuesday's team meeting and share the agenda file with everyone."* And it just… does it. No copy-pasting, no clicking through menus.

That's what becomes possible when you connect Nextcloud to an AI agent using something called **MCP** — the Model Context Protocol.

This guide walks you through exactly how to do that, step by step.

---

## Before We Start: Two Things to Know

**What is Nextcloud?**
Nextcloud is a self-hosted cloud platform — think of it like your own private Google Drive + Google Calendar + Contacts, running on a server you control. Many organizations, universities, and privacy-conscious individuals use it.

**What is MCP?**
MCP (Model Context Protocol) is a standard that lets AI assistants talk to external tools and services. Instead of just answering questions, your AI can actually *do things* — read files, create calendar entries, manage contacts, and more.

Together, they're a powerful combination.

---

## What You'll Need

- A running Nextcloud instance (your own server, or a hosted one like Hetzner, IONOS, or Wolkesicher)
- Docker installed on your computer ([get it here](https://docs.docker.com/get-docker/))
- An AI agent that supports MCP — this guide uses [Hermes Agent](https://hermes-agent.nousresearch.com), but the approach works with any MCP-compatible client

---

## Step 1: Get Your Nextcloud Credentials

You'll need three things:
- Your Nextcloud URL (e.g. `https://mynextcloud.example.com`)
- Your username
- Your password (or an app password — recommended)

**Creating an app password** (more secure than your main password):
1. Log into Nextcloud
2. Go to **Settings → Security**
3. Scroll to "Devices & sessions"
4. Enter a name (e.g. "MCP Agent") and click **Create new app password**
5. Copy the password — you won't see it again

---

## Step 2: Run the MCP Server via Docker

The Nextcloud MCP server is a small bridge program that translates between your AI agent and Nextcloud's API. We'll run it as a Docker container so it stays reliably in the background.

> **Why Docker?** The alternative (running it directly) has a known bug where it crashes after a few requests. Docker + HTTP transport sidesteps this entirely. (See [this GitHub issue](https://github.com/cbcoutinho/nextcloud-mcp-server/issues/717) for the technical details.)

**Create an environment file** to store your credentials safely:

```bash
mkdir -p ~/.config/nextcloud-mcp

cat > ~/.config/nextcloud-mcp/.env << 'EOF'
NEXTCLOUD_HOST=https://your-nextcloud-url.com
NEXTCLOUD_USERNAME=your-username
NEXTCLOUD_PASSWORD=your-app-password
EOF
```

**Create a `docker-compose.yml`:**

```bash
cat > ~/.config/nextcloud-mcp/docker-compose.yml << 'EOF'
services:
  nextcloud-mcp:
    image: ghcr.io/cbcoutinho/nextcloud-mcp-server:latest
    container_name: nextcloud-mcp
    restart: unless-stopped
    ports:
      - "127.0.0.1:8000:8000"
    env_file:
      - .env
EOF
```

**Start the server:**

```bash
cd ~/.config/nextcloud-mcp
docker compose up -d
```

**Verify it's running:**

```bash
curl http://localhost:8000/health/ready
```

You should see something like `{"status": "ok"}`.

---

## Step 3: Connect Hermes Agent to the MCP Server

Now tell your AI agent where to find the MCP server:

```bash
hermes mcp add nextcloud --url http://localhost:8000/mcp
```

Test the connection:

```bash
hermes mcp test nextcloud
```

If it says the connection is successful — you're done with setup! 🎉

---

## Step 4: Try It Out

Start Hermes and try some commands:

**Files & Documents**
```
Upload the file report.pdf to my Nextcloud Documents folder
List all files in my Projects folder
```

**Calendar**
```
Create a calendar event "Team Standup" every Monday at 9am
Show me my events for next week
```

**Contacts**
```
Add a new contact: Maria Müller, maria@example.com, +49 123 456789
Show all contacts from Musterfirma GmbH
```

**Deck (Task Management)**
```
Create a new card "Review Q3 budget" in my To Do board
List all open tasks on the Marketing board
```

**Notes**
```
Create a new note called "Meeting Notes 2026-04-24" with today's agenda
```

---

## 7 Things You Can Automate Once Your AI Assistant Can Actually Use It

Most people use Nextcloud the same way they use any cloud tool: manually. You log in, click around, upload a file, create an event. It works fine.

But there's a newer approach that changes the dynamic entirely. By connecting Nextcloud to an AI agent via MCP, you can simply *describe* what you want done — and it happens. No clicking, no navigating menus, no copy-pasting between apps.

Here are seven real-world scenarios where this makes a noticeable difference.

### 1. Meeting Prep — Done in One Sentence

**The old way:** Check your calendar, open a new note, type the agenda, go to contacts to look up who's attending, create a share link, send it.

**With AI + Nextcloud MCP:**
> *"I have a project review meeting on Thursday. Create a shared note called 'Project Review Agenda', add it to the Projects folder, and list everyone attending so I can add them as editors."*

The agent reads your calendar, creates the file, and sets up sharing — all in one go. You show up to the meeting prepared instead of scrambling beforehand.

### 2. Onboarding New Team Members

Every time someone joins your team, someone has to create their contact entry, share the right folders with them, and maybe add them to a few calendar events.

**With AI + Nextcloud MCP:**
> *"Add Lisa Bauer (lisa@company.com, +49 30 1234567) to contacts, share the 'Team Docs' and 'Projects' folders with her, and add her to the recurring Monday standup."*

Three separate tasks, one instruction. Especially useful for organizations that onboard people regularly — sports clubs, volunteer organizations, growing startups.

### 3. Weekly Reporting Without the Busywork

If you send a weekly status update or generate a recurring report, you know how tedious the file management gets. Creating the document, naming it correctly, putting it in the right folder, sharing it with the right people.

**With AI + Nextcloud MCP:**
> *"Create a new note called 'Weekly Update – KW 17' in the Reports folder, and share it with the management team."*

Pair this with a script that runs automatically every Friday, and the file is ready and shared before you've had your morning coffee.

### 4. Event Planning for Clubs and Associations

Running a sports club, community organization, or association means a constant stream of events to coordinate — general meetings, training sessions, social events.

**With AI + Nextcloud MCP:**
> *"Add our annual general meeting to the calendar on May 15th at 7pm, create an agenda note called 'AGM 2026 Agenda', and share it with everyone in the 'Members' contact group."*

What used to take 20 minutes of clicking takes about 10 seconds to describe.

### 5. Document Routing and Filing

Receipts, invoices, contracts — they pile up. Getting them into the right folder in Nextcloud is one of those small tasks that's easy to postpone and annoying to batch-process later.

**With AI + Nextcloud MCP:**
> *"I just uploaded 'invoice-april.pdf' to my Downloads folder. Move it to Finances/2026/Invoices and add it to the Q2 expenses note."*

Combine this with automatic folder watching and you have a lightweight document management system that actually stays organized.

### 6. Contact Management at Scale

For anyone managing a larger contact list — a membership database, a client roster, a volunteer network — keeping Nextcloud Contacts up to date is a constant low-level chore.

**With AI + Nextcloud MCP:**
> *"Update Tom Müller's phone number to +49 176 9988776 and add a note that he's now the treasurer."*

Or in bulk:
> *"Show me all contacts from Musterfirma GmbH and tell me which ones don't have a phone number."*

The AI can find gaps, suggest updates, and make changes — without you having to open the contacts app at all.

### 7. Personal Knowledge Management

Many people use Nextcloud Notes as a second brain — meeting notes, project logs, reading summaries. The friction of creating and filing notes is often what stops people from actually keeping them up to date.

**With AI + Nextcloud MCP:**
> *"Create a note called 'Call with Stefan – 2026-04-24' and summarize what we discussed: budget approved, kickoff scheduled for May 3rd, he'll send the contract by Friday."*

The note is created, titled correctly, and filed — right from your conversation with the AI, while the details are still fresh.

---

## The Bigger Picture

None of these use cases require technical expertise to *use* — only the initial setup takes a bit of effort. Once the connection is established, the interface is just natural language.

What makes this particularly interesting is that Nextcloud covers a surprisingly broad range of everyday organizational needs: files, calendars, contacts, tasks, notes. Connecting an AI to all of those at once — through a single MCP server — means one assistant that can coordinate across all of them.

The practical ceiling is high. The setup is lower than you'd expect.

---

## Troubleshooting

**"No MCP servers configured" in Hermes**
Don't add MCP servers to the YAML config file — Hermes manages them separately via `hermes mcp add`. The YAML `mcp:` section is ignored.

**Container won't start / wrong architecture**
If you're on Apple Silicon (M1/M2/M3/M4 Mac) and get a "no matching manifest for linux/arm64" error, you'll need to build the image locally. Check the [project README](https://github.com/cbcoutinho/nextcloud-mcp-server) for build instructions.

**Credentials not picked up**
Make sure your `.env` file is in the same directory as your `docker-compose.yml`, and that `NEXTCLOUD_HOST` includes `https://` — without it, the server will reject the configuration.

**Contact fields (email, phone) not saving**
This is a known bug in the current version of the MCP server. As a workaround, use WebDAV to upload vCards directly, or wait for the upstream fix. Tracked [here](https://github.com/cbcoutinho/nextcloud-mcp-server/issues).

---

## What's Next?

Once the basics work, you can start building more powerful workflows:

- **Automated reporting**: Have your agent generate a weekly summary and save it to Nextcloud
- **Meeting prep**: Pull calendar events, create a shared note, and notify attendees automatically
- **Document routing**: Watch a folder and automatically share new files with the right team members

The MCP standard is growing fast — more Nextcloud features and more AI agents are gaining support every month.

---

## Summary

| Step | What you did |
|------|-------------|
| 1 | Got your Nextcloud credentials |
| 2 | Started the MCP server via Docker |
| 3 | Connected your AI agent to the server |
| 4 | Tried it out with real commands |

That's it. Your AI assistant can now work with your Nextcloud — reading files, managing calendars, handling contacts, and more.

---

*Have questions or ran into a different issue? Drop a comment below.*
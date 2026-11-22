---
icon: material/text-box-search
---

# Logs

Open **Administration → Logs** to view live application logs and configure logging.
Logs are stored in `./logs` by default and retained for **30 days**.
The Gameyfin log level defaults to `INFO`; the root level defaults to `WARN`.
Use `DEBUG` temporarily when investigating a problem, then restore the normal level.

See the [reference](reference.md#logs-folder) for log settings and supported levels.
Individual task runs have their own logs under [Tasks](tasks.md).

If live logs do not update behind a reverse proxy, check [WebSocket support](../faq/index.md#library-scan-progress-andor-application-logs-are-not-shown-in-the-ui).

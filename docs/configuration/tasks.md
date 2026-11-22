---
icon: material/calendar-clock
---

# Tasks

Open **Administration → Tasks** to manage background work from Gameyfin and enabled plugins.
You can start tasks manually, configure schedules and settings, inspect progress, cancel supported runs, and read previous run logs.
The task popover also shows current work and recent results.

## Scheduled work

- **Library scan** replaces the old periodic metadata-refresh settings. Its default schedule is `@daily`.
- **Backup** can create database backups, optionally including images. Scheduling is disabled by default; the proposed schedule is `0 0 3 * * *`.
- **Task history cleanup** runs daily by default. Its settings retain runs for 30 days and keep at most 100 runs per task.
- Plugins can register additional tasks. Their settings and schedules are shown here while the plugin is available.

Schedules use [Spring cron expressions](https://docs.spring.io/spring-framework/docs/current/javadoc-api/org/springframework/scheduling/support/CronExpression.html#parse(java.lang.String)).
Use six fields, including seconds, such as `0 0 3 * * *` for 03:00 each day, or a macro such as `@daily`.
Check the displayed next run after saving.

Task settings are stored for future runs. Parameters are values supplied for a manual run.
A failed run's logs usually explain whether credentials, file permissions, or an external service caused the problem.

See [System](system.md) for backup and restore workflows, and [Plugin development](../plugins/info-for-devs.md) for task extensions.

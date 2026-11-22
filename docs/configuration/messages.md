---
icon: material/email
---

# Messages

Open **Administration → Messages** to configure email delivery and notification templates.
Email notifications are disabled by default.

## Email delivery

Enter your SMTP server's hostname, port, username, and password as required by your provider.
The default port is **587**. Use a hostname such as `smtp.example.com`, not a webmail URL.
Enable email notifications, save the settings, and send a test message before relying on delivery.
When using a reverse proxy, forward the original host and protocol so notification links use the URL users visit.

See the [reference](reference.md#messages-providers-email-enabled) for all email settings.

## Templates

Edit the available message templates in this section and send test notifications to check their output.
Plugins can also send notifications through the [plugin API](../plugins/info-for-devs.md).

# distillery

Cloud service providers like Amazon Web Service (AWS), Microsoft Azure, Google Cloud Platform (GCP), etc., provide their CIDR network IPv4/6 ranges for consumption. During analysis, we could use WHOIS information to determine ownership of a specific IP address. However, using this OSINT, we can glean additional information on a particular IP address, like possible services operating in specific regions.

Distillery provides AWS Chatbot integration with Slack Channels for cloud IP range lookups.

```
@aws invoke cidr --payload {"item": "116.129.226.132”}
```

An RSS feed and website track the ever-changing network IP ranges for the following public clouds.

- Amazon Web Services
- Cloudflare
- Digital Ocean
- Google Cloud
- Microsoft Azure
- Microsoft o365
- Oracle Cloud

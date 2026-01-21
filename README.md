# distillery

**Distillery** is an open-source intelligence (OSINT) utility that allows researchers and analysts to glean additional context about IP addresses during investigations. It enriches IPs with CIDR ownership, cloud provider attribution, and inferred cloud regions to help identify services operating within specific infrastructure environments.

Distillery is particularly useful for:

- Threat Intelligence Analysis
- Incident Response
- Network Forensics
- Cloud Infrastructure Research

---

## API Usage

🔗 **[https://api.lukach.io/net/cidr?8.8.8.8](https://api.lukach.io/net/cidr?8.8.8.8)**

```json
{
    "ip": "8.8.8.8",
    "int": "134744072",
    "cidr": [
        [
            "google",
            "2026-01-21T11:00Z",
            "8.8.8.0/24",
            134744064,
            134744319,
            "-",
            "-",
            "-"
        ]
    ],
    "region": "us-east-1"
}
```

---

## Use Cases

- Determine whether an IP belongs to a major cloud provider
- Identify services running in specific cloud regions
- Enhance SIEM, SOAR, or threat intelligence pipelines
- Support investigative and attribution workflows

---

## Public Clouds & SaaS Providers

At **11:00 AM UTC**, the Classless Inter-Domain Routing (CIDR) prefixes are collected from this list of Cloud and SaaS sources.

- Amazon
- Atlassian
- Cloudflare
- Datadog
- Digital Ocean
- Fastly
- GitHub
- Google
- iCloud
- Linode
- Microsoft
- NetSPI
- New Relic
- Okta
- OpenAI
- Oracle Cloud
- Perplexity
- Salesforce
- Tailscale
- Tenable
- Vultr
- Zscalar

---

## Canonical Data Model

| Id | Name | Type |
|:--:|:----:|:----:|
| A  | source | TEXT |
| B  | updated | TEXT |
| C  | cidr | BLOB |
| D  | firstip | INTEGER |
| E  | lastip | INTEGER |
| F  | region | TEXT |
| G  | service | TEXT |
| H  | border | TEXT |
| I  | - | - |
| J  | - | - |
| K  | - | - |
| L  | - | - |
| M  | - | - |
| N  | - | - |
| O  | - | - |
| P  | - | - |
| Q  | - | - |
| R  | - | - |
| S  | - | - |
| T  | - | - |
| U  | - | - |
| V  | - | - |
| W  | - | - |
| X  | - | - |
| Y  | - | - |
| Z  | - | - |

---

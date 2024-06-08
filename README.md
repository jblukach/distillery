# distillery

Distillery aims to provide network IP addresses and associated metadata for cloud service providers like AWS, Azure, and GCP. It allows researchers to glean additional context about IP addresses during analysis, such as determining services operating in a specific cloud region using open-source intelligence.

### Public Clouds & SaaS Providers

Top of the hour, Classless Inter-Domain Routing (CIDR) prefixes collection occurs from **twenty-three** Cloud and SaaS sources.

- Amazon Web Services
- Cloudflare
- Digital Ocean
- Fastly
- Google Cloud
- Microsoft Azure
- Microsoft o365
- NetSPI
- Okta
- Oracle Cloud
- Tailscale
- Tenable
- Vultr
- Zscalar

### Building SQLite Database

A quarter past the hour, the relational database containing the following schema gets generated for distribution.

| Column | Type |
|:------:|:----:|
| pk | INTEGER PRIMARY KEY |
| source | TEXT |
| service | TEXT |
| region | TEXT |
| cidr | BLOB |
| firstip | INTEGER |
| lastip | INTEGER |

### Application Usage

Half past the hour, the API updates with the latest SQLite database.

```
https://cidr.tundralabs.net/116.129.226.132
```

The API will look up the source origination if no IP address is available.

![Distillery](images/distillery.png)

# distillery

Distillery aims to provide network IP addresses and associated metadata for cloud service providers like AWS, Azure, and GCP. It allows researchers to glean additional context about IP addresses during analysis, such as determining services operating in a specific cloud region using open-source intelligence.

### Public Clouds & SaaS Providers

At 10 AM UTC daily, the collection of Classless Inter-Domain Routing (CIDR) prefixes occurs from **twenty** sources.

- Amazon Web Services
- Cloudflare
- Digital Ocean
- Google Cloud
- Microsoft Azure
- Microsoft o365
- NetSPI
- Okta
- Oracle Cloud
- Tenable
- Vultr

### Building SQLite Database

At 10:30 AM UTC daily, the relational database containing the following schema gets generated for distribution.

| Column | Type |
|:------:|:----:|
| pk | INTEGER PRIMARY KEY |
| source | TEXT |
| service | TEXT |
| region | TEXT |
| cidr | BLOB |
| firstip | INTEGER |
| lastip | INTEGER |

### Database Distribution

- Download: https://static.tundralabs.net/distillery.sqlite3
- Verification: https://static.tundralabs.net/distillery.sha256
- Last Updated: https://static.tundralabs.net/distillery.updated
- Prefix Count: https://static.tundralabs.net/distillery.count

### Application Usage

At 11:00 AM UTC daily, the API updates with the latest SQLite database.

```
https://cidr.tundralabs.net/116.129.226.132
```

or

```
https://cidr.tundralabs.net
```

The API will look up the source origination if no IP address is available.

![Distillery](images/distillery.png)

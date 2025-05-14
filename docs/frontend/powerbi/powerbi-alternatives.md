Here we will be exploring alternatives to PowerBi (reasoning: powerbi requires a paid plan to share our project for powerbi with each other. (we have asked the HvA for permission and are waiting the approval, but in case it isn't possible then we will need to have other tools to use as an alternative.))

The applications found so far are the following:
* Metabase
* Apache Superset
* Redash
* Grafana
* Knime Analytics Platform

## 🛠 Tool Details

###  Metabase
- Website: [source:](https://www.metabase.com/)
- Embedding:  *Free public embedding via iframe*
- Features:
  - No-code dashboard builder
  - Works with PostgreSQL, MySQL, MongoDB, etc.
  - REST API and Slack/Email alerts
- Limitations: Secure/filtered embeds require the paid Enterprise version

---

###  Apache Superset
- Website: [source:] (https://superset.apache.org/)
- Embedding:  *Free and customizable iframe or frontend embedding*
- Features:
  - Complex dashboarding capabilities
  - SQL editor, filters, slices, advanced charts
  - React plugin architecture
- Limitations: More technical setup than others

###  Redash
- Website: [source:] (https://redash.io/)
- Embedding:  *Free public dashboard embedding via iframe*
- Features:
  - SQL query editor with preview
  - Scheduled refreshes
  - Alerting and team collaboration
- Limitations: No secure embed options in open-source version

---

###  Grafana
- Website: [source:] (https://grafana.com/)
- Embedding:  *Iframe embedding supported (can be public or private)*
- Features:
  - Great for time-series data (e.g. Prometheus, InfluxDB)
  - Plugin and theme system
  - Alerts and real-time updates
- Limitations: Not built for typical business KPIs\

###  KNIME Analytics Platform
- Website: [source:] (https://www.knime.com/)
- Embedding:  *Not designed for dashboard embedding*
- Features:
  - Visual programming for data science
  - Strong Python/R integration
  - Connectors to databases and cloud services
- Limitations: No out-of-the-box support for dashboards or web embeds

---

##  Summary

If your goal is **embedding** dashboards into a web application for free, here are the top picks:

-  Easiest Embed Option: [Metabase](https://www.metabase.com/) *(simple setup, nice UI, public-only)*
-  Most Flexible and Customizable: [Apache Superset](https://superset.apache.org/) *(full control, open-source secure embedding)*
-  For SQL-savvy teams: [Redash](https://redash.io/) *(simple SQL dashboarding with public embed)*

---

## Quick overview Table

this is a quick overview table for ease of use.

Tool: **Metabase**
- Open Source: Yes
- Free Embedding: Yes (public only)
- Best For: Simple business dashboards
- Notes: Secure/filtered embedding requires paid Enterprise edition

Tool: **Apache Superset**
- Open Source: Yes
- Free Embedding: Yes (full, customizable)
- Best For: Custom analytics and frontend control
- Notes: Embedding via iframe or custom React components; fully open-source

Tool: **Redash**
- Open Source: Yes
- Free Embedding: Yes (public only)
- Best For: SQL-driven dashboards
- Notes: Simple public dashboard embedding; no secure embed in free version

Tool: **Grafana**
- Open Source: Yes
- Free Embedding: Yes (public or private iframe)
- Best For: Monitoring, time-series data
- Notes: Designed more for DevOps than general BI use

Tool: **KNIME**
- Open Source: Yes
- Free Embedding: No
- Best For: Data science and machine learning pipelines
- Notes: Not suitable for embedding dashboards in web apps


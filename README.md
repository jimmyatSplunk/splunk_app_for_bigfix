# HCL BigFix App for Splunk
This app has been updated from the previous version (6.0.1) to run using the HCL BigFix Add-on for Splunk as it's source of data ingestion. The previous versions of this app were responsible for data ingestion using Python scripts querying the SOAP API of BigFix Web Reports. The HCL BigFix Add-on for Splunk now uses the REST API of BigFix which is much more efficient.

Big thanks to Mike Wilson for his previous work on the app.

# Changes from 6.0.1
Numerous changes has been made to the navigation and searches of the app.

1. The dashboards have been heavily reworked so they utilize the data sources ingested using the BigFix TA
2. The dashboards no longer use saved searches as their main source of data presentation. All dashboards have had their searches brought to the dashboard directly so they can be reworked if necessary
3. Some dashboards utilize base searching where appropriate to reduce search footprint when loading some dashboards
4. The "savedsearch=bigfix" to search the index where BigFix data has been ingested has been changed to the macro \`bigfix_index\`
5. Removed the dashboards for "Compliance"
6. Removed the dashboard for monitoring a syslog feed
7. All ingestion and setup using the Python scripts against the SOAP API have been removed
8. Due to changes in field names made in the BigFix TA queries, data brought in using 6.0.1 should be normalized before being added to the dashboards as potential sources

# Installation
It is recommended that the previous version of the BigFix app be removed from the search head and it's ingestion method should be migrated to used the BigFix TA

# Inputs Required per Dashboard
The following inputs should be configured with the BigFix TA for the corresponding dashboard:
1. User Overview
- BigFix Users
2. Client Overview
- BigFix Clients
3. Relay Overview
- BigFix Clients
- BigFix Infrastructure
4. Infrastructure Overview
- BigFix Clients
- BigFix Infrastructure
5. Actions Overview
- BigFix Actions
- BigFix Clients
6. Actions Details
- BigFix Actions
- BigFix Clients
- BigFix client logs (for drilldown)
7. Hardware Overview
- BigFix Analysis (Hardware Information)
- BigFix Analysis (Hardware Information (Windows))
8. Software Overview
- BigFix Clients
- BigFix Analysis (Application Information (Windows))
9. Inventory Details
- BigFix Clients
- BigFix Analysis (Hardware Information)
- BigFix Analysis (Hardware Information (Windows))
- BigFix Analysis (Hardware Information (Linux))

# Additional Analysis
The dashboards included in this app are configured for specific analysis that are built by HCL and deployed with different sites in BigFix. Work with your BigFix administrator to ensure the following analysis are enabled and the account querying for data has, at least, read access to the sites

Site: BES Inventory and License
- BigFix Analysis (Hardware Information)
- BigFix Analysis (Hardware Information (Windows))
- BigFix Analysis (Hardware Information (Linux))

Site: BES Support
- BES Component Versions
- BES Health Checks Analysis
- BES Relay Cache
- BES Relay Cache Information

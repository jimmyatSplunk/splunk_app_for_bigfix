# Splunk App for BigFix
This app has been updated from the previous version (6.0.1) to run using the BigFix TA as it's source of data ingestion. The previous versions of this app were responsible for data ingestion using Python scripts querying the SOAP API of BigFix Web Reports. The BigFix TA now uses the REST API of BigFix which is much more efficient.

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
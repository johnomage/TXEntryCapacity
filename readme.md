# 📊 TEC Register Dashboard
Welcome to the Transmission Entry Capacity (TEC) Register Dashboard. This interactive web application allows users to explore and visualise transmission project data from 2019 to 2038.

The Transmission Entry Capacity (TEC) Register is a record of generation projects that hold contracts for Transmission Entry Capacity (TEC) with National Grid ESO. This includes both connected projects and future connection projects, as well as projects that are directly connected to the National Electricity Transmission System (NETS) or connected at distribution level (and which have a Bilateral Embedded Generator Agreement (BEGA)). TEC is the maximum capacity in MW that a generator is permitted to export into the NETS. It is one of the two types of connection capacity included in transmission offers. The other is Connection Entry Capacity (CEC), which is the maximum potential output of a generation asset onto the NETS. CEC is often set higher than TEC to allow for changes over years in outputs without needing to adapt or modify infrastructure.

<br><br>



## Table of Contents
1. [Overview](#overview)
2. [Features](#features)
3. [Installation](#installation)
4. [Usage](#usage)
5. [Data Sources](#data-sources)
6. [Contact](#contact)

## Overview

This dashboard provides insights into transmission projects, including connection capacity, project status, and various plant types. Users can filter data by transmission owner, project status, and agreement type to tailor the visualisations to their needs.

## Features

- **Dynamic Filtering**: Filter projects by transmission owner, project status, and agreement type.
- **Visualisations**: 
  - Bar charts for connection capacity by plant type.
  - Sunburst charts to visualise capacity by host TO, plant type, and project status.
  - Doughnut charts displaying capacity distribution by project status.
  - Timeline charts to track connection capacity over time.
- **Data Table**: Display raw data for further analysis.

## Installation

To run this dashboard locally, you'll need Python and the following libraries:

1. Streamlit
2. Pandas
3. Plotly etc

You can install the required packages using pip:

```bash
pip install -r requirements.txt
```

## Usage

1. Clone this repository:
   ```bash
   git clone https://github.com/johnomage/TXEntryCapacity.git
   cd TXEntryCapacity
   ```

2. Run the Streamlit app:
   ```bash
   streamlit run app.py
   ```

3. Open your web browser and navigate to `http://localhost:8501` to view the dashboard.



## Table Header Descriptions

| Title                                   | Type   | Description                                                                                                                                                                                                                                                                                                                                                              | Comment                                                                 | Example                          | Unit      |
|-----------------------------------------|--------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------|----------------------------------|-----------|
| Project Name                            | string | Name of Generation Project                                                                                                                                                                                                                                                                                                                                                 |                                                                      | A'Chruach Wind Farm             |        |
| Customer Name                           | string | Name of Generator                                                                                                                                                                                                                                                                                                                                                          |                                                                      | A'CHRUACH WIND FARM LIMITED      |        |
| Connection Site                         | string | Name of Generation Connection Site                                                                                                                                                                                                                                                                                                                                         |                                                                      | Upperboat 132kV                 |        |
| Stage                                   | number | Stage refers to Staged TEC – how much TEC the Customer will connect and when. The customer may choose to bring on capacity in chunks to align with their build/commissioning program. Staged contracts are also used when a customer may only be able to bring on a proportion of their total capacity at a particular point in time ahead of further reinforcement works being carried out, completion of which would allow the remaining TEC onto the system. |                                                                      | 1                                |        |
| MW Connected                            | number | Amount of capacity currently connected to the National Grid                                                                                                                                                                                                                                                                                                              | Field will state 0MW until the project is built and connected           | 43                               | MW        |
| MW Increase / Decrease                  | number | Amount of capacity contracted to connect or be removed at a future date                                                                                                                                                                                                                                                                                                  | Field will state 0MW unless the TEC is due to increase or decrease      | 51.6                             | MW        |
| Cumulative Total Capacity (MW)         | number | Total amount of capacity contracted across all Stages                                                                                                                                                                                                                                                                                                                     |                                                                      | 43                               | MW        |
| MW Effective From                       | date   | Date on which Connection is contracted to be effective from                                                                                                                                                                                                                                                                                                               | Field will only include dates for future connections or increase/decreases to TEC, otherwise this field will be empty               | 2024-08-30                      | ISO 8601  |
| Project Status                          | string | Indicates what stage the Project is at in its build cycle                                                                                                                                                                                                                                                                                                                |                                                                      | Consents Approved                |        |
| Agreement Type                          | string | Indicates if the project is connecting directly to the National Grid or if the connection is embedded                                                                                                                                                                                                                                                                     |                                                                      | Directly Connected               |        |
| HOST TO                                 | string | Indicates which TO is responsible for the connection                                                                                                                                                                                                                                                                                                                      |                                                                      | SHET                             |        |
| Plant Type                              | string | Indicates the fuel type contracted to connect                                                                                                                                                                                                                                                                                                                             |                                                                      | Wind Onshore                     |        |
| Project ID                              | string | Unique Project Identifier                                                                                                                                                                                                                                                                                                                                                  |                                                                      | a0l4L0000005itE                 |        |
| Project Number                          | string |                                   Unique Project Identifier                                                                                                                                                                                                                                                                                                                                         |                                                                         |                                  |           |

<br><br>
## Data Sources

The data is dynamically loaded from `NESO` website (see below) and preprocessed to ensure it is ready for visualisation. The data structure includes columns such as:
- **HOST TO**: Transmission owners
- **Project Status**: Current status of the project (e.g., built, under construction)
- **Agreement Type**: Type of agreements associated with the projects
- **MW Change**: Changes in megawatt capacity
- **Connection Cap (MW)**: Total connection capacity in megawatts

## Transmission Owners (TO)
 - NGET - National Grid Electricity Transmission
 - OFTO - Offshore Electricity Transmission Owner (OFTO)
 - SHET - Scottish HydroElectric Transmission
 - SPT  - Scottish Power Transmission

 ---
 <br><br>
General Info:
 - Source: [NESO Data Portal](https://www.neso.energy/data-portal/transmission-entry-capacity-tec-register)
 - Data Licence: [NESO Open Licence](https://www.neso.energy/data-portal/neso-open-licence)
 - Data Portal: [About the Data Portal](https://www.neso.energy/data-portal/about-data-portal)

---
<br><br>
Contributor: [Praise](https://www.linkedin.com/in/praizerema/)

## Contact

For inquiries or feedback, please reach out to:
- **Email**: [john.e.omage@gmail.com](mailto:john.e.omage@gmail.com)

Feel free to contribute to this project or report any issues. Your feedback is invaluable for enhancing the dashboard.

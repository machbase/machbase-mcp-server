# Machbase MCP Server Performance Evaluation Guide (2025.10.24)

## Overview

**Performance testing of Machbase MCP Server shall be conducted according to the methodology outlined in this document as of the current date.**

## Purpose

To numerically assess the performance of Machbase MCP Server using consistent evaluation criteria.

## Evaluation Criteria

### 1. Scoring System
- Each question response is scored from **0 to 10 points**
- **Response time** is measured for each question

### 2. Deduction Criteria
**Scores will not fall below 0 points**

Deductions are applied based on the following categories:

| Deduction Category | Deduction Criteria | Notes |
|-------------------|-------------------|--------|
| **Presentation Accuracy** | • 0 errors: No deduction<br>• 1 error: -1 point<br>• 2-3 errors: -2 points<br>• 4+ errors: -3 points | Grammar, spelling, expression errors |
| **Definition Accuracy** | • No errors: No deduction<br>• Minor errors: -2 points<br>• Major errors: -4 points<br>• Complete error: 0 points | Technical accuracy, concept explanation accuracy |
| **Code Quality** | • No errors: No deduction<br>• 1 error: -1 point<br>• 2-3 errors: -2 points<br>• 4+ errors: -3 points | Executability, syntax errors, optimization |

## Test Questions

*Additional questions may be added as needed*

### Primary Questions

| No. | Question |
|-----|----------|
| 1 | Show me how to install Machbase Neo |
| 2 | What is TQL? Explain it and give me one executable example in DB |
| 3 | Give me one executable SQL example in DB |
| 4 | Show me what tables currently exist in the DB |
| 5 | Create a test table in DB that includes the rollup function |

### Secondary Questions

| No. | Question |
|-----|----------|
| 6 | Give me an executable TQL visualization code in DB |
| 7 | Explain the rollup function and give me one executable example in DB |
| 8 | Provide an executable geomap example in DB |
| 9 | Show me how to set a timer |
| 10 | Write a TQL that calculates the daily average and volatility of the SP500 table in DB for the last 30 days |

### Tertiary Questions

| No. | Question |
|-----|----------|
| 11 | Analyze the data consistency of the Bitcoin table and explain the method used for the analysis. |
| 12 | Provide TQL code that applies various noise filters to driving behavior data. |
| 13 | Explain how to connect to Machbase Neo from Python. |
| 14 | Provide one executable TQL example that resamples data stored at 1-minute intervals in the Bitcoin table into 5-minute intervals, calculating both the average and maximum values. |
| 15 | Provide one executable example in Machbase Neo that uses to fetch external API data and visualizes it. |

### DBMS Questions

| No. | Question |
|-----|----------|
| 16 | Explain the types of data tables available in Machbase and provide a brief description of each. |
| 17 | Explain the system meta tables in Machbase. |
| 18 | Describe the concept of Tablespace in Machbase and how disk management is handled. |
| 19 | Explain how to create an account named ‘test’ and grant it read-only access to a specific table (sensor_data). |
| 20 | Explain how to create and apply a Retention Policy that keeps sensor data for only 7 days and automatically deletes older data. |

## Test Result Documentation

- Test results must be written in **Markdown format**
- Results are uploaded to Git **by version**
- **Applied starting from version 0.2.0**
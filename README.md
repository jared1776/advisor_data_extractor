# advisor_data_extractor

This tool parses SEC Form ADV XML filings to extract detailed information about registered investment advisers (RIAs) and portfolio managers. It captures key firm attributes—such as AUM, services offered, classification, location, and website—and exports the results into a structured CSV file for further analysis.

## Features

- Parses SEC Form ADV XML data.
- Extracts:
  - Firm name and legal name
  - Location details (street, city, state, country, postal code)
  - Assets under management (AUM) breakdown
  - Services offered (financial planning, portfolio management types, etc.)
  - Client counts and size breakdown
  - Wrap fee program details
  - Website address (as clickable hyperlink in Excel)
  - Firm classification (RIA or Portfolio Manager)
  - Whether the firm has an investment vehicle
- Outputs results in a customizable CSV format.
- Interactive file picker GUI using `tkinter`.

## Requirements

- Python 3.7+
- Standard modules:
  - `xml`
  - `csv`
  - `tkinter` (comes with most Python installations, but may require separate installation on some Linux systems)
# No third-party dependencies required.
# Uses Python standard library only: xml, csv, argparse, tkinter.

## Installation

```bash
git clone https://github.com/jared1776/advisor_data_extractor.git
cd advisor_data_extractor
# (Optional) Create a virtual environment:
python -m venv venv
source venv/bin/activate   # macOS/Linux
venv\Scripts\activate      # Windows
```

## Usage
## Getting the Data

The SEC makes **Form ADV data** for all registered and exempt reporting advisers available for bulk download:

👉 [SEC Investment Adviser Public Disclosure Compilation](https://adviserinfo.sec.gov/compilation)

1. Go to the link above.  
2. Download the latest feed file, named like:  
IA_FIRM_SEC_Feed_YYYY_MM_DD.xml.gz

markdown
Copy
Edit
Example: `IA_FIRM_SEC_Feed_08_20_2025.xml.gz`  
3. **Unzip** the file using 7-Zip, WinRAR, or the command line (`gzip -d`).  
- This will produce a large `.xml` file (~70–80 MB).  
4. Run the extractor against the `.xml` file:  
```bash
python advisor_data_extractor.py --in IA_FIRM_SEC_Feed_08_20_2025.xml --out firms.csv
The script will parse the XML and generate a clean CSV that can be opened directly in Excel.

⚠️ Note: Opening the .gz or .xml file directly in Excel will not work — you must first decompress and then use the extractor to convert the data into CSV.

# Run with CLI mode using included sample
python advisor_data_extractor.py --in samples/example_input.xml --out samples/example_output.csv

# Or run with GUI mode (file pickers)
python advisor_data_extractor.py

Run the script:

```bash
python form_adv_extractor.py
```

- When prompted, select the XML file downloaded from the SEC IAPD site.
- Choose where to save the CSV output file.
- The extracted data will be saved in the specified CSV.

> **Note:** The script launches a desktop GUI (not a web app) to select files.

---

## Example XML Snippet (Input)

```xml
<Firm>
    <Info BusNm="Example Advisers LLC" LegalNm="Example Advisers Legal Name" />
    <MainAddr Strt1="123 Main St" City="New York" State="NY" Cntry="USA" PostlCd="10001" />
    <Item1 Q1ODesc="Over $1B AUM" Q1O="Y" />
    <Item5F Q5F2A="1500000000" Q5F2B="500000000" Q5F2C="2000000000" Q5F3="250000000" />
    <Item5G Q5G1="Y" Q5G2="Y" Q5G4="Y" Q5G12Oth="ESG Consulting" />
    <Item5H Q5H="200" Q5HMT500="Y" />
    <Item5I Q5I1="N" Q5I2A="0" Q5I2B="0" Q5I2C="0" />
    <Item5J Q5J1="N" Q5J2="N" />
    <WebAddrs>
        <WebAddr>https://www.exampleadvisers.com</WebAddr>
    </WebAddrs>
</Firm>
```

---

## XML to CSV Mapping

```
+-------------------------+----------------------------+
|        XML Tag          |        CSV Column          |
+-------------------------+----------------------------+
| Info@BusNm              | Firm Name                  |
| Info@LegalNm            | Legal Name                 |
| MainAddr@Strt1          | Street                     |
| MainAddr@City           | City                       |
| MainAddr@State          | State                      |
| MainAddr@Cntry          | Country                    |
| MainAddr@PostlCd        | Postal Code                |
| Item1@Q1ODesc           | AUM Description            |
| Item1@Q1O               | AUM Over 1B                |
| Item5F@Q5F2A            | Discretionary AUM          |
| Item5F@Q5F2B            | Non-Discretionary AUM      |
| Item5F@Q5F2C            | Total AUM                  |
| Item5F@Q5F3             | Non-US AUM                 |
| Item5G@Q5G1             | Financial Planning         |
| Item5G@Q5G2             | PM (Individuals)           |
| Item5G@Q5G5             | PM (Institutions)          |
| Item5G@Q5G4             | PM (Pooled Vehicles)       |
| Item5G@Q5G12Oth         | Other Services             |
| Item5H@Q5H              | Clients Served             |
| Item5H@Q5HMT500         | Clients Over 500           |
| Item5I@Q5I2A            | Wrap Sponsor AUM           |
| Item5I@Q5I2B            | Wrap Portfolio AUM         |
| Item5I@Q5I2C            | Wrap Combined AUM          |
| Item5J@Q5J1             | Limited Investment Advice  |
| Item5J@Q5J2             | Different Asset Comput.    |
| WebAddr (first)         | Website 1 (Hyperlink)      |
| Derived                 | Firm Type (RIA/PM)         |
| Derived                 | Investment Vehicle (Y/N)   |
+-------------------------+----------------------------+
```

- **Derived Fields:**  
  - _Firm Type_ is determined based on the XML attributes indicating whether the firm is a Registered Investment Adviser or Portfolio Manager.
  - _Investment Vehicle_ is derived from related XML tags indicating the presence of such.

---

## Example Output (CSV)

```csv
Firm Name,State,Total AUM,Firm Type,Website 1
Example Advisers LLC,NY,2000000000,RIA,"=HYPERLINK(""https://www.exampleadvisers.com"")"
```

---

## Notes

- Website links are formatted for Excel using the `HYPERLINK` function.
- The script gracefully handles missing XML fields.
- File write permissions are checked to prevent overwriting issues.

## Acknowledgments

This project was developed with the assistance of ChatGPT (by OpenAI) for code generation and documentation.  
All code has been reviewed, tested, and adapted for this repository’s use case.

---

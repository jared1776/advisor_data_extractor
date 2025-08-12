# advisor_data_extractor
This tool parses SEC Form ADV XML filings to extract detailed information about registered investment advisers (RIAs) and portfolio managers.
It captures key firm attributes such as AUM, services offered, firm classification, location details, and website addresses, then exports the results into a structured CSV file for further analysis.
Features
Parses SEC Form ADV XML data.

Extracts:

Firm name and legal name

Location details (street, city, state, country, postal code)

Assets under management (AUM) breakdown

Services offered (financial planning, portfolio management types, other)

Client counts and size breakdown

Wrap fee program details

Website address (formatted as clickable hyperlink in Excel)

Firm classification (RIA or Portfolio Manager)

Whether the firm has an investment vehicle

Outputs results in customizable CSV format.

Interactive file picker GUI using tkinter.      

Requirements
Python 3.7+

Modules:

xml

csv

tkinter (comes with most Python installations)

Installation
Clone the repository:

bash
Copy
Edit
git clone https://github.com/yourusername/form-adv-extractor.git
cd form-adv-extractor
(Optional) Create a virtual environment:

bash
Copy
Edit
python -m venv venv
source venv/bin/activate   # macOS/Linux
venv\Scripts\activate      # Windows


Usage
Run the script:

bash
Copy
Edit
python form_adv_extractor.py
When prompted, select the XML file downloaded from the SEC IAPD site.

Choose where to save the CSV output file.

The extracted data will be saved in the specified CSV.


Example XML Snippet (Input)
xml
Copy
Edit
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

XML to CSV Mapping Diagram
text
Copy
Edit
+-------------------------+----------------------------+
|        XML Tag          |        CSV Column         |
+-------------------------+----------------------------+
| Info@BusNm              | Firm Name                 |
| Info@LegalNm            | Legal Name                |
| MainAddr@Strt1          | Street                    |
| MainAddr@City           | City                      |
| MainAddr@State          | State                     |
| MainAddr@Cntry          | Country                   |
| MainAddr@PostlCd        | Postal Code               |
| Item1@Q1ODesc           | AUM Description           |
| Item1@Q1O               | AUM Over 1B               |
| Item5F@Q5F2A            | Discretionary AUM         |
| Item5F@Q5F2B            | Non-Discretionary AUM     |
| Item5F@Q5F2C            | Total AUM                 |
| Item5F@Q5F3             | Non-US AUM                |
| Item5G@Q5G1              | Financial Planning        |
| Item5G@Q5G2              | PM (Individuals)          |
| Item5G@Q5G5              | PM (Institutions)         |
| Item5G@Q5G4              | PM (Pooled Vehicles)      |
| Item5G@Q5G12Oth          | Other Services            |
| Item5H@Q5H               | Clients Served            |
| Item5H@Q5HMT500          | Clients Over 500          |
| Item5I@Q5I2A             | Wrap Sponsor AUM          |
| Item5I@Q5I2B             | Wrap Portfolio AUM        |
| Item5I@Q5I2C             | Wrap Combined AUM         |
| Item5J@Q5J1              | Limited Investment Advice |
| Item5J@Q5J2              | Different Asset Comput.   |
| WebAddr (first)         | Website 1 (Hyperlink)     |
| Derived                  | Firm Type (RIA/PM)        |
| Derived                  | Investment Vehicle (Y/N)  |
+-------------------------+----------------------------+


Example Output (CSV)
Firm Name	State	Total AUM	Firm Type	Website 1
Example Advisers LLC	NY	2000000000	RIA	=HYPERLINK("https://exampleadvisers.com")

Notes
Website links are formatted for Excel (HYPERLINK function).

The script handles missing XML fields gracefully.

File write permissions are checked to prevent overwriting issues.

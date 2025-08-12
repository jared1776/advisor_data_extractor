import argparse
import csv
import sys
import os
import xml.etree.ElementTree as ET
import tkinter as tk
from tkinter import filedialog

# ---------- Helpers ----------
def get_attribute(element, attribute, default="N/A"):
    return element.get(attribute, default) if element is not None else default

def get_first_web_address(element):
    if element is not None:
        first_addr = element.find(".//WebAddr")
        if first_addr is not None and first_addr.text:
            return f'=HYPERLINK("{first_addr.text.lower()}")'
    return "N/A"

def determine_firm_type(item2a, item5g, item5i):
    if item2a.get("Q2A1") == "Y" and item5g.get("Q5G2") == "Y":
        return "RIA"
    elif item5g.get("Q5G3") == "Y" or item5g.get("Q5G4") == "Y" or item5i.get("Q5I1") == "Y":
        return "Portfolio Manager"
    return "Unknown"

def has_investment_vehicle(item5g, item5i):
    if item5g.get("Q5G4") == "Y" or item5i.get("Q5I1") == "Y" or item5g.get("Q5G12Oth") not in (None, "", "N/A"):
        return "Yes"
    return "No"

# ---------- Core extraction ----------
def extract_firm_data(xml_file, output_csv):
    firms_data = []

    context = ET.iterparse(xml_file, events=("start", "end"))
    _, root = next(context)  # Get the root element

    for event, elem in context:
        if event == "end" and elem.tag == "Firm":
            info = elem.find(".//Info")
            firm_name = get_attribute(info, "BusNm")
            legal_name = get_attribute(info, "LegalNm")

            # Address
            main_addr = elem.find(".//MainAddr")
            street = get_attribute(main_addr, "Strt1")
            city = get_attribute(main_addr, "City")
            state = get_attribute(main_addr, "State")
            country = get_attribute(main_addr, "Cntry")
            postal_code = get_attribute(main_addr, "PostlCd")

            # AUM high level
            item1 = elem.find(".//Item1")
            aum_desc = get_attribute(item1, "Q1ODesc")
            has_aum_1billion = get_attribute(item1, "Q1O")

            # AUM breakdown
            item5f = elem.find(".//Item5F")
            discretionary_aum = get_attribute(item5f, "Q5F2A")
            non_discretionary_aum = get_attribute(item5f, "Q5F2B")
            total_aum = get_attribute(item5f, "Q5F2C")
            non_us_aum = get_attribute(item5f, "Q5F3")

            # Services offered
            item5g = elem.find(".//Item5G")
            financial_planning = get_attribute(item5g, "Q5G1")
            portfolio_management_individuals = get_attribute(item5g, "Q5G2")
            portfolio_management_institutions = get_attribute(item5g, "Q5G5")
            portfolio_management_pooled = get_attribute(item5g, "Q5G4")
            other_services = get_attribute(item5g, "Q5G12Oth")

            # Client details
            item5h = elem.find(".//Item5H")
            num_clients = get_attribute(item5h, "Q5H")
            clients_over_500 = get_attribute(item5h, "Q5HMT500")

            # Wrap programs
            item5i = elem.find(".//Item5I")
            wrap_sponsor_aum = get_attribute(item5i, "Q5I2A")
            wrap_portfolio_aum = get_attribute(item5i, "Q5I2B")
            wrap_combined_aum = get_attribute(item5i, "Q5I2C")
            wrap_fee_sponsor = get_attribute(item5i, "Q5I1")

            # Advice limitations
            item5j = elem.find(".//Item5J")
            limited_investment_advice = get_attribute(item5j, "Q5J1")
            different_asset_computation = get_attribute(item5j, "Q5J2")

            # Website hyperlink
            website_1 = get_first_web_address(elem.find(".//WebAddrs"))

            # Derived classifications
            firm_type = determine_firm_type(
                item2a=elem.find(".//Item2A").attrib if elem.find(".//Item2A") is not None else {},
                item5g=item5g.attrib if item5g is not None else {},
                item5i=item5i.attrib if item5i is not None else {},
            )

            investment_vehicle = has_investment_vehicle(
                item5g=item5g.attrib if item5g is not None else {},
                item5i=item5i.attrib if item5i is not None else {},
            )

            firm_data = {
                "Firm Name": firm_name,
                "Legal Name": legal_name,
                "Street": street,
                "City": city,
                "State": state,
                "Country": country,
                "Postal Code": postal_code,
                "AUM Description": aum_desc,
                "AUM Over 1B": has_aum_1billion,
                "Discretionary AUM": discretionary_aum,
                "Non-Discretionary AUM": non_discretionary_aum,
                "Total AUM": total_aum,
                "Non-US AUM": non_us_aum,
                "Financial Planning": financial_planning,
                "Portfolio Management (Individuals)": portfolio_management_individuals,
                "Portfolio Management (Institutions)": portfolio_management_institutions,
                "Portfolio Management (Pooled Vehicles)": portfolio_management_pooled,
                "Other Services": other_services,
                "Clients Served": num_clients,
                "Clients Over 500": clients_over_500,
                "Wrap Sponsor AUM": wrap_sponsor_aum,
                "Wrap Portfolio AUM": wrap_portfolio_aum,
                "Wrap Combined AUM": wrap_combined_aum,
                "Limited Investment Advice": limited_investment_advice,
                "Different Asset Computation": different_asset_computation,
                "Firm Type": firm_type,
                "Investment Vehicle": investment_vehicle,
                "Website 1": website_1
            }

            firms_data.append(firm_data)
            elem.clear()  # Free memory

    # Preserve the chosen column order
    column_order = list(firms_data[0].keys()) if firms_data else []

    try:
        # Use utf-8-sig for Excel friendliness
        with open(output_csv, 'w', newline='', encoding='utf-8-sig') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=column_order)
            writer.writeheader()
            writer.writerows(firms_data)
        print(f"Data successfully extracted and saved to {output_csv}")
    except PermissionError:
        print(f"Permission denied: Unable to write to {output_csv}. Close any open instances of the file and try again.")

# ---------- UI + CLI orchestration ----------
def run_with_gui():
    tk.Tk().withdraw()  # Hide root window
    xml_file_path = filedialog.askopenfilename(
        title="Select XML File",
        filetypes=[("XML Files", "*.xml")]
    )
    if not xml_file_path:
        print("No file selected. Exiting...")
        return 1

    output_csv_path = filedialog.asksaveasfilename(
        title="Save CSV As",
        defaultextension=".csv",
        filetypes=[("CSV Files", "*.csv")]
    )
    if not output_csv_path:
        print("No save location selected. Exiting...")
        return 1

    extract_firm_data(xml_file_path, output_csv_path)
    return 0

def run_with_cli(input_path, output_path):
    if not os.path.isfile(input_path):
        print(f"Input file not found: {input_path}")
        return 1
    out_dir = os.path.dirname(os.path.abspath(output_path)) or "."
    if not os.path.isdir(out_dir):
        print(f"Output directory does not exist: {out_dir}")
        return 1
    extract_firm_data(input_path, output_path)
    return 0

def parse_args(argv):
    parser = argparse.ArgumentParser(
        description="Extract RIA and portfolio manager data from SEC Form ADV XML into CSV."
    )
    parser.add_argument("--in", dest="infile", help="Path to input Form ADV XML file")
    parser.add_argument("--out", dest="outfile", help="Path to output CSV file")
    return parser.parse_args(argv)

def main():
    args = parse_args(sys.argv[1:])

    # If both CLI args provided, run headless
    if args.infile and args.outfile:
        return run_with_cli(args.infile, args.outfile)

    # Otherwise, fall back to Tkinter picker
    return run_with_gui()

if __name__ == "__main__":
    sys.exit(main())

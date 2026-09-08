"""
Spoof data loader for AI Expense Tracker.
Provides get_spoof_df() which returns a realistic sample DataFrame
matching the app's expected columns — 6 months of data, weekly cadence.
"""

import pandas as pd


def get_spoof_df() -> pd.DataFrame:
    rows = [

        # ====================================================================
        # JANUARY 2025
        # ====================================================================

        # Week of Jan 06
        {"Date": "2025-01-06", "Vendor": "Staples Canada",        "Doc Type": "Office Supplies", "Category": "Paper Products",         "Description": "A4 Copy Paper (5 reams)",             "Currency": "CAD", "Amount": 54.99,   "Confidence": 0.9},
        {"Date": "2025-01-06", "Vendor": "Staples Canada",        "Doc Type": "Office Supplies", "Category": "Printer Supplies",       "Description": "HP 67XL Black Ink Cartridge",         "Currency": "CAD", "Amount": 42.49,   "Confidence": 0.9},
        {"Date": "2025-01-06", "Vendor": "Staples Canada",        "Doc Type": "Office Supplies", "Category": "Filing & Storage",       "Description": "Manila File Folders (100-pack)",      "Currency": "CAD", "Amount": 19.99,   "Confidence": 0.9},
        {"Date": "2025-01-06", "Vendor": "Staples Canada",        "Doc Type": "Office Supplies", "Category": "Taxes & Fees",           "Description": "HST (13%)",                           "Currency": "CAD", "Amount": 15.27,   "Confidence": 0.9},
        {"Date": "2025-01-07", "Vendor": "Toronto Hydro",         "Doc Type": "Utilities",       "Category": "Electricity",            "Description": "Commercial Electricity — Jan W1",     "Currency": "CAD", "Amount": 398.12,  "Confidence": 0.9},
        {"Date": "2025-01-07", "Vendor": "Toronto Hydro",         "Doc Type": "Utilities",       "Category": "Service Charges",        "Description": "Distribution Charge",                 "Currency": "CAD", "Amount": 38.50,   "Confidence": 0.9},
        {"Date": "2025-01-07", "Vendor": "Toronto Hydro",         "Doc Type": "Utilities",       "Category": "Taxes & Fees",           "Description": "HST (13%)",                           "Currency": "CAD", "Amount": 56.70,   "Confidence": 0.9},

        # Week of Jan 13
        {"Date": "2025-01-13", "Vendor": "Rogers Business",       "Doc Type": "Utilities",       "Category": "Internet",               "Description": "Fibre Internet 1Gbps",                "Currency": "CAD", "Amount": 189.99,  "Confidence": 0.9},
        {"Date": "2025-01-13", "Vendor": "Rogers Business",       "Doc Type": "Utilities",       "Category": "Telephone",              "Description": "Business Phone Lines (3 lines)",      "Currency": "CAD", "Amount": 124.97,  "Confidence": 0.9},
        {"Date": "2025-01-13", "Vendor": "Rogers Business",       "Doc Type": "Utilities",       "Category": "Taxes & Fees",           "Description": "HST (13%)",                           "Currency": "CAD", "Amount": 40.95,   "Confidence": 0.9},
        {"Date": "2025-01-14", "Vendor": "Amazon Business",       "Doc Type": "Office Supplies", "Category": "Desk Accessories",       "Description": "Whiteboard Markers (12-pack)",        "Currency": "CAD", "Amount": 18.99,   "Confidence": 0.9},
        {"Date": "2025-01-14", "Vendor": "Amazon Business",       "Doc Type": "Office Supplies", "Category": "Technology Accessories", "Description": "USB-C Hub 7-in-1",                   "Currency": "CAD", "Amount": 49.99,   "Confidence": 0.9},
        {"Date": "2025-01-14", "Vendor": "Amazon Business",       "Doc Type": "Office Supplies", "Category": "Taxes & Fees",           "Description": "HST (13%)",                           "Currency": "CAD", "Amount": 8.97,    "Confidence": 0.9},

        # Week of Jan 20
        {"Date": "2025-01-20", "Vendor": "CleanPro Services",     "Doc Type": "Services",        "Category": "Cleaning",               "Description": "Weekly Office Cleaning",              "Currency": "CAD", "Amount": 320.00,  "Confidence": 0.9},
        {"Date": "2025-01-20", "Vendor": "CleanPro Services",     "Doc Type": "Services",        "Category": "Taxes & Fees",           "Description": "HST (13%)",                           "Currency": "CAD", "Amount": 41.60,   "Confidence": 0.9},
        {"Date": "2025-01-21", "Vendor": "Dell Technologies",     "Doc Type": "Equipment",       "Category": "Computer Hardware",      "Description": "Dell OptiPlex 7010 Desktop",          "Currency": "CAD", "Amount": 1249.00, "Confidence": 0.9},
        {"Date": "2025-01-21", "Vendor": "Dell Technologies",     "Doc Type": "Equipment",       "Category": "Peripherals",            "Description": "Dell 27 P2725H Monitor",              "Currency": "CAD", "Amount": 389.00,  "Confidence": 0.9},
        {"Date": "2025-01-21", "Vendor": "Dell Technologies",     "Doc Type": "Equipment",       "Category": "Taxes & Fees",           "Description": "HST (13%)",                           "Currency": "CAD", "Amount": 212.57,  "Confidence": 0.9},

        # Week of Jan 27
        {"Date": "2025-01-27", "Vendor": "Apex Consulting Group", "Doc Type": "Services",        "Category": "Consulting",             "Description": "IT Strategy Workshop (8 hrs)",        "Currency": "CAD", "Amount": 2400.00, "Confidence": 0.9},
        {"Date": "2025-01-27", "Vendor": "Apex Consulting Group", "Doc Type": "Services",        "Category": "Taxes & Fees",           "Description": "HST (13%)",                           "Currency": "CAD", "Amount": 312.00,  "Confidence": 0.9},
        {"Date": "2025-01-28", "Vendor": "Enbridge Gas",          "Doc Type": "Utilities",       "Category": "Gas",                    "Description": "Natural Gas — Jan",                   "Currency": "CAD", "Amount": 274.88,  "Confidence": 0.9},
        {"Date": "2025-01-28", "Vendor": "Enbridge Gas",          "Doc Type": "Utilities",       "Category": "Taxes & Fees",           "Description": "HST (13%)",                           "Currency": "CAD", "Amount": 35.74,   "Confidence": 0.9},

        # ====================================================================
        # FEBRUARY 2025
        # ====================================================================

        # Week of Feb 03
        {"Date": "2025-02-03", "Vendor": "Staples Canada",        "Doc Type": "Office Supplies", "Category": "Paper Products",         "Description": "A4 Copy Paper (3 reams)",             "Currency": "CAD", "Amount": 32.99,   "Confidence": 0.9},
        {"Date": "2025-02-03", "Vendor": "Staples Canada",        "Doc Type": "Office Supplies", "Category": "Writing Instruments",    "Description": "BIC Ballpoint Pens (12-pack)",        "Currency": "CAD", "Amount": 8.99,    "Confidence": 0.9},
        {"Date": "2025-02-03", "Vendor": "Staples Canada",        "Doc Type": "Office Supplies", "Category": "Taxes & Fees",           "Description": "HST (13%)",                           "Currency": "CAD", "Amount": 5.46,    "Confidence": 0.9},
        {"Date": "2025-02-04", "Vendor": "Toronto Hydro",         "Doc Type": "Utilities",       "Category": "Electricity",            "Description": "Commercial Electricity — Feb W1",     "Currency": "CAD", "Amount": 421.55,  "Confidence": 0.9},
        {"Date": "2025-02-04", "Vendor": "Toronto Hydro",         "Doc Type": "Utilities",       "Category": "Service Charges",        "Description": "Distribution Charge",                 "Currency": "CAD", "Amount": 38.50,   "Confidence": 0.9},
        {"Date": "2025-02-04", "Vendor": "Toronto Hydro",         "Doc Type": "Utilities",       "Category": "Taxes & Fees",           "Description": "HST (13%)",                           "Currency": "CAD", "Amount": 59.40,   "Confidence": 0.9},

        # Week of Feb 10
        {"Date": "2025-02-10", "Vendor": "Rogers Business",       "Doc Type": "Utilities",       "Category": "Internet",               "Description": "Fibre Internet 1Gbps",                "Currency": "CAD", "Amount": 189.99,  "Confidence": 0.9},
        {"Date": "2025-02-10", "Vendor": "Rogers Business",       "Doc Type": "Utilities",       "Category": "Telephone",              "Description": "Business Phone Lines (3 lines)",      "Currency": "CAD", "Amount": 124.97,  "Confidence": 0.9},
        {"Date": "2025-02-10", "Vendor": "Rogers Business",       "Doc Type": "Utilities",       "Category": "Taxes & Fees",           "Description": "HST (13%)",                           "Currency": "CAD", "Amount": 40.95,   "Confidence": 0.9},
        {"Date": "2025-02-11", "Vendor": "CleanPro Services",     "Doc Type": "Services",        "Category": "Cleaning",               "Description": "Weekly Office Cleaning",              "Currency": "CAD", "Amount": 320.00,  "Confidence": 0.9},
        {"Date": "2025-02-11", "Vendor": "CleanPro Services",     "Doc Type": "Services",        "Category": "Cleaning",               "Description": "Deep Clean — Kitchen",                "Currency": "CAD", "Amount": 185.00,  "Confidence": 0.9},
        {"Date": "2025-02-11", "Vendor": "CleanPro Services",     "Doc Type": "Services",        "Category": "Taxes & Fees",           "Description": "HST (13%)",                           "Currency": "CAD", "Amount": 65.65,   "Confidence": 0.9},

        # Week of Feb 17
        {"Date": "2025-02-17", "Vendor": "Amazon Business",       "Doc Type": "Office Supplies", "Category": "Printer Supplies",       "Description": "Brother TN-760 Toner Cartridge",     "Currency": "CAD", "Amount": 89.99,   "Confidence": 0.9},
        {"Date": "2025-02-17", "Vendor": "Amazon Business",       "Doc Type": "Office Supplies", "Category": "Technology Accessories", "Description": "HDMI Cable 2-pack",                  "Currency": "CAD", "Amount": 22.99,   "Confidence": 0.9},
        {"Date": "2025-02-17", "Vendor": "Amazon Business",       "Doc Type": "Office Supplies", "Category": "Taxes & Fees",           "Description": "HST (13%)",                           "Currency": "CAD", "Amount": 14.69,   "Confidence": 0.9},
        {"Date": "2025-02-18", "Vendor": "Apex Consulting Group", "Doc Type": "Services",        "Category": "Professional Services",  "Description": "Network Security Audit",              "Currency": "CAD", "Amount": 1800.00, "Confidence": 0.9},
        {"Date": "2025-02-18", "Vendor": "Apex Consulting Group", "Doc Type": "Services",        "Category": "Taxes & Fees",           "Description": "HST (13%)",                           "Currency": "CAD", "Amount": 234.00,  "Confidence": 0.9},

        # Week of Feb 24
        {"Date": "2025-02-24", "Vendor": "Enbridge Gas",          "Doc Type": "Utilities",       "Category": "Gas",                    "Description": "Natural Gas — Feb",                   "Currency": "CAD", "Amount": 261.40,  "Confidence": 0.9},
        {"Date": "2025-02-24", "Vendor": "Enbridge Gas",          "Doc Type": "Utilities",       "Category": "Taxes & Fees",           "Description": "HST (13%)",                           "Currency": "CAD", "Amount": 33.98,   "Confidence": 0.9},
        {"Date": "2025-02-25", "Vendor": "Dell Technologies",     "Doc Type": "Equipment",       "Category": "Software Licenses",      "Description": "Microsoft 365 Business (annual)",     "Currency": "CAD", "Amount": 299.99,  "Confidence": 0.9},
        {"Date": "2025-02-25", "Vendor": "Dell Technologies",     "Doc Type": "Equipment",       "Category": "Taxes & Fees",           "Description": "HST (13%)",                           "Currency": "CAD", "Amount": 39.00,   "Confidence": 0.9},

        # ====================================================================
        # MARCH 2025
        # ====================================================================

        # Week of Mar 03
        {"Date": "2025-03-03", "Vendor": "Staples Canada",        "Doc Type": "Office Supplies", "Category": "Paper Products",         "Description": "A4 Copy Paper (5 reams)",             "Currency": "CAD", "Amount": 54.99,   "Confidence": 0.9},
        {"Date": "2025-03-03", "Vendor": "Staples Canada",        "Doc Type": "Office Supplies", "Category": "Printer Supplies",       "Description": "HP 67XL Black Ink Cartridge",         "Currency": "CAD", "Amount": 42.49,   "Confidence": 0.9},
        {"Date": "2025-03-03", "Vendor": "Staples Canada",        "Doc Type": "Office Supplies", "Category": "Filing & Storage",       "Description": "Manila File Folders (100-pack)",      "Currency": "CAD", "Amount": 19.99,   "Confidence": 0.9},
        {"Date": "2025-03-03", "Vendor": "Staples Canada",        "Doc Type": "Office Supplies", "Category": "Taxes & Fees",           "Description": "HST (13%)",                           "Currency": "CAD", "Amount": 15.27,   "Confidence": 0.9},
        {"Date": "2025-03-04", "Vendor": "Toronto Hydro",         "Doc Type": "Utilities",       "Category": "Electricity",            "Description": "Commercial Electricity — Mar W1",     "Currency": "CAD", "Amount": 388.44,  "Confidence": 0.9},
        {"Date": "2025-03-04", "Vendor": "Toronto Hydro",         "Doc Type": "Utilities",       "Category": "Service Charges",        "Description": "Distribution Charge",                 "Currency": "CAD", "Amount": 38.50,   "Confidence": 0.9},
        {"Date": "2025-03-04", "Vendor": "Toronto Hydro",         "Doc Type": "Utilities",       "Category": "Taxes & Fees",           "Description": "HST (13%)",                           "Currency": "CAD", "Amount": 55.44,   "Confidence": 0.9},

        # Week of Mar 10
        {"Date": "2025-03-10", "Vendor": "Rogers Business",       "Doc Type": "Utilities",       "Category": "Internet",               "Description": "Fibre Internet 1Gbps",                "Currency": "CAD", "Amount": 189.99,  "Confidence": 0.9},
        {"Date": "2025-03-10", "Vendor": "Rogers Business",       "Doc Type": "Utilities",       "Category": "Telephone",              "Description": "Business Phone Lines (3 lines)",      "Currency": "CAD", "Amount": 124.97,  "Confidence": 0.9},
        {"Date": "2025-03-10", "Vendor": "Rogers Business",       "Doc Type": "Utilities",       "Category": "Taxes & Fees",           "Description": "HST (13%)",                           "Currency": "CAD", "Amount": 40.95,   "Confidence": 0.9},
        {"Date": "2025-03-11", "Vendor": "Dell Technologies",     "Doc Type": "Equipment",       "Category": "Computer Hardware",      "Description": "Dell Latitude 5540 Laptop",           "Currency": "CAD", "Amount": 1549.00, "Confidence": 0.9},
        {"Date": "2025-03-11", "Vendor": "Dell Technologies",     "Doc Type": "Equipment",       "Category": "Peripherals",            "Description": "Dell Wireless Keyboard and Mouse",    "Currency": "CAD", "Amount": 79.99,   "Confidence": 0.9},
        {"Date": "2025-03-11", "Vendor": "Dell Technologies",     "Doc Type": "Equipment",       "Category": "Taxes & Fees",           "Description": "HST (13%)",                           "Currency": "CAD", "Amount": 212.57,  "Confidence": 0.9},

        # Week of Mar 17
        {"Date": "2025-03-17", "Vendor": "CleanPro Services",     "Doc Type": "Services",        "Category": "Cleaning",               "Description": "Weekly Office Cleaning",              "Currency": "CAD", "Amount": 320.00,  "Confidence": 0.9},
        {"Date": "2025-03-17", "Vendor": "CleanPro Services",     "Doc Type": "Services",        "Category": "Taxes & Fees",           "Description": "HST (13%)",                           "Currency": "CAD", "Amount": 41.60,   "Confidence": 0.9},
        {"Date": "2025-03-18", "Vendor": "Apex Consulting Group", "Doc Type": "Services",        "Category": "Consulting",             "Description": "Cloud Migration Planning (6 hrs)",    "Currency": "CAD", "Amount": 1800.00, "Confidence": 0.9},
        {"Date": "2025-03-18", "Vendor": "Apex Consulting Group", "Doc Type": "Services",        "Category": "Taxes & Fees",           "Description": "HST (13%)",                           "Currency": "CAD", "Amount": 234.00,  "Confidence": 0.9},

        # Week of Mar 24
        {"Date": "2025-03-24", "Vendor": "Amazon Business",       "Doc Type": "Office Supplies", "Category": "Desk Accessories",       "Description": "Ergonomic Desk Mat (2-pack)",         "Currency": "CAD", "Amount": 45.98,   "Confidence": 0.9},
        {"Date": "2025-03-24", "Vendor": "Amazon Business",       "Doc Type": "Office Supplies", "Category": "Technology Accessories", "Description": "USB-C Docking Station",               "Currency": "CAD", "Amount": 129.99,  "Confidence": 0.9},
        {"Date": "2025-03-24", "Vendor": "Amazon Business",       "Doc Type": "Office Supplies", "Category": "Taxes & Fees",           "Description": "HST (13%)",                           "Currency": "CAD", "Amount": 22.87,   "Confidence": 0.9},
        {"Date": "2025-03-25", "Vendor": "Enbridge Gas",          "Doc Type": "Utilities",       "Category": "Gas",                    "Description": "Natural Gas — Mar",                   "Currency": "CAD", "Amount": 238.77,  "Confidence": 0.9},
        {"Date": "2025-03-25", "Vendor": "Enbridge Gas",          "Doc Type": "Utilities",       "Category": "Taxes & Fees",           "Description": "HST (13%)",                           "Currency": "CAD", "Amount": 31.04,   "Confidence": 0.9},

        # ====================================================================
        # APRIL 2025
        # ====================================================================

        # Week of Apr 07
        {"Date": "2025-04-07", "Vendor": "Staples Canada",        "Doc Type": "Office Supplies", "Category": "Paper Products",         "Description": "A4 Copy Paper (4 reams)",             "Currency": "CAD", "Amount": 43.99,   "Confidence": 0.9},
        {"Date": "2025-04-07", "Vendor": "Staples Canada",        "Doc Type": "Office Supplies", "Category": "Writing Instruments",    "Description": "Pilot G2 Pens (10-pack)",             "Currency": "CAD", "Amount": 14.49,   "Confidence": 0.9},
        {"Date": "2025-04-07", "Vendor": "Staples Canada",        "Doc Type": "Office Supplies", "Category": "Taxes & Fees",           "Description": "HST (13%)",                           "Currency": "CAD", "Amount": 7.60,    "Confidence": 0.9},
        {"Date": "2025-04-08", "Vendor": "Toronto Hydro",         "Doc Type": "Utilities",       "Category": "Electricity",            "Description": "Commercial Electricity — Apr W1",     "Currency": "CAD", "Amount": 342.90,  "Confidence": 0.9},
        {"Date": "2025-04-08", "Vendor": "Toronto Hydro",         "Doc Type": "Utilities",       "Category": "Service Charges",        "Description": "Distribution Charge",                 "Currency": "CAD", "Amount": 38.50,   "Confidence": 0.9},
        {"Date": "2025-04-08", "Vendor": "Toronto Hydro",         "Doc Type": "Utilities",       "Category": "Taxes & Fees",           "Description": "HST (13%)",                           "Currency": "CAD", "Amount": 49.58,   "Confidence": 0.9},

        # Week of Apr 14
        {"Date": "2025-04-14", "Vendor": "Rogers Business",       "Doc Type": "Utilities",       "Category": "Internet",               "Description": "Fibre Internet 1Gbps",                "Currency": "CAD", "Amount": 189.99,  "Confidence": 0.9},
        {"Date": "2025-04-14", "Vendor": "Rogers Business",       "Doc Type": "Utilities",       "Category": "Telephone",              "Description": "Business Phone Lines (3 lines)",      "Currency": "CAD", "Amount": 124.97,  "Confidence": 0.9},
        {"Date": "2025-04-14", "Vendor": "Rogers Business",       "Doc Type": "Utilities",       "Category": "Taxes & Fees",           "Description": "HST (13%)",                           "Currency": "CAD", "Amount": 40.95,   "Confidence": 0.9},
        {"Date": "2025-04-15", "Vendor": "CleanPro Services",     "Doc Type": "Services",        "Category": "Cleaning",               "Description": "Weekly Office Cleaning",              "Currency": "CAD", "Amount": 320.00,  "Confidence": 0.9},
        {"Date": "2025-04-15", "Vendor": "CleanPro Services",     "Doc Type": "Services",        "Category": "Taxes & Fees",           "Description": "HST (13%)",                           "Currency": "CAD", "Amount": 41.60,   "Confidence": 0.9},

        # Week of Apr 22
        {"Date": "2025-04-22", "Vendor": "Apex Consulting Group", "Doc Type": "Services",        "Category": "Consulting",             "Description": "DevOps Pipeline Review (4 hrs)",      "Currency": "CAD", "Amount": 1200.00, "Confidence": 0.9},
        {"Date": "2025-04-22", "Vendor": "Apex Consulting Group", "Doc Type": "Services",        "Category": "Taxes & Fees",           "Description": "HST (13%)",                           "Currency": "CAD", "Amount": 156.00,  "Confidence": 0.9},
        {"Date": "2025-04-23", "Vendor": "Amazon Business",       "Doc Type": "Office Supplies", "Category": "Printer Supplies",       "Description": "HP 414A Cyan Toner",                  "Currency": "CAD", "Amount": 74.99,   "Confidence": 0.9},
        {"Date": "2025-04-23", "Vendor": "Amazon Business",       "Doc Type": "Office Supplies", "Category": "Desk Accessories",       "Description": "Monitor Riser Stand",                 "Currency": "CAD", "Amount": 39.99,   "Confidence": 0.9},
        {"Date": "2025-04-23", "Vendor": "Amazon Business",       "Doc Type": "Office Supplies", "Category": "Taxes & Fees",           "Description": "HST (13%)",                           "Currency": "CAD", "Amount": 14.95,   "Confidence": 0.9},

        # Week of Apr 28
        {"Date": "2025-04-28", "Vendor": "Enbridge Gas",          "Doc Type": "Utilities",       "Category": "Gas",                    "Description": "Natural Gas — Apr",                   "Currency": "CAD", "Amount": 189.22,  "Confidence": 0.9},
        {"Date": "2025-04-28", "Vendor": "Enbridge Gas",          "Doc Type": "Utilities",       "Category": "Taxes & Fees",           "Description": "HST (13%)",                           "Currency": "CAD", "Amount": 24.60,   "Confidence": 0.9},
        {"Date": "2025-04-29", "Vendor": "Dell Technologies",     "Doc Type": "Equipment",       "Category": "Networking Equipment",   "Description": "Cisco Catalyst 1000 Switch",          "Currency": "CAD", "Amount": 899.00,  "Confidence": 0.9},
        {"Date": "2025-04-29", "Vendor": "Dell Technologies",     "Doc Type": "Equipment",       "Category": "Installation",           "Description": "Network Switch Installation",         "Currency": "CAD", "Amount": 249.00,  "Confidence": 0.9},
        {"Date": "2025-04-29", "Vendor": "Dell Technologies",     "Doc Type": "Equipment",       "Category": "Taxes & Fees",           "Description": "HST (13%)",                           "Currency": "CAD", "Amount": 149.24,  "Confidence": 0.9},

        # ====================================================================
        # MAY 2025
        # ====================================================================

        # Week of May 05
        {"Date": "2025-05-05", "Vendor": "Staples Canada",        "Doc Type": "Office Supplies", "Category": "Paper Products",         "Description": "A4 Copy Paper (5 reams)",             "Currency": "CAD", "Amount": 54.99,   "Confidence": 0.9},
        {"Date": "2025-05-05", "Vendor": "Staples Canada",        "Doc Type": "Office Supplies", "Category": "Printer Supplies",       "Description": "HP 67XL Black Ink Cartridge",         "Currency": "CAD", "Amount": 42.49,   "Confidence": 0.9},
        {"Date": "2025-05-05", "Vendor": "Staples Canada",        "Doc Type": "Office Supplies", "Category": "Filing & Storage",       "Description": "Label Maker Tape (3-pack)",           "Currency": "CAD", "Amount": 24.99,   "Confidence": 0.9},
        {"Date": "2025-05-05", "Vendor": "Staples Canada",        "Doc Type": "Office Supplies", "Category": "Taxes & Fees",           "Description": "HST (13%)",                           "Currency": "CAD", "Amount": 16.04,   "Confidence": 0.9},
        {"Date": "2025-05-06", "Vendor": "Toronto Hydro",         "Doc Type": "Utilities",       "Category": "Electricity",            "Description": "Commercial Electricity — May W1",     "Currency": "CAD", "Amount": 311.78,  "Confidence": 0.9},
        {"Date": "2025-05-06", "Vendor": "Toronto Hydro",         "Doc Type": "Utilities",       "Category": "Service Charges",        "Description": "Distribution Charge",                 "Currency": "CAD", "Amount": 38.50,   "Confidence": 0.9},
        {"Date": "2025-05-06", "Vendor": "Toronto Hydro",         "Doc Type": "Utilities",       "Category": "Taxes & Fees",           "Description": "HST (13%)",                           "Currency": "CAD", "Amount": 45.49,   "Confidence": 0.9},

        # Week of May 12
        {"Date": "2025-05-12", "Vendor": "Rogers Business",       "Doc Type": "Utilities",       "Category": "Internet",               "Description": "Fibre Internet 1Gbps",                "Currency": "CAD", "Amount": 189.99,  "Confidence": 0.9},
        {"Date": "2025-05-12", "Vendor": "Rogers Business",       "Doc Type": "Utilities",       "Category": "Telephone",              "Description": "Business Phone Lines (3 lines)",      "Currency": "CAD", "Amount": 124.97,  "Confidence": 0.9},
        {"Date": "2025-05-12", "Vendor": "Rogers Business",       "Doc Type": "Utilities",       "Category": "Taxes & Fees",           "Description": "HST (13%)",                           "Currency": "CAD", "Amount": 40.95,   "Confidence": 0.9},
        {"Date": "2025-05-13", "Vendor": "CleanPro Services",     "Doc Type": "Services",        "Category": "Cleaning",               "Description": "Weekly Office Cleaning",              "Currency": "CAD", "Amount": 320.00,  "Confidence": 0.9},
        {"Date": "2025-05-13", "Vendor": "CleanPro Services",     "Doc Type": "Services",        "Category": "Cleaning",               "Description": "Carpet Steam Clean",                  "Currency": "CAD", "Amount": 420.00,  "Confidence": 0.9},
        {"Date": "2025-05-13", "Vendor": "CleanPro Services",     "Doc Type": "Services",        "Category": "Taxes & Fees",           "Description": "HST (13%)",                           "Currency": "CAD", "Amount": 96.20,   "Confidence": 0.9},

        # Week of May 19
        {"Date": "2025-05-19", "Vendor": "Apex Consulting Group", "Doc Type": "Services",        "Category": "Professional Services",  "Description": "Cybersecurity Assessment",            "Currency": "CAD", "Amount": 2200.00, "Confidence": 0.9},
        {"Date": "2025-05-19", "Vendor": "Apex Consulting Group", "Doc Type": "Services",        "Category": "Taxes & Fees",           "Description": "HST (13%)",                           "Currency": "CAD", "Amount": 286.00,  "Confidence": 0.9},
        {"Date": "2025-05-20", "Vendor": "Amazon Business",       "Doc Type": "Office Supplies", "Category": "Technology Accessories", "Description": "Wireless Presenter Clicker",          "Currency": "CAD", "Amount": 34.99,   "Confidence": 0.9},
        {"Date": "2025-05-20", "Vendor": "Amazon Business",       "Doc Type": "Office Supplies", "Category": "Desk Accessories",       "Description": "Cable Management Kit",                "Currency": "CAD", "Amount": 29.99,   "Confidence": 0.9},
        {"Date": "2025-05-20", "Vendor": "Amazon Business",       "Doc Type": "Office Supplies", "Category": "Taxes & Fees",           "Description": "HST (13%)",                           "Currency": "CAD", "Amount": 8.45,    "Confidence": 0.9},

        # Week of May 26
        {"Date": "2025-05-26", "Vendor": "Enbridge Gas",          "Doc Type": "Utilities",       "Category": "Gas",                    "Description": "Natural Gas — May",                   "Currency": "CAD", "Amount": 142.50,  "Confidence": 0.9},
        {"Date": "2025-05-26", "Vendor": "Enbridge Gas",          "Doc Type": "Utilities",       "Category": "Taxes & Fees",           "Description": "HST (13%)",                           "Currency": "CAD", "Amount": 18.53,   "Confidence": 0.9},
        {"Date": "2025-05-27", "Vendor": "Dell Technologies",     "Doc Type": "Equipment",       "Category": "Computer Hardware",      "Description": "WD 2TB External SSD (2-pack)",        "Currency": "CAD", "Amount": 279.98,  "Confidence": 0.9},
        {"Date": "2025-05-27", "Vendor": "Dell Technologies",     "Doc Type": "Equipment",       "Category": "Taxes & Fees",           "Description": "HST (13%)",                           "Currency": "CAD", "Amount": 36.40,   "Confidence": 0.9},

        # ====================================================================
        # JUNE 2025
        # ====================================================================

        # Week of Jun 02
        {"Date": "2025-06-02", "Vendor": "Staples Canada",        "Doc Type": "Office Supplies", "Category": "Paper Products",         "Description": "A4 Copy Paper (5 reams)",             "Currency": "CAD", "Amount": 54.99,   "Confidence": 0.9},
        {"Date": "2025-06-02", "Vendor": "Staples Canada",        "Doc Type": "Office Supplies", "Category": "Writing Instruments",    "Description": "Sharpie Markers (20-pack)",           "Currency": "CAD", "Amount": 19.99,   "Confidence": 0.9},
        {"Date": "2025-06-02", "Vendor": "Staples Canada",        "Doc Type": "Office Supplies", "Category": "Taxes & Fees",           "Description": "HST (13%)",                           "Currency": "CAD", "Amount": 9.75,    "Confidence": 0.9},
        {"Date": "2025-06-03", "Vendor": "Toronto Hydro",         "Doc Type": "Utilities",       "Category": "Electricity",            "Description": "Commercial Electricity — Jun W1",     "Currency": "CAD", "Amount": 298.65,  "Confidence": 0.9},
        {"Date": "2025-06-03", "Vendor": "Toronto Hydro",         "Doc Type": "Utilities",       "Category": "Service Charges",        "Description": "Distribution Charge",                 "Currency": "CAD", "Amount": 38.50,   "Confidence": 0.9},
        {"Date": "2025-06-03", "Vendor": "Toronto Hydro",         "Doc Type": "Utilities",       "Category": "Taxes & Fees",           "Description": "HST (13%)",                           "Currency": "CAD", "Amount": 43.76,   "Confidence": 0.9},

        # Week of Jun 09
        {"Date": "2025-06-09", "Vendor": "Rogers Business",       "Doc Type": "Utilities",       "Category": "Internet",               "Description": "Fibre Internet 1Gbps",                "Currency": "CAD", "Amount": 189.99,  "Confidence": 0.9},
        {"Date": "2025-06-09", "Vendor": "Rogers Business",       "Doc Type": "Utilities",       "Category": "Telephone",              "Description": "Business Phone Lines (3 lines)",      "Currency": "CAD", "Amount": 124.97,  "Confidence": 0.9},
        {"Date": "2025-06-09", "Vendor": "Rogers Business",       "Doc Type": "Utilities",       "Category": "Taxes & Fees",           "Description": "HST (13%)",                           "Currency": "CAD", "Amount": 40.95,   "Confidence": 0.9},
        {"Date": "2025-06-10", "Vendor": "CleanPro Services",     "Doc Type": "Services",        "Category": "Cleaning",               "Description": "Weekly Office Cleaning",              "Currency": "CAD", "Amount": 320.00,  "Confidence": 0.9},
        {"Date": "2025-06-10", "Vendor": "CleanPro Services",     "Doc Type": "Services",        "Category": "Taxes & Fees",           "Description": "HST (13%)",                           "Currency": "CAD", "Amount": 41.60,   "Confidence": 0.9},

        # Week of Jun 16
        {"Date": "2025-06-16", "Vendor": "Apex Consulting Group", "Doc Type": "Services",        "Category": "Consulting",             "Description": "Q2 Tech Roadmap Review (5 hrs)",      "Currency": "CAD", "Amount": 1500.00, "Confidence": 0.9},
        {"Date": "2025-06-16", "Vendor": "Apex Consulting Group", "Doc Type": "Services",        "Category": "Taxes & Fees",           "Description": "HST (13%)",                           "Currency": "CAD", "Amount": 195.00,  "Confidence": 0.9},
        {"Date": "2025-06-17", "Vendor": "Amazon Business",       "Doc Type": "Office Supplies", "Category": "Printer Supplies",       "Description": "HP 410X Black Toner (2-pack)",        "Currency": "CAD", "Amount": 169.98,  "Confidence": 0.9},
        {"Date": "2025-06-17", "Vendor": "Amazon Business",       "Doc Type": "Office Supplies", "Category": "Technology Accessories", "Description": "USB-A to USB-C Adapters (6-pack)",    "Currency": "CAD", "Amount": 17.99,   "Confidence": 0.9},
        {"Date": "2025-06-17", "Vendor": "Amazon Business",       "Doc Type": "Office Supplies", "Category": "Taxes & Fees",           "Description": "HST (13%)",                           "Currency": "CAD", "Amount": 24.37,   "Confidence": 0.9},

        # Week of Jun 23
        {"Date": "2025-06-23", "Vendor": "Dell Technologies",     "Doc Type": "Equipment",       "Category": "Computer Hardware",      "Description": "Dell 27 4K Monitor",                  "Currency": "CAD", "Amount": 649.00,  "Confidence": 0.9},
        {"Date": "2025-06-23", "Vendor": "Dell Technologies",     "Doc Type": "Equipment",       "Category": "Peripherals",            "Description": "Logitech MX Keys Keyboard",           "Currency": "CAD", "Amount": 149.99,  "Confidence": 0.9},
        {"Date": "2025-06-23", "Vendor": "Dell Technologies",     "Doc Type": "Equipment",       "Category": "Taxes & Fees",           "Description": "HST (13%)",                           "Currency": "CAD", "Amount": 103.99,  "Confidence": 0.9},
        {"Date": "2025-06-24", "Vendor": "Enbridge Gas",          "Doc Type": "Utilities",       "Category": "Gas",                    "Description": "Natural Gas — Jun",                   "Currency": "CAD", "Amount": 98.40,   "Confidence": 0.9},
        {"Date": "2025-06-24", "Vendor": "Enbridge Gas",          "Doc Type": "Utilities",       "Category": "Taxes & Fees",           "Description": "HST (13%)",                           "Currency": "CAD", "Amount": 12.79,   "Confidence": 0.9},

        # ====================================================================
        # JULY 2025
        # ====================================================================

        # Week of Jul 07
        {"Date": "2025-07-07", "Vendor": "Staples Canada",        "Doc Type": "Office Supplies", "Category": "Paper Products",         "Description": "A4 Copy Paper (5 reams)",             "Currency": "CAD", "Amount": 54.99,   "Confidence": 0.9},
        {"Date": "2025-07-07", "Vendor": "Staples Canada",        "Doc Type": "Office Supplies", "Category": "Printer Supplies",       "Description": "HP 67XL Colour Ink Cartridge",        "Currency": "CAD", "Amount": 46.99,   "Confidence": 0.9},
        {"Date": "2025-07-07", "Vendor": "Staples Canada",        "Doc Type": "Office Supplies", "Category": "Desk Accessories",       "Description": "Staple Remover & Stapler Set",        "Currency": "CAD", "Amount": 12.99,   "Confidence": 0.9},
        {"Date": "2025-07-07", "Vendor": "Staples Canada",        "Doc Type": "Office Supplies", "Category": "Taxes & Fees",           "Description": "HST (13%)",                           "Currency": "CAD", "Amount": 14.84,   "Confidence": 0.9},
        {"Date": "2025-07-08", "Vendor": "Toronto Hydro",         "Doc Type": "Utilities",       "Category": "Electricity",            "Description": "Commercial Electricity — Jul W1",     "Currency": "CAD", "Amount": 334.20,  "Confidence": 0.9},
        {"Date": "2025-07-08", "Vendor": "Toronto Hydro",         "Doc Type": "Utilities",       "Category": "Service Charges",        "Description": "Distribution Charge",                 "Currency": "CAD", "Amount": 38.50,   "Confidence": 0.9},
        {"Date": "2025-07-08", "Vendor": "Toronto Hydro",         "Doc Type": "Utilities",       "Category": "Taxes & Fees",           "Description": "HST (13%)",                           "Currency": "CAD", "Amount": 48.45,   "Confidence": 0.9},

        # Week of Jul 14
        {"Date": "2025-07-14", "Vendor": "Rogers Business",       "Doc Type": "Utilities",       "Category": "Internet",               "Description": "Fibre Internet 1Gbps",                "Currency": "CAD", "Amount": 189.99,  "Confidence": 0.9},
        {"Date": "2025-07-14", "Vendor": "Rogers Business",       "Doc Type": "Utilities",       "Category": "Telephone",              "Description": "Business Phone Lines (3 lines)",      "Currency": "CAD", "Amount": 124.97,  "Confidence": 0.9},
        {"Date": "2025-07-14", "Vendor": "Rogers Business",       "Doc Type": "Utilities",       "Category": "Taxes & Fees",           "Description": "HST (13%)",                           "Currency": "CAD", "Amount": 40.95,   "Confidence": 0.9},
        {"Date": "2025-07-15", "Vendor": "CleanPro Services",     "Doc Type": "Services",        "Category": "Cleaning",               "Description": "Weekly Office Cleaning",              "Currency": "CAD", "Amount": 320.00,  "Confidence": 0.9},
        {"Date": "2025-07-15", "Vendor": "CleanPro Services",     "Doc Type": "Services",        "Category": "Cleaning",               "Description": "Window Cleaning — Exterior",          "Currency": "CAD", "Amount": 280.00,  "Confidence": 0.9},
        {"Date": "2025-07-15", "Vendor": "CleanPro Services",     "Doc Type": "Services",        "Category": "Taxes & Fees",           "Description": "HST (13%)",                           "Currency": "CAD", "Amount": 78.00,   "Confidence": 0.9},

        # Week of Jul 21
        {"Date": "2025-07-21", "Vendor": "Apex Consulting Group", "Doc Type": "Services",        "Category": "Consulting",             "Description": "AI Readiness Assessment (6 hrs)",     "Currency": "CAD", "Amount": 1800.00, "Confidence": 0.9},
        {"Date": "2025-07-21", "Vendor": "Apex Consulting Group", "Doc Type": "Services",        "Category": "Taxes & Fees",           "Description": "HST (13%)",                           "Currency": "CAD", "Amount": 234.00,  "Confidence": 0.9},
        {"Date": "2025-07-22", "Vendor": "Amazon Business",       "Doc Type": "Office Supplies", "Category": "Technology Accessories", "Description": "USB 3.0 Hub 10-port",                 "Currency": "CAD", "Amount": 59.99,   "Confidence": 0.9},
        {"Date": "2025-07-22", "Vendor": "Amazon Business",       "Doc Type": "Office Supplies", "Category": "Filing & Storage",       "Description": "Accordion File Organiser",            "Currency": "CAD", "Amount": 27.99,   "Confidence": 0.9},
        {"Date": "2025-07-22", "Vendor": "Amazon Business",       "Doc Type": "Office Supplies", "Category": "Taxes & Fees",           "Description": "HST (13%)",                           "Currency": "CAD", "Amount": 11.44,   "Confidence": 0.9},

        # Week of Jul 28
        {"Date": "2025-07-28", "Vendor": "Enbridge Gas",          "Doc Type": "Utilities",       "Category": "Gas",                    "Description": "Natural Gas — Jul",                   "Currency": "CAD", "Amount": 82.10,   "Confidence": 0.9},
        {"Date": "2025-07-28", "Vendor": "Enbridge Gas",          "Doc Type": "Utilities",       "Category": "Taxes & Fees",           "Description": "HST (13%)",                           "Currency": "CAD", "Amount": 10.67,   "Confidence": 0.9},
        {"Date": "2025-07-29", "Vendor": "Dell Technologies",     "Doc Type": "Equipment",       "Category": "Computer Hardware",      "Description": "Crucial 32GB RAM Kit (2x16GB)",       "Currency": "CAD", "Amount": 189.99,  "Confidence": 0.9},
        {"Date": "2025-07-29", "Vendor": "Dell Technologies",     "Doc Type": "Equipment",       "Category": "Peripherals",            "Description": "Logitech MX Master 3S Mouse",         "Currency": "CAD", "Amount": 119.99,  "Confidence": 0.9},
        {"Date": "2025-07-29", "Vendor": "Dell Technologies",     "Doc Type": "Equipment",       "Category": "Taxes & Fees",           "Description": "HST (13%)",                           "Currency": "CAD", "Amount": 40.30,   "Confidence": 0.9},

        # ====================================================================
        # AUGUST 2025
        # ====================================================================

        # Week of Aug 04
        {"Date": "2025-08-04", "Vendor": "Staples Canada",        "Doc Type": "Office Supplies", "Category": "Paper Products",         "Description": "A4 Copy Paper (3 reams)",             "Currency": "CAD", "Amount": 32.99,   "Confidence": 0.9},
        {"Date": "2025-08-04", "Vendor": "Staples Canada",        "Doc Type": "Office Supplies", "Category": "Writing Instruments",    "Description": "Expo Whiteboard Markers (12-pack)",   "Currency": "CAD", "Amount": 16.99,   "Confidence": 0.9},
        {"Date": "2025-08-04", "Vendor": "Staples Canada",        "Doc Type": "Office Supplies", "Category": "Taxes & Fees",           "Description": "HST (13%)",                           "Currency": "CAD", "Amount": 6.49,    "Confidence": 0.9},
        {"Date": "2025-08-05", "Vendor": "Toronto Hydro",         "Doc Type": "Utilities",       "Category": "Electricity",            "Description": "Commercial Electricity — Aug W1",     "Currency": "CAD", "Amount": 358.44,  "Confidence": 0.9},
        {"Date": "2025-08-05", "Vendor": "Toronto Hydro",         "Doc Type": "Utilities",       "Category": "Service Charges",        "Description": "Distribution Charge",                 "Currency": "CAD", "Amount": 38.50,   "Confidence": 0.9},
        {"Date": "2025-08-05", "Vendor": "Toronto Hydro",         "Doc Type": "Utilities",       "Category": "Taxes & Fees",           "Description": "HST (13%)",                           "Currency": "CAD", "Amount": 51.58,   "Confidence": 0.9},

        # Week of Aug 11
        {"Date": "2025-08-11", "Vendor": "Rogers Business",       "Doc Type": "Utilities",       "Category": "Internet",               "Description": "Fibre Internet 1Gbps",                "Currency": "CAD", "Amount": 189.99,  "Confidence": 0.9},
        {"Date": "2025-08-11", "Vendor": "Rogers Business",       "Doc Type": "Utilities",       "Category": "Telephone",              "Description": "Business Phone Lines (3 lines)",      "Currency": "CAD", "Amount": 124.97,  "Confidence": 0.9},
        {"Date": "2025-08-11", "Vendor": "Rogers Business",       "Doc Type": "Utilities",       "Category": "Taxes & Fees",           "Description": "HST (13%)",                           "Currency": "CAD", "Amount": 40.95,   "Confidence": 0.9},
        {"Date": "2025-08-12", "Vendor": "CleanPro Services",     "Doc Type": "Services",        "Category": "Cleaning",               "Description": "Weekly Office Cleaning",              "Currency": "CAD", "Amount": 320.00,  "Confidence": 0.9},
        {"Date": "2025-08-12", "Vendor": "CleanPro Services",     "Doc Type": "Services",        "Category": "Taxes & Fees",           "Description": "HST (13%)",                           "Currency": "CAD", "Amount": 41.60,   "Confidence": 0.9},

        # Week of Aug 18
        {"Date": "2025-08-18", "Vendor": "Apex Consulting Group", "Doc Type": "Services",        "Category": "Professional Services",  "Description": "Data Privacy Compliance Review",      "Currency": "CAD", "Amount": 2600.00, "Confidence": 0.9},
        {"Date": "2025-08-18", "Vendor": "Apex Consulting Group", "Doc Type": "Services",        "Category": "Taxes & Fees",           "Description": "HST (13%)",                           "Currency": "CAD", "Amount": 338.00,  "Confidence": 0.9},
        {"Date": "2025-08-19", "Vendor": "Amazon Business",       "Doc Type": "Office Supplies", "Category": "Printer Supplies",       "Description": "Canon PG-245XL Black Ink",            "Currency": "CAD", "Amount": 38.99,   "Confidence": 0.9},
        {"Date": "2025-08-19", "Vendor": "Amazon Business",       "Doc Type": "Office Supplies", "Category": "Technology Accessories", "Description": "Screen Privacy Filter 27in",          "Currency": "CAD", "Amount": 44.99,   "Confidence": 0.9},
        {"Date": "2025-08-19", "Vendor": "Amazon Business",       "Doc Type": "Office Supplies", "Category": "Taxes & Fees",           "Description": "HST (13%)",                           "Currency": "CAD", "Amount": 10.92,   "Confidence": 0.9},

        # Week of Aug 25
        {"Date": "2025-08-25", "Vendor": "Enbridge Gas",          "Doc Type": "Utilities",       "Category": "Gas",                    "Description": "Natural Gas — Aug",                   "Currency": "CAD", "Amount": 74.30,   "Confidence": 0.9},
        {"Date": "2025-08-25", "Vendor": "Enbridge Gas",          "Doc Type": "Utilities",       "Category": "Taxes & Fees",           "Description": "HST (13%)",                           "Currency": "CAD", "Amount": 9.66,    "Confidence": 0.9},
        {"Date": "2025-08-26", "Vendor": "Dell Technologies",     "Doc Type": "Equipment",       "Category": "Software Licenses",      "Description": "Adobe Creative Cloud (annual)",       "Currency": "CAD", "Amount": 839.88,  "Confidence": 0.9},
        {"Date": "2025-08-26", "Vendor": "Dell Technologies",     "Doc Type": "Equipment",       "Category": "Taxes & Fees",           "Description": "HST (13%)",                           "Currency": "CAD", "Amount": 109.18,  "Confidence": 0.9},

        # ====================================================================
        # SEPTEMBER 2025
        # ====================================================================

        # Week of Sep 01
        {"Date": "2025-09-01", "Vendor": "Staples Canada",        "Doc Type": "Office Supplies", "Category": "Paper Products",         "Description": "A4 Copy Paper (5 reams)",             "Currency": "CAD", "Amount": 54.99,   "Confidence": 0.9},
        {"Date": "2025-09-01", "Vendor": "Staples Canada",        "Doc Type": "Office Supplies", "Category": "Printer Supplies",       "Description": "HP 67XL Black Ink Cartridge",         "Currency": "CAD", "Amount": 42.49,   "Confidence": 0.9},
        {"Date": "2025-09-01", "Vendor": "Staples Canada",        "Doc Type": "Office Supplies", "Category": "Filing & Storage",       "Description": "Binder Dividers 5-tab (10-pack)",     "Currency": "CAD", "Amount": 22.99,   "Confidence": 0.9},
        {"Date": "2025-09-01", "Vendor": "Staples Canada",        "Doc Type": "Office Supplies", "Category": "Taxes & Fees",           "Description": "HST (13%)",                           "Currency": "CAD", "Amount": 15.65,   "Confidence": 0.9},
        {"Date": "2025-09-02", "Vendor": "Toronto Hydro",         "Doc Type": "Utilities",       "Category": "Electricity",            "Description": "Commercial Electricity — Sep W1",     "Currency": "CAD", "Amount": 318.90,  "Confidence": 0.9},
        {"Date": "2025-09-02", "Vendor": "Toronto Hydro",         "Doc Type": "Utilities",       "Category": "Service Charges",        "Description": "Distribution Charge",                 "Currency": "CAD", "Amount": 38.50,   "Confidence": 0.9},
        {"Date": "2025-09-02", "Vendor": "Toronto Hydro",         "Doc Type": "Utilities",       "Category": "Taxes & Fees",           "Description": "HST (13%)",                           "Currency": "CAD", "Amount": 46.38,   "Confidence": 0.9},

        # Week of Sep 08
        {"Date": "2025-09-08", "Vendor": "Rogers Business",       "Doc Type": "Utilities",       "Category": "Internet",               "Description": "Fibre Internet 1Gbps",                "Currency": "CAD", "Amount": 189.99,  "Confidence": 0.9},
        {"Date": "2025-09-08", "Vendor": "Rogers Business",       "Doc Type": "Utilities",       "Category": "Telephone",              "Description": "Business Phone Lines (3 lines)",      "Currency": "CAD", "Amount": 124.97,  "Confidence": 0.9},
        {"Date": "2025-09-08", "Vendor": "Rogers Business",       "Doc Type": "Utilities",       "Category": "Taxes & Fees",           "Description": "HST (13%)",                           "Currency": "CAD", "Amount": 40.95,   "Confidence": 0.9},
        {"Date": "2025-09-09", "Vendor": "CleanPro Services",     "Doc Type": "Services",        "Category": "Cleaning",               "Description": "Weekly Office Cleaning",              "Currency": "CAD", "Amount": 320.00,  "Confidence": 0.9},
        {"Date": "2025-09-09", "Vendor": "CleanPro Services",     "Doc Type": "Services",        "Category": "Cleaning",               "Description": "Post-Summer Deep Clean",              "Currency": "CAD", "Amount": 490.00,  "Confidence": 0.9},
        {"Date": "2025-09-09", "Vendor": "CleanPro Services",     "Doc Type": "Services",        "Category": "Taxes & Fees",           "Description": "HST (13%)",                           "Currency": "CAD", "Amount": 105.30,  "Confidence": 0.9},

        # Week of Sep 15
        {"Date": "2025-09-15", "Vendor": "Apex Consulting Group", "Doc Type": "Services",        "Category": "Consulting",             "Description": "Q3 Business Review Facilitation",     "Currency": "CAD", "Amount": 2000.00, "Confidence": 0.9},
        {"Date": "2025-09-15", "Vendor": "Apex Consulting Group", "Doc Type": "Services",        "Category": "Taxes & Fees",           "Description": "HST (13%)",                           "Currency": "CAD", "Amount": 260.00,  "Confidence": 0.9},
        {"Date": "2025-09-16", "Vendor": "Amazon Business",       "Doc Type": "Office Supplies", "Category": "Technology Accessories", "Description": "Laptop Stand Adjustable (2-pack)",    "Currency": "CAD", "Amount": 69.98,   "Confidence": 0.9},
        {"Date": "2025-09-16", "Vendor": "Amazon Business",       "Doc Type": "Office Supplies", "Category": "Desk Accessories",       "Description": "Mesh Desk Organiser",                 "Currency": "CAD", "Amount": 34.99,   "Confidence": 0.9},
        {"Date": "2025-09-16", "Vendor": "Amazon Business",       "Doc Type": "Office Supplies", "Category": "Taxes & Fees",           "Description": "HST (13%)",                           "Currency": "CAD", "Amount": 13.63,   "Confidence": 0.9},

        # Week of Sep 22
        {"Date": "2025-09-22", "Vendor": "Dell Technologies",     "Doc Type": "Equipment",       "Category": "Computer Hardware",      "Description": "Dell OptiPlex 7020 Desktop",          "Currency": "CAD", "Amount": 1349.00, "Confidence": 0.9},
        {"Date": "2025-09-22", "Vendor": "Dell Technologies",     "Doc Type": "Equipment",       "Category": "Networking Equipment",   "Description": "TP-Link Wi-Fi 6 Access Point",        "Currency": "CAD", "Amount": 229.99,  "Confidence": 0.9},
        {"Date": "2025-09-22", "Vendor": "Dell Technologies",     "Doc Type": "Equipment",       "Category": "Installation",           "Description": "Hardware Setup & Imaging",            "Currency": "CAD", "Amount": 199.00,  "Confidence": 0.9},
        {"Date": "2025-09-22", "Vendor": "Dell Technologies",     "Doc Type": "Equipment",       "Category": "Taxes & Fees",           "Description": "HST (13%)",                           "Currency": "CAD", "Amount": 230.49,  "Confidence": 0.9},
        {"Date": "2025-09-23", "Vendor": "Enbridge Gas",          "Doc Type": "Utilities",       "Category": "Gas",                    "Description": "Natural Gas — Sep",                   "Currency": "CAD", "Amount": 121.60,  "Confidence": 0.9},
        {"Date": "2025-09-23", "Vendor": "Enbridge Gas",          "Doc Type": "Utilities",       "Category": "Taxes & Fees",           "Description": "HST (13%)",                           "Currency": "CAD", "Amount": 15.81,   "Confidence": 0.9},

    ]

    df = pd.DataFrame(rows)
    df = df[["Date", "Vendor", "Doc Type", "Category", "Description", "Currency", "Amount", "Confidence"]]
    return df

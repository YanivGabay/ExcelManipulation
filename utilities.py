import re


def extract_mid(text, start_position, length):
    adjusted_start = start_position - 1
    return text[adjusted_start:adjusted_start + length]

def is_hebrew(s):
    return bool(re.search('[\u0590-\u05FF]', s))

def reverse_word_if_hebrew(word):
    return word[::-1] if is_hebrew(word) else word
column_to_field_mapping = {
    "Identifier": "costumer_code",
    "Driver's Name": "full_name",
    "Driver's Address-City": "city_name",
    "Driver's Address-Street": "street_name",
    "Driver's Address-House Number": "house_number",
    "Driver's Address-PO Box": "po_box",
    "Driver's Address-Zip Code": "postal_code",
    "Ownership Date": "ownership_date"
    # Add more mappings as needed...
}
column_names = [
    "Identifier",
    "Reporting Date",
    "Reporting Time",
    "Approval Date",
    "Driver's Name",
    "Driver's Address-City",
    "Driver's Address-Street",
    "Driver's Address-House Number",
    "Driver's Address-PO Box",
    "Driver's Address-Zip Code",
    "License Number",
    "Reported Location-Town",
    "Reported Location-Street",
    "Reported Location-Road",
    "Number of Violations",
    "Type of Violation 1",
    "Type of Violation 2",
    "Type of Violation 3",
    "Link",
    "Username",
    "Access Code",
    "Why Violation Is Serious 1",
    "Why Violation Is Serious 2",
    "Why Violation Is Serious 3",
    "Possible Accident 1",
    "Possible Accident 2",
    "Possible Accident 3",
    "Name of Violation Image File",
    "Name of Barcode Image File",
    "Type of Letter",
    "Reported Location-Kilometer",
    "Ownership Date",
]


extraction_specs = [
    # (column_name, start_position, length)
    ("costumer_code", 1, 3),
    ("response_code", 4, 1),
    ("series", 5, 1),
    ("filler", 6, 6),
    ("date", 12, 6),
    ("hour", 18, 4),
    ("address", 42, 6),
      ("type_of_ownership", 48, 1),
      ("handicap", 49, 1),
       ("number_of_offend", 50, 4),
        ("number_of_offend", 54, 3),
         
    ("trial_date", 57, 6),
    ("pusher", 63, 4),
    ("vehicle_number", 67, 8),
    ("postal_code", 75, 7),
    ("city_code", 82, 4),
    ("city_name", 86, 13),
    # "city_name_corrected" would be used when we know what @mmm(R2) does
    ("street_name", 99, 17),
    # "street_name_corrected" would be used when we know what @mmm(T2) does
    ("house_number", 116, 5),
    ("apartment_number", 121, 4),
    ("family", 125, 14),
    # "family_corrected" would be used when we know what @mmm(X2) does
    ("private", 139, 8),
    # "private_corrected" would be used when we know what @mmm(Z2) does
    ("identity", 147, 9),
    ("ownership_date", 156, 6),
    ("vehicle_type", 162, 3),
    # "vehicle_type_description" might be used for the next three, but need more context to differentiate them
    ("vehicle_type_description1", 165, 7),
    ("logo_where", 172, 5),
    ("name_of_where", 177, 14),
    # "vehicle_type_description_corrected" would be used when we know what @mmm(AH2) does
    ("color", 191, 2),
    ("code_of_note", 193, 1),
    # "manufacturer_name_corrected" would be used when we know how to handle the duplicate names
    ("production_year", 194, 2),
    ("expiry", 196, 6),
    # We will need to handle the CONCATENATE function separately
]


# constants.py

# Column indices
COLUMN_A_INDEX = 0
COLUMN_K_INDEX = 10

# Formatting configuration for text output
FORMAT_CONFIG = {
    'start_code': '913',
    'date_format': '%d%m%y',
    'end_static': '50050095',
    'spaces_after_start': 0,
    'spaces_between_first_date': 11,
    'spaces_between_date_last': 20,
    'spaces_between_last_end': 18
}

RULES_COLUMN_MAPPING = {
    #H into V
    #I into W
    #F into X
    #G into Y
    "H": "V",
    "I": "W",
    "F": "X",
    "G": "Y"
}

NEW_COLUMN_NAMES = {
    # V into כותרת
    # W into  מלל
    # X into סכום הקנס
    # Y into נקודות

    "V": "כותרת",
    "W": "מלל",
    "X": "סכום הקנס",
    "Y": "נקודות"

    }

EXCEL_COLUMN_MAPPING = {
    "full_name": 4, #E
    "city_name": 5, #F
    "street_name": 6, #G
    "house_number": 7, #H
    "po_box": 8, #I
    "postal_code": 9, #J
    
}

# this is the formula taken from the original excel file
# this translate the response from the txt file TOMOT
# into the following fields depend on the position, length
EXTRACTION_FORMULA = [
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
 
]
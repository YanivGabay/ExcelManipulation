




def apply_formula(row, today, config):
    """Apply formatting based on the given configuration."""
    # Access by position using .iloc
    first_part = str(row.iloc[0]).zfill(8)
    date_part = today.strftime(config['date_format'])
    last_part = str(row.iloc[1]).zfill(6)

    # Combine all parts with specific spacings
    formatted_string = (
        f"{config['start_code']}" + " " * config['spaces_after_start'] +
        f"{first_part}" + " " * config['spaces_between_first_date'] +
        f"{date_part}" + " " * config['spaces_between_date_last'] +
        f"{last_part}" + " " * config['spaces_between_last_end'] +
        f"{config['end_static']}"
    )
    return formatted_string


def extract_bytes(byte_array, start: int, count: int):
    """
    Extract from the byte_array the given number (count) of bytes from the start position

    Parameters:
    - byte_array (bytes): The byte array to extract from
    - start (int): Start position in the byte array to extract from
    - count (int): Number of bytes to extract from the start position

    Returns:
    - bytes: The extracted bytes from the byte array
    """

    # Calculates the end position and checks if it is within the range
    end = start + count
    if end > len(byte_array):
        raise ValueError("The end position of the byte array must be within the range")

    return byte_array[start:end]

def hexstr_to_ipv4(hexstr):
    """
    Converts a hex string into its corresponding IPv4 address

    Parameters:
    - hexstr (string): a hex string

    Returns:
    - string (string): a string representation of IPv4
    """
    try:
        decimal = int(hexstr, 16)

        # Converts hexadecimal number to IPv4 address
        return ".".join(map(str, [
            (decimal >> 24) & 255,
            (decimal >> 16) & 255,
            (decimal >>  8) & 255,
            decimal & 255,
        ]))
    except ValueError as err:
        raise ValueError(f"[Please provide a valid hexadecimal string value] {err}")
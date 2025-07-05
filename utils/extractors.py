def extract_valid_data(response_data: dict):
    data = {
        k: v
        for k, v in response_data.items()
        if v not in ([], "", None) and k not in ["certifications"]
    }
    return data
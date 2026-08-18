def format_currency(value):
    if value < 0:
        return f"-${abs(value):,.2f}"
    return f"${value:,.2f}"

def format_percent(value):
    if value > 0:
        return f"+{value:.2f}%"
    return f"{value:.2f}%"

def get_color(value):
    if value > 0:
        return "green"
    elif value < 0:
        return "red"
    return "gray"

def is_empty(value):
    if not value or value == "N/A":
        return True
    else:
        return False


def convert_quantity_units(amount, unit):
    if is_empty(amount):
        raise ValueError("Amount missing")
    if is_empty(unit):
        try:
            chunks = amount.split()
            amount = chunks[0]
            unit = chunks[1]
        except Exception as e:
            raise ValueError(str.format("Amount missing: {}", e))
    mass_unit_mg = 'mg'
    mass_unit_kg = 'kg'
    mass_unit_g = 'g'
    volume_unit_L = 'l'
    volume_unit_mL = 'ml'
    unit = unit.casefold()
    if unit == mass_unit_mg:
        converted_amount = float(amount) * 0.001
        converted_unit = mass_unit_g
    elif unit == mass_unit_kg:
        converted_amount = float(amount) * 1000
        converted_unit = mass_unit_g
    elif unit == mass_unit_g:
        converted_amount = float(amount)
        converted_unit = mass_unit_g
    elif unit == volume_unit_L:
        converted_amount = float(amount) * 1000
        converted_unit = volume_unit_mL
    elif unit == volume_unit_mL:
        converted_amount = float(amount)
        converted_unit = volume_unit_mL
    else:
        raise ValueError(str.format('Incorrect unit {}', unit))

    return converted_amount, converted_unit

class Quantity:
    def __init__(self, amount, unit):
        converted_amount, converted_unit = convert_quantity_units(amount, unit)
        self.amount, self.unit = converted_amount, converted_unit

    # c = self + other (100, L) + (200, mg)
    def __add__(self, other):
        if self.unit == other.unit:
            combined_amount = float(self.amount) + float(other.amount)
        else:
            raise ValueError(str.format('Impossible to add {} and {}', self.unit, other.unit))
        return Quantity(combined_amount, self.unit)

        # q += b (shorthand for q = q + b)
    def __iadd__(self, other):
        if self.unit == other.unit:
            self.amount += other.amount
        else:
           raise ValueError(str.format('Impossible to add {} and {}', self.unit, other.unit)) 
        return self

    def __str__(self):
        return str.format("{} {}", self.amount, self.unit)

# a = Quantity(20, L)

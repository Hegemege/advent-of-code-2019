import math
import time


class Product:
    def __init__(self, chem_id, amount):
        self.id = chem_id
        self.amount = amount
        self.requirements = {}
        self.surplus = {}

    def replace_requirements(self, chemicals):
        new_requirements = {}
        new_requirements["ORE"] = 0
        for key, value in self.requirements.items():
            if key == "ORE":
                new_requirements["ORE"] += value
                continue

            # Find the formula for the requirement
            req_chemical = chemicals[key]

            req_amount = value

            if key in self.surplus:
                if req_amount < self.surplus[key]:
                    self.surplus[key] -= req_amount
                    req_amount = 0
                else:
                    surplus_reduction = self.surplus[key]
                    req_amount -= surplus_reduction
                    self.surplus[key] -= surplus_reduction

            if req_amount == 0:
                continue

            # Find how many repeats of the requirement formula we need
            # Add any surplus to the surplus reserve

            req_repeats = math.ceil(req_amount / req_chemical.amount)
            to_produce = req_repeats * req_chemical.amount
            to_surplus = to_produce - req_amount

            # Add the requirements of the required product to the new requirements
            for req_key, req_value in req_chemical.requirements.items():
                if req_key not in new_requirements:
                    new_requirements[req_key] = 0
                new_requirements[req_key] += req_repeats * req_value

            # Store surplus
            if key not in self.surplus:
                self.surplus[key] = 0
            self.surplus[key] += to_surplus

        self.requirements = new_requirements


def part1(part_input):
    print("PART1")

    # Every chemical can be produced in only one way
    chemicals = {}
    for row in part_input:
        reqs, product = row.split(" => ")
        reqs.strip()
        product.strip()

        chem_amount, chem_id = product.split(" ")
        chemical = Product(chem_id, int(chem_amount))
        for req in reqs.split(", "):
            req_amount, req_id = req.split(" ")
            chemical.requirements[req_id] = int(req_amount)

        chemicals[chemical.id] = chemical

    while True:
        # Check if there are only ORE requirements left
        if (
            sum(
                map(
                    lambda k: chemicals["FUEL"].requirements[k] if k != "ORE" else 0,
                    chemicals["FUEL"].requirements,
                )
            )
            == 0
        ):
            break

        # Otherwise replace the current requirements
        chemicals["FUEL"].replace_requirements(chemicals)

    print(chemicals["FUEL"].requirements["ORE"])


def part2(part_input):
    print("PART2")

    chemicals = {}
    for row in part_input:
        reqs, product = row.split(" => ")
        reqs.strip()
        product.strip()

        chem_amount, chem_id = product.split(" ")
        chemical = Product(chem_id, int(chem_amount))
        for req in reqs.split(", "):
            req_amount, req_id = req.split(" ")
            chemical.requirements[req_id] = int(req_amount)

        chemicals[chemical.id] = chemical

    original_fuel_requirements = chemicals["FUEL"].requirements.copy()

    ore_tally = 0
    fuel_created = 0
    while True:
        if ore_tally >= 1000000000000:
            break

        # Reset the requirements map
        # Keeps the surplus counters
        chemicals["FUEL"].requirements = original_fuel_requirements.copy()

        fuel_created += 1
        while True:
            # Check if there are only ORE requirements left
            if len(chemicals["FUEL"].requirements) == 1:
                break

            # Otherwise replace the current requirements
            chemicals["FUEL"].replace_requirements(chemicals)

        ore_tally += chemicals["FUEL"].requirements["ORE"]

    print(
        fuel_created - 1
    )  # Exit condition is the limit of surpassing 10 trillion, so subtract 1


if __name__ == "__main__":
    with open("input", "r") as input_file:
        input_file_contents = list(map(str.strip, input_file.readlines()))

        p1_time = time.time()
        part1(input_file_contents)
        print("Took", time.time() - p1_time)

        p2_time = time.time()
        part2(input_file_contents)
        print("Took", time.time() - p2_time)

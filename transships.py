import csv

""" My understanding:
        When a ship arrives it discharges some cargo, which is then stored.
        This cargo can then be added to other ships, or kept at the port.
        Cargo that is added to other ships is called "transshiped".
        I will assume that cargo is stored in a stack. """


# VesselDataDebug was just a csv file I created to test my approach on smaller datasets where I could understand what was happening

class Cargo:
    """ Cargo class. I needed to make this so it can store its origin """
    def __init__(self, cargo_type, quantity, origin):
        # Store quantity here to reduce runtime (having multiple cargo objects of the same data would increase runtime complexity by a factor of the size of a load and discharge)
        self.cargo_type = cargo_type
        self.quantity = quantity
        self.origin = origin

    def __repr__(self):
        return f"{self.quantity} blocks of {['ore', 'coal', 'oil', 'petroleum'][self.cargo_type]} cargo"


""" First I sorted the vesselData by time of arrival. This is done to make the
    process easier. I will simulate ships, by going through each one
    in the order they arrive to the port. If they discharge cargo I will add that
    to the stack. If they load cargo I will remove it from the stack """

# I use a list as a stack. Differents lists are used for ore, coal, oil and petroleum
# Instead of defining each stack differently, grouping them together is done, to make
# the process scale easier, to other kinds of cargo
cargo_stacks = [list(), list(), list(), list()] 

# Dictionary used to store how much a vessel id transships
transships = {}

with open("VesselDataDebug.csv", "r") as csvFile:
    reader = csv.reader(csvFile, delimiter=',', quotechar='"')

    next(reader) # Skip header file
    
    for ship_data in reader:
        # Extract discharge1, load1, discharge2, load2, ... , discharge4, load4
        _, _, _, _, _, d1, l1, d2, l2, d3, l3, d4, l4, _, _, _, _, _, _, _, _, vessel_id = ship_data

        for i, (cargo_stack, data) in enumerate(zip(cargo_stacks, [(d1, l1), (d2, l2), (d3, l3), (d4, l4)])):
            discharge, load = map(int, data)

            # Simulate discharging cargo onto the stack
            if discharge > 0:
                cargo_stack.append(Cargo(i, discharge, vessel_id))
            # print(cargo_stack)
            
            # Simulate loading cargo onto the ship.
            # While doing this store how much cargo other ships have passed onto this ship
            while load > 0:
                # Check to see if any cargo from other ships can be used in the load
                # If not just add cargo and dont update the transships dictionary
                if not cargo_stack:
                    break
                if cargo_stack[-1].quantity >= load:
                    # If the load can be finished using cargo from one ship
                    cargo_stack[-1].quantity -= load
                    
                    transship_cargo_origin_id = cargo_stack[-1].origin
                    transship_quantity = load

                    load = 0
                else:
                    # If the load uses up all the cargo from one ship
                    moved_cargo = cargo_stack.pop()
                    load -= moved_cargo.quantity

                    transship_cargo_origin_id = moved_cargo.origin
                    transship_quantity = moved_cargo.quantity

                
                transships[transship_cargo_origin_id] = transships.get(transship_cargo_origin_id, 0) + transship_quantity
            
print(transships)

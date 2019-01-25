import csv
import datetime

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

# Dictionary used to store data about ships for analysis
ship_data_dict = {}

with open("VesselData.csv", "r") as csvFile:
    reader = csv.reader(csvFile, delimiter=',', quotechar='"')

    next(reader) # Skip header file
    
    for ship_data in reader:
        # Extract discharge1, load1, discharge2, load2, ... , discharge4, load4 as well as other data for analysis
        eta, ata, atd, vesseldwt, vesseltype, d1, l1, d2, l2, d3, l3, d4, l4, stevedore, hasnohamis, earliesteta, latesteta, traveltype, previousportid, nextportid, isremarkable, vessel_id = ship_data
        
        ship_data_dict[vessel_id] = {"eta": eta,
                                "ata": ata,
                                "atd": atd,
                                "vesseldwt": vesseldwt,
                                "vesseltype":vesseltype,
                                "stevedore": stevedore,
                                "hasnohamis": hasnohamis,
                                "earliesteta": earliesteta,
                                "latesteta": latesteta,
                                "traveltype": traveltype           
            }
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

                    # Keep track of origin of cargo and how much cargo has been transported
                    transship_cargo_origin_id = cargo_stack[-1].origin
                    transship_quantity = load

                    load = 0
                else:
                    # If the load uses up all the cargo from one ship
                    moved_cargo = cargo_stack.pop()
                    load -= moved_cargo.quantity

                    # Keep track of origin of cargo and how much cargo has been transported
                    transship_cargo_origin_id = moved_cargo.origin
                    transship_quantity = moved_cargo.quantity

                # Update tranship counter for each vessel
                transships[transship_cargo_origin_id] = transships.get(transship_cargo_origin_id, 0) + transship_quantity

# First graph (vessel type to transshipments)
'''for ship in sorted(transships, key=lambda n:transships[n]):
    print(transships[ship], ship_data_dict[ship]['vesseltype'])'''

# Mean and SD
'''for vessel_type in ['1', '2', '3', '4', '5', '6']:
    # Find ships that are of a given vessel type
    filtered_data = [transships[ship] for ship in transships if ship_data_dict[ship]['vesseltype'] == vessel_type]

    if not filtered_data:
        # Skip if there are no ships of the given vessel type
        continue
    
    mean = sum(filtered_data) / len(data)

    print(vessel_type)
    print("Mean", mean)
    print("SD", (sum((item - mean) ** 2 for item in filtered_data) / len(filtered_data)) ** 0.5)'''


# Second graph (lateness to transshipments)
'''for ship in sorted(transships, key=lambda n:transships[n]):
    eta = datetime.datetime.strptime(ship_data_dict[ship]['eta'], '%Y-%m-%d %H:%M:%S+00')
    ata = datetime.datetime.strptime(ship_data_dict[ship]['ata'], '%Y-%m-%d %H:%M:%S+00')
    print(transships[ship], (ata - eta).days)'''


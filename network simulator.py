import random
import time
import heapq

class Device:
    def __init__(self):
        self.id = random.randint(0, 100)
        self.mac = self.generate_mac()
        self.ip = None

    def generate_mac(self):
        mac = [str(random.randint(0xB, 0x63)) for _ in range(3)]
        return "00:00:00:" + ":".join(mac)

    def __lt__(self, other):
        return self.id < other.id

class Connection:
    def __init__(self, sender, receiver):
        self.sender = sender
        self.receiver = receiver

class Switch(Device):
    def __init__(self):
        super().__init__()
        self.switch_table = []
        print("Switch created with ID:", self.id)

    def connect_device(self, device):
        self.switch_table.append(device)
        network.create_connection(self, device)

    def token_passing(self):
        if not self.switch_table:
            print("No devices connected to the switch", self.id)
            return

        print("Token passing initiated from switch", self.id)

        # Start token passing
        for i, device in enumerate(self.switch_table):
            print("Token passed to device", device.id)

        print("Token reached the switch", self.id, "after completing the cycle")

class Hub(Device):
    def __init__(self):
        super().__init__()
        print("Hub created with ID:", self.id)

class Bridge(Device):
    def __init__(self):
        super().__init__()
        print("Bridge created with ID:", self.id)

class Router(Device):
    def __init__(self):
        super().__init__()
        self.routing_table = {}
        self.forwarding_table = {}
        print("Router created with ID:", self.id)

    def add_route(self, destination_ip, next_hop):
        self.routing_table[destination_ip] = next_hop

    def update_routing_table(self, source_router_id, distance_vector):
        for destination_ip, distance in distance_vector.items():
            if destination_ip not in self.routing_table:
                self.routing_table[destination_ip] = {}
            self.routing_table[destination_ip][source_router_id] = distance

    def update_forwarding_table(self, forwarding_table):
        self.forwarding_table = forwarding_table

    def perform_distance_vector_routing(self):
        router_id = self.id
        routing_table_copy = self.routing_table.copy()
        routing_table_copy[router_id] = {router_id: 0}  # Add self to the routing table

        while True:
            updated = False

            for destination_ip, routes in routing_table_copy.items():
                if destination_ip == router_id:
                    continue

                best_distance = float('inf')
                next_hop = None

                if isinstance(routes, dict):  # Ensure routes is a dictionary
                    for neighbor_router_id, distance in routes.items():
                        if neighbor_router_id == router_id:
                            continue

                        if distance < best_distance:
                            best_distance = distance
                            next_hop = neighbor_router_id

                    if next_hop != self.routing_table[destination_ip]:
                        self.routing_table[destination_ip] = next_hop
                        updated = True
                else:
                    # Handle the case when routes is not a dictionary (e.g., if it's a string)
                    # Add appropriate error handling or debug statements
                    pass

            if not updated:
                break

    def forward_data(self, sender, receiver, data):
        print("Data transmission initiated from", sender.id, "to", receiver.id)

        if receiver.ip not in self.forwarding_table.keys():
            print("Destination IP is not in the forwarding table.")
            return

        next_hop = self.forwarding_table[receiver.ip]
        print("Next hop:", next_hop)

        if next_hop == "local":
            print("Data reached the destination:", receiver.ip)
        else:
            next_hop_device = None
            for device in network.devices:
                if isinstance(device, Router) and device.ip == next_hop:
                    next_hop_device = device
                    break

            if next_hop_device is None:
                print("Next hop device not found.")
                return

            if isinstance(sender, Hub):
                # Forward data from the hub to the next hop device directly
                print("Data transmitted from", sender.id, "to", next_hop_device.id)
                print("Data:", data)
                print("Sender waiting for ACK from", next_hop_device.id)
                time.sleep(2)  # Simulating delay in receiving ACK
                print("ACK received from", next_hop_device.id)
                print("Transmission completed between", sender.id, "and", next_hop_device.id)
            else:
                path = network.find_shortest_path(sender, next_hop_device)
                if not path:
                    print("No valid path to the next hop device.")
                    return

                for i in range(len(path) - 1):
                    current_device = path[i]
                    next_device = path[i + 1]
                    connection = network.connections[(current_device, next_device)]
                    print("Data transmitted from", current_device.id, "to", next_device.id)
                    print("Data:", data)
                    print("Sender waiting for ACK from", next_device.id)
                    time.sleep(2)  # Simulating delay in receiving ACK
                    print("ACK received from", next_device.id)
                    print("Transmission completed between", current_device.id, "and", next_device.id)

                self.forward_data(next_hop_device, receiver, data)

class Network:
    def __init__(self):
        self.devices = []
        self.connections = {}

    def add_device(self, device):
        self.devices.append(device)

    def create_connection(self, sender, receiver):
        connection = Connection(sender, receiver)
        self.connections[(sender, receiver)] = connection
        self.connections[(receiver, sender)] = connection

    def assign_ipv4_addresses(self):
        num_devices = len(self.devices)
        network_address_1 = 192
        network_address_2 = 168
        network_address_3 = 0
        network_address_4 = 0
        subnet_bits = 24

        host_bits = 32 - subnet_bits
        num_hosts = 2 ** host_bits - 2

        if num_hosts < num_devices:
            print("Insufficient IP addresses for the number of devices.")
            return

        assigned_ips = 0

        for device in self.devices:
            if isinstance(device, Switch) or isinstance(device, Hub) or isinstance(device, Bridge):
                continue

            while True:
                ip_address = f"{network_address_1}.{network_address_2}.{network_address_3}.{network_address_4}"
                network_address_4 += 1

                if network_address_4 == 256:
                    network_address_3 += 1
                    network_address_4 = 0

                if network_address_3 == 256:
                    network_address_2 += 1
                    network_address_3 = 0

                if network_address_2 == 256:
                    network_address_1 += 1
                    network_address_2 = 0

                if assigned_ips >= num_hosts:
                    print("Insufficient IP addresses for the number of devices.")
                    return

                if ip_address not in [dev.ip for dev in self.devices]:
                    device.ip = ip_address
                    assigned_ips += 1
                    print("Device", device.id, "assigned IP address:", device.ip)
                    break


    def connect_devices(self, device1, device2):
        self.create_connection(device1, device2)

    def print_network_details(self):
        print("---------------")
        print("Network Devices:")
        for device in self.devices:
            print("Device Name:",device.__class__.__name__)
            print("Device ID:", device.id)
            print("Device MAC:", device.mac)
            print("Device IP:", device.ip)
            print("---------------")
            print()

    def find_shortest_path(self, source, destination):
        queue = [(0, source, [])]
        visited = set()

        while queue:
            cost, current, path = heapq.heappop(queue)
            if current == destination:
                return path + [current]

            if current in visited:
                continue

            visited.add(current)

            for neighbor in self.get_neighbors(current):
                if isinstance(current, Router) and isinstance(neighbor, Router):
                    next_hop = current.routing_table.get(destination.ip)
                    if next_hop and next_hop != current.id:
                        for router in self.devices:
                            if isinstance(router, Router) and router.id == next_hop:
                                next_router = router
                                break
                        else:
                            continue
                        cost += 1
                        heapq.heappush(queue, (cost, next_router, path + [current]))
                    continue

                heapq.heappush(queue, (cost + 1, neighbor, path + [current]))

        return []


    def get_neighbors(self, device):
        neighbors = []

        for connection in self.connections.values():
            if connection.sender == device:
                neighbors.append(connection.receiver)

        return neighbors

    def transmit_data_stop_and_wait(self, sender, receiver, data):
        print("Stop-and-Wait Data Transmission")
        print("------------------------------")
        print("Data transmission initiated from", sender.id, "to", receiver.id)
        print("Data:", data)
        print("Sender waiting for ACK from", receiver.id)
        time.sleep(2)  # Simulating delay in receiving ACK
        print("ACK received from", receiver.id)
        print("Data transmission completed from", sender.id, "to", receiver.id,"\n")

    def transmit_data_sliding_window(self, sender, receiver, data, window_size):
        print("Sliding Window Data Transmission")
        print("--------------------------------")
        print("Data transmission initiated from", sender.id, "to", receiver.id)
        print("Data:", data)
        print("Sender waiting for ACK from", receiver.id)
        time.sleep(2)  # Simulating delay in receiving ACK
        print("ACK received from", receiver.id)
        print("Data transmission completed from", sender.id, "to", receiver.id,"\n")


# Example usage

network = Network()

# Create two hubs
hub1 = Hub()
hub2 = Hub()
network.add_device(hub1)
network.add_device(hub2)

# Create two switches
switch1 = Switch()
switch2 = Switch()
network.add_device(switch1)
network.add_device(switch2)

# Create two routers
router1 = Router()
router2 = Router()
network.add_device(router1)
network.add_device(router2)

# Create six end devices
end_device1 = Device()
end_device2 = Device()
end_device3 = Device()
end_device4 = Device()
end_device5 = Device()
end_device6 = Device()
network.add_device(end_device1)
network.add_device(end_device2)
network.add_device(end_device3)
network.add_device(end_device4)
network.add_device(end_device5)
network.add_device(end_device6)

# Connect devices
network.connect_devices(hub1, end_device1)
network.connect_devices(hub1, end_device2)
network.connect_devices(hub1, end_device3)
network.connect_devices(switch1, hub1)
network.connect_devices(switch1, router1)
network.connect_devices(router1, router2)
network.connect_devices(router2, switch2)
network.connect_devices(switch2, hub2)
network.connect_devices(hub2, end_device4)
network.connect_devices(hub2, end_device5)
network.connect_devices(hub2, end_device6)

# Assign IP addresses
network.assign_ipv4_addresses()

network.print_network_details()

# Update routing table and forwarding table for routers
router1.add_route("192.168.0.3", "192.168.0.3")
router1.add_route("192.168.0.1", "192.168.0.1")  # Route to connected network
router1.add_route("192.168.0.7", "192.168.0.1")
router1.update_forwarding_table({"192.168.0.3": "eth1", "192.168.0.1": "eth0", "192.168.0.0": "local"})
router2.add_route("192.168.0.2", "192.168.0.0")
router2.add_route("192.168.0.1", "192.168.0.1")  # Route to connected network
router2.update_forwarding_table({"192.168.0.2": "eth0", "192.168.0.1": "eth1", "192.168.0.0": "local"})

# Example data transmission
sender_device = end_device6
receiver_device = end_device1
data_to_transmit = "Hello, World!"
window_size = 2

network.transmit_data_stop_and_wait(sender_device, receiver_device, data_to_transmit)
network.transmit_data_sliding_window(sender_device, receiver_device, data_to_transmit, window_size)

# Perform distance-vector routing
router1.perform_distance_vector_routing()
router2.perform_distance_vector_routing()

print("Router 1 Routing Table:")
print(router1.routing_table)
print("Router 2 Routing Table:")
print(router2.routing_table)

# Forward data using the routing tables
router1.forward_data(sender_device, receiver_device, data_to_transmit)

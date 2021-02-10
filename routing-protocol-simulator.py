"""
Creator: Sonja Ek
Created: 1.3.2020
This is a text-based routing protocol simulator. The program allows
downloading router data from a CVS file as well as adding new data manually.
Each router in the simulated network is represented by a Router-object and
interacts with other routers according to the commands that it receives as user
input.
"""


class Router:
    """
    Creates objects which represent individual routers in a network.
    """

    def __init__(self, name):
        self.__name = name
        self.__neighbours = []  # neighbours' names in string format
        self.__routingtable = {}  # connected networks corresponding distances

    def get_neighbours(self):
        """
        Returns the router's known neighbours. Needed in the main function.
        :return: routers found on the current router object's __neighbours-list
        """
        return self.__neighbours

    def print_info(self):
        """
        Prints all the known routers, their routing tables and known neighbours.
        """
        print(" ", self.__name)

        if self.__neighbours:
            print("    N:", ", ".join(sorted(self.__neighbours)))
        else:
            print("    N:")

        if self.__routingtable:
            print("    R:", ", ".join('{}:{}'.format(key, value) for key, value
                                      in sorted(self.__routingtable.items())))
        else:
            print("    R:")

    def add_neighbour(self, neighbour):
        """
        Adds a new neighbour's name as a string to the router's info.
        :param neighbour: the neighbour to be added, in object-format
        """
        self.__neighbours.append(neighbour.__name)

    def add_network(self, network, distance):
        """
        Adds new network info to the router's routing table.
        :param network: name of the network to be added
        :param distance: how many hops away the new network is from the router
        """
        self.__routingtable[network] = distance

    def receive_routing_table(self, sender):
        """
        Receive network info from a neighbouring router.
        :param sender: the neighbour (as a Router-object) to fetch info from
        """
        received_rt = sender.__routingtable  # Fetch the sender's routing table.
        for info in received_rt:
            if info not in self.__routingtable:
                # Network name and its distance to the router is will now be
                # added to the routing table. The distance will be one hop more
                # than it was in the sending router's routing table.
                self.__routingtable[info] = str(int(received_rt[info]) + 1)

    def has_route(self, network):
        """
        Provides info on whether the router is connected to a certain network
        and, if so, how many hops away it is.
        :param network: the network we're interested in
        """
        if network in self.__routingtable:
            distance = self.__routingtable[network]

            if distance == "0":
                print("Router is an edge router for the network.")
            else:
                print("Network", network, "is", distance, "hops away")
        else:
            print("Route to the network is unknown.")


def main():

    routers = {}  # router names and the Router-objects connected to them.
    ask_commands = True
    routerfile = input("Network file: ")

    if routerfile != "":
        try:
            file = open(routerfile, "r")
            neighbour_dict = {}  # This dict will temporarily hold information
                                 # about each router's neighbours.
            for row in file:
                pieces = row.rstrip().split("!")
                name = pieces[0]
                new_router = Router(name)  # A new Router-object is created.
                routers[name] = new_router  # The new Router-object is assigned
                                            # to the corresponding name key.
                if pieces[1] != "":
                    # Create a list containing names of neighbouring routers:
                    neighbours = pieces[1].split(";")
                    # The list of neighbours is assigned to the router's name
                    # so that the corresponding router objects can be added to
                    # the router's info later:
                    neighbour_dict[name] = neighbours
                if pieces[2] != "":
                    # Create a list containing a network name and its distance:
                    nw_elements = pieces[2].split(":")
                    new_router.add_network(nw_elements[0], nw_elements[1])

            # Next each Router-object gets its neighbours added to its info.
            for r in neighbour_dict:
                for n in neighbour_dict[r]:
                    routers[r].add_neighbour(routers[n])  # the parametre is a
                                                          # Router-object.
        except OSError:
            print("Error: the file could not be read or there is something "
                  "wrong with it.")
            ask_commands = False

    while ask_commands:
        command = input("> ")
        command = command.upper()

        if command == "P":  # Print the data of a certain router.
            routername = input("Enter router name: ")
            if routername in routers:
                routers[routername].print_info()
            else:
                print("Router was not found.")

        elif command == "PA":  # Print the data of all the routers.
            for router in routers:
                routers[router].print_info()

        elif command == "S":  # Make a router send it's routing table info.
            sender = input("Sending router: ")
            if sender in routers:
                # Receive a list of the sender's neighbours:
                neighbours = routers[sender].get_neighbours()
                for n in neighbours:
                    # Each neighbour updates its own routing table:
                    routers[n].receive_routing_table(routers[sender])
            else:
                print("Router was not found.")

        elif command == "C":  # Add two routers as each other's neighbours.
            first = input("Enter 1st router: ")
            second = input("Enter 2nd router: ")

            if first and second in routers:
                # Now the Router-objects under the given names will add each
                # other on their list of neighbours.
                routers[first].add_neighbour(routers[second])
                routers[second].add_neighbour(routers[first])
            else:
                print("One or more of the routers was not found.")

        elif command == "RR":  # Ask whether a router knows a way to a network.
            router = input("Enter router name: ")
            network = input("Enter network name: ")
            routers[router].has_route(network)
            # The has_route -method takes care of printing the info.

        elif command == "NR":  # Create a new router.
            newname = input("Enter a new name: ")
            if newname not in routers:
                newrouter = Router(newname)  # Creates a new Router-object.
                # Adds the name of the new router and the Router-object in a dict
                # called "routers". Name is the key and the object is its value:
                routers[newname] = newrouter
            else:
                print("Name is taken.")

        elif command == "NN":  # Connect a router to a new network created here.
            routername = input("Enter router name: ")
            if routername in routers:
                network = input("Enter network: ")
                distance = input("Enter distance: ")
                # The Router-object under the given name calls its method to add
                # the new network info to its own routing table:
                routers[routername].add_network(network, int(distance))
            else:
                print("Router was not found.")

        elif command == "Q":  # Quit processing the file.
            print("Simulator closes.")
            return

        else:
            print("Erroneous command!")
            print("Enter one of these commands:")
            print("NR (new router)")
            print("P (print)")
            print("C (connect)")
            print("NN (new network)")
            print("PA (print all)")
            print("S (send routing tables)")
            print("RR (route request)")
            print("Q (quit)")


main()
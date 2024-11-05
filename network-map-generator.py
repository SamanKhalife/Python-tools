import matplotlib.pyplot as plt
import networkx as nx

def create_network_map(devices):
    G = nx.Graph()

    for device in devices:
        G.add_node(device['ip'], device_type=device.get('type', 'unknown'), status=device.get('status', 'active'))
        if 'connected_to' in device:
            G.add_edge(device['ip'], device['connected_to'], bandwidth=device.get('bandwidth', 'N/A'))

    colors = []
    sizes = []
    for node in G.nodes(data=True):
        if node[1]['device_type'] == 'router':
            colors.append('lightblue')
            sizes.append(700)
        elif node[1]['device_type'] == 'switch':
            colors.append('lightgreen')
            sizes.append(500)
        else:
            colors.append('gray')
            sizes.append(300)


    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True, node_color=colors, node_size=sizes, font_size=10, font_color='black')

    edge_labels = nx.get_edge_attributes(G, 'bandwidth')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

    plt.title("Network Map")
    plt.axis('off')
    plt.show()

    save_option = input("Do you want to save the network map as an image? (yes/no): ")
    if save_option.lower() == 'yes':
        plt.savefig("network_map.png", format="png")
        print("Network map saved as 'network_map.png'.")

devices = [
    {'ip': '192.168.1.1', 'type': 'router', 'status': 'active', 'connected_to': '192.168.1.2', 'bandwidth': '1Gbps'},
    {'ip': '192.168.1.2', 'type': 'switch', 'status': 'active', 'connected_to': '192.168.1.3', 'bandwidth': '1Gbps'},
    {'ip': '192.168.1.3', 'type': 'pc', 'status': 'inactive'}
]

create_network_map(devices)


import matplotlib.pyplot as plt
import networkx as nx


def plot_metrics(history):
    ticks = range(len(history))

    supply = [h["supply"] for h in history]
    burned = [h["burned"] for h in history]
    visit_load = [h["avg_visit_load"] for h in history]
    survival = [h["survival_rate"] for h in history]

    plt.figure()
    plt.plot(ticks, supply)
    plt.title("Total Supply Over Time")
    plt.xlabel("Tick")
    plt.ylabel("Supply")
    plt.show()

    plt.figure()
    plt.plot(ticks, visit_load)
    plt.title("Avg Visit Load")
    plt.xlabel("Tick")
    plt.ylabel("⤵️")
    plt.show()

    plt.figure()
    plt.plot(ticks, survival)
    plt.title("Survival Rate")
    plt.xlabel("Tick")
    plt.ylabel("Rate")
    plt.show()


def draw_graph(graph):
    pos = nx.spring_layout(graph)

    connectors = [n for n in graph.nodes if n.startswith("C")]
    nodes = [n for n in graph.nodes if n.startswith("N")]

    plt.figure()
    nx.draw_networkx_nodes(graph, pos, nodelist=connectors)
    nx.draw_networkx_nodes(graph, pos, nodelist=nodes)
    nx.draw_networkx_edges(graph, pos)

    plt.title("Social Graph")
    plt.show()


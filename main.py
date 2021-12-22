import torch
import bittensor as bt
import streamlit as st


@st.cache
def get_metagraph():
    metagraph = bt.metagraph(network="nakamoto")
    metagraph.sync()
    return metagraph


def main():
    metagraph = get_metagraph()

    st.title('Bittensor Network Summary')

    active_nodes = metagraph.active.sum()
    st.write('Number of active nodes: ', active_nodes.item())

    ranks = metagraph.ranks.data
    sorted_ranks, indices = torch.sort(ranks, descending=True)
    st.write('List of ranks: ')
    top_10 = sorted_ranks[:30]
    st.write(top_10)

    st.write(dir(metagraph))


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/

import torch
import pandas as pd
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
    sorted_ranks, sorted_indices = torch.sort(ranks, descending=True)
    st.write('Top 30 Bittensor nodes by rank:')
    top_30 = list(map(lambda x: x.item(), sorted_ranks[:30]))
    top_30_indices = list(map(lambda x: x.item(), sorted_indices[:30]))
    top_30_public_keys = list(map(lambda x: metagraph.hotkeys[x.item()], sorted_indices[:30]))
    top_30_df = pd.DataFrame(
        list(zip(top_30_public_keys, top_30)),
        index=top_30_indices,
        columns=['Public Key', 'Rank']
    )
    st.write(top_30_df)

    holdings = metagraph.stake.data
    sorted_holdings, sorted_indices = torch.sort(holdings, descending=True)
    st.write('Top 30 tao holders:')
    top_30_holdings = list(map(lambda x: x.item(), sorted_holdings[:30]))
    top_30_indices = list(map(lambda x: x.item(), sorted_indices[:30]))
    top_30_public_keys = list(map(lambda x: metagraph.hotkeys[x.item()], sorted_indices[:30]))
    top_30_holdings_df = pd.DataFrame(
        list(zip(top_30_public_keys, top_30_holdings)),
        index=top_30_indices,
        columns=['Public Key', 'Rank']
    )
    st.write(top_30_holdings_df)

    st.write(dir(metagraph))


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/

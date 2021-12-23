import torch
import pandas as pd
import bittensor as bt
import streamlit as st


@st.cache
def get_metagraph():
    metagraph = bt.metagraph(network="nakamoto")
    metagraph.sync()
    return metagraph


def get_top_n(t, n, name, hotkeys):
    t = t.data
    sorted_t, sorted_indices = torch.sort(t, descending=True)
    top_n = list(map(lambda value: value.item(), sorted_t[:n]))
    top_n_indices = list(map(lambda i: i.item(), sorted_indices[:n]))
    top_n_public_keys = list(map(lambda i: hotkeys[i], top_n_indices))
    top_n_df = pd.DataFrame(
        list(zip(top_n_public_keys, top_n)),
        index=top_n_indices,
        columns=['Public Key', name]
    )
    return top_n_df


def main():
    metagraph = get_metagraph()

    st.title('Bittensor Network Analytics')

    active_nodes = metagraph.active.sum()
    st.write('Number of active nodes: ', active_nodes.item())

    ranks = metagraph.ranks.data
    top_30_ranks = get_top_n(t=ranks, n=30, name='Rank', hotkeys=metagraph.hotkeys)
    st.write('Top 30 nodes by rank: ', top_30_ranks)

    holdings = metagraph.stake.data
    top_30_holders = get_top_n(t=holdings, n=30, name='Holdings', hotkeys=metagraph.hotkeys)
    st.write('Top 30 holders of tao: ', top_30_holders)

    dividends = metagraph.dividends.data
    top_100_dividend_receivers = get_top_n(t=dividends, n=100, name='Dividends', hotkeys=metagraph.hotkeys)
    st.write('Top 50 dividend receivers: ', top_100_dividend_receivers)

    st.write(dir(metagraph))


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/

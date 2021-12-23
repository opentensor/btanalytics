import torch
import pandas as pd
import bittensor as bt
import streamlit as st
import altair as alt
import matplotlib.pyplot as plt


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
    top_100_dividend_receivers = get_top_n(t=dividends, n=100, name='Dividend', hotkeys=metagraph.hotkeys)
    st.write('Top 100 dividend receivers: ', top_100_dividend_receivers)

    incentives = metagraph.incentive.data
    top_30_incentive_receivers = get_top_n(t=incentives, n=30, name='Incentive', hotkeys=metagraph.hotkeys)
    st.write('Top 30 incentive receivers: ', top_30_incentive_receivers)

    ranks = pd.DataFrame(ranks.numpy(), columns=['Rank'])
    incentives = pd.DataFrame(incentives.numpy(), columns=['Incentive'])
    holdings = pd.DataFrame(holdings.numpy(), columns=['Holdings'])
    dividends = pd.DataFrame(dividends.numpy(), columns=['Dividend'])
    hotkeys = pd.DataFrame(metagraph.hotkeys, columns=['Public Key'])
    combined_df = pd.concat([hotkeys, ranks, holdings, dividends, incentives], axis=1)
    combined_df['UID'] = combined_df.index
    # st.write(combined_df)

    st.write('Dividends vs Holdings')
    min_holding, max_holding = st.slider("Min Holdings", 1, 100000), st.slider('Max Holdings', 1, 100000)
    combined_df = combined_df[combined_df.Holdings >= min_holding]
    combined_df = combined_df[combined_df.Holdings <= max_holding]
    c = alt.Chart(combined_df).mark_circle().encode(
        x='Holdings', y='Dividend',
    )
    st.altair_chart(c, use_container_width=True)

    fig, ax = plt.subplots()
    ax.scatter(combined_df['UID'], combined_df['Holdings'])
    ax.set_title('Holdings vs UID')
    st.pyplot(fig)

    fig, ax = plt.subplots()
    ax.scatter(combined_df['UID'], combined_df['Rank'])
    ax.set_title('Rank vs UID')
    st.pyplot(fig)

    fig, ax = plt.subplots()
    ax.scatter(combined_df['UID'], combined_df['Dividend'])
    ax.set_title('Dividend vs UID')
    st.pyplot(fig)


if __name__ == '__main__':
    main()

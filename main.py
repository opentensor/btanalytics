import torch
import pandas as pd
import bittensor as bt
import streamlit as st
import seaborn as sns
import numpy as np
import altair as alt
import matplotlib.pyplot as plt

# Turn off console because it doesnt play with
# streamlit
try:
    bt.__use_console__ = False
except:
    pass

@st.cache
def get_metagraph():
    metagraph = bt.metagraph(network="nakamoto")
    metagraph.sync()
    return metagraph

def metagraph_to_dataframe(metagraph):
    index = metagraph.uids.tolist()
    columns = [ 'uid', 'active', 'stake', 'rank', 'trust', 'consensus', 'incentive', 'dividends', 'emission']
    df = pd.DataFrame( columns = columns, index = index )
    for uid in metagraph.uids.tolist():
        v = {
            'uid': metagraph.uids[uid].item(),
            'active': metagraph.active[uid].item(),             
            'stake': metagraph.stake[uid].item(),             
            'rank': metagraph.ranks[uid].item(),            
            'trust': metagraph.trust[uid].item(),             
            'consensus': metagraph.consensus[uid].item(),             
            'incentive': metagraph.incentive[uid].item(),             
            'dividends': metagraph.dividends[uid].item(),             
            'emission': metagraph.emission[uid].item()
        }
        df.loc[uid] = pd.Series( v )
    df['uid'] = df.index
    return df

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
    print (metagraph)
    df = metagraph_to_dataframe(metagraph)

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

    markers = {1: "s", 0: "X"}
    fig, ax = plt.subplots(figsize=(20, 5))
    ax.set_title('Stake')
    sns.scatterplot(
        data = df, 
        x = "uid", 
        y = "stake", 
        size = "stake",
        hue = 'stake',
        hue_norm = (0, 1000), 
        style = "active", 
        markers = markers
    )
    st.pyplot(fig)

    markers = {1: "s", 0: "X"}
    fig, ax = plt.subplots(figsize=(20, 5))
    ax.set_title('Rank')
    sns.scatterplot(
        data = df, 
        x = "uid",
        y = "rank",
        size = "consensus", 
        hue = 'incentive', 
        style = "active", 
        markers = markers
    )
    st.pyplot(fig)

    markers = {1: "s", 0: "X"}
    fig, ax = plt.subplots(figsize=(20, 5))
    ax.set_title('Incentive')
    sns.scatterplot(
        data = df, 
        x = "uid",
        y = "incentive",
        size = "rank",
        hue = 'stake', 
        hue_norm = (0, 1000), 
        style = "active", 
        markers = markers
    )
    st.pyplot(fig)

    markers = {1: "s", 0: "X"}
    fig, ax = plt.subplots(figsize=(20, 5))
    ax.set_title('Trust')
    sns.scatterplot(
        data = df, 
        x = "uid", 
        y = "trust", 
        size = "rank",
        hue = 'stake',
        hue_norm = (0, 1000), 
        style = "active", 
        markers = markers
    )
    st.pyplot(fig)

    markers = {1: "s", 0: "X"}
    fig, ax = plt.subplots(figsize=(20, 5))
    ax.set_title('Consensus')
    sns.scatterplot (
        data = df, 
        x = "uid", 
        y = "consensus", 
        size = "rank", 
        hue = 'stake', 
        hue_norm = (0, 1000), 
        style = "active", 
        markers = markers
    )
    st.pyplot(fig)

    markers = {1: "s", 0: "X"}
    fig, ax = plt.subplots(figsize=(20, 5))
    ax.set_title('Dividends')
    sns.scatterplot(
        data = df, 
        x = "uid", 
        y = "dividends", 
        size = "stake", 
        hue = 'stake', 
        hue_norm = (0, 1000), 
        style = "active", 
        markers = markers
    )
    st.pyplot(fig)

    markers = {1: "s", 0: "X"}
    fig, ax = plt.subplots(figsize=(20, 5))
    ax.set_title('Emission')
    sns.scatterplot(
        data = df, 
        x = "uid", 
        y = "emission", 
        size = "rank",
        hue = 'stake',
        hue_norm = (0, 1000), 
        style = "active", 
        markers = markers
    )
    st.pyplot(fig)

    fig, ax = plt.subplots(figsize=(15, 15))
    ax.set_title('Weights')
    sns.heatmap(
        metagraph.W.numpy(),
        vmin=0, vmax=np.mean(metagraph.W.numpy()), center=0
    )
    st.pyplot(fig)

    fig, ax = plt.subplots(figsize=(15, 15))
    ax.set_title('Bond Ownership')
    sns.heatmap(
        metagraph.B.numpy(),
        vmin=0, vmax=2*np.mean(metagraph.B.numpy()), center=0
    )
    st.pyplot(fig)


if __name__ == '__main__':
    main()

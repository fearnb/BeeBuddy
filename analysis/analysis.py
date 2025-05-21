import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import mannwhitneyu, wilcoxon, shapiro
import numpy as np

if __name__ == "__main__":
    # Note that code for charts needs to be commented and uncommented as appropriate

    df = pd.read_json("./data/bees.json")
    species_count = df['species'].value_counts().rename_axis('species').to_frame('counts')
    species_count.reset_index(level=0, inplace=True)
    # sns.barplot(species_count, x='species', y='counts')
    # plt.xticks(rotation=-40)
    # plt.show()

    # count the number of short and long hops a bee has done
    def get_hop_count(hops):
        short = 0
        long = 0
        for hop in hops:
            if hop['type'] == 's':
                short = short + 1
            else:
                long = long + 1
        return {
            'short' : short,
            'long' : long
        }
    
    # Accessors because I don't know if you can access individual variables when using apply
    def get_short_count(hops):
        counts = get_hop_count(hops)
        return counts['short']

    def get_long_count(hops):
        counts = get_hop_count(hops)
        return counts['long']
    
    def get_total_count(hops):
        counts = get_hop_count(hops)
        return counts['short'] + counts['long']
    
    def get_difference(hops):
        counts = get_hop_count(hops)
        return counts['short'] - counts['long']

    # 'c' stands for count
    df['c_short'] = df['hops'].apply(get_short_count)
    df['c_long'] = df['hops'].apply(get_long_count)
    df['c_total'] = df['hops'].apply(get_total_count)
    df['c_diff'] = df['hops'].apply(get_difference)

    #dataframe of short and long counts to vis means
    counts_df = df.filter(['id','c_short','c_long'], axis=1)
    counts_df.rename(columns={'c_short':'short', 'c_long':'long'}, inplace=True)
    counts_df = counts_df.melt(id_vars = 'id', value_vars=['short', 'long'], var_name='hop_type', value_name='count')
    # sns.barplot(data=counts_df, x='hop_type', y='count')
    # plt.show()

    # change the data used for x to look at short/long counts and difference
    sns.histplot(data=df, x="c_diff", kde=True)
    # Only have one plot show method called!
    plt.show() 

    # Look at the mean of each type of hop
    short_mean = (df['c_short'].sum()/df['c_short'].count())
    long_mean = (df['c_long'].sum()/df['c_long'].count())
    means = {
        'condition' : ['short', 'long'],
        'mean' : [short_mean, long_mean]
    }

    means_df = pd.DataFrame(data = means)
    # sns.barplot(data=means_df, x='condition', y='mean')
    # plt.show()
    print("Means:")
    print(f"Short: {short_mean}")
    print(f"Long: {long_mean}")
    print("-------------")
    print(" ")

    reject = 0.05

    # Null hypothesis of this test is that they are normally distributed
    # So counter-intuitively we want to see a big p value so we don't reject the null hypothesis
    shap_short = shapiro(df['c_short'])
    print("Short count is normally distributed:")
    print(f"Statistic: {shap_short.statistic}")
    print(f"p-value: {shap_short.pvalue}")
    shap_long = shapiro(df['c_long'])
    print("Long count is normally distributed:")
    print(f"Statistic: {shap_long.statistic}")
    print(f"p-value: {shap_long.pvalue}")
    shap_diff = shapiro(df['c_diff'])
    print("Difference count is normally distributed:")
    print(f"Statistic: {shap_diff.statistic}")
    print(f"p-value: {shap_diff.pvalue}")
    print("-------------")
    print(" ")

    # Not a great test to use since data is paired, but I'm not meant to know about Wilcoxon yet
    U1, p = mannwhitneyu(df['c_short'], df['c_long'])
    nx, ny = df['c_short'].count(), df['c_long'].count()
    U2 = nx*ny - U1
    z = (U1 - nx*ny/2 + 0.5) / np.sqrt(nx*ny * (nx + ny + 1)/ 12)
    print("Mann-Whit U results:")
    print(f"U1: {U1}")
    print(f"U2: {U2}")
    print(f"z: {z}")
    print(f"p: {p}")
    if p <= reject:
        print("Reject the null!")
    else:
        print("Accept the null!")
    print("-------------")
    print(" ")

    # The actual correct test to use, this shows whether there is a difference
    wilcoxon_res = wilcoxon(df['c_diff'])
    print("Wilcoxon results:")
    print(f"Short median: {df['c_short'].median()}")
    print(f"Long median: {df['c_long'].median()}")
    print(f"Statistic: {wilcoxon_res.statistic}")
    print(f"p: {wilcoxon_res.pvalue}")
    if wilcoxon_res.pvalue <= reject:
        print("Reject the null!")
    else:
        print("Accept the null!")
    print("-------------")
    print(" ")

    # Checking that the directionality (more short hops than long)
    wilcoxon_greater = wilcoxon(df['c_diff'], alternative='greater')
    print("Wilcoxon greater results:")
    print(f"Statistic: {wilcoxon_greater.statistic}")
    print(f"p: {wilcoxon_greater.pvalue}")
    if wilcoxon_greater.pvalue <= reject:
        print("Reject the null!")
    else:
        print("Accept the null!")
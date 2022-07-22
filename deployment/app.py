import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

st.set_page_config(
    page_title="Milestone 1 - Ivan Yapputra Yappi",
    layout="wide",
    initial_sidebar_state="expanded"
)
st.set_option('deprecation.showPyplotGlobalUse', False)

# Function get csv


def get_data():
    temp = pd.read_csv("../h8dsft_Milestone1_TheLook_Ecommerce.csv")
    temp.dropna(inplace=True)
    temp.rename(columns={
        "name": "product_name",
        "category": "product_category",
        "brand": "product_brand",
        "cost": "product_cost",
        "distribution_name": "distribution",
        "id": "user_id",
        "num_of_item": "quantity"
    }, inplace=True)
    temp['income'] = (temp['sale_price'] -
                      temp['product_cost']) * temp['quantity']

    temp["created_at"] = pd.to_datetime(temp["created_at"])
    temp['created_at'] = temp.created_at.dt.date
    temp["created_at"] = pd.to_datetime(temp["created_at"])
    return temp

# End Function get csv


thelook = get_data()

st.sidebar.title('Navigation')
selected = st.sidebar.selectbox(
    'Select Page:', ['Visualisasi', 'Statistical Analysis'])

if selected == 'Visualisasi':
    st.markdown(
        "<h1 style='text-align: center;'>Visualization Dashboard `The Look`</h1>",
        unsafe_allow_html=True)

    with st.expander("About Dataset"):
        if st.checkbox("Show Dataset"):
            st.write(thelook)
        st.write(
            """
        Dataset ini berisi 181.657 baris dengan 15 kolom. Berikut adalah keterangan dari kolom pada dataset:

        | Feature                 | Description                                                                                                                                                    |
        | ----------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------- |
        | create_at               | Tanggal customer order produk                                                                                                                                  |
        | product_name            | Nama produk                                                                                                                                                    |
        | product_category        | Kategori produk                                                                                                                                                |
        | product_brand           | Brand produk                                                                                                                                                   |
        | product_cost            | Harga pembuatan produk                                                                                                                                         |
        | distribution            | Pendistribusian produk / nama merchant yang menyimpan produk                                                                                                   |
        | department              | Departemen berdasarkan gender                                                                                                                                  |
        | sale_price              | Harga jual produk kepada customer                                                                                                                              |
        | user_id                 | Id user / customer                                                                                                                                             |
        | gender                  | Jenis kelamin customer                                                                                                                                         |
        | age                     | Umur customer                                                                                                                                                  |
        | country                 | Negara customer berasal                                                                                                                                        |
        | quantity                | Jumlah pembelian produk                                                                                                                                        |
        | status                  | Status pembelian produk                                                                                                                                        |
        | traffic_source          | Sumber iklan                                                                                                                                                   |
        """
        )

    ### Area Chart ###
    areaplot = px.area(
        thelook.groupby(thelook.created_at).income.mean(),
        labels={"created_at": "Tanggal", "value": "Pendapatan kotor"},
        title="Rata-rata pendapatan kotor dalam sehari",
    )
    areaplot.update_layout(hovermode="x")
    areaplot.update_traces(
        hovertemplate="Average Gross Income: %{y:$.2f}<extra></extra>"
    )
    st.plotly_chart(areaplot, use_container_width=True)
    with st.expander("Insight:"):
        st.write("Dari grafik diatas dapat dilihat beberapa bulan pada awal tahun 2019 pendapatan rata-rata toko `the look` mengalami kenaikan yang cukup tinggi, pada awal tahun 2020 sampai tahun 2022 rata-rata pendapatan toko `the look` mengalami penurunan, dan pada bulan juli 2022 rata-rata pendapatan toko `the look` menunjukkan adanya kenaikan.")

    ### Persentase Penjualan ###
    statusdf = thelook.groupby("status").size().reset_index(name="count")
    pieplotstatus = px.pie(
        statusdf, values="count", names="status", title="Persentase Status Penjualan The Look"
    )
    pieplotstatus.update_traces(hovertemplate="%{label}: %{value}x")
    st.plotly_chart(pieplotstatus, use_container_width=True)
    with st.expander("Insight:"):
        st.write("Dapat dilihat dari pie plot di atas bahwa persentase penjualan di toko `the look` dengan persentase paling tinggi adalah penjualan dengan status `Shipped` atau bisa dikatan produk sedang dikirim/dalam perjalanan menuju customer dan persentase paling rendah adalah penjualan dengan status `Returned` atau bisa dikatakan produk dikembalikan. Dapat dilihat juga persentase penjualan dengan status `Complete` atau berhasil terjual sebesar 24.9%, persentase penjualan dengan status `Processing` atau sedang diproses sebesar 20%, dan persentase penjualan dengan status `Cancelled` atau dibatalkan sebesar 15.2%.")

    ### Total penjualan berdasarkan merchant###
    barplot1 = px.bar(
        thelook.groupby('distribution').quantity.sum(),
        labels={"distribution": "Merchant", "value": "Quantity"},
        title="Jumlah Penjualan Berdasarkan Merchant",
    )
    barplot1.update_layout(
        xaxis=dict(
            tickmode="linear",
            tick0=10,
            dtick=1,
        )
    )
    barplot1.update_traces(
        hovertemplate="%{x}<br>%{y:$.2f}<extra></extra>")
    st.plotly_chart(barplot1, use_container_width=True)

    ### Rata-rata pendapatan kotornya ###
    barplot2 = px.bar(
        thelook.groupby('distribution').income.mean(),
        labels={"distribution": "Merchant", "value": "Quantity"},
        title="Rata-rata Pendapatan Kotor Berdasarakan Merchant",
    )
    barplot2.update_layout(
        xaxis=dict(
            tickmode="linear",
            tick0=10,
            dtick=1,
        )
    )
    barplot2.update_traces(
        hovertemplate="%{x}<br>%{y:$.2f}<extra></extra>")
    st.plotly_chart(barplot2, use_container_width=True)

    with st.expander("Insight:"):
        st.write("Dapat dilihat dari pie plot di atas merchant `Chicago IL` dan merchant `Memphis TN` adalah merchant dengan total penjualan paling tinggi sedangkan `Savannah GA` adalah merchant dengan total penjualan paling rendah, namun walaupun merchant `Charleston SC` memiliki total penjualan yang lebih tinggi dari merchant `Savannah GA`, merchant `Charleston SC` memiliki persentase pendapatan kotor yang paling rendah. Akan dilakukan sedikit explorasi data yang berkaitan dengan merchant `Chicago IL`.")

    ### Rata-rata pendapatan berdasarkan tanggal di merchant Chicago IL ###
    areaplot2 = px.area(
        thelook[(thelook.distribution == 'Chicago IL') & (
            thelook.status == 'Complete')].groupby(thelook.created_at).income.mean(),
        labels={"created_at": "Tanggal", "value": "Pendapatan"},
        title="Rata-rata pendapatan pada merchant Chicago IL",
    )
    areaplot2.update_layout(hovermode="x")
    areaplot2.update_traces(
        hovertemplate="Average Income: %{y:$.2f}<extra></extra>"
    )
    st.plotly_chart(areaplot2, use_container_width=True)
    st.write("Rata-rata penjualan tertinggi di merchant `Chicago IL` ini berada pada sekitar akhir tahun 2020 dengan rata-rata lebih dari $400.")

    ### Rata-rata pendapatan kotornya ###
    barplot3 = px.bar(
        thelook[(thelook.distribution == 'Chicago IL') & (
            thelook.status == 'Complete')].groupby(thelook.age).quantity.sum(),
        labels={"quantity": "Quantity", "value": "Quantity"},
        title="Usia customer di merchant Chicago IL",
    )
    barplot3.update_layout(
        xaxis=dict(
            tickmode="linear",
            tick0=10,
            dtick=1,
        )
    )
    barplot3.update_traces(
        hovertemplate="%{x}<br>%{y:$.2f}<extra></extra>")
    st.plotly_chart(barplot3, use_container_width=True)

    with st.expander("Insight:"):
        st.write("Diketahui bahwa customer pada usia 16 tahun di merchant `Chicago IL` yang paling banyak berbelanja total pembelian produknya lebih dari 250, usia 38 tahun dengan total pembelian lebih dari 200 produk, dan customer yang memiliki total pembelian produk paling rendah berada pada usia 70 tahun.")
elif selected == 'Statistical Analysis':
    st.markdown(
        "<h1 style='text-align: center;'>Statistical Analysis</h1>",
        unsafe_allow_html=True,
    )
    st.markdown(
        "<p style='text-align: center;'>Pada bagian ini berisi statistical analysis meliputi central tendency dan hipotesis testing.</p>",
        unsafe_allow_html=True,
    )
    st.markdown(
        "<h2 style='text-align: center;'>Central Tendency</h2>", unsafe_allow_html=True
    )
    st.write("""- Berapa nilai minimum, maksimum, mean, median, dan modus di toko `the look` berdasarkan quantity?""")
    df_complete = thelook.groupby(['status']).agg(Minimum=('quantity', np.min),
                                                  Maximum=('quantity', np.max),
                                                  Mean=('quantity', np.mean),
                                                  Median=(
                                                      'quantity', np.median),
                                                  Modus=('quantity', stats.mode))

    df_complete
    with st.expander("Insight:"):
        st.write("Diketahui bahwa status `Complete` merupakan status dengan nilai rata-rata paling tinggi berdasarkan `quantity` sedangkan status `Returned` atau produk yang dikembalikan merupakan status dengan nilai rata-rata terendah.")
    st.markdown(
        "<h2 style='text-align: center;'>Hypothesis Testing</h2>", unsafe_allow_html=True
    )
    st.write("""- Melakukan uji hipotesis untuk mengetahui apakah rata-rata penjualan produk dari merchant yang penjualan produknya tertinggi memiliki perbedaan signifikan dengan merchant yang penjualan produknya terendah?""")
    st.write("""
    Karena merchant `Chicago IL` adalah merchant dengan penjualan produk paling tinggi dan merchant `Savannah GA` adalah merchant dengan penjualan produk paling rendah, maka akan menggunakan two sample t-test dengan significant threshold sebesar 0.05:
    - Null Hypothesis (H0): μ Chicago IL = μ Savannah GA
    - Alternative Hypothesis (H1): μ Chicago IL != μ Savannah GA
    """)
    significant_threshold = 0.05
    chicago_qty = thelook[(thelook.distribution == 'Chicago IL') & (
        thelook.status == 'Complete')].groupby(thelook.created_at).quantity.sum()
    savannah_qty = thelook[(thelook.distribution == 'Savannah GA') & (
        thelook.status == 'Complete')].groupby(thelook.created_at).quantity.sum()
    tstat, pvalue = stats.ttest_ind(chicago_qty, savannah_qty)
    st.write("P-value ", pvalue)
    st.write("T-stat ", tstat)
    if st.checkbox("Show Visualization"):
        kol1, kol2, kol3 = st.columns([1, 3, 1])
        with kol2:
            plt.figure(figsize=(10, 6))
            chicago_pop = np.random.normal(
                chicago_qty.mean(), chicago_qty.std(), 10000)
            savannah_pop = np.random.normal(
                savannah_qty.mean(), savannah_qty.std(), 10000)
            ci = stats.norm.interval(
                0.95, loc=chicago_qty.mean(), scale=chicago_qty.std())
            sns.histplot(chicago_pop, bins=50, label='Chicago IL',
                         color='red', kde=True)
            sns.histplot(savannah_pop, bins=50,
                         label='Savannah GA', color='blue', kde=True)
            plt.axvline(x=chicago_qty.mean(), color='red',
                        label='Chicago IL mean')
            plt.axvline(x=savannah_qty.mean(), color='blue',
                        label='Savannah GA mean')
            plt.axvline(ci[1], color='green', linestyle='dashed',
                        linewidth=2, label='confidence threshold of 95%')
            plt.axvline(ci[0], color='green', linestyle='dashed', linewidth=2)
            plt.axvline(chicago_pop.mean()+tstat*chicago_pop.std(), color='black',
                        linestyle='dashed', linewidth=2, label='Alternative Hypothesis')
            plt.axvline(chicago_pop.mean()-tstat*chicago_pop.std(),
                        color='black', linestyle='dashed', linewidth=2)
            plt.axvline(
                x=ci[0], color="green", linestyle="--", label="Confidence Interval"
            )
            plt.axvline(x=ci[1], color="green", linestyle="--")
            plt.title('Chicago IL and Savannah GA population distribution')
            plt.xlabel('Quantity')
            plt.ylabel('Frequency')
            plt.legend()
            st.pyplot()
    with st.expander("Kesimpulan"):
        st.markdown(
            "<h3 style='text-align: center;'>H0 Rejected</h3>",
            unsafe_allow_html=True,
        )
        st.write(
            "Dari hasil uji hipotesis ini p-value kurang dari 0.05. Jadi pada uji hipotesis ini `H0 rejected`, maka disimpulkan bahwa perbedaan rata-rata penjualan pada merchant `Chicago IL` dan `Savannah GA` di toko `the look` ini signifikan."
        )

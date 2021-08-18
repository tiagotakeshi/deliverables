import folium
import pandas as pd
import streamlit as st
from folium.plugins import MarkerCluster
from streamlit_folium import folium_static
from geopy.geocoders import Nominatim
from sklearn.preprocessing import MinMaxScaler
from sklearn.cluster import DBSCAN
import numpy as np
import plotly.graph_objects as go

st.set_page_config(layout='wide')


@st.cache(allow_output_mutation=True)
def get_data(path):
    database = pd.read_csv(path, encoding='utf=16')

    return database


def final_df(database):
    database.drop_duplicates(inplace=True)
    auxiliar = database[['grade_id', 'climb_type', 'lat', 'long']]

    return auxiliar


def alg_dbscan(dataset_alg):
    scaler = MinMaxScaler()
    dataset_alg[['lat', 'long']].astype(float, errors='ignore')
    X = pd.DataFrame(scaler.fit_transform(dataset_alg.values), columns=dataset_alg.columns, index=dataset_alg.index)
    clustering = DBSCAN(eps=0.03, min_samples=10).fit(X)
    labels = clustering.labels_
    dataset_alg['cluster'] = labels

    return dataset_alg, labels


def header():
    st.image('header.png')
    st.title("A new way to find climbing spots")
    st.header("Welcome!")

    return None


def instructions():
    st.subheader("Please, to help you finding new climbing places, we need you to fill in some information after "
                 "reading this instructions:")

    st.text("We need a few informations about grades and location to show you some recomendations.\n\n"

            "Please, follow the steps below:\n\n"

            '1 - Check if the side bar is expanded, otherwise click in the icon ">" on the top in the rigth side\n\n'

            '2 - Select the Type of Climbing (Route or Boulder)\n\n'

            '3 - Inform the city where you want to discovery new climbing spots nearby. Follow the example below.\n'

            '    Ex: "City Name, Country" ; Ex. 2: "Pindamonhangaba, Brazil"\n\n'

            '4 - Select the difficult grade. The difficulties grades for Routes follows the French graduation, and the '
            'Boulder grades follows the USA graduation.\n\n'

            'If all the steps are clear then click on the Checkbox below to start:\n\n')

    check = st.checkbox(label="I Understanded all the steps")

    return check


def initial():
    header_container = st.container()
    form_container = st.expander(label="Instruction", expanded=True)

    with header_container:
        header()

    with form_container:

        check = instructions()

        return check


def sidebar(status, grades):

    if status:
        climbtype_selectbox = st.sidebar.selectbox(
            "Which modality would you like to search?",
            ("Route", "Boulder")
        )
        location = st.sidebar.text_input(label="City and Country: ")
        if climbtype_selectbox == 'Route':
            grade = st.sidebar.selectbox(label="Please, insert the difficult grade desired",
                                         options=['4b', '4c', '5a', '5b', '5c', '6a', '6a+', '6b',
                                                  '6b+', '6c', '6c+', '7a', '7a+', '7b', '7b+',
                                                  '7c', '7c+', '8a', '8a+', '8b', '8b+', '8c', '8c+',
                                                  '9a', '9a+'])
            grade_id = int(grades[grades['fra_routes'] == grade]['id'].head(1))
            climbtype = 0
        else:
            grade = st.sidebar.selectbox(label="Please, insert the difficult grade desired",
                                         options=['V0', 'V1', 'V2', 'V3', 'V3/V4', 'V4', 'V4/V5',
                                                  'V5', 'V5/V6', 'V6', 'V7', 'V8', 'V8/V9', 'V10',
                                                  'V11', 'V12', 'V13', 'V14', 'V15', 'V16'])
            grade_id = int(grades[grades['usa_boulders'] == grade]['id'].head(1))
            climbtype = 1
        sm = st.sidebar.checkbox("Show in Map")
        lr = st.sidebar.checkbox("Show the list result")
        ss = st.sidebar.checkbox("Show statistics")
        find = st.sidebar.button('Find')

        return location, climbtype, grade_id, sm, lr, ss, find


def button_find(find_status, loc, dfs):
    if find_status:
        with st.spinner('Wait for it...'):
            aux = []
            info = {}
            try:
                local = Nominatim(user_agent='climb_study').geocode(loc)
                info['lat'] = local.latitude
                info['long'] = local.longitude
            except:
                info['lat'] = 0
                info['long'] = 0
            aux.append(info)
            geo = pd.DataFrame(aux)
            user = {
                'grade_id': grade_id,
                'climb_type': climbtype,
                'lat': geo['lat'],
                'long': geo['long']
            }
            user_info = pd.DataFrame(user)
            df_user = dfs.append(user_info, sort=False)
            df_user.reset_index(inplace=True)
            df_user.drop(columns='index', inplace=True)

            aux, label = alg_dbscan(df_user)
            nro_cluster = int(aux.tail(1).cluster)

    return geo['lat'], geo['long'], nro_cluster, label


def maps(selected_cluster, lat, long):

    with st.expander(label="Show Map", expanded=True):
        density_map = folium.Map(location=[selected_cluster['lat'].mean(),
                                           selected_cluster['long'].mean()],
                                 tiles="OpenStreetMap",
                                 zoom_start=5)
        # location informed
        folium.Marker(
            location=[lat, long],
            popup="You Are Here!",
            icon=folium.Icon(color="green"),
        ).add_to(density_map)
        marker_cluster = MarkerCluster().add_to(density_map)
        for name, row in selected_cluster.iterrows():
            folium.Marker([row['lat'], row['long']],
                          popup='{0}'.format(row['name'])).add_to(marker_cluster)
        folium_static(density_map)

    return None


def lists(climb_type, selected_cluster):
    with st.expander(label="List Results", expanded=True):
        if climb_type == 0:
            st.dataframe(selected_cluster[['name', 'crag', 'city', 'grade_route']].sort_values(
                by="city"))
        else:
            st.dataframe(
                selected_cluster[['name', 'crag', 'city', 'grade_boulder']].sort_values(
                    by="city"))

    return None


def statistics(selected_cluster, climb_type):
    with st.expander(label="Statistical Results", expanded=True):
        st.subheader("Result: {0}".format(len(selected_cluster['name'])))
        if climb_type == 0:
            grade_name='grade_route'
        else:
            grade_name='grade_boulder'

        list_result = {"Grade(s) found": np.array(selected_cluster[grade_name].unique()),
                       "Quantity": np.array(selected_cluster[grade_name].value_counts())}
        st.dataframe(list_result)

        chart = selected_cluster[grade_name]
        qtd = np.array(chart.value_counts())
        trace = go.Bar(x=chart.value_counts().index, y=chart.value_counts(),
                       showlegend=False)
        layout = go.Layout(title="Quantity of Each Grade")
        da = [trace]
        fig = go.Figure(data=da, layout=layout)
        fig.update_traces(texttemplate=qtd, textposition='outside')
        fig.update_layout(xaxis_title="Grade(s)",
                          yaxis_title="Quantity of Grade")
        st.plotly_chart(fig, use_container_width=True)

    return None


def results(lat, long, n_cluster, labels, data, map_status, list_status, statistics_status, climb_type):
    if n_cluster == -1:
        st.error("We can't find any places to recommend! Try in another location.")

    else:
        labels = labels[0:-1]
        data['cluster'] = labels
        selected_cluster = dataset[dataset['cluster'] == n_cluster]
        if map_status:
            maps(selected_cluster, lat, long)

        if list_status:
            lists(climb_type, selected_cluster)

        if statistics_status:
            statistics(selected_cluster, climb_type)

        st.success('Done!')

    return None


if __name__ == '__main__':
    # ETL

    # Extraction
    dataset_path = 'dataset/final_climbing_dataset.csv'
    dataset = get_data(dataset_path)
    df = final_df(dataset)

    grades_path = 'dataset/final_grades_results.csv'
    grades = get_data(grades_path)

    # Transformation

    agreed_check = initial()
    if agreed_check:
        location, climbtype, grade_id, sm, lr, ss, find = sidebar(agreed_check, grades)
        if find:
            geo_lat, geo_long, cluster, label = button_find(find, location, df)

            # Loading

            results(geo_lat, geo_long, cluster, label, dataset, sm, lr, ss, climbtype)

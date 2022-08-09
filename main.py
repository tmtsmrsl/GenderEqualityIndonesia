# Import libraries
import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import geopandas as gpd
import requests
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Loading json file
r = requests.get('https://raw.githubusercontent.com/superpikar/indonesia-geojson/master/indonesia.geojson')
province_json = r.json()
geo_df = gpd.read_file("https://raw.githubusercontent.com/superpikar/indonesia-geojson/master/indonesia.geojson")

# Loading data 
df = pd.read_csv("unp_pro_df.csv")
color_list = px.colors.qualitative.Dark24[:]+px.colors.qualitative.Vivid[:]
color_dict = dict.fromkeys(df['Province'].unique())
n = 0
for province in color_dict:
    color_dict[province] = color_list[n]
    n += 1

# For visualization purpose, the null value for Kalimantan Utara population (2010-2014) will be backward filled.
df['Population'] = df['Population'].fillna(method='bfill')

# Website layout
st.set_page_config(layout="wide", page_title="⚥ Gender Equality in Indonesia", page_icon="⚥")
st.markdown("# ⚥ Gender Equality in Indonesia")
st.markdown("###### by Timotius Marselo ")
st.markdown("[Website](https://tmtsmrsl.github.io/) | [GitHub](https://github.com/tmtsmrsl) | [LinkedIn](https://www.linkedin.com/in/timotius-marselo//)")
tab1_1, tab1_2 = st.tabs(["Home", "Documentation"])

# Home tab
with tab1_1:
    st.markdown("### Introduction") 
    st.markdown("Equality of male and female participation in various aspects of life (e.g., health, economy, education, social, and politic) is very crucial to the success of country development. In order to achieve gender equality, there should be equal access, participation, control, and right in all sectors for both male and female. This allows both male and female to maximize their potential which will benefit both human and country development. However, some societies in Indonesia still have a patriarchal culture in which male have higher positions compared to female. In this article, we will explore the data regarding gender equality in Indonesia from 2010 to 2021, by evaluating two main indicators: Gender Development Index (GDI) and Gender Empowerment Measure (GEM).")
    st.markdown("---")
    st.markdown("### Gender Development Index and Related Measures")
    st.markdown("")
    
    col1_1, col1_2 = st.columns([2,3])
    with col1_1:
        st.markdown("**Human Development Index (HDI)** is an index that measures the dimensions of health (through life expectancy), education (through expected and average years of schooling) and standard of living (through income per capita). Due to data unavailability at the city level, income per capita is replaced by expenditure per capita to calculate HDI in Indonesia.")
        st.markdown("The HDI of both male and female have been increasing since 2010, which means the health, education and economic conditions in Indonesia are getting better each year. However, we can clearly see that there is a gap between male and female HDI in Indonesia.")
        st.markdown("The **Gender Development Index (GDI)** is the ratio between female HDI and male HDI. The overall trend for GDI is increasing in Indonesia, which means the gap between male and female HDI is narrowing. On 2021, the GDI value is 91.27 which means the value of female HDI is 0.91 times the value of male HDI.")
        
    with col1_2:
        # Create figure with secondary y-axis
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        # Add traces
        fig.add_trace(
            go.Bar(x=df.query('Province == "Indonesia"')['Year'], y=df.query('Province == "Indonesia"')['MaleHDI'], name="Male HDI", marker_color='dodgerblue', text=df.query('Province == "Indonesia"')['MaleHDI'], textposition='inside',hovertemplate ='%{y:.2f}'),
            secondary_y=False,
        )
        fig.add_trace(
            go.Bar(x=df.query('Province == "Indonesia"')['Year'], y=df.query('Province == "Indonesia"')['FemaleHDI'], name="Female HDI", marker_color='indianred', text=df.query('Province == "Indonesia"')['FemaleHDI'],textposition='inside', hovertemplate ='%{y:.2f}'),
            secondary_y=False,
        )
        fig.add_trace(
            go.Scatter(x=df.query('Province == "Indonesia"')['Year'], y=df.query('Province == "Indonesia"')['GDI'], name="GDI", marker_color='limegreen',),
            secondary_y=True,
        )

        # Set x-axis title
        fig.update_xaxes(title_text="Year")
        # Set y-axes titles
        fig.update_yaxes(title_text="Gender Development Index", secondary_y=True)
        fig.update_yaxes(title_text="Human Development Index", secondary_y=False)
        
        fig.update_traces(marker_line_color='black')
        fig.update_layout(barmode='group', height=500, width=900, hovermode='x unified',paper_bgcolor='honeydew', 
            plot_bgcolor='lavender', font_color='black', 
            title="<b>Male & Female Human Development Index and Gender Development Index in Indonesia (2010-2021)</b>")
        st.plotly_chart(fig,use_container_width=True)
    st.markdown("")
        
    col2_1, col2_2 = st.columns([2,3])
    with col2_1:
        st.markdown("")
        st.markdown("")
        st.markdown("")
        st.markdown("From the map, we can see that the overall GDI across all provinces is increasing from 2010 to 2021 (the intensity of red color is decreasing, while the intensity of blue color is increasing), which means the gap between female and male HDI is narrowing.")
        st.markdown("In 2021, Yogyakarta and Jakarta have the highest GDI, while Papua and Papua Barat have the lowest GDI. The GDI for Kalimantan region in 2021 is also relatively low. 15 provinces have a higher GDI than the national average GDI (91.27), while 19 provinces have a lower GDI than the national average GDI.")
        st.markdown("Keep in mind that the GDI value is not always correlated to the HDI value, a province may have a high GDI with low HDI (which means the HDI is equally low for both male and female).")
        
    with col2_2:
        tab2_1, tab2_2 = st.tabs(["Map (2010-2021)", "Bar Chart (2021)"])
        with tab2_1:
            fig = px.choropleth_mapbox(df, geojson=province_json, featureidkey='properties.state',
                        locations='Province', animation_frame='Year', range_color=(75,95),
                        color="GDI", color_continuous_scale='rdbu', hover_name='Province', 
                        zoom = 3.4, height=600, width=1000, hover_data={'Year':False, 'Province':False,},
                        mapbox_style="carto-positron", center = {
                            "lon": sum(geo_df.total_bounds[[0, 2]]) / 2,
                            "lat": sum(geo_df.total_bounds[[1, 3]]) / 2})
            fig.update_layout(margin={"l":0,"r":0,"t":60,"b":0}, paper_bgcolor='honeydew', font_color='black', 
                                title='<b>Gender Development Index by Province (2010-2021)</b>')
            last_frame_num = int(len(fig.frames) -1)
            fig.layout['sliders'][0]['active'] = last_frame_num
            fig = go.Figure(data=fig['frames'][last_frame_num]['data'], frames=fig['frames'], layout=fig.layout)
            st.plotly_chart(fig,use_container_width=True)
            
        with tab2_2:
            fig = px.bar(df.query('Year == 2021').sort_values('GDI', ascending=False), x='Province', y='GDI', 
                        orientation='v', title = "<b>Gender Development Index by Province (2021)</b>",height=600, width=800, 
                        color='GDI', color_continuous_scale='rdbu', range_color=(75,95),hover_name='Province', hover_data={'Province': False},)
            fig.update_traces(marker_line_color='black')
            fig.add_annotation(xref="x", yref="y", x=15, y=45, font_color='black', text="National Average", 
                            showarrow=False, textangle=-90)
            fig.update_layout(xaxis_tickangle=-90, paper_bgcolor='honeydew', plot_bgcolor='#e6e6e6', font_color='black',yaxis_title='Gender Development Index')
            st.plotly_chart(fig, use_container_width=True)
    st.markdown("")    
    
    col3_1, col3_2 = st.columns([2,3])
    with col3_1:
        st.markdown("**Life expectancy** is the average years a person is expected to live, which is based on the mortality rate at that time. The life expectancy for both male and female in Indonesia are increasing since 2010.")
        st.markdown("The life expectancy of female in all provinces are always higher compared to male. Some factors that cause female to live longer compared to male include lifestyle and genetic factors. Female has two X chromosomes while male has one X chromosome along with one Y chromosome. The additional X chromosome in female provides a protective effect which leads to a higher life expectancy. Besides that, female also has higher estrogen level which have antioxidant properties and can lower the rate of cardiovascular diseases.") 
        
    with col3_2:
        fig = px.scatter(df.query('Province != "Indonesia"'), x='MaleLE', y='FemaleLE', animation_frame='Year', animation_group='Province', color='Province', range_x=[60.5,75], range_y=[60.5,77.5], color_discrete_map=color_dict, height = 600, width = 700, title='<b>Female vs Male Life Expectancy by Province (2010-2021)</b><br>Bubble size based on population', size='Population', labels={'FemaleLE':'Female LE',"MaleLE":'Male LE', 'Population':'Pop'}, hover_name = 'Province',hover_data={'Year':False, 'Province':False,'Population':False})

        fig.update_layout(shapes = [{'type': 'line', 'yref': 'y', 'xref': 'x', 'y0': 1, 'y1': 100, 'x0': 1, 'x1':100, 'line_color':'lightgray', 'line_dash':'dot'}],paper_bgcolor='honeydew', plot_bgcolor='lavender', font_color='black',xaxis_title='Male Life Expectancy (Years)', yaxis_title='Female Life Expectancy (Years)')

        last_frame_num = int(len(fig.frames) -1)
        fig.layout['sliders'][0]['active'] = last_frame_num
        fig = go.Figure(data=fig['frames'][last_frame_num]['data'], frames=fig['frames'], layout=fig.layout)
        fig.update_traces(marker_sizemin=5, marker_sizeref=80000, marker_opacity=0.5, marker_line_color='black', marker_line_width=0.5)
        for frame in fig.frames:
            for data in frame.data:
                data.marker.sizemin=5
                data.marker.sizeref=80000
        st.plotly_chart(fig, use_container_width=True)
    st.markdown("")
        
    col4_1, col4_2 = st.columns([2,3])
    with col4_1:
        st.markdown("")
        st.markdown("")
        st.markdown("")
        st.markdown("**Expected schooling years** is the expected years of schooling for a 7-year-old child based on the current school enrollment rate, while **average schooling years** is the average years of schooling for population aged more than 25. Eexpected and average schooling years are steadily increasing for both male and female in Indonesia. Since 2010, the expected schooling years for female is always higher compared to male but the average for female is always lower compared to male.")
        st.markdown("Even though the average schooling years for female is always lower compared to male, the gap between them has been decreasing as shown in the line chart. If the higher expected schooling years for female can be maintained, the gap between male and female average schooling years will be closed in the coming years.")
        
    with col4_2:
        tab3_1, tab3_2 = st.tabs(["Bar Chart (2010-2021)", "Line Chart (2010-2021)"])
        with tab3_1:
            fig = make_subplots(rows=2,cols=1, subplot_titles=('<b>Expected Schooling Years in Indonesia (2010-2021)</b>', '<b>Average Schooling Years in Indonesia (2010-2021)</b>'), vertical_spacing=0.15)
            fig.add_trace(
                go.Bar(
                        name="Female",
                        x=df.query('Province == "Indonesia"')['Year'],
                        y=df.query('Province == "Indonesia"')['FemaleESY'],
                        offsetgroup=0,
                        marker_color="indianred",
                        legendgroup='group1',
                        text = df.query('Province == "Indonesia"')['FemaleESY'],
                        hovertemplate = '%{y:.2f}'),
                        row = 1, col = 1)
            fig.add_trace(
                go.Bar(
                        name="Male",
                        x=df.query('Province == "Indonesia"')['Year'],
                        y=df.query('Province == "Indonesia"')['MaleESY'],
                        offsetgroup=1,
                        marker_color="dodgerblue",
                        legendgroup='group2',
                        text = df.query('Province == "Indonesia"')['MaleESY'],
                        hovertemplate = '%{y:.2f}'),
                        row = 1, col =1)
            fig.add_trace(
                go.Bar(
                        name="Female",
                        x=df.query('Province == "Indonesia"')['Year'],
                        y=df.query('Province == "Indonesia"')['FemaleASY'],
                        offsetgroup=0,
                        marker_color="indianred",
                        showlegend=False,
                        legendgroup='group1',
                        text = df.query('Province == "Indonesia"')['FemaleASY'],
                        hovertemplate = '%{y:.2f}'),
                        row = 2, col = 1)
            fig.add_trace(
                go.Bar(
                        name="Male",
                        x=df.query('Province == "Indonesia"')['Year'],
                        y=df.query('Province == "Indonesia"')['MaleASY'],
                        offsetgroup=1,
                        marker_color="dodgerblue",
                        showlegend=False,
                        legendgroup='group2',
                        text = df.query('Province == "Indonesia"')['MaleESY'],
                        hovertemplate = '%{y:.2f}'),
                        row = 2, col = 1)
            fig.update_traces(marker_line_color='black')
            fig.update_layout(hovermode="x unified", yaxis_title="Expected Scooling Years", xaxis_title='Year', yaxis2_title = 'Average Schooling Years', xaxis2_title = 'Year', paper_bgcolor='honeydew', plot_bgcolor='lavender', font_color='black', height=700, margin={"t":50,"b":50})
            fig.layout.annotations[0].update(x=0.22)
            fig.layout.annotations[1].update(x=0.22)
            st.plotly_chart(fig, use_container_width=True)
        
        with tab3_2:
            fig = px.line(df.query('Province == "Indonesia"'), x='Year', y=(df.query('Province == "Indonesia"')['MaleASY']-df.query('Province == "Indonesia"')['FemaleASY']), height=600, title='<b>Difference Between Male and Female Average Schooling Years in Indonesia (2010-2021)</b>',)
            fig.update_layout(
                yaxis_title="Difference in Years (Male ASY - Female ASY)",paper_bgcolor='honeydew', plot_bgcolor='lavender', font_color='black')
            fig.update_traces(line_color='limegreen')
            fig.data[0].hovertemplate = '%{x}<br>Difference in Years=%{y} <extra></extra>'
            st.plotly_chart(fig, use_container_width=True)
    st.markdown("")
    
    col5_1, col5_2 = st.columns([2,3])
    with col5_1:
        st.markdown("In 2021, male have higher average schooling years than female in almost all provinces, which means on average male has longer years of education than female in those regions. In Papua Barat, male has significantly longer years of education compared to female. The only provinces where female has longer years of education are Gorontalo and Sulawesi Utara.")
        
    with col5_2:
        asy_diff_2021 = df.query('Year == 2021')[['Province','MaleASY','FemaleASY']]
        asy_diff_2021["ASY_diff"] = df.query('Year == 2021')['MaleASY']-df.query('Year == 2021')['FemaleASY']
        fig = px.bar(asy_diff_2021.sort_values('ASY_diff', ascending=False), x='ASY_diff', y='Province', title = "<b>Difference Between Male and Female Average Schooling Years by Province (2021)</b>",height=800, width=1000, color='ASY_diff', color_continuous_scale='darkmint', labels={'ASY_diff':'Difference in Years'}, hover_name='Province', hover_data={"Province":False, 'ASY_diff':':.2f'})
        fig.update_traces(marker_line_color='black')
        fig.update_layout(xaxis_title="Difference in Years (Male ASY - Female ASY)",paper_bgcolor='honeydew', plot_bgcolor='lavender', font_color='black')
        fig.add_vline(x=0, line_width=3, line_dash="dash", line_color="black")
        st.plotly_chart(fig, use_container_width=True)
    st.markdown("")
    
    col6_1, col6_2 = st.columns([2,3])
    with col6_1:
        st.markdown("")
        st.markdown("")
        st.markdown("")
        st.markdown("As mentioned earlier, HDI measures the standard of living dimension using **expenditure per capita** instead of income per capita. The trend of expenditure per capita in Indonesia is generally increasing from 2010 to 2021 for both male and female, but on 2020 it decreased probably due to the COVID pandemic. Male expenditure per capita is always significantly higher compared to female, which means there is huge gender inequality in the standard of living. This could be related to the income difference between male and female.")
        st.markdown("From 2010 to 2021, female expenditure per capita in all provinces are always lower than male. The further a point is from the linear line, the higher the gap (in ratio) between female and male expenditure per capita. Provinces with high inequality between male and female expenditure per capita in 2021 include Kalimantan Timur, Gorontalo, Bangka-Belitung, Kalimantan Selatan, and Riau.")
        
    with col6_2:
        tab4_1, tab4_2 = st.tabs(["Line Chart (2010-2021)", "Scatter Plot (2010-2021)"])
        with tab4_1:
            epc_df = df[['Province','Year','Population','MaleEPC','FemaleEPC']]
            epc_df[['MaleEPC','FemaleEPC']] = epc_df[['MaleEPC','FemaleEPC']].apply(lambda x: x/10e5)
            fig = px.line(epc_df.query('Province == "Indonesia"'), x='Year', y=['MaleEPC','FemaleEPC'], width=600, height=500, title='<b>Male & Female Expenditure per Capita in Indonesia (2010-2021)</b>', labels={'variable':'Gender'},)
            fig.data[0].hovertemplate = 'Male EPC=%{y:.2f}M<extra></extra>'
            fig.data[1].hovertemplate = 'Female EPC=%{y:.2f}M<extra></extra>'
            fig.update_layout(yaxis={'range':[6,18]},
                hovermode='x unified',
                yaxis_title="Expenditure Per Capita in Million IDR",paper_bgcolor='honeydew', plot_bgcolor='lavender', font_color='black',
                xaxis_tickangle=-45)
            for idx, name in enumerate(['Male','Female']):
                fig.data[idx].name = name
            st.plotly_chart(fig, use_container_width=True)
            
        with tab4_2:
            fig = px.scatter(epc_df.query('Province != "Indonesia"'), x='MaleEPC', y='FemaleEPC', animation_frame='Year', animation_group='Province', color='Province', color_discrete_map=color_dict, height = 600, width = 850, range_x=[2.8,24], range_y=[2.8,22], title='<b>Female vs Male Expenditure per Capita by Province (2010-2021)</b><br>Bubble size based on population',size='Population', labels={'FemaleEPC':'Female EPC',"MaleEPC":'Male EPC', 'Population':'Pop'}, hover_name = 'Province',hover_data={'Year':False, 'Province':False,'Population':False,})
            fig.update_layout(shapes = [{'type': 'line', 'yref': 'y', 'xref': 'x', 'y0': 1, 'y1': 24, 'x0': 1, 'x1': 24, 'line_color':'lightgray', 'line_dash':'dot'}], xaxis_title = 'Male Expenditure Per Capita in Million IDR', yaxis_title = 'Female Expenditure Per Capita in Million IDR', paper_bgcolor='honeydew', plot_bgcolor='lavender', font_color='black',)
            last_frame_num = int(len(fig.frames) -1)
            fig.layout['sliders'][0]['active'] = last_frame_num
            fig = go.Figure(data=fig['frames'][last_frame_num]['data'], frames=fig['frames'], layout=fig.layout)
            fig.update_traces(marker_sizemin=5, marker_sizeref=80000, marker_opacity=0.5, marker_line_color='black', marker_line_width=0.5)
            for frame in fig.frames:
                for data in frame.data:
                    data.marker.sizemin=5
                    data.marker.sizeref=80000
            custom_ht = '<b>%{hovertext}</b><br><br>Male EPC=%{x:.2f}M<br>Female EPC=%{y:.2f}M<extra></extra>'
            fig.update_traces(hovertemplate=custom_ht)
            for frame in fig.frames:
                for data in frame.data:
                    data.hovertemplate = custom_ht
            st.plotly_chart(fig, use_container_width=True)
    st.markdown("---")
    st.markdown("### Gender Empowerment Measure and Related Measures")
    st.markdown("")
    
    col7_1, col7_2 = st.columns([2,3])
    with col7_1:
        st.markdown("**Gender Empowerment Measure (GEM)** measures the participation of female in economic activities (through share of economic income), political activities (through involvement in parliament) and decision making (through involvement in professional positions). GEM value of 100 indicates that there is equal participation of male and female. The trend for GEM in Indonesia is increasing since 2010, with a drastic growth of GEM in 2019.")
    with col7_2:
        fig = px.line(df.query('Province == "Indonesia"'), x='Year', y='GEM', color="Province", color_discrete_map=color_dict, title='<b>Gender Empowerment Measure in Indonesia (2010-2021)</b>', hover_data={'Province':False})
        fig.update_layout(height = 500, paper_bgcolor='honeydew', 
            plot_bgcolor='lavender', font_color='black',)
        fig.update_traces(line_color='limegreen')
        fig.update_layout(showlegend=False,yaxis_title='Gender Empowerment Measure')
        st.plotly_chart(fig, use_container_width=True)
    st.markdown("")
    
    col8_1, col8_2 = st.columns([2,3])
    with col8_1:
        st.markdown("")
        st.markdown("")
        st.markdown("")
        st.markdown("From the map, we can see that the overall GEM for all provinces is increasing each year. (the intensity of red color is decreasing, while the intensity of blue color is increasing), which means there is increasing female participation in economic activities, parliament activities and decision-making across all provinces.")
        st.markdown("In 2021, there are only 4 provinces in which the GEM value is higher than the national average. This means gender empowerment is not yet spread evenly across all provinces.")
        
    with col8_2:
        tab5_1, tab5_2 = st.tabs(["Map (2010-2021)", "Bar Chart (2021)"])
        with tab5_1:
            fig = px.choropleth_mapbox(df, geojson=province_json, featureidkey='properties.state',
                        locations='Province', animation_frame='Year', range_color=(50,85),
                        color="GEM", color_continuous_scale='rdbu', hover_name='Province', 
                        zoom = 3.4, height=600, width=1000, hover_data={'Year':False, 'Province':False,},
                        mapbox_style="carto-positron", center = {
                            "lon": sum(geo_df.total_bounds[[0, 2]]) / 2,
                            "lat": sum(geo_df.total_bounds[[1, 3]]) / 2})
            fig.update_layout(margin={"l":0,"r":0,"t":60,"b":0}, paper_bgcolor='honeydew', font_color='black', 
                                title='<b>Gender Empowerment Measure by Province (2010-2021)</b>')
            last_frame_num = int(len(fig.frames) -1)
            fig.layout['sliders'][0]['active'] = last_frame_num
            fig = go.Figure(data=fig['frames'][last_frame_num]['data'], frames=fig['frames'], layout=fig.layout)
            st.plotly_chart(fig,use_container_width=True)
            
        with tab5_2:
            fig = px.bar(df.query('Year == 2021').sort_values('GEM', ascending=False), x='Province', y='GEM', 
                        orientation='v', title = "<b>Gender Empowerment Measure by Province (2021)</b>",height=600, width=800, 
                        range_color=(50,85), color="GEM", color_continuous_scale='rdbu', hover_name='Province', hover_data={'Province': False})
            fig.add_annotation(xref="x", yref="y", x=4, y=38, font_color='black', text="National Average", 
                            showarrow=False, textangle=-90)
            fig.update_layout(xaxis_tickangle=-90, paper_bgcolor='honeydew', plot_bgcolor='#e6e6e6', font_color='black',yaxis_title='Gender Empowerment Measure')
            fig.update_traces(marker_line_color='black')
            st.plotly_chart(fig, use_container_width=True)
    st.markdown("")
    
    col9_1, col9_2 = st.columns([2,3])
    with col9_1:
        st.markdown("")
        st.markdown("")
        st.markdown("")
        st.markdown("**Female share of income** is the indicator used by GEM to measure the participation of female in economic activities, and it measures the percentage of a country economic income that is earned by female population. According to the population census on 2020, there is roughly an equal number of female and male in Indonesia. So ideally, the female share of income should be around 50%.")
        st.markdown("Since 2010, female share of income in Indonesia is always lower compared to male share of income. This means female participation in economic activities is lower compared to male. Although the gap between female and male share of income is quite large, we can see that FSI has been slowly increasing each year. THe lower share of income for female is most likely related to the gender wage gap, which could be drived by difference in jobs or hours worked, difference in experience and also discrimination.")
        st.markdown("In 2021, only 5 provinces have a higher female share of income than the national average. This indicates a disparity in female economic participation between provinces.")
    with col9_2:
        tab6_1, tab6_2 = st.tabs(["Bar Chart (2010-2021)", "Bar Chart by Province (2021)"])
        with tab6_1:
            fig = px.bar(df.query('Province == "Indonesia"'), x='Year', y=['FemaleSI','MaleSI'],orientation='v', barmode='stack', title = "<b>Male and Female Share of Income in Indonesia (2010-2021)</b>",height=600, width=900, color_discrete_map={'MaleSI':'dodgerblue', 'FemaleSI':'indianred'}, labels={'variable':'Gender', 'value':'Share of Income (%)'}, text_auto=True)
            fig.update_layout(hovermode='x unified', paper_bgcolor='honeydew', plot_bgcolor='lavender', font_color='black',margin={"l":100,})
            fig.update_traces(marker_line_color='black', hovertemplate=None)
            fig.layout.yaxis.tickformat = ',.0%'
            for idx, name in enumerate(['Female','Male']):
                fig.data[idx].name = name
            st.plotly_chart(fig, use_container_width=True)
        with tab6_2:
            fig = px.bar(df.query('Year == 2021').sort_values('FemaleSI', ascending=False), x='Province', y='FemaleSI', 
                        orientation='v', title = "<b>Female Share of Income by Province (2021)</b>",height=600, width=800, 
                        color='FemaleSI', color_continuous_scale='rdbu', hover_name='Province', hover_data={'Province': False, 'FemaleSI':':,.1%'},labels={'FemaleSI':'FSI'})
            fig.add_annotation(xref="x", yref="y", x=5, y=0.18, font_color='black', text="National Average", 
                            showarrow=False, textangle=-90)
            fig.update_layout(xaxis_tickangle=-90, paper_bgcolor='honeydew', plot_bgcolor='#e6e6e6', font_color='black',margin={"l":100,}, yaxis_title='Female Share of Income')
            fig.layout.yaxis.tickformat = ',.0%'
            fig.update_coloraxes(colorbar_tickformat=',.0%')
            fig.update_traces(marker_line_color='black',)
            st.plotly_chart(fig, use_container_width=True)
    st.markdown("")
    
    col10_1, col10_2 = st.columns([2,3])
    with col10_1:
        st.markdown("")
        st.markdown("")
        st.markdown("")
        st.markdown("**Female involvement in parliament** is an important measure because it affects political decision-making. Female's aspirations would be better represented if female is empowered in political activities, which leads to better democracies.")
        st.markdown("In Indonesia, the parliaments are very male-dominated. This could be related to the patriarchal culture in Indonesia. Before 2019, less than 20% of the parliament seats are held by female. However, there's a significant increase of female involvement in parliament in 2019 due to the election period in 2018-2019, which also caused a notable increase of GEM in 2019.")
        st.markdown("In 2021, there are only 7 provinces in which the female involvement in parliament is higher than the national average. This means female participation in political activities is not yet evenly spread across all provinces. The representation of female in parliament across all provinces should be increased to ensure that the interests and needs of both genders are fulfilled.")
    with col10_2:
        tab7_1, tab7_2 = st.tabs(["Bar Chart (2010-2021)", "Bar Chart by Province (2021)"])
        with tab7_1:
            fig = px.bar(df.query('Province == "Indonesia"'), x='Year', y=['FemaleIP','MaleIP'],orientation='v', barmode='stack', title = "<b>Male and Female Involvement in Parliament in Indonesia (2010-2021)</b>",height=600, width=900, color_discrete_map={'MaleIP':'dodgerblue', 'FemaleIP':'indianred'}, labels={'variable':'Gender', 'value':'Involvement in Parliament (%)'}, text_auto=True)
            fig.update_layout(hovermode='x unified', paper_bgcolor='honeydew', plot_bgcolor='lavender', font_color='black',margin={"l":100,})
            fig.update_traces(marker_line_color='black', hovertemplate=None)
            fig.layout.yaxis.tickformat = ',.0%'
            for idx, name in enumerate(['Female','Male']):
                fig.data[idx].name = name
            st.plotly_chart(fig, use_container_width=True)
        with tab7_2:
            fig = px.bar(df.query('Year == 2021').sort_values('FemaleIP', ascending=False), x='Province', y='FemaleIP', 
                        orientation='v', title = "<b>Female Involvement in Parliament by Province (2021)</b>",height=600, width=800, 
                        color='FemaleIP', color_continuous_scale='rdbu', hover_name='Province', hover_data={'Province': False, 'FemaleIP':':,.1%'},labels={'FemaleIP':'FIP'})
            fig.add_annotation(xref="paper", yref="paper", x=0.195, y=0.20, font_color='black', text="National Average", 
                            showarrow=False, textangle=-90)
            fig.update_layout(xaxis_tickangle=-90, paper_bgcolor='honeydew', plot_bgcolor='#e6e6e6', font_color='black',margin={"l":100,}, yaxis_title='Female Involvement in Parliament')
            fig.layout.yaxis.tickformat = ',.0%'
            fig.update_coloraxes(colorbar_tickformat=',.0%')
            fig.update_traces(marker_line_color='black',)
            st.plotly_chart(fig, use_container_width=True)
    st.markdown("")
    
    col11_1, col11_2 = st.columns([2,3])
    with col11_1:
        st.markdown("")
        st.markdown("")
        st.markdown("")
        st.markdown("GEM indicator uses **female involvement in professional position** (i.e., managerial, professional, administrative, and technical staff) measure female participation in decision making. Female involvement in professional position in Indonesia has been increasing since 2010 and has reached a value of 50% in 2021, which means both male and female are regarded equally in professional positions.")
        st.markdown("In 2021, there are 22 provinces in which the female involvement in professional position is higher than the national average. So unlike economic and political activities, female participation in decision-making is distributed quite well across the provinces in Indonesia.")
    with col11_2:
        tab8_1, tab8_2 = st.tabs(["Bar Chart (2010-2021)", "Bar Chart by Province (2021)"])
        with tab8_1:
            fig = px.bar(df.query('Province == "Indonesia"'), x='Year', y=['FemalePP','MalePP'],orientation='v', barmode='stack', title = "<b>Male and Female Involvement in Professional Position in Indonesia (2010-2021)</b>",height=600, width=900, color_discrete_map={'MalePP':'dodgerblue', 'FemalePP':'indianred'}, labels={'variable':'Gender', 'value':'Involvement in Professional Position (%)'}, text_auto=True)
            fig.update_layout(hovermode='x unified', paper_bgcolor='honeydew', plot_bgcolor='lavender', font_color='black',margin={"l":100,})
            fig.update_traces(marker_line_color='black', hovertemplate=None)
            fig.layout.yaxis.tickformat = ',.0%'
            for idx, name in enumerate(['Female','Male']):
                fig.data[idx].name = name
            st.plotly_chart(fig, use_container_width=True)
        with tab8_2:
            fig = px.bar(df.query('Year == 2021').sort_values('FemalePP', ascending=False), x='Province', y='FemalePP', 
                        orientation='v', title = "<b>Female Involvement in Professional Position by Province (2021)</b>",height=600, width=800, 
                        color='FemalePP', color_continuous_scale='rdbu', hover_name='Province', hover_data={'Province': False, 'FemalePP':':,.1%'},labels={'FemalePP':'FPP'})
            fig.add_annotation(xref="x", yref="y", x=22, y=0.25, font_color='black', text="National Average", 
                            showarrow=False, textangle=-90)
            fig.update_layout(xaxis_tickangle=-90, paper_bgcolor='honeydew', plot_bgcolor='#e6e6e6', font_color='black',margin={"l":100,}, yaxis_title='Female in Professional Position')
            fig.layout.yaxis.tickformat = ',.0%'
            fig.update_coloraxes(colorbar_tickformat=',.0%')
            fig.update_traces(marker_line_color='black',)
            st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")
    st.markdown("### Conclusion")
    st.markdown("Overall, we can see that inequality of access, participation, control, and right between male and female still exist in many provinces in Indonesia. The largest gender inequality can be seen in standard of living, economic and political sectors. Fortunately, the situation has been getting better in the last 10 years. Hopefully, our society can work together with the government to improve gender equality which will result in fair and equal development across the whole country.")
    
    # Scroll to top after loading the data
    components.html(
        f"""
            <script>
                window.parent.document.querySelector('section.main').scrollTo(0, 0);
            </script>
        """,
        height=0
    )
            
# Documentation tab    
with tab1_2:
    st.markdown("### Data Sources")
    st.markdown("All data for this article are sourced from [Badan Pusat Statistik](https://bps.go.id/) in form of Excel file. The Excel files are also available on my Github.")
    st.markdown('### Data Cleaning and Exploration Steps')
    st.markdown("The csv data used by this python script (unp_pro_df.csv) is obtained by processing the Excel files. The complete processes for data cleaning and exploration are documented in this [notebook](https://github.com/tmtsmrsl/GenderEqualityIndonesia/blob/main/CapstoneProject.ipynb).")
    st.markdown('### Inspiration')
    st.markdown("This article was inspired by [Our World in Data](https://ourworldindata.org/), an open-source publication that focuses on the world's largest problem.")
    

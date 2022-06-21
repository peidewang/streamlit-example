from collections import namedtuple
import altair as alt
import math
import pandas as pd
import streamlit as st


"""
# Welcome to Covid Simulation powered by Xplain Data and Streamlit!

Edit `/streamlit_app.py` to customize this app to your heart's desire :heart:

If you likes, checkout streamlit [documentation](https://docs.streamlit.io) and [xplain python API doc](https://docs.xplain-data.de/xplaindoc/interfaces/xplainpy.html).

This is an example application to demonstrate how to build application based on streamlit and xplain data
The data source are served by covid simulation https://demo.aws-xplain-data.de/objectexplorer/index.html


In the meantime, below is an example of what you can do with just a few lines of code:
"""
user_2_replace = "user"
password_2_replace = "xplainData"

with st.echo(code_location='below'):
    import xplain
    import plotly.express as px

    x = xplain.Xsession(url="https://demo.aws-xplain-data.de", user=user_2_replace,
                        password=password_2_replace)
    x.startup("Covid Simulation 300d")

    x.open_query({
        "requestName": "covid",
        "aggregations": [{
            "aggregationType": "COUNT",
            "object": "Static Network",
            "type": "COUNT"

        }],
        "externalSelections": "external / global",
        "groupBys": [
            {
                "subGroupings": [
                    {
                        "attribute": {
                            "dimension": "Connection Number Household Members",
                            "name": "Connection Number Household Members",
                            "object": "Static Network"
                        },
                        "groupByLevelNumber": 1,
                        "includeUpperLevels": False
                    },

                    {
                        "attribute": {
                            "dimension": "Infected by",
                            "name": "Infected by",
                            "object": "Resident"
                        },
                        "groupByLevelNumber": 1,
                        "includeUpperLevels": False
                    }

                ]
            }
        ],
    })



    scenario = st.radio(
        "Simulated Scenario",
        ('1) Without Intervention',
         '2) Slow Contact Restrictions',
         '3) Quick Contact Restrictions',
         '4) Random Quicktests',
         '5) AI-Based Quicktests'
         ))

    plot_spot = st.empty()

    x.run({
        "method": "select",
        "selection": {
            "attribute": {
                "name": "Simulated Scenario",
                "dimension": "Simulated Scenario",
                "object": "Resident"
            },
            "selectedStates": [scenario]
        }
    })



    df = x.get_result("covid")

    print(scenario)
    print(df)

    fig =px.bar(df, x="Connection Number Household Members",
                y="# Static Network",
                color="Infected by",
                title="Static Network by number household members")

    with plot_spot:
        st.plotly_chart(fig)





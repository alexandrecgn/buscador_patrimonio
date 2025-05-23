import streamlit as st
from test.busca import pesquisar, refinar_material, refinar_imaterial


sitios = pesquisar("XXXXXXXXXXXX", "http://portal.iphan.gov.br/geoserver/SICG/ows?service=WFS&version=1.0.0&request=GetFeature&typeName=SICG%3Asitios&maxFeatures=2147483647&outputFormat=application%2Fjson")
tabela = refinar_material(sitios, "Patrimônio Arqueológico")

st.dataframe(tabela)
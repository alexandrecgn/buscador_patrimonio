import streamlit as st
import pandas as pd
from utils import pesquisar, to_dict, refinar_material, refinar_imaterial


base_sitios = "http://portal.iphan.gov.br/geoserver/SICG/ows?service=WFS&version=1.0.0&request=GetFeature&typeName=SICG%3Asitios&maxFeatures=2147483647&outputFormat=application%2Fjson"
base_imaterial_pol = "https://raw.githubusercontent.com/alexandrecgn/buscador_patrimonio/refs/heads/main/bens/imaterial_pol.geojson"
base_imaterial_pt = "https://raw.githubusercontent.com/alexandrecgn/buscador_patrimonio/refs/heads/main/bens/imaterial_pt.geojson"
base_tombados = "https://raw.githubusercontent.com/alexandrecgn/buscador_patrimonio/refs/heads/main/bens/tombados.geojson"
base_valorados = "https://raw.githubusercontent.com/alexandrecgn/buscador_patrimonio/refs/heads/main/bens/valorados.geojson"


if "mapinha" not in st.session_state:
    st.session_state.mapinha = st.empty()


st.title("Buscador do Patrimônio")

st.write(
    "Faça o upload de um POLÍGONO georreferenciado para definir a área onde será feita a busca por Bens Culturais acautelados em âmbito federal e, em seguida, clique em **Pesquisar** para exibir os resultados"
)

st.warning("Formatos de arquivo suportados: KML (Google Earth), Geopackage, GeoJSON")

area = st.file_uploader("Selecionar área", type=["kml", "gpkg", "geojson"])

enviado = st.button("Pesquisar")
    
if enviado:
    with st.status("Pesquisando Bens Culturais na área inserida", expanded=True) as status:
        sitios= pesquisar(area, base_sitios)
        imaterial_pol = pesquisar(area, base_imaterial_pol)
        imaterial_pt = pesquisar(area, base_imaterial_pt)
        tombados = pesquisar(area, base_tombados)
        valorados = pesquisar(area, base_valorados)

        sit_dict = to_dict(sitios)
        imapol_dict = to_dict(imaterial_pol)
        imapt_dict = to_dict(imaterial_pt)
        tom_dict = to_dict(tombados)
        val_dict = to_dict(valorados)

        tab_sit = refinar_material(sit_dict)

        tab_imtpol = refinar_imaterial(imapol_dict)
        tab_imtpt = refinar_imaterial(imapt_dict)
        impol = pd.DataFrame(tab_imtpol)
        impt = pd.DataFrame(tab_imtpt)
        tab_im_tot = pd.concat([impol, impt])
        
        tab_tmb = refinar_material(tom_dict)
        
        tab_val = refinar_material(val_dict)
        
        status.update(label="Pesquisa Concluída", state="complete")

    tab1, tab2, tab3, tab4 = st.tabs(["Patrimônio Arqueológico", "Patrimônio Imaterial", "Patrimônio Tombado", "Patrimônio Ferroviário"])

    with tab1:
        st.header("Sítios Arqueológicos Cadastrados")
        tabela, mapa = st.columns(2)
        if tab_sit.empty:
            st.write("Não foi identificado Patrimônio Arqueológico na área de busca")
        if not tab_sit.empty:
            tabela.dataframe(tab_sit)
            mapa.map(sit_dict["features"])
    
    with tab2:
        st.header("Bens Imateriais Registrados")
        if tab_imtpol.empty and tab_imtpt.empty:
            st.write("Não foi identificado Patrimônio Imaterial na área de busca")
        elif tab_imtpol.empty and not tab_imtpt.empty:
            st.dataframe(tab_imtpt)
        elif tab_imtpt.empty and not tab_imtpol.empty:
            st.dataframe(tab_imtpol)
        elif not tab_imtpt.empty and not tab_imtpol.empty:
            st.dataframe(tab_im_tot)
    
    with tab3:
        st.header("Bens Materiais Tombados")
        tabela, mapa = st.columns(2)
        if tab_tmb.empty:
            st.write("Não foi identificado Patrimônio Tombado na área de busca")
        if not tab_tmb.empty:
            tabela.dataframe(tab_tmb)
            mapa.map(tom_dict["features"])
    
    with tab4:
        st.header("Bens Materiais Valorados")
        tabela, mapa = st.columns(2)
        if tab_val.empty:
            st.write("Não foi identificado Patrimônio Ferroviário na área de busca")
        if not tab_val.empty:
            tabela.dataframe(tab_val)
            mapa.map(val_dict["features"])

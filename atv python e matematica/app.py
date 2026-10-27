
from pathlib import Path
import json
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

caminho_populacao_padrao = r"H:\python-1\3 etp\atv python e matematica\CD2022_Populacao_2010_Compatibilizada_20231222.ods" 

st.set_page_config(page_title='Demografia Inteligente | Belo Horizonte', page_icon='🏙️', layout='wide')
BASE = Path(__file__).resolve().parent
REGIOES = {'Norte':['AC','AP','AM','PA','RO','RR','TO'],
           'Nordeste':['AL','BA','CE','MA','PB','PE','PI','RN','SE'],
            'Centro-Oeste':['DF','GO','MT','MS'],
              'Sudeste':['ES','MG','RJ','SP'],
                'Sul':['PR','RS','SC']}


UF_REGIAO = {uf: reg for reg, ufs in REGIOES.items() for uf in ufs}
CAPITAIS = {'Belo Horizonte':('MG','Elisa'),
    'Curitiba':('PR','Carlos'),
    'Porto Alegre':('RS','Eduardo'), 
    'Salvador':('BA','Jorge'),
    'Florianópolis':('SC','Roberto')}

@st.cache_data(show_spinner='Lendo dados do IBGE...')
def carregar_populacao(arquivo):
    nome = str(getattr(arquivo,'name',arquivo)).lower()
    if nome.endswith('.ods'):
        bruto = pd.read_excel(arquivo, engine='odf', header=None)
    elif nome.endswith(('.xlsx','.xls')):
        bruto = pd.read_excel(arquivo, header=None)
    elif nome.endswith('.csv'):
        try:
            pronto = pd.read_csv(arquivo, sep=None, engine='python')
        except UnicodeDecodeError:
            if hasattr(arquivo,'seek'): arquivo.seek(0)
            pronto = pd.read_csv(arquivo, sep=None, engine='python', encoding='latin1')
        normalizadas = {str(c).lower().strip(): c for c in pronto.columns}
        if {'municipio','uf','pop_2010','pop_2022'}.issubset(normalizadas):
            df = pronto.rename(columns={normalizadas[k]:k for k in ['municipio','uf','pop_2010','pop_2022']}).copy()
            if 'codigo_ibge' not in df.columns: df['codigo_ibge'] = ''
            return preparar(df)
        bruto = pronto
    else:
        raise ValueError('Envie um arquivo .ods, .xlsx, .xls ou .csv válido.')


    if bruto.shape[1] < 8: raise ValueError('Arquivo sem as oito colunas esperadas da tabela IBGE.')
    df = bruto.iloc[3:, [1,2,3,4,6,7]].copy()
    df.columns = ['uf','codigo_uf','codigo_municipio','municipio','pop_2010','pop_2022']
    df['codigo_ibge'] = df['codigo_uf'].astype(str).str.replace(r'\.0$','',regex=True).str.zfill(2) + df['codigo_municipio'].astype(str).str.replace(r'\.0$','',regex=True).str.zfill(5)
    return preparar(df)

def preparar(df):
    df = df.copy()
    for c in ['pop_2010','pop_2022']:
        df[c] = pd.to_numeric(df[c], errors='coerce')
    df['uf'] = df['uf'].astype(str).str.strip().str.upper()
    df['municipio'] = df['municipio'].astype(str).str.strip()
    df = df[df['uf'].isin(UF_REGIAO) & df['pop_2010'].gt(0) & df['pop_2022'].notna()].copy()
    df['regiao'] = df['uf'].map(UF_REGIAO)
    df['variacao_abs'] = df['pop_2022'] - df['pop_2010']
    df['crescimento_pct'] = (df['pop_2022'] / df['pop_2010'] - 1) * 100
    df['taxa_anual_pct'] = ((df['pop_2022'] / df['pop_2010']) ** (1/12) - 1) * 100
    df['capital'] = df.apply(lambda r: r['municipio'] in CAPITAIS and CAPITAIS[r['municipio']][0] == r['uf'], axis=1)
    return df

@st.cache_data
def carregar_etaria(arquivo):
    d = pd.read_csv(arquivo) if str(getattr(arquivo,'name',arquivo)).lower().endswith('.csv') else pd.read_excel(arquivo)
    obrig = {'uf','municipio','ano','faixa_etaria','sexo','populacao'}
    if not obrig.issubset(d.columns): raise ValueError('A base etária precisa das colunas: '+', '.join(sorted(obrig)))
    d['ano'] = pd.to_numeric(d['ano'],errors='coerce')
    d['populacao'] = pd.to_numeric(d['populacao'],errors='coerce')
    d['sexo'] = d['sexo'].astype(str).str.strip().str.lower().map({'masculino':'Homens','homens':'Homens','m':'Homens','feminino':'Mulheres','mulheres':'Mulheres','f':'Mulheres'})
    return d.dropna(subset=['populacao','sexo','ano'])

st.title('🏙️ Demografia Inteligente — Planejamento Urbano')
st.caption('Startup de análise de dados | Persona: Elisa, prefeita de Belo Horizonte | Fonte: IBGE, Censos 2010 e 2022')
st.sidebar.header('⚙️ Filtros e fontes')
padrao = next((p for p in [BASE/'CD2022_Populacao_2010_Compatibilizada_20231222.ods', BASE/'dados'/'populacao_2010_2022.csv'] if p.exists()), None)
upload = st.sidebar.file_uploader('Base populacional IBGE', type=['ods','xlsx','xls','csv'])
if upload is None and padrao is None:
    st.info('Envie na barra lateral a planilha CD2022_Populacao_2010_Compatibilizada_20231222.ods, ou coloque-a na mesma pasta deste app.py.')
    st.stop()
try:
    dados = carregar_populacao(upload if upload is not None else str(padrao))
except Exception as e:
    st.error(f'Não foi possível ler a base populacional: {e}')
    st.stop()

regiao = st.sidebar.selectbox('Região', ['Todas'] + list(REGIOES), index=0)
ufs = sorted(dados['uf'].unique()) if regiao == 'Todas' else sorted(set(REGIOES[regiao]) & set(dados['uf']))
uf = st.sidebar.selectbox('Unidade da Federação', ['Todas']+ufs, index=(ufs.index('MG')+1 if regiao == 'Todas' and 'MG' in ufs else 0))
anos = st.sidebar.multiselect('Anos de Censo/Pesquisa', [2010,2022], default=[2010,2022])
faixa = st.sidebar.selectbox('Faixa etária', ['Todas','0–14','15–59','60+'])
etaria_upload = st.sidebar.file_uploader('Base etária complementar (opcional)', type=['csv','xlsx'])
geo_upload = st.sidebar.file_uploader('GeoJSON municipal/UF (opcional)', type=['geojson','json'])

fil = dados.copy()
if regiao != 'Todas': fil = fil[fil['regiao']==regiao]
if uf != 'Todas': fil = fil[fil['uf']==uf]
if fil.empty: st.warning('Não há municípios nesse recorte.'); st.stop()

pagina = st.sidebar.radio('Visualização', ['🏠 Visão geral','📊 Crescimento e outliers','🗺️ Mapa','👥 Pirâmide etária','📈 Projeções'])
fmt = lambda n: f'{n:,.0f}'.replace(',','.')
pct = lambda n: f'{n:+.2f}%'.replace('.',',')

if pagina == '🏠 Visão geral':
    st.subheader('Panorama demográfico do recorte selecionado')
    p10,p22 = fil['pop_2010'].sum(),fil['pop_2022'].sum()
    k1,k2,k3,k4 = st.columns(4)
    k1.metric('População 2010',fmt(p10) if 2010 in anos else 'Não selecionado')
    k2.metric('População 2022',fmt(p22) if 2022 in anos else 'Não selecionado')
    k3.metric('Crescimento acumulado (2010–22)',pct((p22/p10-1)*100) if len(anos)==2 else 'Selecione ambos os anos')
    k4.metric('Municípios analisados',fmt(len(fil)))
    st.caption('O crescimento do conjunto é calculado pelos totais populacionais, não pela média simples das taxas municipais.')
    st.subheader('As cinco capitais da roda de conversa')
    caps = dados[dados['capital']].copy()
    caps['Gestor'] = caps['municipio'].map(lambda c: CAPITAIS[c][1])
    st.dataframe(caps[['Gestor','municipio','uf','pop_2010','pop_2022','crescimento_pct','taxa_anual_pct']].rename(columns={'municipio':'Cidade','uf':'UF','pop_2010':'População 2010','pop_2022':'População 2022','crescimento_pct':'Crescimento acumulado (%)','taxa_anual_pct':'Taxa média anual (%)'}), hide_index=True, use_container_width=True)
    fig=px.bar(caps.sort_values('crescimento_pct'),x='crescimento_pct',y='municipio',orientation='h',color='crescimento_pct',color_continuous_scale='RdYlGn',title='Crescimento das cinco capitais — 2010 a 2022',labels={'crescimento_pct':'Crescimento (%)','municipio':'Capital'})
    fig.add_vline(x=0,line_color='gray');st.plotly_chart(fig,use_container_width=True)
    st.info('Elisa deve avaliar a redução ou expansão de habitantes de Belo Horizonte em conjunto com a evolução dos municípios metropolitanos, para orientar saúde, mobilidade e habitação.')

elif pagina == '📊 Crescimento e outliers':
    st.subheader('Onde estão as maiores expansões e retrações?')
    st.metric('Média simples das taxas acumuladas dos municípios',pct(fil['crescimento_pct'].mean()))
    q1,q3=fil['crescimento_pct'].quantile([.25,.75]); iqr=q3-q1
    inferior,superior=q1-1.5*iqr,q3+1.5*iqr
    out=fil[(fil['crescimento_pct']<inferior)|(fil['crescimento_pct']>superior)].copy()
    st.caption(f'Outliers pelo método IQR: abaixo de {pct(inferior)} ou acima de {pct(superior)}. Taxas municipais, sem ponderação pela população.')
    c1,c2=st.columns(2)
    with c1:
        st.plotly_chart(px.histogram(fil,x='crescimento_pct',nbins=45,title='Distribuição das taxas municipais',labels={'crescimento_pct':'Variação acumulada (%)'}),use_container_width=True)
    with c2:
        st.plotly_chart(px.box(fil,x='regaiao',y='crescimento_pct',points='outliers',title='Distribuição por região',labels={'regiao':'Região','crescimento_pct':'Variação (%)'}),use_container_width=True)
    st.subheader(f'Municípios discrepantes: {len(out)}')
    st.dataframe(out.sort_values('crescimento_pct',ascending=False)[['municipio','uf','pop_2010','pop_2022','crescimento_pct']],hide_index=True,use_container_width=True)
    c1,c2=st.columns(2)
    with c1:
        st.write('**Dez maiores crescimentos**')
        st.dataframe(fil.nlargest(10,'crescimento_pct')[['municipio','uf','crescimento_pct']],hide_index=True)
    with c2:
        st.write('**Dez maiores retrações**')
        st.dataframe(fil.nsmallest(10,'crescimento_pct')[['municipio','uf','crescimento_pct']],hide_index=True)

elif pagina == '🗺️ Mapa':
    st.subheader('Mapa coroplético do crescimento municipal')
    st.caption('Para desenhar limites municipais reais, envie um GeoJSON com código IBGE de 7 dígitos na propriedade CD_MUN (ou code_muni / codigo_ibge).')
    if geo_upload is None:
        st.warning('O arquivo de população não contém polígonos geográficos. Envie o GeoJSON municipal na barra lateral para habilitar o mapa sem criar geometrias fictícias.')
    else:
        try:
            geo=json.load(geo_upload)
            for feat in geo.get('features',[]):
                props=feat.get('properties',{})
                feat['id']=str(props.get('CD_MUN',props.get('code_muni',props.get('codigo_ibge',feat.get('id','')))))
            mapa=fil.copy();mapa['codigo_ibge']=mapa['codigo_ibge'].astype(str).str.zfill(7)
            fig=px.choropleth_mapbox(mapa,geojson=geo,locations='codigo_ibge',featureidkey='id',color='crescimento_pct',hover_name='municipio',hover_data=['uf','pop_2010','pop_2022'],color_continuous_scale='RdYlGn',mapbox_style='carto-positron',zoom=3,center={'lat':-14.2,'lon':-51.9},opacity=.7)
            fig.update_layout(height=620,margin=dict(l=0,r=0,t=0,b=0))
            st.plotly_chart(fig,use_container_width=True)
        except Exception as e: st.error(f'Erro ao processar GeoJSON: {e}')

elif pagina == '👥 Pirâmide etária':
    st.subheader('Pirâmide etária — homens e mulheres')
    if etaria_upload is None:
        st.warning('A planilha populacional fornecida não possui sexo ou faixa etária. Para uma pirâmide real, carregue uma base etária do IBGE com as colunas uf, municipio, ano, faixa_etaria, sexo, populacao.')
        st.caption('O filtro de faixa etária permanece disponível, mas não altera totais censitários sem essa base adicional.')
    else:
        try:
            idade=carregar_etaria(etaria_upload)
            if uf!='Todas': idade=idade[idade['uf'].astype(str).str.upper()==uf]
            elif regiao!='Todas': idade=idade[idade['uf'].astype(str).str.upper().isin(REGIOES[regiao])]
            ano_et=st.selectbox('Ano disponível',sorted(idade['ano'].dropna().unique(),reverse=True))
            idade=idade[idade['ano']==ano_et]
            if faixa!='Todas':
                def grupo(s):
                    import re
                    m=re.search(r'\d+',str(s)); n=int(m.group()) if m else -1
                    return '0–14' if 0<=n<=14 else '15–59' if 15<=n<=59 else '60+' if n>=60 else 'Indefinido'
                idade=idade[idade['faixa_etaria'].map(grupo)==faixa]
            agg=idade.groupby(['faixa_etaria','sexo'],as_index=False)['populacao'].sum()
            agg['valor']=np.where(agg['sexo']=='Homens',-agg['populacao'],agg['populacao'])
            fig=px.bar(agg,x='valor',y='faixa_etaria',color='sexo',orientation='h',barmode='relative',color_discrete_map={'Homens':'#377eb8','Mulheres':'#e3779b'},labels={'valor':'População (homens à esquerda)','faixa_etaria':'Faixa etária','sexo':'Sexo'})
            fig.update_layout(xaxis_tickformat=',.0f');st.plotly_chart(fig,use_container_width=True)
        except Exception as e: st.error(f'Erro ao ler base etária: {e}')

elif pagina == '📈 Projeções':
    st.subheader('Projeção matemática exploratória')
    cidade=st.selectbox('Município',fil.sort_values('municipio')['municipio'].unique(),index=(list(fil.sort_values('municipio')['municipio'].unique()).index('Belo Horizonte') if 'Belo Horizonte' in fil['municipio'].values else 0))
    linha=fil[fil['municipio']==cidade].iloc[0]
    fim=st.slider('Projetar até o ano',2023,2050,2035)
    taxa=(linha['pop_2022']/linha['pop_2010'])**(1/12)-1
    anos_proj=np.arange(2022,fim+1)
    proj=linha['pop_2022']*(1+taxa)**(anos_proj-2022)
    fig=go.Figure()
    fig.add_trace(go.Scatter(x=[2010,2022],y=[linha['pop_2010'],linha['pop_2022']],mode='lines+markers',name='Censos observados'))
    fig.add_trace(go.Scatter(x=anos_proj,y=proj,mode='lines',line=dict(dash='dash'),name='Cenário extrapolado'))
    fig.update_layout(xaxis_title='Ano',yaxis_title='Habitantes',title=f'{cidade} — cenário de continuidade da taxa 2010–2022')
    st.plotly_chart(fig,use_container_width=True)
    st.metric(f'População projetada para {fim}',fmt(proj[-1]))
    st.warning('A curva é uma extrapolação matemática da taxa anual composta entre os censos; NÃO é uma projeção oficial do IBGE. Não considera migração futura, fecundidade, mortalidade ou mudanças urbanas.')


st.divider()
st.caption('Fonte: IBGE — Censo Demográfico 2010 (população compatibilizada com limites de 2022) e Censo Demográfico 2022. Período intercensitário tratado como 12 anos para taxa anual composta.')
with st.expander('Baixar dados municipais tratados'):
    st.download_button('Baixar CSV',fil.to_csv(index=False).encode('utf-8-sig'),'demografia_municipios.csv','text/csv')

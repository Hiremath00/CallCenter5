import streamlit as st
import os
import pandas
from st_aggrid.shared import JsCode
from dotenv import load_dotenv
from MongoDBAccess import MongoDBAccess
from AudioFile import AudioFile
from WhisperProc import transcribe_audio
from LLM_interface import summarize_text, sentiment_analyze
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode, DataReturnMode, ColumnsAutoSizeMode

audFile = AudioFile()
ag_grid_response = None

if 'show_form' not in st.session_state:
    st.session_state.show_form = False

if 'show_grid' not in st.session_state:
    st.session_state.show_grid = False

if 'file' not in st.session_state:
    st.session_state.file = None

st.title('CallCenter Recordings')

@st.dialog("Select Audio File")
def show_dialog ():
    with st.form("select_form"):
        file = st.file_uploader('Select File', type=['wav', 'mp3', 'flac', 'm4a'])
        submit_button = st.form_submit_button("Submit")
        if submit_button:
            if file is not None:
                audFile.file  = file
                st.session_state.file = file
                st.success("File Selected!")
            else:
                audFile.file  = None
                st.session_state.file = None
            st.session_state.show_form = False
            st.rerun()


#if st.session_state.show_form:
    #show_dialog()


if st.sidebar.button ('Select File'):
    show_dialog()
    #st.session_state.show_form = True

    
if st.sidebar.button ('Transcribe Audio File'):
    st.empty()
    st.write('Transcribing File... ' + audFile.file.name)    # Add transcription logic here
    temp_dir = "temp_uploads"
    os.makedirs(temp_dir, exist_ok=True)   
        # Construct the path for the saved file
    file_path = os.path.join(temp_dir, audFile.file.name)
    st.write('File saved to: {}'.format(file_path))
    
        # Write the uploaded file's content to the temporary path
    with open(file_path, "wb") as f:
        f.write(audFile.file.getbuffer())
   
    audFile.text = transcribe_audio(file_path)
    st.write("**Transcribed Text:**")
    st.markdown(audFile.text)
    st.write('Transcribe complete!')


if st.sidebar.button ("Summarize"):
    st.empty()
    st.write('Summarizing file:   ' +  audFile.file.name)
    audFile.summary = summarize_text(audFile.text).strip()
    st.write('Summary: {}'.format(audFile.summary))    # Add summarization logic here
    st.write('Summary complete!')
    

if st.sidebar.button ("Analyze Sentiment"):
    st.empty()
    st.write('Analyzing Sentiment of ' + audFile.file.name)
    audFile.sentiment = sentiment_analyze(audFile.text).strip()
    st.write('Sentiment: ',audFile.sentiment)    # Add summarization logic here
    st.write('Sentiment complete!')


if st.sidebar.button ("Save to MongoDB"):
    st.empty()
    st.write('Persisting ... ' + audFile.file.name)
    db_access = MongoDBAccess()
    db_access.insert_document(audFile)  
    st.write('Successfully persisted to DB!')
    #st.rerun()


@st.dialog("Call Center Recordings History" , width="medium")
def show_Recordings ():
    with st.form("Recordings", width="stretch"):
        st.set_page_config("Recordings", layout="wide")
        st.empty()   
        db_access = MongoDBAccess()
        data_df = db_access.get_recordings()  
        if data_df.empty:
            st.warning("No data found in the MongoDB collection.")
            exit()
        data_df['file_id'] = data_df['file_id'].astype(str)
        gb = GridOptionsBuilder.from_dataframe(data_df)
        #, enableRowGroup=True, enableValue=True, enablePivot=True  )
        gb.configure_selection('single')  
        #gb.configure_side_bar()  # Add a sidebar
        gb.configure_grid_options(domLayout='normal')
        gb.configure_column("transcription", tooltipField="transcription",width=300)
        gb.configure_column("summary", tooltipField="summary")
        gb.configure_column("sentiment", tooltipField="sentiment", width=100)          
        #gb.configure_column("file_id", tooltipField="file_id", width=100)        
        gb.configure_column("file_name", tooltipField="file_name", width=150)    
        gb.configure_auto_height(True)
        gb.configure_columns(data_df.columns, resizable=True, sortable=True, filterable=True)

        gridOptions = gb.build()
        gridOptions['fit_columns_on_grid_load'] = True
        
        # Display the ag-grid
        ag_grid_response = AgGrid(
            data_df,
            gridOptions=gridOptions,
            #data_return_mode='AS_INPUT',
            #update_mode='MODEL_CHANGED',
            allow_unsafe_jscode=True,
            fit_columns_on_grid_load=True,
            columns_auto_size_mode=ColumnsAutoSizeMode.FIT_ALL_COLUMNS_TO_VIEW,
            theme="Streamlit", # or 'dark' or 'blue'
            enable_enterprise_modules=True,
            height='100%',
            width=1000,
        )
        if st.form_submit_button("Close"):
            st.session_state.show_grid = False
            st.rerun()

if st.session_state.show_grid:
      show_Recordings()

if st.sidebar.button ("Get History"):
    #st.session_state.show_grid = True
    show_Recordings()

if(st.session_state.file ):
    audFile.file = st.session_state.file

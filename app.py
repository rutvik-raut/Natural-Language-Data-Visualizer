import os
import pandas as pd
import openai
import streamlit as st
import warnings
warnings.filterwarnings("ignore")


# ************************** LLM Prompt Functions **************************


def prompt_structure(query_input, api_key):
    # Define the initial prompt for generating Python code.
    prompt = "Generate Python Code. The script should only include code and no comments."

     # Set OpenAI API key and request completion for the given query input.
    openai.api_key = api_key
    result = openai.ChatCompletion.create(model="gpt-4o-2024-05-13",
        messages=[{"role": "system", "content": prompt}, {"role": "user", "content": query_input}])
    
    # Get the completed prompt from the API response.
    prompt_completion = result["choices"][0]["message"]["content"]

    # Process the completed prompt to remove unwanted lines.
    prompt_completion = response_structure(prompt_completion)
    return prompt_completion


def response_structure(result):
    # Find the index of the first occurrence of "read_csv" in the result.
    index = result.find("read_csv")
    if index > 0:
        pre_match = result[:index].rfind("\n")
        post_match = result[index:].find("\n")
        if pre_match != -1:
            result = result[:pre_match] + result[index + post_match:]
        else:
            result = result[index + post_match:]
    return result


def process_structure(dataframe, name):
    # Construct the prompt template.
    prompt_template = (
        f"Consider the dataframe with variable name df from data_file.csv with columns."
        f"'{', '.join(dataframe.columns)}'."
    )
    
    # Loop through dataframe columns to add information about each column.
    for column in dataframe.columns:
        unique_values = dataframe[column].drop_duplicates()
        column_info = (
            f"\n'{column}' is of categorical type '{', '.join(map(str, unique_values))}'." 
            if len(unique_values) < 100 and dataframe.dtypes[column] == "object" else
            f"\n'{column}' is of type {dataframe.dtypes[column]} and has numerical values."
        )
        prompt_template += column_info
    
    # Add instructions for labeling axes, adding a title, using colours and generating the code.
    prompt_template += (
        "\nGenerate labels for x and y axes."
        "\nGive the plot a suitable title."
        "\nUse appropriate colours for the plots."
        "\nUsing Python programming language, generate code using the dataframe as the source to plot the following:"
    )
    
    # Additional prompt additions for imports.
    prompt_additions = (
        "import pandas as pd\nimport matplotlib.pyplot as plt\n"
        "fig = plt.figure(figsize=(12, 6))\n"
        f"df = {name}.copy()\n"
    )
    
    return prompt_template, prompt_additions




# ************************** Streamlit UI Code **************************


# Set up Streamlit page configuration and title with icons.
st.set_page_config(page_title='Data Visualizer', layout='centered', page_icon=':chart_with_upwards_trend:', initial_sidebar_state="expanded")
st.title(':bar_chart: Data Visualizer')


# Load OpenAI API key from .env file.
openai_key = os.getenv('OPEN_AI_API_KEY')


# Check if datasets are stored in session state, and initialize them.
if "datasets" not in st.session_state:
    st.session_state["datasets"] = {}
datasets = st.session_state["datasets"]


# Sidebar for uploading datasets and selecting from existing ones.
with st.sidebar:
    uploaded_dataset = st.file_uploader(":file_folder: Upload your CSV file:", type="csv")
    if uploaded_dataset:
        file_name = uploaded_dataset.name[:-4].capitalize()
        datasets[file_name] = pd.read_csv(uploaded_dataset)

    if datasets:
        selected_dataset = st.selectbox(":page_facing_up: Select your dataset:", list(datasets.keys()))
    else:
        st.warning(":warning: No dataset is currently uploaded.")
        selected_dataset = None


# Text area for entering visualization query and button for plotting.
query = st.text_area("Enter your visualization query: :question:", height=15)
plot_button = st.button("Plot")


# Plotting logic based on OpenAI API key and selected dataset.
if plot_button:
    if openai_key.startswith('sk-'):
        try:
            if selected_dataset:
                blueprint_1, blueprint_2 = process_structure(datasets[selected_dataset], 'datasets["'+ selected_dataset + '"]')
                blueprint_1 = blueprint_1.format("")
                query_input = f'"""\n{blueprint_1}{{}}{query}\n"""\n{blueprint_2}'
                response = prompt_structure(query_input, api_key=openai_key)
                response = blueprint_2 + response
                print(response)
                empty_plot = st.empty()
                empty_plot.pyplot(exec(response))
            else:
                st.warning("Dataset not selected.")
        except Exception as e:
            if type(e) == openai.error.APIError:
                st.error("OpenAI API returned an API Error. (" + str(e) + ")")
            elif type(e) == openai.error.Timeout:
                st.error("OpenAI API request timed out. (" + str(e) + ")")
            elif type(e) == openai.error.APIConnectionError:
                st.error("OpenAI API request failed to connect. (" + str(e) + ")")
            elif type(e) == openai.error.InvalidRequestError:
                st.error("OpenAI API request was invalid. (" + str(e) + ")")
            elif type(e) == openai.error.AuthenticationError:
                st.error("OpenAI API request was not authorized. (" + str(e) + ")")
            elif type(e) == openai.error.PermissionError:
                st.error("OpenAI API request was not permitted. (" + str(e) + ")")
            elif type(e) == openai.error.RateLimitError:
                st.error("OpenAI API request exceeded rate limit. (" + str(e) + ")")
            elif type(e) == openai.error.ServiceUnavailableError:
                st.error("OpenAI API service unavailable. (" + str(e) + ")")
            else:
                st.error("Code execution failed due to errors.")
    else:
        st.error("OpenAI API key invalid.")


# Display selected dataset in a subheader and dataframe format.
if selected_dataset and selected_dataset in datasets:
    st.subheader(selected_dataset)
    st.dataframe(datasets[selected_dataset], hide_index=True)



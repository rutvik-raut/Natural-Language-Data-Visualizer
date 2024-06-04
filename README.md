# Natural-Language-Data-Visualizer

This is an end to end application built using Streamlit to demonstrate how natural language can be used to create beautiful visualizations for any data that is uploaded.

In the backend the application calls the OpenAI API to complete all the requests.

You are free to upload any datasets, even those which have not been cleaned and processed to quickly get a visual summary of the information you want to analyze.

# Assumptions
1. User Interface: The application uses Streamlit to create a user-friendly interface for data upload, selection, and visualizing query input.

2. Data Upload and Selection: Users can upload CSV files, which are then processed and stored in the session state for later use.

3. Error Handling: The system includes comprehensive error handling for various OpenAI API errors such as API errors, timeouts, connection errors, invalid requests, authentication issues, permission errors, rate limits, and service unavailability.

4. Environment Configuration: The OpenAI API key is securely loaded from an environment variable. (Key is not provided with the code)

  
# Architecture

The AI feature in the application is designed to generate Python code for data visualizations based on user queries. The architecture includes the following components:

1. Prompt Structure Function: Constructs the prompt to be sent to the OpenAI API, including the dataset structure and specific user queries.

2. Response Structure Function: Processes the API response to remove unnecessary lines and ensure the code is ready for execution.

3. Process Structure Function: Prepares the prompt by analyzing the dataframe's columns and generating appropriate descriptions for the AI to understand the data structure.

4. Streamlit Interface: Manages user interactions, including file upload, dataset selection, and visualization query input. It also handles displaying the generated plots and any errors that occur during the process.


# Models
The application uses the latest version of the GPT-4 model named GPT-4o from OpenAI which was released on 13th May 2024 that has a context window of 128,000 tokens and has been trained on data until Oct 2023. The model is accessed via the ChatCompletion API.


# Demo

1. The below image shows how we can upload a csv consisting of GDP of various nations to visualize and compare the GDP of top 5 nations. 

![image](https://github.com/rutvik-raut/Natural-Language-Data-Visualizer/assets/20756263/8fa51344-cfd6-4a2c-8df7-33cf8bdcf5d2)



2. The below image shows how we can upload a csv consisting of salaries for Data Scientist roles across US and use this tool to visualize and compare the top 3 companies that provided the highest salaries in 2021. 


![image](https://github.com/rutvik-raut/Natural-Language-Data-Visualizer/assets/20756263/b9cd4035-4046-40df-bbce-859d0f80b72f)



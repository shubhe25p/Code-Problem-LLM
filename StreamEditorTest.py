import streamlit as st
from streamlit_ace import st_ace
import time
import os
import psutil

def get_memory_usage():
    # Returns the memory usage in MB
    process = psutil.Process(os.getpid())
    mem_info = process.memory_info()
    return mem_info.rss / (1024 ** 2)

def exec_code(code):
    start_time = time.time()
    start_memory = get_memory_usage()

    result = exec(code)

    end_time = time.time()
    end_memory = get_memory_usage()

    elapsed_time = end_time - start_time
    memory_used = end_memory - start_memory

    return result, elapsed_time, memory_used

def PromptingAndSubmit():
    # returns user's input
    input = null

def ProblemGenerator(user_input):
    # returns GPT's output
    input = null

def CodeEditorAndExecute():
    # returns user code and execution result
    col1, col2 = st.columns(2)
    execute = False
    with col1:
        user_code = st_ace(language = 'python', theme = 'cobalt')
        execute = st.button('Execute')
    
    with col2:
        st.header('Execution Result')
        if execute:
            output, time_to_execute, mem_alloc = exec_code(user_code)
            st.write(output)
            st.subheader('Metrics')
            st.write('Time to execute: ' + str(time_to_execute))
            st.write('Memory allocated: ' + str(mem_alloc))
    
    return user_code, output, time_to_execute, mem_alloc




def ScoreCalculator(user_code, execution_result, time_to_execute, mem_alloc):
    # returns score and feedback
    input = null
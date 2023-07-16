import streamlit as st
from streamlit_ace import st_ace
from langchain.chat_models import ChatOpenAI
from langchain import LLMChain
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

os.environ["OPENAI_API_KEY"] = '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'
chat = ChatOpenAI(model="gpt-4", temperature=0) 


def prompting_and_submit_streamlit():
    # Create a text input widget
    user_input = st.text_input("problem area: ")

    # Create a submit button
    if st.button("Submit"):
        # If the Submit button is pushed
        return user_input
    return None

def complexity_level():
    # Create a selectbox with options 1 through 5
    selection = st.selectbox('Choose a number:', options=[1, 2, 3, 4, 5])
    # Return the selection
    return selection

def ProblemGenerator(user_input, level):
    smg = '''You are an AI code examiner. You have to create an examination task for Python developers.
    Inputs are the problem area, and level of complexity(from 1 to 5), create a task based on that. Here is an example of a task:
    ------------------
    'You are given two non-empty linked lists representing two non-negative integers. The digits are stored in reverse order, and each of their nodes contains a single digit. Add the two numbers and return the sum as a linked list.
    You may assume the two numbers do not contain any leading zero, except the number 0 itself.
    Example 1:
    Input: l1 = [2,4,3], l2 = [5,6,4]
    Output: [7,0,8]
    Explanation: 342 + 465 = 807.
    Example 2:
    Input: l1 = [0], l2 = [0]
    Output: [0]
    Example 3:
    Input: l1 = [9,9,9,9,9,9,9], l2 = [9,9,9,9]
    Output: [8,9,9,9,0,0,0,1]
    Constraints:
    The number of nodes in each linked list is in the range [1, 100].
    0 <= Node.val <= 9
    It is guaranteed that the list represents a number that does not have leading zeros.'
    ------------------
    Your output should look exactly like that. Even if the input is not obviously a problem area, make a task.
    Never output anything else, only the task.
    '''
    messages = [
        SystemMessage(content=smg),
        HumanMessage(content=f'problem area: + {user_input} +\n\n + level: + {level}')
    ]
    
    result = chat(messages)
    #print(result.content)
    return result.content

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

prompt = prompting_and_submit_streamlit()
level = complexity_level()
problem = ProblemGenerator(prompt, level)
user_code, execution_result, time_to_execute, mem_alloc = CodeEditorAndExecute()
# score, feedback = ScoreCalculator(user_code, execution_result, time_to_execute, mem_alloc)
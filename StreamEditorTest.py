import streamlit as st
from streamlit_ace import st_ace
import time
import os
import psutil
import openai
import re

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


system_prompt_for_score = """
Given some code and execution time and memory allocation as json, give a score from 0-100 in percentage and feedback in text and code also: Follow this format for sample input and output?

Input: 
Code: class Solution {
    public int[] twoSum(int[] nums, int target) {
        int n = nums.length;
        for (int i = 0; i < n - 1; i++) {
            for (int j = i + 1; j < n; j++) {
                if (nums[i] + nums[j] == target) {
                    return new int[]{i, j};
                }
            }
        }
        return new int[]{}; // No solution found
    }
}

Time to Execute: 1ms
Memory Allocation: 0.5Mb

Output: 
Feedback: [Generate text here]

Score: [Generate score here from 0-100 in percentage]

Improved Code: [based on the feedback give updated code here]

Don't output anything else. Only output these 3 parts."""

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




def formatresult(result):
    match = re.search(r'Code(.*)', result)
    st.code(match.group(1))

def ScoreCalculator(user_code, execution_result, time_to_execute, mem_alloc):
    # returns score and feedback
    user_prompt = f"Code: {user_code}\nTime to Execute: {time_to_execute}\nMemory Allocation: {mem_alloc}\nExpected Output: {execution_result}\n\n"
    completion = openai.ChatCompletion.create(model="gpt-4-0613",messages=[{"role": "system", "content": system_prompt_for_score},{"role": "user", "content": user_prompt}])
    result = completion.choices[0].message.content
    formatresult(result)
    st.write(result)
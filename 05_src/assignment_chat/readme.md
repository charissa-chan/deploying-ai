# AI Knowledge Explorer Chatbot

## Overview
This project is a conversational AI chat client designed to answer user queries about word definitions and provide interesting facts. It uses an explorer’s guide tone of voice and incorporates nautical turns of phrase to encourage engagement and a sense of curiosity. 

Much of this project, including some of the language used in this readme file, is built on the basis of the template provided by the course_chat folder.

## Services Provided
+ The chat client provides the following three services organized in tools_*.py files.

+ Each tool is imported to the main and included in the list 'tools'.

+ The tools node uses LangGraph's `ToolNode` class and `tools_condition` is the standard tool stopping criteria.

+ All restrictions and tone requirements are in the instructions prompt. You can find this in prompts.py.

### Service 1: Dictionary Lookup using API Call 
Uses a dictionary API to retrieve word definitions. 


### Service 2: Fun Facts Search through Semantic Query
Allows users to search for relevant facts from a curated collection of interesting facts.


### Service 3: Random Fact Generator
Draws on the same dataset used for Service 2 to provide a random fact when asked.


#### Note on Processing, Cleaning, and Creating Embeddings from Dataset
+ Database sourced from the Curiosity Dataset Repository (https://github.com/Mr-Vicente/Curiosity-Dataset/blob/main/dataset/diy/diy_final.txt). For this simple chat client, only the diy_final.txt file is used.
+ Embeddings created using chromadb persistent client instance. 
+ The fact dataset was processed by splitting individual facts along the <sep> markers present in the original file. White space was also cleaned from the file.
+ Each fact was converted into an embedding vector and stored in ChromaDB with its corresponding document and identifier.
+ The script for this process can be found under the 'scripts' folder.


## Implementation Decisions
+ Using a dataset of fun facts was allows control over what information is provided rather than relying fully on the language model’s generated knowledge. 
+ The chatbot was designed with an explorer’s guide communication style to make responses more engaging while maintaining an informative and educational tone.
+ Instructions were added to encourage the chatbot to state when no relevant information is available instead of generating unsupported facts.


## Guardrails and Other Limitations
In according with assignment instructions, I have includd guardrails that prevent users from:

  * Accessing or revealing the system prompt.
  * Modifying the system prompt directly.

I have also included instructions in the prompt to prevent the model from answering on certain restricted topics:

  * Cats or dogs
  * Horoscopes or Zodiac Signs
  * Taylor Swift

## Implementation
Code is implemented in the folder "05_src/assignment_chat"
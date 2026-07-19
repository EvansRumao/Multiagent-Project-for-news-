from agents import build_search_agent, build_reader_agent, writer_chain, critic_prompt

def run_research_pipeline(topic:str)->str:
    state ={}

    #search agent working
    print("\n" + "="*50)
    print(f"Running search agent is working")
    print("="*50 + "\n")

    search_agent = build_search_agent()
    search_results = search_agent.invoke({
        "messages":[("user",f"Search for recent and reliable information on the topic: {topic}")]

    })


    state['search_results'] = search_results['messages'][-1].content

    print("\n search results: \n", state['search_results'])

    #step 2 reader agent working
    print("\n" + "="*50)
    print(f"Running reader agent is working")
    print("="*50 + "\n")  
    reader_agent = build_reader_agent()
    reader_results = reader_agent.invoke({
        "messages":[("user",f"Scrape and summarize the content from the following URLs:\n{state['search_results'][:500]}")]
    })


    state['reader_results'] = reader_results['messages'][-1].content
    print("\n reader results: \n", state['reader_results'])

    #step 3 - writer chain 

    print("\n"+" ="*50)
    print("step 3 - Writer is drafting the report ...")
    print("="*50)

    research_combined = (
        f"SEARCH RESULTS : \n {state['search_results']} \n\n"
        f"DETAILED SCRAPED CONTENT : \n {state['reader_results']}"
    )

    state["report"] = writer_chain.invoke({
        "topic" : topic,
        "research" : research_combined
    })

    print("\n Final Report\n",state['report'])

    #critic report 

    print("\n"+" ="*50)
    print("step 4 - critic is reviewing the report ")
    print("="*50)

    state["feedback"] = critic_prompt.invoke({
        "report":state['report']
    })

    print("\n critic report \n", state['feedback'])

    return state



if __name__ == "__main__":
    topic = input("\n Enter a research topic : ")
    run_research_pipeline(topic)



 
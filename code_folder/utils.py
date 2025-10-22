import base64
from langchain_core.messages import HumanMessage, SystemMessage
import re
import string
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_core.prompts import ChatPromptTemplate


def encode_image(image_path):
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode('utf-8')
    

def describe_input_image(encoded_image, llm):

    messages = [
        SystemMessage(content="You are an AI assistant specializing in analyzing and describing food images. Your task is to provide a concise and accurate description of the food item."),
        HumanMessage(content=[
            {
                "type": "text",
                "text": f"""You are an assistant tasked with providing detailed descriptions of the dish in the image. Your descriptions should focus exclusively on the food and its ingredients, without mentioning any non-food items such as plates, utensils, or decorations. Follow these guidelines to create a detailed and accurate description in a short paragraph:
                        
                        Your short and concise description should suggest what the user is looking for with key search terms. Do not include any unnecessary terms which do not help in word similarity search.
                        Identify the dish, if not sure, mention how it looks, specify the cuisine, mention the key ingridients used in the dish."""
            },
            {
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/jpeg;base64,{encoded_image}"
                },
            },
        ])
    ]

    response = llm.invoke(messages)
    return response.content





def enhance_search(user_input, llm):

    hyde_prompt = [
            SystemMessage(content="You are an expert culinary assistant. Your task is to produce a search query description based on user input or preference."),
            HumanMessage(content=[
                {
                    "type": "text",
                    "text": f'''You are an expert culinary assistant tasked with generating a search query that helps recommends a variety of menu items based on user preferences. 
                    User Input:

                    {user_input}

                    Generate a Response That Includes Just the Key Unique Search Terms according to the user's preference, do not include unnecessary words that don't help search.
                    The search query may or may not contain the following parameters. For example you can include similar menu items as per the user preference if mentioned, if preferences is mentioned enhance and give key search terms based on preferences.
                    The goal is to either create a detailed query using specific information provided by the user or enhance the input to find similar preferences when the information is vague.
                    
                    Menu Items:

                    List different dishes or food items that resemble the user's input.
                    Mention their respective cuisines.

                    Cuisines:

                    Include a variety of cuisines that may match or complement the user's preferences.

                    Descriptions and Ingredients:
                    Provide a very short description of each dish.
                    List key ingredients for each dish.

                    Dietary Preferences:

                    Add any dietary preferences mentioned by the user, such as vegetarian, non-vegetarian, vegan, etc.

                    Nutritional Information:

                    Add important nutritional preference mentioned by the user if any such as high protein, number of calories, etc.
                    Mention serving sizes.
                    Dietary Warnings and Suggestions:

                    Avoid any dishes or ingredients containing any allergen mentioned by the user if any suggest menu items without these, and ensure all recommended items are free from this allergen.

    '''}])]
    response = llm.invoke(hyde_prompt)


    return response.content





def clean_text(text):
    """
    Cleans and normalizes the input text.
    
    Parameters:
    - text: str, the text to clean.
    
    Returns:
    - str, the cleaned text.
    """
    # Remove HTML tags
    text = re.sub(r'<.*?>', '', text)

    # Replace newline and tab characters with a space
    text = text.replace('\n', ' ').replace('\t', ' ')

    # Remove punctuation
    text = text.translate(str.maketrans('', '', string.punctuation))

    # Remove extra spaces
    text = re.sub(r'\s+', ' ', text).strip()

    # Convert to lowercase
    text = text.lower()

    return text




def relevance_checker(context, preference, llm):


    relevance_prompt = [
                SystemMessage(content="You are a restaurant assistant specializing in helping customers find the food they want."),
                HumanMessage(content=[
                    {
                        "type": "text",
                        "text": f'''Answer the question "Is this dish relevant to the user by comparing dish details and user preference?" in one word either Yes or No, based only on the following context. Say Yes only if it is relevant otherwise say No.
                        Context:
                        {context}
                        User Preference: {preference}
                        Answer:'''}])]
    response = llm.invoke(relevance_prompt)


    return response.content






def dish_summary(dish_description, preference, llm):


    summary_prompt = [
                SystemMessage(content="You are a culinary assistant designed to summarize the dish description in accordance with the user preference."),
                HumanMessage(content=[
                    {
                        "type": "text",
                        "text": f'''
 Your task is to create a very short two lines summary of the dish in a savoury manner by highlighting the user preference. The summary should suggest why the dish is perfect for the user as per their preference.
 The summary should include dish name, origin, ingredients and any other relevant information requested by the user in a friendly way. Do not include unnecessary sentences or additional comments like here is your response. Just give the summry description.


            Dish Description:

            {dish_description} 
            
            User Preference:

            {preference}
'''}])]
    response = llm.invoke(summary_prompt)


    return response.content



def recommend_dishes_by_preference(search_results, original_input,llm):
    # Extract the user's preferences from the search results

    # context = ""
    relevant_images = {}
    responses = []

    i = 0
    for doc in search_results:
        relevant = relevance_checker(doc.page_content, original_input, llm)
        if relevant.lower().strip(' ') == 'yes':
            relevant_images[doc.metadata['image_path']] = doc.metadata
            responses.append(dish_summary(doc.page_content, original_input, llm))
            # context += doc.page_content + "\n\n"
            i += 1
        if i ==3:
            break
        

    return responses, relevant_images






def assistant(context, user_input, llm):


    assistant_prompt = [
                SystemMessage(content="You are a helpful and knowledgeable assistant capable of providing food recommendations and answering general queries."),
                HumanMessage(content=[
                    {
                        "type": "text",
                        "text": f'''
  Your task is to engage users in natural, friendly dialogue to understand their preferences, dietary restrictions, and culinary interests.
Your goal is to summarize relevant food recommendations in a single sentence based on the user's inputs and the context if the user query is indicting that they want a recommendation. 
Otherwise you can simply request user to provide preferences such which cuisine or dish they would like based on the context given. Do not answer if you don't have relevant knowledge about the query.

Remember the context given is all the dishes we have.
User Input:

{user_input}


Context:
{context}


The output should be strictly formatted in JSON, with the following structure:
"recommendation": A field indicating whether a recommendation was made ("yes" or "no").
"response": A text field containing the chatbot's conversational response to the user's input, including recommendations or additional questions if necessary.
"
'''}])]
    response = llm.invoke(assistant_prompt)
    return response.content


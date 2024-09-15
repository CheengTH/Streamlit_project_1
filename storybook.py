from openai import OpenAI
import streamlit as st

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

def gen_story(prompt):
  response = client.chat.completions.create(
      model = 'gpt-4o-mini',
      messages = [
          {'role':'system','content':"""You are a story teller. You published short stories for young adults for 5 years.
          Given a title, you can write stories with anticlimatic ending.
          Short stories are only 100 to 150 words in length."""},
          {'role':'user','content':prompt}
      ],
      temperature = 1.2,
      max_tokens = 1000
  )
  return response.choices[0].message.content

def cover_prompt(prompt):
    response = client.chat.completions.create(
        model = 'gpt-4o-mini',
        messages = [
            {'role':'system','content':"""You are going to give the main elements of the story to create the cover of a storybook."""},
            {'role':'user','content':prompt}
        ],
        temperature = 1.2,
        max_tokens = 200
    )
    return response.choices[0].message.content

def cover_art(prompt):
  response = client.images.generate(
      model = 'dall-e-3',
      prompt = prompt,
      size = '1024x1024',
      quality = 'standard',
      style = 'vivid',
      n = 1,
  )
  return response.data[0].url

def storybook(prompt):
  story = gen_story(prompt)
  story_cover = cover_prompt(story)
  image = cover_art(story_cover)
  
  st.image(image)
  st.caption(prompt)
  st.divider()
  st.write(story)
  
prompt = st.text_input("Give me a story title")

if st.button("Generate!"):
  storybook(prompt)

import openai
import streamlit as st
import fitz
            
import streamlit as st

def developer_details():
    st.sidebar.markdown("# Developer Details")
    
    developers = [
        {
            "name": "Sudhir Sharma",
            "role": "B.Tech CSE - IIT Bhilai 2024",
            "email": "sudhirsharma@iitbhilai.ac.in",
            "github": "https://github.com/Sudhir878786",
            "linkedin": "https://www.linkedin.com/in/sudhirsharma87/",
            "avatar": "https://avatars.githubusercontent.com/u/92601949?v=4",  # Replace with actual image URL
        },
        # Add more developers if needed
    ]
    
    for developer in developers:
        st.sidebar.markdown(f"## {developer['name']}")
        st.sidebar.image(developer['avatar'], width=150)
        st.sidebar.write(f"**Role:** {developer['role']}")
        st.sidebar.write(f"**Email:** {developer['email']}")
        st.sidebar.write(f"**GitHub:** {developer['github']}")
        st.sidebar.write(f"**LinkedIn:** {developer['linkedin']}")
        st.sidebar.markdown("---")

# Call the function to display the container in the sidebar
developer_details()


def prompt1(company,position,round,intervier_level):
    prompt=f"""
    I want you to act as a {intervier_level} for {round} interviews on {company} company for the position of {position}. You'll suggest the characteristics of this job interview and the characteristics of the {company}'s interview. 
    The return format should bullet point be like this:
    Characteristics of this job interview:
    - name: detail explanation  
    Characteristics of {company}:
    - name: detail explanation
    """
    return prompt

def followup1(company,position,round,bullet_point):
    prompt=f"""
    Can you talk the detail about {bullet_point} for {round} interviews on {company} company for the position of {position}?
    The return format should bullet point be like this:
    - name: detail explanation
    """
    return prompt

def prompt2(position):
    prompt=f"""
    I want you to act as a talent recruiter for the position of {position}'s interviews. You'll suggest the characteristics of this job interview for both behavior requirement and technical requirement. 
    The return format should bullet point be like this:
    Characteristics of this behavior requirement:
    - name: detail explanation  
    Characteristics of technical requirement:
    - name: detail explanation
    """
    return prompt

def followup2(position,bullet_point):
    prompt=f"""
    Can you talk the detail about {bullet_point} for the interview of {position}?
    The return format should bullet point be like this:
    - name: detail impovement advice
    """
    return prompt

def prompt3(position,resume,dis_num,ad_num):
    prompt=f"""
    I want you to act as a talent recruiter for hiring {position}. I will give you a resume and you'll suggest what are {dis_num}+ disadvantages and {ad_num}+ advantages of the {position} position. Please remember, the return should be highly related to the {position} position.
    The return format should bullet point be like this:
      Disadvatage: 
      - name: Suggestions for improvements to make the resume more appropriate for the {position} position and link to specific sentences on the resume.
      Advantage:
      - name: use one sentence to explain why it is advantageous for the {position} position.
      
    Here is the resume:
    {resume}.
    """
    return prompt

def followup3(position,resume,bullet_point):
    prompt=f"""
    Can you talk the detail about {bullet_point} for the position of {position} based on {resume}?
    The return format should bullet point be like this:
    - name: detail impovement advice
    """
    return prompt


def ask(prompt):
  rsp = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
          {"role": "system", "content": prompt},
      ]
  )

  output=rsp.choices[0].message.content
  return output

####################

st.title('IntervuPro.Ai')
st.subheader('A tool using to help people prepare their interview by using gpt3.5')

# environment setup
key=st.text_input('Please input your OpenAI key')
openai.api_key=key

option = st.selectbox(
    'How would you like to prepare for the interview?',
    ('Prepare for a specific interview',
    'Understand the requirement of a specific position',
    'Analyze resume', 
    ))

if "submit" not in st.session_state:
    st.session_state["submit"] = False

st.write('')
###### option 1
if option=='Prepare for a specific interview':
    col1, col2= st.columns(2)
    with col1:
        company=st.text_input('Input your company','Amazon')
    with col2:
        position=st.text_input('Input your position','Data engineer')
        
    col3, col4 = st.columns(2)
    with col3:
        intervier_level=st.text_input('Input your interviewer level: ','Talent Recuriter')
    with col4:
        round=st.radio('Select your round: ',('Phone Screen','Behavior Interview','Technical Interview', 'General'))
        if round=='General':
            round=''
    
    st.write('Click button again if you want to regenerate a new ansewer.')
    submit_button=st.button('Submit')
    
    if st.session_state.get('button') != True:
        st.session_state['button'] = submit_button
    if st.session_state['button'] == True:
        prompt=prompt1(company,position,round,intervier_level)
        output=ask(prompt)
        st.write(output)  
            
        followup_time=0
        followup=''
        while True:
            output_list=output.split('\n')
            indexes = [i for i, word in enumerate(output_list) if '- ' in word]
            new_list = [output_list[i] for i in indexes]
            Cq=[i.split(':')[0].strip('- ') for i in new_list]
            Cq = ['None']+ Cq
            
            followup_radio = st.radio('I want to follow up:', tuple(Cq),key='0')
            if followup_radio:
                followup_time +=1
                if followup_radio == 'None':
                    break
                else:
                    if followup_radio != 'None':
                        followup = followup1(company, position, round, followup_radio)
                        output = ask(followup)
                        st.write(output)
                    if followup_time>5:
                        break   


###### option 2
if option =='Understand the requirement of a specific position':
    position=st.text_input('Input your position','Data engineer')
        
    st.write('Click button again if you want to regenerate a new ansewer.')

    #submit=st.checkbox('submit')
    submit=st.button('submit')

    if submit:
        prompt=prompt2(position)
        output=ask(prompt)
        st.write(output)  
            
        followup=''
        output_list=output.split('\n')
        indexes = [i for i, word in enumerate(output_list) if '- ' in word]
        new_list = [output_list[i] for i in indexes]
        Cq=[i.split(':')[0].strip('- ') for i in new_list]
        Cq = ['None']+ Cq


        followup_radio = st.radio('I want to follow up:', tuple(Cq))
        if followup_radio!='None':
            followup = followup2(position,followup_radio)
            op = ask(followup)
            st.write(op)
    
    
###### option 3

if option =='Analyze resume':
    
    # col31, col32,col33= st.columns(3)
    # with col31:
    #     position=st.text_input('Input your position','data engineer')
    # with col32:
    #     dis_num=st.text_input('Input your dis_num','6')
    # with col33:
    #     ad_num=st.text_input('Input your ad_num','4')
    
    position=st.text_input('Input your position','data engineer')
    dis_num=6
    ad_num=4

    uploaded_file = st.file_uploader("Upload your resume", type=["pdf"]) 
    if uploaded_file:
        
        if "submit" not in st.session_state:
            st.session_state["submit"] = False
        
        doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
        resume = ""
        for page in doc:
            resume += page.get_text()
        
        st.write('Click button again if you want to regenerate a new ansewer.')
        submit_button=st.button('Submit')
        
        if st.session_state.get('button') != True:
            st.session_state['button'] = submit_button
        if st.session_state['button'] == True:
            prompt=prompt3(position,resume,dis_num,ad_num)
            output=ask(prompt)
            st.write(output)  
            
            followup_time=0
            while True:
                output_list=output.split('\n')
                output_list= [element for element in output_list if element != '']

                ind = [i for i, word in enumerate(output_list) if 'Advantage:' in word]
                Cdis_list=output_list[1:int(dis_num)+1]
                Cdis=[i.split(':')[0].strip('- ') for i in Cdis_list]
                Cdis = ['None']+ Cdis
                
                followup_radio = st.radio('I want to follow up:', tuple(Cdis),key=followup_time)
                followup_time +=1
                if followup_radio == 'None':
                    break
                else:
                    followup = followup3(position,resume,followup_radio)
                    output = ask(followup)
                    st.write(output)
                if followup_time>4:
                    break
            

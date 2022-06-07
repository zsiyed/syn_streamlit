#import streamlit as st
#import multipage_template_streamlit as multipage

import streamlit as st
import os
import joblib

path = os.getcwd()
cache = os.path.join(path, 'cache')

def change_page(pag):
	with open(os.path.join(cache, 'cache.txt'), "w") as f:
		f.truncate()
		f.write(f"{pag}")
		f.close()

def read_page():
	with open(os.path.join(cache, 'cache.txt'), "r") as f:
		pag = f.readline()
		pag = int(pag)
		f.close()
	return pag

@st.cache(suppress_st_warning=True)
def initialize(initial_page_test=False):
	if initial_page_test:
		toWrite= -1
	else:
		toWrite= 0
	try:
		change_page(toWrite)
	except FileNotFoundError:
		os.mkdir(cache)
		change_page(toWrite)

def save(var_list, name, page_names):
	try:
		dic = joblib.load(os.path.join(cache, 'dic.pkl'))
	except FileNotFoundError:
		dic = {}

	for app in page_names:
		if app in list(dic.keys()):
			if name not in dic[app]:
				dic[app] += [name]
		else:
			dic[app] = [name]


	joblib.dump(var_list, os.path.join(cache, name + '.pkl'))
	joblib.dump(dic, os.path.join(cache, 'dic.pkl'))

	return os.path.join(cache, name + '.pkl')

def load(name):
	try:
		return joblib.load(os.path.join(cache, name + '.pkl'))
	except FileNotFoundError:
		return ''

def clear_cache(filenames=None):
	if filenames:
		for element in filenames:
			os.remove(os.path.join(cache, element + '.pkl'))
	else:
		filelist = [file for file in os.listdir(cache) if file.endswith(".pkl")]
		for file in filelist:
			os.remove(os.path.join(cache, file))

@st.cache(suppress_st_warning=True)
def start_app():
	try:
		clear_cache()
	except:
		pass

class app:
	def __init__(self, name, func):
		self.name = name
		self.func = func


class MultiPage:
	def __init__(self, next_page="Next Page", previous_page="Previous Page", navbar_name="Navigation", start_button="Let's go!"):
		self.__initial_page = None
		self.start_button = start_button
		self.__initial_page_set = False
		self.__apps = []
		self.navbar_name = navbar_name
		self.__block_navbar = False
		self.next_page_button = next_page
		self.previous_page_button = previous_page

	def disable_navbar(self):
		self.__block_navbar = True

	def set_initial_page(self, func):
		self.__initial_page = app("__INITIALPAGE__", func)
		self.__initial_page_set = True


	def add_app(self, name, func):
		new_app = app(name, func)
		self.__apps.append(new_app)

	def run(self):
		initialize(self.__initial_page_set)

		pag = read_page()

		container_1 = st.container()

		if pag == -1:
			container_2 = st.container()
			placeholder = st.empty()
			with container_2:
				if placeholder.button(self.start_button):
					pag = 0
					change_page(pag)
					placeholder.empty()
		with container_1:
			if pag==-1:
				self.__initial_page.func()

			else:
				side_1, side_2 = st.sidebar.columns(2)

				with side_1:
					if st.button(self.previous_page_button):
						if pag > 0:
							pag -= 1
						else:
							pag = 0

						change_page(pag)


				with side_2:
					if st.button(self.next_page_button):
						if pag < len(self.__apps)-1:
							pag +=1
						else:
							pag = len(self.__apps)-1

						change_page(pag)



				st.sidebar.markdown(f"""<h1 style="text-align:center;">{self.navbar_name}</h1>""", unsafe_allow_html=True)
				st.sidebar.text('\n')


				for i in range(len(self.__apps)):
					if st.sidebar.button(self.__apps[i].name):
						pag = i
						change_page(pag)

				try:
					prev_vars = []
					dic = joblib.load(os.path.join(cache, 'dic.pkl'))
					for appname in dic[self.__apps[pag].name]:
						prev_vars += load(os.path.join(cache, appname))
					if len(prev_vars) == 1:
						prev_vars = prev_vars[0]
				except:
					prev_vars = None

				self.__apps[pag].func(prev_vars)


#start of app code

#wide layout
st.set_page_config(layout='wide')

#Clears the cache when the app is started
start_app()

#multipage object
app = MultiPage()
app.start_button = "Let's explore this!"
# app.navbar_name = "Table of Contents"
# app.next_page_button = "Next Question"
# app.previous_page_button = "Previous Page"


# intro page function to start
def intropage():
	st.header("Welcome to our climate change chatbot, we hope this chat bot shows you new perspectives and information on the topic of global warming.")
# 	st.markdown("# Lets dive in!")

def homepage(prevpage):
    st.header("Here we have an interactive slider to help us understand your background as it applies to climate change.")
    knowledge_lvl = st.slider("How educated do you feel you are about climate change on a scale of 1-10", min_value=1, max_value=10, value = 0)
    if knowledge_lvl > 0 and knowledge_lvl > 5:
        st.write("Please navigate to page 2.")
    if knowledge_lvl > 0 and knowledge_lvl <= 5:
        st.write("Please navigate to page 1.")
    
def Page1(prevpage):
    st.write("No worries! Everybody starts somewhere.")
    direction = st.selectbox('What are you more interested in learning about',('None', 'Large Scale Impact', 'Personal Impacts'), index = 0)
    if (direction == 'Large Scale Impact'):
        st.header("Below is a resource from NASA to learn more about large scale impacts.") # nasa
        st.write("https://urldefense.proofpoint.com/v2/url?u=https-3A__climate.nasa.gov_&d=DwIGaQ&c=-35OiAkTchMrZOngvJPOeA&r=BmF5uiBgkrvN4DQtKa9Q0w&m=ph6ebrS_ATFX90WAmyX5rDBh28z_-1z5WXFOta-A4S9J7AQef_szcgYyP7Z8GDJx&s=vgtY8X5fBRukX6SL9mI9E4OTG4V99DetpeBJL0fCy-4&e= ")
        st.write("These are some basic facts about how we know that climate change is happening, and how severe these effects are. This is a very valuable resource to someone just getting started on understanding climate change. Notable effects mentioned are the increase in CO2 by 417 parts per million, the global temperature increase by 1 celsius, and sea levels rising by 3.94 inches.")
        hoax = st.selectbox('Do you believe these state effects of climate change are a real or fabricated issue?',('None', 'Real', 'Fabricated'), index = 0)
        if (hoax == 'Real'):
            st.write('Excellent! Now that you\'ve become familiar with some of the effects of climate change, the next step is understanding why this is happening. The short answer is an increase in greenhouse gasses. That means humans are creating more water vapor, carbon dioxide, and methane to name a few. These greenhouse gases have warmed our planet. For more information, please visit the NASA resource below.')
            st.write('https://climate.nasa.gov/causes/')
            time_left = st.slider("How long do you think we have(years) before climate change causes irreversible damage", min_value=1, max_value=100, value = 0)
            if (time_left != 0 and abs(time_left-100) <= 100):
                st.write('Not too far off! The real number is 100 years. However, here is another way to understand that amount of time. \n In her paper entitled Fatally Confused: Telling the Time in the Midst of Ecological Crisis, Michelle Bastian presents to the reader the strain that the climate crisis has put on our world and how our lack of political advocacy is not to blame, but perhaps the fatal confusion we hold in regards to nature of time and space are. Throughout her paper, Bastian advocates for a form of telling time that relates to the condition of our environment, which by doing so we would not be living in a constative world where our time is based on something as stable and predictable as an atom, augmented by the movements of a planet around a star. Instead, it would be something more unpredictable and performative that would, in theory, reveal more information about a particular subject. In this instance, that particular subject being the current ecological crisis. Bastians methodical structure of her paper allows her to organize her thoughts well, all while helping the reader understand an important aspect regarding the background of how we perceive and utilize time in our everyday lives. This enables the author to elaborate more on her stance and, ultimately, devise a new way of telling time that fits original as well as new criteria. Her constant use of references to outside papers further strengthens the point Bastian is trying to drive by justifying claims she seeks to make, which in turn results in an informative paper regarding a crucial crisis.')
        if (hoax == 'Fabricated'):    
            st.write('Your apprehension is understandable. Many call into question the validity of these data points. However, taking a deeper dive into the data can help you to understand why there is a scientific consensus on this topic. Below is a NASA report explaining how we know that climate change is actually happening. For example, satellite tracking has allowed scientists to see at a large scale what is happening to the globe. Furthermore, they break down the causes of what is happening into more understandable chunks.')
            st.write('https://climate.nasa.gov/evidence/')
    if (direction == 'Personal Impacts'):
        st.write("Below is a resource to learn more about this topic. Author Nikayla Jefferson tells a riveting story about her personal experience with climate change as a Black American woman. Her words about the American Dream actaully being a nightmare show how different perspectives are shaped by climate change. She talks about how the American Dream which heavily promotes consumption has been a driving force in America's role in climate change. Among many other issues, Jefferson hopes to undo the harmful effects of climate change that have polluted her city, a scary sign as she mentions Black children are 5 times more likely to die from asthma. Read more to here more about how climate change has personally affected Nikayla.")
        st.write("https://urldefense.proofpoint.com/v2/url?u=https-3A__www.thenation.com_article_environment_environmental-2Djustice-2Dracism-2Dcovid_&d=DwIGaQ&c=-35OiAkTchMrZOngvJPOeA&r=BmF5uiBgkrvN4DQtKa9Q0w&m=ph6ebrS_ATFX90WAmyX5rDBh28z_-1z5WXFOta-A4S9J7AQef_szcgYyP7Z8GDJx&s=LeVdENFTnFKzQPTSABIvct2m7CKqJn871zPnQMWRw84&e= ")
        
  
  
def Page2(prevpage):
    st.write("Glad to hear! But keep in mind, “no matter how well informed, you are surely not alarmed enough” - Wallace Wells ")
    direction = st.selectbox('Where do you feel you can further your understanding of climate change',('None', 'Personal Impacts', 'Ways to Help'), index = 0)	    
    if (direction == 'Personal Impacts'):
        st.write("That is very understandable! In fact, even though some people may view climate change as a serious problem, there are still a vast majority of those who overlook the idea that any serious apocalyptic danger can come to their own communities in a large scale manner as well. When the greenhouse gasses that stay trapped in the atmosphere result in an increase of earth\'s temperature, it is not just the developing countries that will suffer like some media coverage might suggest, but everyone everywhere will face some sort of vulnerability that could come in the form of anything ranging from drier seasons and food scarcity to rise in sea levels and community displacement. To help you grasp more clearly these very possible scenarios, linked below is the book entitled The Collapse of Western Civilization that gives us some insight into the horrors of what will be waiting for us if immediate action is not taken.")
        st.write("https://urldefense.proofpoint.com/v2/url?u=https-3A__nymag.com_intelligencer_2017_07_climate-2Dchange-2Dearth-2Dtoo-2Dhot-2Dfor-2Dhumans.html&d=DwIGaQ&c=-35OiAkTchMrZOngvJPOeA&r=BmF5uiBgkrvN4DQtKa9Q0w&m=ph6ebrS_ATFX90WAmyX5rDBh28z_-1z5WXFOta-A4S9J7AQef_szcgYyP7Z8GDJx&s=Q40D2_jGhJPzjSa95lwxsvxyRqo8eS_fIqQ2gycJWsQ&e=")
        more = st.selectbox('When you discuss issues relating to the ongoing climate crisis, do you find yourself thinking in a more broad scope encompassing communities all around the world or a more narrow scope dealing with issues related to areas near you?',('None', 'Broad', 'Narrow'), index = 0)
        if(more == 'Broad'):
            st.write("Nice! Thinking about how the affects of climate change can affect people all around the globe can be beneficial in many ways; however, it is also important that we as a society be able to shift our perspective to be more in tune in aspects regarding how the climate crisis will affect us personally within our communites or even within our homes. By doing this, we not only learn more about how our communites may already be affected by climate change, but also to make the problem more personal, which can allow us to observe how our habits may be contributing to the climate crisis. Linked below is a video arranged by DEPS Colum of climate activist Katharine Hayhoe further explaining this thought.")
            st.write("https://urldefense.com/v3/__https://www.youtube.com/watch?v=FHkZ7aOE3hQ__;!!Mih3wA!C0VfXzA0YNOqa9n814rkHLYsFfw79SL4ZbWuYARD5_cM62a2UV3t3jnh1bJ4PpRoNtYoDrzwgIXFBo1xnV-J2t0I$ ")
        if(more == 'Narrow'):
            st.write("Nice! Thinking about how the effects of climate change can affect the communites around you can be very beneficial in many ways; however, thinking about the apocolyptic like events that can be triggered in areas all around the world is also worth thinking about as action from governments of all countries is needed in order to potentially combat this crisis. At the end of the day, fossil fuels being burned in a country half way accross the globe is still fossil fuels being burned. To learn more about how governments can take action as well as how the affects of climate change can alter our way of life, click the respective links below!")
            st.write("[Government Action](https://urldefense.com/v3/__https://www.un.org/sustainabledevelopment/climate-action/__;!!Mih3wA!C0VfXzA0YNOqa9n814rkHLYsFfw79SL4ZbWuYARD5_cM62a2UV3t3jnh1bJ4PpRoNtYoDrzwgIXFBo1xnUiIEvPn$ )")
            st.write("[Global Affects](https://urldefense.com/v3/__https://nymag.com/intelligencer/2017/07/climate-change-earth-too-hot-for-humans.html__;!!Mih3wA!C0VfXzA0YNOqa9n814rkHLYsFfw79SL4ZbWuYARD5_cM62a2UV3t3jnh1bJ4PpRoNtYoDrzwgIXFBo1xnWNglNwZ$ )")
    if (direction == 'Ways to Help'):
        st.write("The affects that can and have resulted from this ongoing climate crisis are only going to get worse if proper action is not taken. Science has shown us indisputibly what climate change can do, but it can also show us paths towards a more regenerative future in the form of a variety of solutions. Whether we adopt these solutions into our everyday lives and save generations of life here on earth is up to us.")
        st.write("The documentary 2040 directed by Darmon Gameau shows us what life could be like if we embraced the best climate solutions available today! Watch the trailer below.")
        url = 'https://www.youtube.com/watch?v=p-rTQ443akE'
        st.video(url)
        solutions = st.selectbox('What would you like to read more about?', ('None', 'Green Energy', 'Trees', 'Lifestyle'))
        if(solutions == 'Green Energy'):
            st.write("Currently, eighty-four percent of our world\'s energy comes from non-renewable sources despite the emergence of technology that can produce clean energy. In an article for The New York Times, Bill McKibben dives deeper into the facts of our burning reality")
            st.write("https://urldefense.com/v3/__https://www.newyorker.com/news/essay/in-a-world-on-fire-stop-burning-things__;!!Mih3wA!C0VfXzA0YNOqa9n814rkHLYsFfw79SL4ZbWuYARD5_cM62a2UV3t3jnh1bJ4PpRoNtYoDrzwgIXFBo1xnch1sQxo$ ")
        if(solutions == 'Trees'):
            st.write("Forests are important carbon sinks, which allows them to draw carbon released into the atomsphere; however, with more and more deforestation occuring every minute, we risk fatal degredation to all life on earth.Burning fossil fuels, in combination with destruction of carbon sinks due to deforestation and other activities, has contributed to more and more carbon dioxide building up in the atmosphere – more than can be absorbed from existing carbon sinks such as forests. The build-up of carbon dioxide in the atmosphere is driving global warming, as it traps heat in the lower atmosphere. While this may be a scary thought, there is a bright side. Youtubers from all around the world have banned together to help plant more than twenty million trees! To learn more about how impactful trees can be in our fight against climate change and how these youtubers called their audiences to action to achieve this goal, click on the link below!")
            st.write("https://urldefense.com/v3/__https://www.youtube.com/watch?v=U7nJBFjKqAY&t=669s__;!!Mih3wA!C0VfXzA0YNOqa9n814rkHLYsFfw79SL4ZbWuYARD5_cM62a2UV3t3jnh1bJ4PpRoNtYoDrzwgIXFBo1xnU9oDsba$ ")
        if(solutions == 'Lifestyle'):
            st.write("One of the biggest ways an individual can help lessen their impact on the earth\'s climate is by adopting a more eco-friendly way of life. From the food you eat to the waste you produce, nearly every choice you make can be subsituted with a more sustainable way of living. Below are just two of the many ways in which you can lead a green life!")
            st.write("[Composting](https://urldefense.com/v3/__https://www.youtube.com/watch?v=bqDQD8cvO5Y__;!!Mih3wA!C0VfXzA0YNOqa9n814rkHLYsFfw79SL4ZbWuYARD5_cM62a2UV3t3jnh1bJ4PpRoNtYoDrzwgIXFBo1xnSoOlh71$ )")
            st.write("[Meat = bad](https://urldefense.com/v3/__https://www.youtube.com/watch?v=-k-V3ESHcfA&t=196s__;!!Mih3wA!C0VfXzA0YNOqa9n814rkHLYsFfw79SL4ZbWuYARD5_cM62a2UV3t3jnh1bJ4PpRoNtYoDrzwgIXFBo1xnZmUVkob$ )")
            st.write("Additionally, if you would like to calculate you own carbon footprint and see an aproximation of how much carbon your household produces [click here](https://urldefense.com/v3/__https://www.nature.org/en-us/get-involved/how-to-help/carbon-footprint-calculator/__;!!Mih3wA!C0VfXzA0YNOqa9n814rkHLYsFfw79SL4ZbWuYARD5_cM62a2UV3t3jnh1bJ4PpRoNtYoDrzwgIXFBo1xncTvXqvv$ )")
  
def Page3(prevpage)  :
    st.header('Thank you for visiting. We hope you were able to learn a bit about climate change. Below we have a link to climate change organizations that you can donate to so you can help the fight against global warming. \n https://www.charitynavigator.org/index.cfm?bay=content.view&cpid=8636')
  
  
  
  
  
  

# def Page2(prevpage):
#     st.write("Glad to hear. However keep in mind “But no matter how well informed you are surely not alarmed enough” - Wallace Wells ")
#     direction = st.selectbox('Where do you feel you can further your understanding of climate change',('None', 'Large Scale Impact', 'Personal Impacts'), index = 0)	    
#     if (direction == 'Large Scale Impact'):
#         st.header("Below is a resource to learn more about this topic")
#         st.write("https://urldefense.proofpoint.com/v2/url?u=https-3A__nymag.com_intelligencer_2017_07_climate-2Dchange-2Dearth-2Dtoo-2Dhot-2Dfor-2Dhumans.html&d=DwIGaQ&c=-35OiAkTchMrZOngvJPOeA&r=BmF5uiBgkrvN4DQtKa9Q0w&m=ph6ebrS_ATFX90WAmyX5rDBh28z_-1z5WXFOta-A4S9J7AQef_szcgYyP7Z8GDJx&s=Q40D2_jGhJPzjSa95lwxsvxyRqo8eS_fIqQ2gycJWsQ&e= ")
#    
#     if (direction == 'Personal Impacts'):
#         st.header("Below is a resource to learn more about this topic")
#         st.write("https://urldefense.proofpoint.com/v2/url?u=https-3A__thegeorgiareview.com_posts_is-2Dall-2Dwriting-2Denvironmental-2Dwriting_&d=DwIGaQ&c=-35OiAkTchMrZOngvJPOeA&r=BmF5uiBgkrvN4DQtKa9Q0w&m=ph6ebrS_ATFX90WAmyX5rDBh28z_-1z5WXFOta-A4S9J7AQef_szcgYyP7Z8GDJx&s=9FGudG6MTOOcIwzqPp9xMahNKPEa548RfDGJVcdnApI&e= ")

# 
# def Page3(prevpage):
#     st.header("Below is a resource to learn more about this topic")
#     st.write("https://urldefense.proofpoint.com/v2/url?u=https-3A__climate.nasa.gov_&d=DwIGaQ&c=-35OiAkTchMrZOngvJPOeA&r=BmF5uiBgkrvN4DQtKa9Q0w&m=ph6ebrS_ATFX90WAmyX5rDBh28z_-1z5WXFOta-A4S9J7AQef_szcgYyP7Z8GDJx&s=vgtY8X5fBRukX6SL9mI9E4OTG4V99DetpeBJL0fCy-4&e= ")
#     
# def Page4(prevpage):
#     st.header("Below is a resource to learn more about this topic")
#     st.write("https://urldefense.proofpoint.com/v2/url?u=https-3A__www.thenation.com_article_environment_environmental-2Djustice-2Dracism-2Dcovid_&d=DwIGaQ&c=-35OiAkTchMrZOngvJPOeA&r=BmF5uiBgkrvN4DQtKa9Q0w&m=ph6ebrS_ATFX90WAmyX5rDBh28z_-1z5WXFOta-A4S9J7AQef_szcgYyP7Z8GDJx&s=LeVdENFTnFKzQPTSABIvct2m7CKqJn871zPnQMWRw84&e= ")
#     
# def Page5(prevpage):
#     st.header("Below is a resource to learn more about this topic")
#     st.write("https://urldefense.proofpoint.com/v2/url?u=https-3A__nymag.com_intelligencer_2017_07_climate-2Dchange-2Dearth-2Dtoo-2Dhot-2Dfor-2Dhumans.html&d=DwIGaQ&c=-35OiAkTchMrZOngvJPOeA&r=BmF5uiBgkrvN4DQtKa9Q0w&m=ph6ebrS_ATFX90WAmyX5rDBh28z_-1z5WXFOta-A4S9J7AQef_szcgYyP7Z8GDJx&s=Q40D2_jGhJPzjSa95lwxsvxyRqo8eS_fIqQ2gycJWsQ&e= ")
#     
# def Page6(prevpage):
#     st.header("Below is a resource to learn more about this topic")
#     st.write("https://urldefense.proofpoint.com/v2/url?u=https-3A__thegeorgiareview.com_posts_is-2Dall-2Dwriting-2Denvironmental-2Dwriting_&d=DwIGaQ&c=-35OiAkTchMrZOngvJPOeA&r=BmF5uiBgkrvN4DQtKa9Q0w&m=ph6ebrS_ATFX90WAmyX5rDBh28z_-1z5WXFOta-A4S9J7AQef_szcgYyP7Z8GDJx&s=9FGudG6MTOOcIwzqPp9xMahNKPEa548RfDGJVcdnApI&e= ")
	
app.set_initial_page(intropage)
app.add_app("Home", homepage) # ask about education lvl
app.add_app("Page 1", Page1) # lower education lvl
app.add_app("Page 2", Page2)  # higher education lvl 
app.add_app("Page 3", Page3)  # higher education lvl 

# app.add_app("Page 3", Page3) # low edu large
# app.add_app("Page 4", Page4) # low edu personal
# app.add_app("Page 5", Page5) # high edu large
# app.add_app("Page 6", Page6) # low edu personal
app.run()

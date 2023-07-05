import openai
import warnings
import ipywidgets as widgets
from app_config import API_KEY
warnings.filterwarnings('ignore')

class Gpt_Api:

    def __init__(self):
        ''' intialize the UI '''
        self.key = API_KEY
        image = self.load_image()
        self.initailize_widgets(image)
        self.getUserInput()

    def load_image(self):
        ''' load the initial image '''
        file = open("gpt_image.avif", "rb")
        image = file.read()
        return image

    def initailize_widgets(self, image):
        ''' function to initailize widgets '''
        self.image_headline = widgets.Image(
                                value=image,
                                format='jpg',
                                layout=widgets.Layout(padding = '10px'),
                            )
        self.user_input     = widgets.Text(
                                placeholder='Type input to ask from chat GPT',
                                layout=widgets.Layout(padding = '10px'),
                            )
        self.button_send    = widgets.Button(
                                description='Generate response',
                                tooltip='Send',
                                style={'description_width': 'initial'},
                            )
        box_layout          = widgets.Layout(display='flex',
                                flex_flow='column',
                                align_items='center',
                            )
        self.output_widget  = widgets.Output(layout={'border': '1px solid black'})
        self.mainBox        = widgets.VBox([self.image_headline, self.user_input, self.button_send, self.output_widget], 
                                           layout=box_layout)

    def get_completion(self, prompt, model="gpt-3.5-turbo"):
        ''' function to get response from open ai api and exert error handling as well '''
        openai.api_key = self.key
        messages = [{"role": "user", "content": prompt}]
        try:
            response = openai.ChatCompletion.create(
                model=model,
                messages=messages,
                temperature=0.5,
            )
            return response.choices[0].message["content"]
        
        except openai.error.APIError as e:
            return f"OpenAI API returned an API Error: {e}"

        except openai.error.APIConnectionError as e:
            return f"Failed to connect to OpenAI API: {e}"

        except openai.error.RateLimitError as e:
            return f"OpenAI API request exceeded rate limit: {e}"

        except openai.error.Timeout as e:
            return f"OpenAI API request timed out: {e}"

        except openai.error.InvalidRequestError as e:
            return f"Invalid request to OpenAI API: {e}"

        except openai.error.AuthenticationError as e:
            return f"Authentication error with OpenAI API: {e}"

        except openai.error.ServiceUnavailableError as e:
            return f"OpenAI API service unavailable: {e}"
        
        except Exception as e:
            if "TooManyRequests" in str(e):
                return "Oops! Too many requests. Please try again later."

            elif "TimeoutError" in str(e):
                return "Sorry, the request timed out. Please try again later."

            elif "RequestEntityTooLarge" in str(e):
                return "The request size is too large. Please provide a shorter input."

            elif "InvalidRequest" in str(e):
                return "Invalid request. Please check your input and try again."

            elif "ModelUnavailable" in str(e):
                return "The model is currently unavailable. Please try again later."

            elif "Unavailable" in str(e):
                return "The service is currently unavailable. Please try again later."

            elif "Too many tokens" in str(e):
                return "Sorry, my response is too long. Can you please provide more context?"

            else:
                return e
    
    def trigger_api(self, event):
        ''' the function which triggers open ai api and prints response from the api '''
        response = self.get_completion(self.user_input.value)
        self.output_widget.clear_output()
        with self.output_widget:
            print(response)

    def getUserInput(self):
        ''' the base class function to show ui response when generate response button is clicked '''
        self.button_send.on_click(self.trigger_api)
import os, requests, uuid

class Translator:
    '''
    To Use the Translator, an api-key and an endpoint of Azure Translate 
    must be exported to the environment as
    AZURE_API_KEY_UCOLLEGEX = your-api-key
    AZURE_ENDPOINT_UCOLLEGEX = your-end-point
    '''
    def __init__(self):
        apiKey_var = 'AZURE_API_KEY_UCOLLEGEX'
        endpoint_var = 'AZURE_ENDPOINT_UCOLLEGEX'

        if not apiKey_var in os.environ:
            raise Exception('Please set/export the environment variable: {}'.format(apiKey_var))
        if not endpoint_var in os.environ:
            raise Exception('Please set/export the environment variable: {}'.format(endpoint_var))

        self.url = os.environ[endpoint_var] + '/translate?api-version=3.0'
        self.apiKey = os.environ[apiKey_var]

    def toChinese(self, word):
        '''
        Translate to Chinese
        '''
        if word == "Taiwan, China":
            return '中国台湾'
        
        if word == 'Hong Kong, China':
            return '中国香港'
        
        if word == 'Macao, China':
            return '中国澳门'
        
        if word == 'Mainland, China':
            return '中国大陆'
        
        constructed_url = self.url + '&to=zh-CN'
        
        headers = {
            'Ocp-Apim-Subscription-Key': self.apiKey,
            'Content-type': 'application/json',
            'Ocp-Apim-Subscription-Region':'eastasia',
            'X-ClientTraceId': str(uuid.uuid4())
        }

        body = [{
            'text': word
        }]
        response = requests.post(constructed_url, headers = headers, json = body)
        print(response.json())
        return response.json()[0]['translations'][0]['text']

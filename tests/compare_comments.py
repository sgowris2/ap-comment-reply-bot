# This file loads a CSV file and runs the generate_replies function on each row's "comment" field, and adds the
# reply into the "reply" column, then saves the results to a new CSV file with an extra column for a human evaluator to
# compare the generated reply with the original reply in the "original_reply" column.

from utils.load_secrets import inject_secrets_to_env
inject_secrets_to_env()

import pandas as pd
from services.generate_replies import generate_replies
from clients.claude_client import ClaudeClient
from prompts.v5 import DEFAULT_CONFIG
from domain.models import PromptConfig


def compare_comments(input_csv, output_csv, config, model, temperature, client):

    df = pd.read_csv(input_csv, on_bad_lines='warn')
    df['new_reply'] = None  # Add a new column for generated replies

    for index, row in df.iterrows():
        user_input = row['comment']
        print(f"Processing comment: {user_input}")  # Debug print to track progress
        generated_replies, usage, cost = generate_replies(config, user_input, n=1, model=model, temperature=temperature, client=client)
        df.at[index, 'new_reply'] = generated_replies[0]['text']  # Assuming we want the first generated reply
        print(f"Generated reply: {generated_replies[0]['text']}\n\n")

    df.to_csv(output_csv, index=False)


if __name__ == "__main__":
    # Example usage
    input_csv = 'hindi_comments4.csv'  # CSV file with columns: comment, original_reply
    output_csv = '{}_comparison.csv'.format(input_csv.replace('.csv', ''))  # Output file with an additional column for generated replies
    config_dict = DEFAULT_CONFIG.copy()
    config_dict["context"] = \
    """हमारे अंदर, हमारे युवाओं के अंदर पेशेंस 
     बहुत कम हो गया है। यह जो क्विक डिलीवरी 
     एप्स हैं जो हमारे पास 10 मिनट में सामान 
     पहुंचाते हैं। 8 मिनट में सामान पहुंचाते 
     हैं। एक तो इससे मुझे लगता है कि पेशेंस 
     और इमोशन रेगुलेशन कम हो रहा है। 
     इंपल्सिविटी भी बढ़ रही है लोगों की। यह 
     इस बात पर डिप्रेशन पर चले जा रहे हैं कि 
     किसी ने बोल दिया तेरे बाल झड़ रहे हैं। 
     हंसने की बात नहीं है। वो सेल्फ हार्म की 
     तरफ चले जा रहे हैं। किसी को कॉलेज में 
     किसी ने बोल दिया कि तुम्हारे बाल गिर रहे 
     हैं। डूड योर हेयर लाइन इज रिसीविंग। वापस 
     आकर हफ्ते भर तक सोच रहा है कि अब जीना है 
     कि नहीं जीना है। हंसने की बात नहीं है। 
     सचमुच लोग अपनी जान लिए ले रहे हैं। एक 
     तरफ जबरदस्त कंजमशन का दबाव है उनके ऊपर। 
     खरीदो खरीदो खरीदो खरीदो। तुम यह खरीदो। 
     तो तुम्हारे लिए यह नया प्रोडक्ट आया है। 
     तुम्हें ऐसे कूल बनना है। तुम्हें यह करना 
     है। जिंदगी जीने के लिए जीने वाले को 
     जानना जरूरी है। बाकी सब बस गैस का 
     गुब्बारा है बहुत बड़ा। आप उसके भरोसे जी 
     नहीं पाएंगे। धैर्य के लिए तो कुछ ऐसा 
     चाहिए जो इस लायक हो कि उसके लिए धैर्य रख 
     सको और लंबा इंतजार कर सको। जीवन में उतना 
     मूल्यवान कुछ होना चाहिए और वास्तव में 
     तुम्हारे लिए मूल्यवान क्या है यह तुम्हें 
     तभी पता चल सकता है जब तुम्हें पता हो कि 
     तुम कौन हो।
    """
    config = PromptConfig(**config_dict)
    model = 'claude-sonnet-4-6'  # Example model
    temperature = 0.6  # Example temperature
    client =  ClaudeClient() # Your API client instance

    compare_comments(input_csv, output_csv, config, model, temperature, client)
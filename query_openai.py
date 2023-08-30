import tqdm
import argparse
import json
import openai

def queryQuestions(
        model_name,
        spam_data_list,
    ) :
    """
    - args
        - model_name
        - spam_data_list
            TextMessage 객체의 리스트
    """
    # spam_data_list 에서 쿼리를 날릴 원소들의 인덱스를 골라낸다.
    # query_succeed == False 인 원소들의 인덱스를 골라낸다.
    indice_to_process_list = list(filter(
        lambda idx : not spam_data_list[idx].query_succeed,
        range(len(spam_data_list))
    ))

    print("number of data to process : ", len(indice_to_process_list))
    print("processing..")
    with tqdm.tqdm(total=len(indice_to_process_list)) as pbar :
        for data_idx in indice_to_process_list :
            try :
                data = spam_data_list[data_idx]
                messages = [{
                    "role" : "user",
                    "content" : data.query_content
                }]
                response = openai.ChatCompletion.create(
                    model    = model_name,
                    messages = messages
                )
                data.query_response = response['choices'][0]['message']['content']
                data.query_succeed = True
            except Exception as e :
                data.error_message = str(e)
                print(e)

            pbar.update(1)
    
    indice_to_process_list = list(filter(
        lambda idx : not spam_data_list[idx].query_succeed,
        range(len(spam_data_list))
    ))
    print(f"[{len(indice_to_process_list)}] data left to process")
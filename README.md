# IEEE Access 실험 코드

## Overview
- openAI API를 통해 chatGPT 모델에게 문자메시지의 스팸 메시지 여부를 문의하는 코드

- chatGPT API 에는 rate limit 이 존재합니다
    - [링크 참조](https://platform.openai.com/docs/guides/rate-limits/overview)
    - 유료 플랜의 경우 아무 문제 없이 사용할 수 있습니다.
        - openai 에서 api의 병렬 쿼리를 지원하지 않으므로 문자메시지의 개수가 많으면 시간이 오래 걸립니다.
    - 무료 플랜의 경우 일별 제한이 있어 처리할 수 있는 스팸 데이터의 수가 매우 적어집니다.

## Direcotry Structure
```md
.
├── README.md
├── [IEEE ACCESS] ChatGPT 스팸 분류 실험 설계.docx
├── data
│   ├── 20220830_GBL.csv
│   └── ...
├── data.txt
├── openai_api_keys.json
├── query_openai.py
├── query_chatGPT_basic.ipynb
├── question.txt
├── results
│   ├── 20220830_GBL_processed_20230828142030.json
│   └── ...
├── tests
│   └── playground.ipynb
└── text_message.py
```

- data/
    - KISA에서 받은 csv 파일들을 여기에 가져다 놓으시면 됩니다.

- results/
    - 실험 결과가 저장되는 디렉토리 입니다.
    - 파일 이름 포맷은 다음과 같습니다
        - 스팸 데이터 csv 파일을 처리한 결과물인 경우
        - {스팸 데이터 csv 파일 이름}_processed_{년도 달 날짜 시간 분 초}.json
        - ex
            - 20220830_GBL.csv 을 처리하여 2023년 8월 28일 14시 20분 30초에 저장한 경우 :
                - 20220830_GBL_processed_20230828142030.json
                - chatGPT에 같은 내용을 쿼리해도 매번 결과가 달라지고, 어떻게 질문하냐에 따라 쿼리 자체도 달라지기 때문에 처리한 시간도 같이 기록합니다.

- tests/
    - 테스트를 위한 코드들을 저장하였습니다. 보지 않아도 됩니다.

- openai_api_keys.json
    - openAI API key를 저장합니다.
    - 다음과 같은 형식으로 저장해야 합니다.
        ```json
        [
            "KEY1"
            "KEY2"
        ]
        ```
        - 현재는 첫번쨰 키만을 사용합니다.
    - .gitignore에 openapi_api_keys.json 추가해 이 파일이 추적되지 않도록 하였습니다.
    - clone 받은 후 추가하십시오

## Code
- text_message.py
    - 문자메시지에 대응하는 TextMessage dataclass 및 KISA에서 제공하는 스팸 문자를 파싱하는 코드 포함.
    - TextMessage 클래스
        - KISA에서 제공하는 문자메시지에 대한 정보, chatGPT에게 보내는 문의 내용, 응답 결과, 성공 여부 등을 저장하는 필드가 있음.
        - parseRawInput()
            - KISA에서 제공하는 문자메시지 데이터 중 raw string 데이터를 파싱하는 메서드
        - toDict()
            - 클래스의 정보를 담은 dict 리턴

- query_openai.py
    - openai api를 이용해 쿼리를 보내고 답변과 성공 여부를 기록하는 코드 포함.
    - queryQuestion(model_name, spam_data_list)
        - openai API가 지원하는 model_name ([참조](https://platform.openai.com/docs/models/overview)) 과 TextMessage 인스턴스들을 원소로 가지는 spam_data_list를 입력으로 받음.
        - TextMessage 들 중 TextMessage.query_succeed == False 인 원소들만을 필터링해 쿼리를 날림.
        - 이후 응답을 받는데 성공하면 TextMessage.query_succeed를 True로 설정하고 TextMessage.query_response에 응답 내용을 기록



## Usage
- openai 라이브러리가 설치된 가상환경이 있다고 가정함
- dependancy 설정이 까다로운 라이브러리는 사용하지 않음.

```bash
# clone this repository
git clone https://github.com/2InfinityN6eyond/chatGPT_spam_filter
cd chatGPT_spam_filter

# openai api key 저장을 위한 파일 만들기. 이 파일 속 "" 안에 api key를 붙여넣으세요
echo "[\n\t\"\"\n]" >> openai_api_keys.json

mkdir data
# 이 안에 KISA에서 제공한 스팸 메시지 데이터 파일들을 위치시키세요

mkdir results
# 처리 결과가 이 디렉토리에 저장됩니다.
```

- query_chatGPT.ipynb 노트북을 실행시키면 됩니다.
- 워드 파일에 명시된 실험용 코드는 아직 작업중입니다.
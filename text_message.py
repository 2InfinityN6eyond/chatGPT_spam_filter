import dataclasses
import datetime

@dataclasses.dataclass
class TextMessage :
    """
    KISA에서 제공하는 스팸 문자 csv 파일 내용에 대응하는 데이터 클래스
    """
    title : str      = None # 문자 제목
    label : str      = None # 문자 타입
    content : str    = None # 문지 내용
    time1 : datetime = None #
    time2 : datetime = None #
    
    query_succeed : bool  = False # chatGPT 쿼리 성공 여부를 저장
    query_content : str   = None  # chatGPT 쿼리 내용을 저장함
    query_response : str  = None  # chatGPT 답변 내용을 저장함
    error_message : str   = None  # chatGPT 쿼리 실패시 에러 내용을 저장함  

    def __init__(self, input_txt_lines) :
        self.parseRawInput(input_txt_lines)

    def parseRawInput(self, input_txt_lines) :
        time_str1, time_str2, self.label, self.content = input_txt_lines[0].split("[(KISA)]")
        #self.time1 = datetime.datetime.strptime(time_str1.removeprefix("[(KISA:SOL)]"), "%Y%m%d%H%M")
        self.time1 = datetime.datetime.strptime(time_str1.replace("[(KISA:SOL)]", ""), "%Y%m%d%H%M")
        self.time2 = datetime.datetime.strptime(time_str2, "%Y%m%d%H%M")
        for line in input_txt_lines[1:-1] :
            self.content += line
        #self.title = input_txt_lines[-1].removesuffix("[(KISA:EOL)]\n")
        self.title = input_txt_lines[-1].replace("[(KISA:EOL)]\n", "")


    def toDict(self) :
        return {
            "title" : self.title,
            "label" : self.label,
            "content" : self.content,
            "time1" : self.time1.strftime("%Y%m%d%H%M"),
            "time2" : self.time2.strftime("%Y%m%d%H%M"),

            "query_succeed" : self.query_succeed,
            "query_content" : self.query_content,
            "query_response" : self.query_response,
            "error_message" : self.error_message,
        }

def parseKISASpamDataFile(file_path) :
    """
    kisa 에서 제공하는 스팸 데이터 파일을 파싱한다.
    """
    try :
        with open(file_path, "r", encoding="utf-8") as fp :
            data_raw = fp.readlines()[1:]
    except UnicodeDecodeError as e :
        print(e)
        print("utf-8 encoding failed. trying to open file with cp949 encoding")
        with open(file_path, "r", encoding="cp949") as fp :
            data_raw = fp.readlines()[1:]

        

    SOL_IDX_LIST = list(filter(
        lambda x : False if x is False else True,
        list(map(
            lambda line_idx, string : line_idx if "[(KISA:SOL)]" in string else False,
            range(len(data_raw)),
            data_raw
        ))
    ))
    EOL_IDX_LIST = list(filter(
        lambda x : False if x is False else True,
        list(map(
            lambda line_idx, string : line_idx if "[(KISA:EOL)]" in string else False,
            range(len(data_raw)),
            data_raw
        ))
    ))
    assert len(SOL_IDX_LIST) == len(EOL_IDX_LIST), """
        number of SOL lines and EOL lines are different.
        check if data is valid
    """
    text_message_list = []
    for text_data_start_line_idx, text_data_end_line_idx in zip(SOL_IDX_LIST, EOL_IDX_LIST) :
        text_message_list.append(
            TextMessage(input_txt_lines = data_raw[
                text_data_start_line_idx:text_data_end_line_idx + 1
            ])
        )
    return text_message_list

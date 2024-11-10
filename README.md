# GPT-Agent  [[교안(실습파일)]](https://docs.google.com/document/d/18b000S_9fnYCvJx_JBZUjULU1r7Fatx1c-mbZejOp-g/edit?usp=sharing)  [[Paper]](https://drive.google.com/file/d/1YZIvoPfnxh6VM0FhfAgtXGMR9ItUs_xy/view?usp=sharing)
Agentic workflow 


## Agent 란?

에이전트의 핵심 아이디어는 언어 모델을 사용하여 수행할 일련의 동작을 선택하는 것


## Tool 이란?

도구는 에이전트, 체인, 또는 대형 언어 모델(LLM)이 세상과 상호작용할 수 있게 하는 인터페이스이고, 에이전트에서 사용하는 도구의 정의는 다음과 같음

1. **도구 이름**: 도구의 이름을 지정합니다.
2. **도구 설명**: 도구가 무엇인지, 어떤 기능을 하는지에 대한 설명을 작성합니다.
3. **입력 JSON 스키마**: 도구에 입력으로 제공될 데이터의 JSON 스키마를 정의합니다.
4. **호출 함수**: 도구를 실행하기 위해 호출할 함수입니다.
5. **결과 반환 여부**: 도구의 결과를 사용자에게 직접 반환할지 여부를 지정합니다.

이 정의는 에이전트가 다양한 도구와 효과적으로 상호작용할 수 있도록 하는데 필수적입니다.

## [Default Tools](https://python.langchain.com/v0.1/docs/modules/tools/)   ex) [간단한 실습](https://github.com/JSJeong-me/GPT-Agent/blob/main/00-WikiTools.ipynb)

## [다양한 Tools](https://python.langchain.com/v0.1/docs/integrations/tools/)   ex) [PassioAI](https://www.passio.ai/)

##
![LLM+IoT](https://github.com/JSJeong-me/GPT-Agent/assets/54794815/4cbba222-f50b-4eb9-a7ab-0b9af3013ef2)
##

## correlation matrix
##
![correlation_heatmap](https://github.com/user-attachments/assets/c4122a7a-118b-4e05-81a8-0a570807f39d)

## Agents State Transition
##
![agent-state-transition](https://github.com/user-attachments/assets/d973f09a-4147-4ab1-a29a-3d8f7579ec2c)



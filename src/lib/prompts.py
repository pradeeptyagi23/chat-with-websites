from pydantic import BaseModel
from typing import Optional,List
from langchain_core.prompts import ChatPromptTemplate,MessagesPlaceholder





class ChatPromptTmpl(BaseModel):
    user_input: str
    system_input: str
    context:Optional[List[str]] = None

    def get_prompt(cls) -> ChatPromptTemplate:
        if(cls.context):
            cls.system_input = cls.system_input+"\n\n"+cls.context
        print(f"========={cls.system_input}---------------")
        prompt = ChatPromptTemplate.from_messages(
            MessagesPlaceholder(variable_name="chat_history"),
            ("system","Given the above conversation,generate a search query to lookup in order to get information relevant to the conversation"),
            ("user",cls.user_input),
        )

        return prompt

# if "__name__" == "__main__":
#     promt = ChatPromptTmpl(user_input="from user",system_input="from system")
#     print(promt.get_prompt())
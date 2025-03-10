from openai import OpenAI

class NLInferencer:
    def __init__(self, model_name: str, base_url: str, api_key: str) -> None:
        self.model_name = model_name
        self.base_url = base_url
        self.api_key = api_key
        self.model = None
    
    def _init_model(self) -> None:
        self.model = OpenAI(
            base_url=self.base_url, 
            api_key=self.api_key,
            timeout=6000,
            max_retries=5)
    
    def release_model(self):
        self.model = None
    
    def get_query(self, statement: str, gen_statement: str) -> list[dict]:
        sys_prompt = 'Please check the following two math problems are the same or different? Please consider each statement in the two problems; they are different if any statement is different. Please point out any differences you found. Please reply ||same|| or ||different|| in the final sentence with "||" format.'
        prompt = f'Problem 1:\n{statement}\nProblem 2:\n{gen_statement}'
        return [
            {'role': 'system', 'content': sys_prompt},
            {'role': 'user', 'content': prompt}
        ]
    
    def generate(self, statement: str, gen_statement: str, sampling_params: dict) -> str:
        if self.model is None:
            self._init_model()
        response = self.model.chat.completions.create( # type: ignore
            model=self.model_name,
            messages=self.get_query(statement, gen_statement), # type: ignore
            **sampling_params
        )
        return response.choices[0].message.content
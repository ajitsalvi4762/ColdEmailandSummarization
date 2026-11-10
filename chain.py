import os   
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException


load_dotenv()  # Load environment variables from .env file


class chain:
    def __init__(self):
        self.llm = ChatGroq(
                    temperature=0,
                    model="llama-3.3-70b-versatile",
                    groq_api_key=os.getenv("GROQ_API_KEY")
                    )
        
    def extract_jobs(self, cleaned_text):
        prompt_extract = PromptTemplate.from_template(
                        """
                        ### SCRAPED TEST FROM WEBSITE:
                        {page_data}
                        ### INSTRUCTION:
                        The scraped test is from the careers's page of a website.
                        Your job is to  extract the job posting and return them in json format containing the
                        folowing keys: 'role','experience', 'skills' and 'description'.
                        Only return the valid JSON.
                        ### VALID JSON (NO PREAMBLE):
                        """
                    )

        chain_extract = prompt_extract | self.llm
        res = chain_extract.invoke(input={'page_data': cleaned_text})
        try:
            json_parser = JsonOutputParser()
            res = json_parser.parse(res.content)
            
        except OutputParserException as e:
            raise OutputParserException("context too big unable to parse jobs")
        return res if isinstance(res, list) else [res]  # Ensure the output is always a list of job postings
        
    def write_mail(self, job, links):
            prompt_email = PromptTemplate.from_template(
                        """
                        ### JOB Description:
                        {job_description}
                        ### INSTRUCTION:
                        you are Ajit, a business development executive at ABC company. ABC is an AI and softare consulting company. the seamless
                        integration of AI business process through automation.
                        Our experties , tailored soluton, fostering process optimizaton, cost reduction and heightened overall efficiency.
                        Your job is to write a cold email to the client regarding the job mentioned above and in fullfilling their needs.
                        Also add the most relevant ones from the followng links to shocase ABC portfolio:{link_list}
                        remenber you are Ajit, BDX at ABC company.
                        Do not provide Premable.
                        """
                    )

            chain_email = prompt_email | self.llm
            res= chain_email.invoke(input={'job_description': str(job), 'link_list': links})
            return res.content


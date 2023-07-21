import json

from anki.config import GPT_MODEL
from langchain.chat_models import ChatOpenAI
from langchain.chains.summarize import load_summarize_chain
from langchain import PromptTemplate
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import TokenTextSplitter
from langchain.docstore.document import Document
from collections import abc
from dotenv import load_dotenv, find_dotenv

from anki.formatter import AnkiCard

_ = load_dotenv('/Users/evvbmstu/PycharmProjects/deepstudy/anki/.env')


def load_pages_from_pdf(filepath: str, start: int, end: int) -> list[Document]:
    """
    Slice pages from pdf document.
    :param filepath: path to pdf file
    :param start: first page
    :param end: last page
    :return: pages slice
    """
    loader = PyPDFLoader(filepath)
    pages = loader.load_and_split()
    return pages[start:end]


def split_pages(pages: abc.Sequence[Document], chunk_size: int = 5_000, chunk_overlap=0) -> list[Document]:
    """

    :param pages: sequence of Document
    :param chunk_size: size of chunk
    :param chunk_overlap: token count for overlap
    :return: docs based on tokens count
    """
    splitter = TokenTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    texts = splitter.split_text(" ".join([page.page_content for page in pages]))
    docs = [Document(page_content=t) for t in texts]
    return docs


def anki_cards_chain_call(docs):
    prompt_template = """
    Create anki cards based on the following chapter.
    Try to get main points for these anki cards, create questions for interview preparing.
    Keep answer short and clear.Provide your answer in array of json with keys answer and question.
    Reply with only the answer in JSON form and include no other commentary.
    {text}
    """

    anki_cards_prompt = PromptTemplate(template=prompt_template, input_variables=["text"])
    llm = ChatOpenAI(model_name=GPT_MODEL, temperature=0)

    chain = load_summarize_chain(llm,
                                 chain_type="map_reduce",
                                 map_prompt=anki_cards_prompt,
                                 combine_prompt=anki_cards_prompt,
                                 return_intermediate_steps=False,
                                 verbose=False)

    output = chain({"input_documents": docs}, return_only_outputs=True)

    return json.loads(output.get('output_text'))


def generate_anki_cards(filepath: str, *,
                        start_page: int,
                        end_page: int) -> list[AnkiCard]:
    pages = load_pages_from_pdf(filepath, start_page, end_page)
    docs = split_pages(pages)
    anki_cards = anki_cards_chain_call(docs)
    return anki_cards

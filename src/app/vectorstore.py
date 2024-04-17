from langchain_community.vectorstores.chroma import Chroma


async def make_collection_from_documents(docs):
    collection = await Chroma.afrom_documents(docs)
    return collection

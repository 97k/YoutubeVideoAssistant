# Youtube Video | Question - Answer | Summary | Revisit
Why watch the haystack when LLMs can finds the needle for you!

![Visitors](https://api.visitorbadge.io/api/visitors?path=https%3A%2F%2Fgithub.com%2F97k%2Fyt_qa_n_summary&label=Explorers&labelColor=%23c1e1c1&countColor=%23caad7e&style=flat)

### Why I built it?
The motivation behind creating this solution stemmed from a personal need to pinpoint where in an hour-long video, has what I am looking for.
There I have it, my weekend plan all set up and I made this!

![image](https://github.com/97k/yt_qa_n_summary/assets/21143936/bdc76722-961c-4be3-80c3-6c5b952d1449)

Saves you from watching an hour long video just to know one thing that you were looking for, Get summary on top of a youtube video

## How to run?
> :loudspeaker: **You do not need OpenAI API KEYr**: but you need one from [HuggingFace](https://huggingface.co/docs/api-inference/en/quicktour)

This makes use of HuggingFace Inference API for LLMs
- create a .env in the root of repository
- add HF_TOKEN (Get your token from hugging face API)
- `docker-compose build`
- `docker-compose up`

## Technology Stack
- [LangChain](https://github.com/langchain-ai/langchain) for everything RAG + LLM wrapper
- [Streamlit](https://streamlit.io/) for frontend dashboard
- [HuggingFace/MistralAI](https://huggingface.co/mistralai) for LLMs via Inference API
- [Docker Compose](https://docker.com) for evelopment / deployment

## 🚨 Forking this repo (please read!)

I prioritize maintaining my work as open source, but it's crucial to acknowledge that _**plagiarism is unacceptable**_. I spent a non-trivial amount of effort building and designing this, and I am proud of it! While forking this repository is permissible, I kindly ask for proper attribution by referencing https://techyaditya.xyz. Thank you!


## Issues

You can report the bugs at the [issue tracker](https://github.com/97k/yt_qa_n_summary/issues)

## License

Built with ♥ by [Aditya Kaushik](https://techyaditya.xyz) under MIT License.
If this code helps you in

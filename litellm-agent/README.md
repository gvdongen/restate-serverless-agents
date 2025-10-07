# Patterns for building resilient LLM-based apps and agents with Restate


## Running the examples

1. Export your OpenAI API key as an environment variable:
    ```shell
    export OPENAI_API_KEY=your_openai_api_key
    ```
2. [Start the Restate Server](https://docs.restate.dev/develop/local_dev) in a separate shell:
    ```shell
    restate-server
    ```
3. Start the services:
    ```shell
    uv run .
    ```
4. Register the services (use `--force` if you already had another deployment registered at 9080): 
    ```shell
    restate -y deployments register localhost:9080 --force
    ```
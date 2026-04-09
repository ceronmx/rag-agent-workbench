from rag.utils.llm_robustness import clean_json_response


def test_clean_json():
    # 1. Simple JSON
    assert clean_json_response('{"key": "val"}') == '{"key": "val"}'

    # 2. Markdown block
    assert (
        clean_json_response(
            'Here is the json: ```json\n{"key": "val"}\n``` Hope it helps!'
        )
        == '{"key": "val"}'
    )

    # 3. Preamble/Postamble
    assert clean_json_response('Results: {"count": 1} End.') == '{"count": 1}'

    # 4. Multi-line markdown
    input_text = """
    Thinking...
    ```
    {
      "statements": ["A", "B"]
    }
    ```
    """
    assert clean_json_response(input_text) == '{\n      "statements": ["A", "B"]\n    }'


if __name__ == "__main__":
    test_clean_json()
    print("All cleaning tests passed.")

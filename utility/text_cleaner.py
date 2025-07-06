from classes.option import Option
import re

class TextCleaner:
    _EMOJI_PATTERN = re.compile(
        "["
        "\U0001F600-\U0001F64F"
        "\U0001F300-\U0001F5FF"
        "\U0001F680-\U0001F6FF"
        "\U0001F1E0-\U0001F1FF"
        "\U00002500-\U00002BEF"
        "\U00002702-\U000027B0"
        "\U0001F900-\U0001F9FF"
        "\U0001FA70-\U0001FAFF"
        "\u200d"
        "\u2640-\u2642"
        "\u2600-\u2B55"
        "\u23cf"
        "\u23e9"
        "\u231a"
        "\ufe0f"
        "\u3030"
        "]+",
        flags=re.UNICODE
    )

    @staticmethod
    def clean(text: str) -> Option[str].OptionOpt:
        if text is None or not isinstance(text, str) or text.strip() == "":
            return Option.Empty()

        text = text.lower()
        text = re.sub(r"@[A-Za-z0-9_]+", "", text) # Remove @mentions
        text = re.sub(r"http\S+", "", text) # Remove URLs
        text = TextCleaner._EMOJI_PATTERN.sub("", text) # Remove emojis
        # Convert hashtags to regular words (remove # but keep content)
        text = re.sub(r"#([A-Za-z0-9_]+)", r"\1", text) # #MachineLearning -> MachineLearning

        text = re.sub(r"[^a-z0-9]", " ", text) # Keep alphanumerics
        text = re.sub(r"\s+", " ", text).strip() # Normalize whitespace

        return Option.Some(text) if text else Option.Empty()

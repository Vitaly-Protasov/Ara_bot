from transliterate import translit
from itranslate import itranslate
import urllib.parse
from enum import Enum
from Naked.toolshed.shell import muterun_js


class Functions:
    def __init__(self):
        pass

    def translit(
        self,
        text: str,
        latin_lang_code: Enum = 'ka'
    ) -> str:
        return translit(text, latin_lang_code)
    
    def get_translation_link(
        self,
        text: str,
        latin_lang_code: Enum = 'ka',
        target_lang: Enum = 'ru'
    ) -> str:
        parsed_text = urllib.parse.quote_plus(text)
        link = f'https://translate.google.com/?&sl={latin_lang_code}&tl={target_lang}&text={parsed_text}&op=translate'
        return link
    
    def get_translation(
        self,
        text: str,
        source_lang: Enum,
        target_lang: Enum
    ) -> str:
        # return itranslate(text, to_lang=target_lang)

        file_request = 'request.js'
        template = f"""const translate = require('@iamtraction/google-translate');
        translate(
            '{text}',
            {{from: '{source_lang}', to: '{target_lang}' }}).then(res => {{
        console.log(res.text); }}).catch(err => {{
        console.error(err);
        }});
        """
        with open(file_request, "w", encoding="utf-8") as f:
            f.write(template)
        response = muterun_js(file_request)
        return response.stdout.decode("utf-8")


    def pipeline(
        self,
        latin_text: str,
        latin_lang_code: Enum = 'ka',
        target_lang: Enum = 'ru'
    ) -> str:
        transliterated_text = self.translit(latin_text, latin_lang_code)
        link = self.get_translation_link(transliterated_text, latin_lang_code, target_lang)
        translated_text = self.get_translation(transliterated_text, latin_lang_code, target_lang)
        return translated_text, link

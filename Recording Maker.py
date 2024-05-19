""" Recording Maker - Python.

Uses Googles Text-to-Speech, PyAv, Playsound and deep-translator services to 
convert entered text to spoke word in mono WAV format.

This program is free software: you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free Software
Foundation, either version 3 of the License, or (at your option) any later
version.
This program is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
You should have received a copy of the GNU General Public License along with
this program. If not, see <http://www.gnu.org/licenses/>.
"""


__author__ = "Jason Callen"
__credits__ = ["Jason Callen"]
__license__ = "GPLv3"
__version__ = "1.0.1"
__maintainer__ = "Jason Callen"
__email__ = "jason.callen@ascension.org"
__status__ = "Production"
__date__ = "2024/05/19"
__deprecated__ = False

import subprocess, sys, os

try:
    from gtts import gTTS
except ImportError:
    print('gTTS not found. Please install with "pip install gTTS"')
    sys.exit(0)

try:
    import av
except ImportError:
    print('PyAv not found. Please install with "pip install av"')
    sys.exit(0)

try:
    from playsound import playsound
except ImportError:
    print('playsound not found. Please install with "pip install playsound==1.2.2" Some Windows environments have issues with versions later than 1.2.2')
    sys.exit(0)

try:
    from deep_translator import GoogleTranslator
except ImportError:
    print('deep-translator not found. Please install with "pip install deep-translator"')
    sys.exit(0)

DIALECT = {
    'af': 'Afrikaans', 'id': 'Indonesian', 'ro': 'Romanian', 'zh': 'Chinese (Mandarin)',
    'ar': 'Arabic', 'is': 'Icelandic', 'ru': 'Russian',
    'bg': 'Bulgarian', 'it': 'Italian', 'si': 'Sinhala',
    'bn': 'Bengali', 'iw': 'Hebrew', 'sk': 'Slovak',
    'bs': 'Bosnian', 'ja': 'Japanese', 'sq': 'Albanian',
    'ca': 'Catalan', 'jw': 'Javanese', 'sr': 'Serbian',
    'cs': 'Czech', 'km': 'Khmer', 'su': 'Sundanese',
    'da': 'Danish', 'kn': 'Kannada', 'sv': 'Swedish',
    'de': 'German', 'ko': 'Korean', 'sw': 'Swahili',
    'el': 'Greek', 'la': 'Latin', 'ta': 'Tamil',
    'en': 'English', 'lv': 'Latvian', 'te': 'Telugu',
    'es': 'Spanish', 'ml': 'Malayalam', 'th': 'Thai',
    'et': 'Estonian', 'mr': 'Marathi', 'tl': 'Filipino',
    'fi': 'Finnish', 'ms': 'Malay', 'tr': 'Turkish',
    'fr': 'French', 'my': 'Myanmar (Burmese)', 'uk': 'Ukrainian',
    'gu': 'Gujarati', 'ne': 'Nepali', 'ur': 'Urdu',
    'hi': 'Hindi', 'nl': 'Dutch', 'vi': 'Vietnamese',
    'hr': 'Croatian', 'no': 'Norwegian', 'zh-CN': 'Chinese (Simplified)',
    'hu': 'Hungarian', 'pt': 'Portuguese', 'zh-TW': 'Chinese (Mandarin/Taiwan)',
}

def dialect_list():
    col1, col2, col3 = [], [], []
    for i, (code, name) in enumerate(DIALECT.items()):
        if i % 3 == 0:
            col1.append(f"{code}: {name}")
        elif i % 3 == 1:
            col2.append(f"{code}: {name}")
        else:
            col3.append(f"{code}: {name}")

    for i in range(max(len(col1), len(col2), len(col3))):
        row = [col1[i] if i < len(col1) else "",
                col2[i] if i < len(col2) else "",
                col3[i] if i < len(col3) else ""]
        print("{:<30}{:<30}{}".format(*row))

def dialect_select():
    while True:
        lang_selected = input("Select language dialect, default is 'en' :").lower()
        if lang_selected in DIALECT:
            return lang_selected
        elif lang_selected == "":
            lang_selected = "en"
            return lang_selected
        elif lang_selected == "zh-cn":
            return "zh-CN"
        elif lang_selected == "zh-tw":
            return "zh-TW"
        else:
            print("Invlaid selection, try again.")

def input_text_default_opt1_opt2 (prompt,default,opt1, opt2):
## Function to check input text or return default
    while(True):
        option = ''
        try:
            option = str(input(prompt))
            if len(option) == 0:
                return default
            if option.upper() == opt1:
                return opt1
            if option.upper() == opt2:
                return opt2
            else:
                print('Invalid option. Please enter',opt1,'or',opt2)
        except ValueError:
            print('Invalid option. Please enter',opt1,'or',opt2)
        except KeyboardInterrupt:
            print('\nPlease do not stop the program.')

if __name__ == '__main__':

    while True:
        os.system('cls')
        print("Recording and Translator \n\n")
        dialect = "en"
        see_dialect = input_text_default_opt1_opt2(f"Would you like to see dialect list? Y/N [N]: ","N", "Y", "N")
        if see_dialect == "Y":
            dialect_list()
            dialect = dialect_select()
        # Take user input
        text = input("Enter the text you want to convert to audio: ")

        file_out_name = input("Enter the name of the file to save (will be saved as wav): ")
        output_file =file_out_name + ".wav"
        require_translate = input_text_default_opt1_opt2("Does it require translation? Y/N [N]: ","N", "Y", "N")
        if require_translate == "Y":
            translate_to_lang = dialect_select()
            text = GoogleTranslator(source='auto', target=translate_to_lang).translate(text)

        # Create a text-to-speech object
        tts = gTTS(text, lang=dialect)
        hear_file = input_text_default_opt1_opt2("Would you like to hear the recording? Y/N [N]: ","N", "Y", "N")
        
        # Save the audio file
        if file_out_name.endswith != '.mp3':
            file_out_name = file_out_name + ".mp3"
        tts.save(file_out_name)

        with av.open(file_out_name) as in_container:
            in_stream = in_container.streams.audio[0]
            with av.open(output_file, 'w', 'wav') as out_container:
                out_stream = out_container.add_stream(
                    'pcm_mulaw',
                    rate=8000,
                    layout='mono'
                )
                for frame in in_container.decode(in_stream):
                    for packet in out_stream.encode(frame):
                        out_container.mux(packet)
        
        os.remove(file_out_name)
        
        if hear_file =="Y":
            # Play the audio file
            playsound(output_file)

        # Ask if another needs to be created
        create_another = input_text_default_opt1_opt2("Would you like to do another? Y/N [N]: ","N", "Y", "N")
        if create_another == "N":
            break

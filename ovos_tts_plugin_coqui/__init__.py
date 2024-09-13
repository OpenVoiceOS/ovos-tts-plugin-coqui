import os.path

from TTS.api import TTS as CTTS
from langcodes import Language
from ovos_config import Configuration
from ovos_plugin_manager.templates.tts import TTS as AbstractTTS
from ovos_plugin_manager.tts import load_tts_plugin
from ovos_utils.log import LOG


def standardize_lang_tag(lang_code, macro=True):
    """https://langcodes-hickford.readthedocs.io/en/sphinx/index.html"""
    # TODO - move to ovos-utils
    try:
        from langcodes import standardize_tag as std
        return std(lang_code, macro=macro)
    except:
        if macro:
            return lang_code.split("-")[0].lower()
        return lang_code.lower()


class CoquiTTSPlugin(AbstractTTS):
    """Interface to coqui TTS."""
    _MODELS = {}
    LANG2MODEL = {
        "bg": 'tts_models/bg/cv/vits',
        "cs": ['tts_models/cs/cv/vits',
               'tts_models/multilingual/multi-dataset/xtts_v2',
               'tts_models/multilingual/multi-dataset/xtts_v1.1'],
        "da": 'tts_models/da/cv/vits',
        "et": 'tts_models/et/cv/vits',
        "ga": 'tts_models/ga/cv/vits',
        "en": [
            'tts_models/en/vctk/vits',
            'tts_models/en/ljspeech/vits',
            'tts_models/en/ljspeech/vits--neon',
            'tts_models/en/ljspeech/glow-tts',
            'tts_models/multilingual/multi-dataset/xtts_v2',
            'tts_models/multilingual/multi-dataset/xtts_v1.1',
            'tts_models/multilingual/multi-dataset/your_tts',
            'tts_models/en/ek1/tacotron2',
            'tts_models/en/ljspeech/tacotron2-DDC',
            'tts_models/en/ljspeech/tacotron2-DDC_ph',
            'tts_models/en/ljspeech/tacotron2-DCA',
            'tts_models/en/sam/tacotron-DDC',
            'tts_models/en/blizzard2013/capacitron-t2-c50',
            'tts_models/en/blizzard2013/capacitron-t2-c150_v2',
            'tts_models/en/ljspeech/speedy-speech',
            'tts_models/en/ljspeech/neural_hmm',
            'tts_models/en/ljspeech/overflow',
            'tts_models/en/ljspeech/fast_pitch',
            'tts_models/en/vctk/fast_pitch'
        ],
        "es": ['tts_models/es/css10/vits',
               'tts_models/multilingual/multi-dataset/xtts_v2',
               'tts_models/multilingual/multi-dataset/xtts_v1.1',
               'tts_models/es/mai/tacotron2-DDC'],
        "fr": ['tts_models/fr/css10/vits',
               'tts_models/multilingual/multi-dataset/xtts_v2',
               'tts_models/multilingual/multi-dataset/xtts_v1.1',
               'tts_models/multilingual/multi-dataset/your_tts',
               'tts_models/fr/mai/tacotron2-DDC'],
        "uk": ['tts_models/uk/mai/vits',
               'tts_models/uk/mai/glow-tts'],
        "nl": ['tts_models/nl/css10/vits',
               'tts_models/multilingual/multi-dataset/xtts_v2',
               'tts_models/multilingual/multi-dataset/xtts_v1.1',
               'tts_models/nl/mai/tacotron2-DDC'],
        "de": ['tts_models/de/thorsten/vits',
               'tts_models/de/thorsten/vits--neon',
               'tts_models/multilingual/multi-dataset/xtts_v2',
               'tts_models/multilingual/multi-dataset/xtts_v1.1',
               'tts_models/de/thorsten/tacotron2-DCA',
               'tts_models/de/thorsten/tacotron2-DDC'],
        "it": ['tts_models/it/mai_male/vits',
               'tts_models/it/mai_female/vits',
               'tts_models/it/mai_male/glow-tts',
               'tts_models/it/mai_female/glow-tts',
               'tts_models/multilingual/multi-dataset/xtts_v2',
               'tts_models/multilingual/multi-dataset/xtts_v1.1'],
        "el": 'tts_models/el/cv/vits',
        "fi": 'tts_models/fi/css10/vits',
        "hr": 'tts_models/hr/cv/vits',
        "lt": 'tts_models/lt/cv/vits',
        "lv": 'tts_models/lv/cv/vits',
        "mt": 'tts_models/mt/cv/vits',
        "pl": ['tts_models/pl/mai_female/vits',
               'tts_models/multilingual/multi-dataset/xtts_v2',
               'tts_models/multilingual/multi-dataset/xtts_v1.1'],
        "pt": [
            'tts_models/pt/cv/vits'
        ],
        "pt-br": [
            'tts_models/multilingual/multi-dataset/xtts_v2',
            'tts_models/multilingual/multi-dataset/xtts_v1.1',
            'tts_models/multilingual/multi-dataset/your_tts'
        ],
        "ro": 'tts_models/ro/cv/vits',
        "sk": 'tts_models/sk/cv/vits',
        "sl": 'tts_models/sl/cv/vits',
        "sv": 'tts_models/sv/cv/vits',
        "ca": 'tts_models/ca/custom/vits',
        "bn": ['tts_models/bn/custom/vits-male',
               'tts_models/bn/custom/vits-female'],
        "hu": ['tts_models/hu/css10/vits',
               'tts_models/multilingual/multi-dataset/xtts_v2'],
        "tr": ['tts_models/tr/common-voice/glow-tts',
               'tts_models/multilingual/multi-dataset/xtts_v2',
               'tts_models/multilingual/multi-dataset/xtts_v1.1'],
        "fa": 'tts_models/fa/custom/glow-tts',
        "be": 'tts_models/be/common-voice/glow-tts',
        "zh": ['tts_models/multilingual/multi-dataset/xtts_v2',
               'tts_models/multilingual/multi-dataset/xtts_v1.1',
               'tts_models/zh-CN/baker/tacotron2-DDC-GST'],
        "ja": ['tts_models/ja/kokoro/tacotron2-DDC',
               'tts_models/multilingual/multi-dataset/xtts_v2',
               'tts_models/multilingual/multi-dataset/xtts_v1.1'],
        "ewe": 'tts_models/ewe/openbible/vits',
        "hau": 'tts_models/hau/openbible/vits',
        "lin": 'tts_models/lin/openbible/vits',
        "tw_akuapem": 'tts_models/tw_akuapem/openbible/vits',
        "tw_asante": 'tts_models/tw_asante/openbible/vits',
        "yor": 'tts_models/yor/openbible/vits',
        "ko": 'tts_models/multilingual/multi-dataset/xtts_v2',
        "hi": ['tts_models/multilingual/multi-dataset/xtts_v2',
               'tts_models/multilingual/multi-dataset/xtts_v1.1'],
        "ru": ['tts_models/multilingual/multi-dataset/xtts_v2',
               'tts_models/multilingual/multi-dataset/xtts_v1.1'],
        "ar": ['tts_models/multilingual/multi-dataset/xtts_v2',
               'tts_models/multilingual/multi-dataset/xtts_v1.1']
    }

    def __init__(self, lang="en-us", config=None):
        config = config or {}
        config["lang"] = lang
        super().__init__(config=config, audio_ext='wav')
        self.default_model = (self.config.get("model") or
                              self.LANG2MODEL.get(self.lang) or
                              self.LANG2MODEL.get(self.lang.split("-")[0]))
        if isinstance(self.default_model, list):
            self.default_model = self.default_model[0]
        if not self.default_model:
            raise ValueError(f"{self.lang} is not supported, pass 'model' explicitly in config")
        if os.path.isfile(self.default_model):
            raise NotImplementedError("model loading from file not implemented")
        self.get_model()

    def get_model(self, model_id: str = None):
        model_id = model_id or self.default_model
        if model_id not in self._MODELS:
            self._MODELS[model_id] = CTTS(model_id)
            if self.config.get("gpu"):
                self._MODELS[model_id].to("cuda")
        return self._MODELS[model_id]

    def get_tts(self, sentence: str, wav_file: str,
                lang: str = None, voice: str = None,
                reference_speaker: str = None,
                model_id: str = None):
        if model_id:
            tts = self.get_model(model_id)
            lang = lang or self.lang
        elif lang is None:
            tts = self.get_model(self.default_model)
            lang = self.lang
        else:
            model = (self.LANG2MODEL.get(lang) or
                     self.LANG2MODEL.get(lang.split("-")[0]))
            if not model:
                raise ValueError(f"{lang} is not supported")
            if isinstance(model, list):
                model = model[0]
            tts = self.get_model(model)

        if tts.is_multi_speaker:
            voice = voice or tts.speakers[0]
            if voice not in tts.speakers:
                raise ValueError(f"speaker '{voice}' is not valid for selected TTS, valid: {tts.speakers}")

        lang = lang.split("-")[0]
        if tts.is_multi_lingual and lang not in tts.languages:
            raise ValueError(f"lang '{lang}' is not valid for selected TTS, valid: {tts.available_languages}")

        reference_speaker = reference_speaker or self.config.get("reference_speaker")
        if reference_speaker and self.config.get("use_freeVC"):
            tts.tts_with_vc_to_file(pt,
                                    speaker_wav="/home/miro/PycharmProjects/ovos-tts-plugin-nos/test.wav",
                                    speaker=voice if tts.is_multi_speaker else None,
                                    language=lang.split("-")[0] if tts.is_multi_lingual else None,
                                    file_path=wav_file
                                    )
        else:
            tts.tts_to_file(sentence, file_path=wav_file,
                            speaker_wav=reference_speaker,
                            language=lang.split("-")[0] if tts.is_multi_lingual else None,
                            speaker=voice if tts.is_multi_speaker else None)
        return (wav_file, None)  # No phonemes

    @property
    def available_languages(self) -> set:
        """Return languages supported by this TTS implementation in this state
        This property should be overridden by the derived class to advertise
        what languages that engine supports.
        Returns:
            set: supported languages
        """
        return set(standardize_lang_tag(t) for t in self.LANG2MODEL.keys())


class CoquiXTTSPlugin(AbstractTTS):
    """Interface to coqui xTTS."""
    SUPPORTED_LANGS = ["ar", "zh", "cs", "nl", "en", "fr", "de", "hi",
                       "hu", "it", "ja", "ko", "pl", "pt", "ru", "es", "tr"]

    def __init__(self, lang="en-us", config=None):
        config = config or {}
        super().__init__(config=config, audio_ext='wav')
        self.default_model = self.config.get("model", "tts_models/multilingual/multi-dataset/xtts_v2")
        self.model = CoquiTTSPlugin(config={"model": self.default_model, "lang": lang})

    def get_tts(self, sentence: str, wav_file: str,
                lang: str = None, voice: str = None):
        lang = lang or self.lang
        if standardize_lang_tag(lang) not in self.available_languages:
            raise ValueError(f"{lang} is not supported for selected TTS, valid: {self.available_languages}")
        return self.model.get_tts(sentence, wav_file, lang=lang, voice=voice)

    @property
    def available_languages(self) -> set:
        """Return languages supported by this TTS implementation in this state
        This property should be overridden by the derived class to advertise
        what languages that engine supports.
        Returns:
            set: supported languages
        """
        return set(standardize_lang_tag(t) for t in self.SUPPORTED_LANGS)


class CoquiFreeVCTTS(AbstractTTS):
    """Interface to https://github.com/OlaWod/FreeVC via Coqui TTS"""

    def __init__(self, lang="en-us", config=None):
        config = config or {}
        super().__init__(config=config, audio_ext='wav')
        tts_module = self.config.get("tts_module", "ovos-tts-plugin-coqui")
        self.reference_wav = self.config.get("reference_speaker")
        if not self.reference_wav:
            raise ValueError(
                "'reference_speaker' must be set to absolute path of wav file containing the voice to clone")
        if not tts_module:
            raise ValueError("'tts_module' must be set to a valid ovos plugin")
        clazz = load_tts_plugin(tts_module)
        if clazz is None:
            raise ValueError(f"{tts_module} failed to load, is it installed?")
        tts_config = Configuration().get("tts", {}).get(tts_module) or {}
        tts_config.update(self.config)
        self.model: AbstractTTS = clazz(lang=lang, config=tts_config)
        LOG.info(f"FreeVC base TTS: {tts_module} - {clazz} - {tts_config}")
        self.vc = CTTS(model_name="voice_conversion_models/multilingual/vctk/freevc24")
        if self.config.get("gpu"):
            self.vc.to("cuda")

    def get_tts(self, sentence: str, wav_file: str,
                lang: str = None, voice: str = None):
        tmp = wav_file.replace(".wav", "_original.wav")
        voice = voice or self.voice
        tmp, phonemes = self.model.get_tts(sentence, tmp, lang=lang, voice=voice)
        self.vc.voice_conversion_to_file(source_wav=tmp,
                                         target_wav=self.reference_wav,
                                         file_path=wav_file)
        return wav_file, phonemes

    @property
    def available_languages(self) -> set:
        """Return languages supported by this TTS implementation in this state
        This property should be overridden by the derived class to advertise
        what languages that engine supports.
        Returns:
            set: supported languages
        """
        return self.model.available_languages


class CoquiFairSeqTTSPlugin(AbstractTTS):
    """Interface to coqui FairSeq"""
    SUPPORTED_LANGS = [
        'abi', 'ace', 'aca', 'acn', 'acr', 'ach', 'acu', 'guq', 'ade', 'adj', 'agd', 'agx', 'agn', 'aha', 'aka', 'knj',
        'ake', 'aeu', 'ahk', 'bss', 'alj', 'sqi', 'alt', 'alp', 'alz', 'kab', 'amk', 'mmg', 'amh', 'ami', 'azg', 'agg',
        'boj', 'cko', 'any', 'arl', 'ara', 'atq', 'luc', 'hyw', 'apr', 'aia', 'msy', 'cni', 'cjo', 'cpu', 'cpb', 'asm',
        'asa', 'teo', 'ati', 'djk', 'ava', 'avn', 'avu', 'awb', 'kwi', 'awa', 'agr', 'agu', 'ayr', 'ayo', 'abp', 'blx',
        'sgb', 'azj-script_cyrillic', 'azj-script_latin', 'azb', 'bba', 'bhz', 'bvc', 'bfy', 'bgq', 'bdq', 'bdh', 'bqi',
        'bjw', 'blz', 'ban', 'bcc-script_latin', 'bcc-script_arabic', 'bam', 'ptu', 'bcw', 'bqj', 'bno', 'bbb', 'bfa',
        'bjz', 'bak', 'eus', 'bsq', 'akb', 'btd', 'btx', 'bts', 'bbc', 'bvz', 'bjv', 'bep', 'bkv', 'bzj', 'bem', 'bng',
        'ben', 'bom', 'btt', 'bha', 'bgw', 'bht', 'beh', 'sne', 'ubl', 'bcl', 'bim', 'bkd', 'bjr', 'bfo', 'biv', 'bib',
        'bis', 'bzi', 'bqp', 'bpr', 'bps', 'bwq', 'bdv', 'bqc', 'bus', 'bnp', 'bmq', 'bdg', 'boa', 'ksr', 'bor', 'bru',
        'box', 'bzh', 'bgt', 'sab', 'bul', 'bwu', 'bmv', 'mya', 'tte', 'cjp', 'cbv', 'kaq', 'cot', 'cbc', 'car', 'cat',
        'ceb', 'cme', 'cbi', 'ceg', 'cly', 'cya', 'che', 'hne', 'nya', 'dig', 'dug', 'bgr', 'cek', 'cfm', 'cnh', 'hlt',
        'mwq', 'ctd', 'tcz', 'zyp', 'cco', 'cnl', 'cle', 'chz', 'cpa', 'cso', 'cnt', 'cuc', 'hak', 'nan', 'xnj', 'cap',
        'cax', 'ctg', 'ctu', 'chf', 'cce', 'crt', 'crq', 'cac-dialect_sansebastiáncoatán',
        'cac-dialect_sanmateoixtatán', 'ckt', 'ncu', 'cdj', 'chv', 'caa', 'asg', 'con', 'crn', 'cok',
        'crk-script_latin', 'crk-script_syllabics', 'crh', 'cui', 'dsh', 'dbq', 'dga', 'dgi', 'dgk',
        'dnj-dialect_gweetaawueast', 'dnj-dialect_blowowest', 'daa', 'dnt', 'dnw', 'dar', 'tcc', 'dwr', 'ded', 'mzw',
        'ntr', 'ddn', 'des', 'dso', 'nfa', 'dhi', 'gud', 'did', 'mhu', 'dip', 'dik', 'tbz', 'dts', 'dos', 'dgo', 'mvp',
        'nld', 'jen', 'dzo', 'idd', 'eka', 'cto', 'emp', 'eng', 'enx', 'sja', 'myv', 'mcq', 'ese', 'evn', 'eza', 'fal',
        'fao', 'far', 'fij', 'fin', 'fon', 'frd', 'fra', 'ful', 'flr', 'gau', 'gbk', 'gag-script_cyrillic',
        'gag-script_latin', 'gbi', 'gmv', 'lug', 'pwg', 'gbm', 'cab', 'grt', 'krs', 'gso', 'nlg', 'gej', 'deu', 'gri',
        'kik', 'acd', 'glk', 'gof-script_latin', 'gog', 'gkn', 'wsg', 'gjn', 'gqr', 'gor', 'gux', 'gbo', 'ell', 'grc',
        'guh', 'gub', 'grn', 'gyr', 'guo', 'gde', 'guj', 'gvl', 'guk', 'rub', 'dah', 'gwr', 'gwi', 'hat', 'hlb', 'amf',
        'hag', 'hnn', 'bgc', 'had', 'hau', 'hwc', 'hvn', 'hay', 'xed', 'heb', 'heh', 'hil', 'hin', 'hif', 'hns', 'hoc',
        'hoy', 'hus-dialect_westernpotosino', 'hus-dialect_centralveracruz', 'huv', 'hui', 'hun', 'hap', 'iba', 'isl',
        'dbj', 'ifa', 'ifb', 'ifu', 'ifk', 'ife', 'ign', 'ikk', 'iqw', 'ilb', 'ilo', 'imo', 'ind', 'inb', 'irk', 'icr',
        'itv', 'itl', 'atg', 'ixl-dialect_sanjuancotzal', 'ixl-dialect_sangasparchajul',
        'ixl-dialect_santamarianebaj', 'nca', 'izr', 'izz', 'jac', 'jam', 'jav', 'jvn', 'kac', 'dyo', 'csk', 'adh',
        'jun', 'jbu', 'dyu', 'bex', 'juy', 'gna', 'urb', 'kbp', 'cwa', 'dtp', 'kbr', 'cgc', 'kki', 'kzf', 'lew', 'cbr',
        'kkj', 'keo', 'kqe', 'kak', 'kyb', 'knb', 'kmd', 'kml', 'ify', 'xal', 'kbq', 'kay', 'ktb', 'hig', 'gam', 'cbu',
        'xnr', 'kmu', 'kne', 'kan', 'kby', 'pam', 'cak-dialect_santamaríadejesús', 'cak-dialect_southcentral',
        'cak-dialect_yepocapa', 'cak-dialect_western', 'cak-dialect_santodomingoxenacoj', 'cak-dialect_central', 'xrb',
        'krc', 'kaa', 'krl', 'pww', 'xsm', 'cbs', 'pss', 'kxf', 'kyz', 'kyu', 'txu', 'kaz', 'ndp', 'kbo', 'kyq', 'ken',
        'ker', 'xte', 'kyg', 'kjh', 'kca', 'khm', 'kxm', 'kjg', 'nyf', 'kij', 'kia', 'kqr', 'kqp', 'krj', 'zga', 'kin',
        'pkb', 'geb', 'gil', 'kje', 'kss', 'thk', 'klu', 'kyo', 'kog', 'kfb', 'kpv', 'bbo', 'xon', 'kma', 'kno', 'kxc',
        'ozm', 'kqy', 'kor', 'coe', 'kpq', 'kpy', 'kyf', 'kff-script_telugu', 'kri', 'rop', 'ktj', 'ted', 'krr', 'kdt',
        'kez', 'cul', 'kle', 'kdi', 'kue', 'kum', 'kvn', 'cuk', 'kdn', 'xuo', 'key', 'kpz', 'knk', 'kmr-script_latin',
        'kmr-script_arabic', 'kmr-script_cyrillic', 'xua', 'kru', 'kus', 'kub', 'kdc', 'kxv', 'blh', 'cwt', 'kwd',
        'tnk', 'kwf', 'cwe', 'kyc', 'tye', 'kir', 'quc-dialect_north', 'quc-dialect_east', 'quc-dialect_central', 'lac',
        'lsi', 'lbj', 'lhu', 'las', 'lam', 'lns', 'ljp', 'laj', 'lao', 'lat', 'lav', 'law', 'lcp', 'lzz', 'lln', 'lef',
        'acf', 'lww', 'mhx', 'eip', 'lia', 'lif', 'onb', 'lis', 'loq', 'lob', 'yaz', 'lok', 'llg', 'ycl', 'lom', 'ngl',
        'lon', 'lex', 'lgg', 'ruf', 'dop', 'lnd', 'ndy', 'lwo', 'lee', 'mev', 'mfz', 'jmc', 'myy', 'mbc', 'mda', 'mad',
        'mag', 'ayz', 'mai', 'mca', 'mcp', 'mak', 'vmw', 'mgh', 'kde', 'mlg', 'zlm', 'pse', 'mkn', 'xmm', 'mal', 'xdy',
        'div', 'mdy', 'mup', 'mam-dialect_central', 'mam-dialect_northern', 'mam-dialect_southern',
        'mam-dialect_western', 'mqj', 'mcu', 'mzk', 'maw', 'mjl', 'mnk', 'mge', 'mbh', 'knf', 'mjv', 'mbt', 'obo',
        'mbb', 'mzj', 'sjm', 'mrw', 'mar', 'mpg', 'mhr', 'enb', 'mah', 'myx', 'klv', 'mfh', 'met', 'mcb', 'mop', 'yua',
        'mfy', 'maz', 'vmy', 'maq', 'mzi', 'maj', 'maa-dialect_sanantonio', 'maa-dialect_sanjerónimo', 'mhy', 'mhi',
        'zmz', 'myb', 'gai', 'mqb', 'mbu', 'med', 'men', 'mee', 'mwv', 'meq', 'zim', 'mgo', 'mej', 'mpp', 'min', 'gum',
        'mpx', 'mco', 'mxq', 'pxm', 'mto', 'mim', 'xta', 'mbz', 'mip', 'mib', 'miy', 'mih', 'miz', 'xtd', 'mxt', 'xtm',
        'mxv', 'xtn', 'mie', 'mil', 'mio', 'mdv', 'mza', 'mit', 'mxb', 'mpm', 'soy', 'cmo-script_latin',
        'cmo-script_khmer', 'mfq', 'old', 'mfk', 'mif', 'mkl', 'mox', 'myl', 'mqf', 'mnw', 'mon', 'mog', 'mfe', 'mor',
        'mqn', 'mgd', 'mtj', 'cmr', 'mtd', 'bmr', 'moz', 'mzm', 'mnb', 'mnf', 'unr', 'fmu', 'mur', 'tih', 'muv', 'muy',
        'sur', 'moa', 'wmw', 'tnr', 'miq', 'mos', 'muh', 'nas', 'mbj', 'nfr', 'kfw', 'nst', 'nag', 'nch', 'nhe', 'ngu',
        'azz', 'nhx', 'ncl', 'nhy', 'ncj', 'nsu', 'npl', 'nuz', 'nhw', 'nhi', 'nlc', 'nab', 'gld', 'nnb', 'npy', 'pbb',
        'ntm', 'nmz', 'naw', 'nxq', 'ndj', 'ndz', 'ndv', 'new', 'nij', 'sba', 'gng', 'nga', 'nnq', 'ngp', 'gym', 'kdj',
        'nia', 'nim', 'nin', 'nko', 'nog', 'lem', 'not', 'nhu', 'bud', 'nus', 'yas', 'nnw', 'nwb', 'nyy', 'nyn', 'rim',
        'lid', 'nuj', 'nyo', 'nzi', 'ann', 'ory', 'ojb-script_latin', 'ojb-script_syllabics', 'oku', 'bsc', 'bdu',
        'orm', 'ury', 'oss', 'ote', 'otq', 'stn', 'sig', 'kfx', 'bfz', 'sey', 'pao', 'pau', 'pce', 'plw', 'pmf', 'pag',
        'pap', 'prf', 'pab', 'pbi', 'pbc', 'pad', 'ata', 'pez', 'peg', 'fas', 'pcm', 'pis', 'pny', 'pir', 'pjt', 'poy',
        'pol', 'pps', 'pls', 'poi', 'poh-dialect_eastern', 'poh-dialect_western', 'por', 'prt', 'pui', 'pan',
        'tsz', 'suv', 'lme', 'quy', 'qvc', 'quz', 'qve', 'qub', 'qvh', 'qwh', 'qvw', 'quf', 'qvm', 'qul', 'qvn', 'qxn',
        'qxh', 'qvs', 'quh', 'qxo', 'qxr', 'qvo', 'qvz', 'qxl', 'quw', 'kjb', 'kek', 'rah', 'rjs', 'rai',
        'lje', 'rnl', 'rkt', 'rap', 'yea', 'raw', 'rej', 'rel', 'ril', 'iri', 'rgu', 'rhg', 'rmc-script_latin',
        'rmc-script_cyrillic', 'rmo', 'rmy-script_latin', 'rmy-script_cyrillic', 'ron', 'rol', 'cla', 'rng', 'rug',
        'run', 'rus', 'lsm', 'spy', 'sck', 'saj', 'sch', 'sml', 'xsb', 'sbl', 'saq', 'sbd', 'smo', 'rav', 'sxn', 'sag',
        'sbp', 'xsu', 'srm', 'sas', 'apb', 'sgw', 'tvw', 'lip', 'slu', 'snw', 'sea', 'sza', 'seh', 'crs', 'ksb', 'shn',
        'sho', 'mcd', 'cbt', 'xsr', 'shk', 'shp', 'sna', 'cjs', 'jiv', 'snp', 'sya', 'sid', 'snn', 'sri', 'srx', 'sil',
        'sld', 'akp', 'xog', 'som', 'bmu', 'khq', 'ses', 'mnx', 'spa', 'srn', 'sxb', 'suc', 'tgo', 'suk', 'sun', 'suz',
        'sgj', 'sus', 'swh', 'swe', 'syl', 'dyi', 'myk', 'spp', 'tap', 'tby', 'tna', 'shi', 'klw', 'tgl', 'tbk', 'tgj',
        'blt', 'tbg', 'omw', 'tgk', 'tdj', 'tbc', 'tlj', 'tly', 'ttq-script_tifinagh', 'taj', 'taq', 'tam', 'tpm',
        'tgp', 'tnn', 'tac', 'rif-script_latin', 'rif-script_arabic', 'tat', 'tav', 'twb', 'tbl', 'kps', 'twe', 'ttc',
        'tel', 'kdh', 'tes', 'tex', 'tee', 'tpp', 'tpt', 'stp', 'tfr', 'twu', 'ter', 'tew', 'tha', 'nod', 'thl', 'tem',
        'adx', 'bod', 'khg', 'tca', 'tir', 'txq', 'tik', 'dgr', 'tob', 'tmf', 'tng', 'tlb', 'ood', 'tpi', 'jic', 'lbw',
        'txa', 'tom', 'toh', 'tnt', 'sda', 'tcs', 'toc', 'tos', 'neb', 'trn', 'trs', 'trc', 'tri', 'cof', 'tkr', 'kdl',
        'cas', 'tso', 'tuo', 'iou', 'tmc', 'tuf', 'tur', 'tuk-script_latin', 'tuk-script_arabic', 'bov', 'tue', 'kcg',
        'tzh-dialect_bachajón', 'tzh-dialect_tenejapa', 'tzo-dialect_chenalhó', 'tzo-dialect_chamula',
        'tzj-dialect_western', 'tzj-dialect_eastern', 'aoz', 'udm', 'udu', 'ukr', 'ppk', 'ubu', 'urk', 'ura', 'urt',
        'urd-script_devanagari', 'urd-script_arabic', 'urd-script_latin', 'upv', 'usp', 'uig-script_arabic',
        'uig-script_cyrillic', 'uzb-script_cyrillic', 'vag', 'bav', 'vid', 'vie', 'vif', 'vun', 'vut', 'prk', 'wwa',
        'rro', 'bao', 'waw', 'lgl', 'wlx', 'cou', 'hub', 'gvc', 'mfi', 'wap', 'wba', 'war', 'way', 'guc', 'cym', 'kvw',
        'tnp', 'hto', 'huu', 'wal-script_latin', 'wal-script_ethiopic', 'wlo', 'noa', 'wob', 'kao', 'xer', 'yad', 'yka',
        'sah', 'yba', 'yli', 'nlk', 'yal', 'yam', 'yat', 'jmd', 'tao', 'yaa', 'ame', 'zpo', 'zad', 'zpc', 'zca', 'zpg',
        'zai', 'zpl', 'zam', 'zaw', 'zpm', 'zac', 'zao', 'ztq', 'zar', 'zpt', 'zpi', 'zas', 'zaa', 'zpz', 'zab', 'zpu',
        'zae', 'zty', 'zav', 'zza', 'zyb', 'ziw', 'zos', 'gnd', 'ewe']
    _MODELS = {}

    def __init__(self, lang="en-us", config=None):
        super().__init__(config=config, audio_ext='wav')

    def get_model(self, lang: str = None) -> CoquiTTSPlugin:
        lang = lang or self.lang
        norm_l = str(Language.get(lang).to_alpha3())
        if norm_l not in self._MODELS:
            cfg = dict(self.config)
            cfg["lang"] = lang
            cfg["model"] = f"tts_models/{norm_l}/fairseq/vits"
            self._MODELS[norm_l] = CoquiTTSPlugin(lang=lang, config=cfg)
        return self._MODELS[norm_l]

    def get_tts(self, sentence: str, wav_file: str,
                lang: str = None, voice: str = None):
        lang = lang or self.lang
        norm_l = str(Language.get(lang).to_alpha3())
        model = self.get_model(lang)
        return model.get_tts(sentence, wav_file, lang=lang,
                             model_id=f"tts_models/{norm_l}/fairseq/vits")

    @property
    def available_languages(self) -> set:
        """Return languages supported by this TTS implementation in this state
        This property should be overridden by the derived class to advertise
        what languages that engine supports.
        Returns:
            set: supported languages
        """
        return set(standardize_lang_tag(t) for t in self.SUPPORTED_LANGS)


if __name__ == "__main__":
    print(len(CoquiFairSeqTTSPlugin.SUPPORTED_LANGS))

    rvc = CoquiFreeVCTTS(config={
        "voice": 'p232',
        "model": 'tts_models/en/ljspeech/vits',
        "reference_speaker": "/home/miro/PycharmProjects/ovos-tts-plugin-coqui/wjune.wav"})
    rvc.get_tts("It took me a long time to have a voice, now that i have I'm not going to be silent",
                "output.wav", lang="en-us")

    exit()
    tts = CoquiTTSPlugin(lang="en",
                         config={"gpu": True, "reference_speaker": "/home/miro/PycharmProjects/ovos-tts-plugin-coqui/wjune.mp3"})
    print(tts.available_languages)
    # {'tr', 'lin', 'ja', 'fa', 'ko', 'ewe', 'yor', 'da', 'bg', 'mt', 'pl', 'et', 'hau',
    # 'ro', 'sl', 'hu', 'hr', 'zh', 'lt', 'cs', 'tw_asante', 'ar', 'es', 'ru',
    # 'pt-br', 'hi', 'be', 'el', 'de', 'fr', 'en', 'fi', 'lv', 'nl', 'pt', 'it',
    # 'sv', 'tw_akuapem', 'ga', 'ca', 'bn', 'uk', 'sk'}
    tts.get_tts("It took me a long time to have a voice, now that i have I'm not going to be silent",
                "output.wav", lang="pt-pt")

    exit()
    tts = CoquiFairSeqTTSPlugin()
    print(len(tts.available_languages))  # 1127

    pt = "O jurebes é um jurebeiro que gosta de jurebar, ele veio da jurebónia para trazer a jurebação aos jurebiticos"
    tts.get_tts(pt, "output.wav", lang="pt-pt")

    rvc = CoquiFreeVCTTS(config={"tts_module": "ovos-tts-plugin-nos",
                            "reference_speaker": "/home/miro/PycharmProjects/ovos-tts-plugin-nos/test.wav"})
    rvc.get_tts(pt, "output.wav")

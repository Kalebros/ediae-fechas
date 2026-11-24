from app.datafiles.formatters.formatterdatafile import FormatterDatafile
from app.models.almacen import Almacen

import arrow
import simplejson as json
from datetime import date
from loguru import logger

class FormatterJson(FormatterDatafile):
    def read(self, file_path: str):
        try:
            with open(file_path,"r",encoding="utf-8") as f:
                data_raw = json.load(f)
                for usuario in data_raw.get('usuarios', []):
                    vacaciones_date = list()
                    for vacacion in usuario.get('vacaciones', []):
                        if isinstance(vacacion, str):
                            vacaciones_date.append(arrow.get(vacacion, "YYYY-MM-DD").date())
                    usuario['vacaciones'] = vacaciones_date
                return Almacen(**data_raw)
        except FileNotFoundError:
            logger.warning("JSON file not found: {}", file_path)
            return None
        except json.JSONDecodeError:
            logger.warning("JSON decode error in file: {}", file_path)
            return None 

    def write(self, file_path: str, data):

        for usuario in data.get("usuarios", []):
            vacaciones_str = []
            for vacacion in usuario.get('vacaciones', []):
                if isinstance(vacacion, date):
                    vacaciones_str.append(arrow.get(vacacion).format("YYYY-MM-DD"))
            usuario['vacaciones'] = vacaciones_str

        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False)
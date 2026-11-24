from typer import Typer
from loguru import logger

from app.configuration.config import FechasConfig
from app.datafiles.datafile import Datafile
from app.datafiles.formatters.formatterjson import FormatterJson
from app.models.almacen import Almacen
from app.models.usuario import Usuario

cli = Typer()
usuarios = Typer()
cli.add_typer(usuarios, name="usuarios")
configuration = Typer()
cli.add_typer(configuration, name="configuration")

@usuarios.command()
def list():
    """
    List all users in the application.
    """
    config = FechasConfig()
    datafile = Datafile(config.get_data_file_path())

    if datafile.it_exists():
        formatter = FormatterJson()
        almacen: Almacen | None = datafile.read(formatter)
        if almacen is None:
            logger.error("Failed to read almacen from JSON data file.")
            exit(-1)
        for usuario in almacen.usuarios:
            print(usuario.username)
    else:
        logger.info("No users found.")

@usuarios.command()
def create(username: str):
    """
    Create a new username for the application.

    Args:
        username (str): The username for the new configuration.
    """
    config = FechasConfig()
    datafile = Datafile(config.get_data_file_path())
    if datafile.it_exists():
        almacen: Almacen | None = datafile.read()
        if almacen is None:
            logger.error("Failed to read almacen from JSON data file.")
            exit(-1)
        if almacen.usuario_exists(username):
            logger.error("User with username '{}' already exists.", username)
            exit(-1)
        almacen.usuarios.append(Usuario(username=username))
        datafile.write(almacen)
        logger.info("User with username '{}' has been added.", username)
    else:
        almacen: Almacen = Almacen(usuarios=[Usuario(username=username)])
        datafile.write(almacen)
        logger.info("User with username '{}' has been added.", username)

@usuarios.command(name="add-vacaciones")
def add_vacaciones(username: str, vacation_date: str):
    """
    Añade una nueva fecha de vacaciones para el usuario especificado. Esta
    fecha se tiene que indicar en el formato 'YYYY-MM-DD'.

    Args:
        username (str): El nombre de usuario al que se le añadirá la fecha de vacaciones.
        vacation_date (str): La fecha de vacaciones en el formato 'YYYY-MM-DD'.
    """
    from datetime import date, datetime
    from app.datafiles.formatters.formatterjson import FormatterJson
    import arrow
    config = FechasConfig()
    datafile = Datafile(config.get_data_file_path())
    formatter = FormatterJson()

    almacen: Almacen | None = None
    if datafile.it_exists():
        almacen: Almacen | None = datafile.read()

    if almacen is None:
        logger.error("Failed to read almacen from JSON data file.")
        exit(-1)

    if not almacen.usuario_exists(username):
        logger.error("User with username '{}' does not exist.", username)
        exit(-1)

    usuario: Usuario = almacen.get_usuario(username)

    vacation_arrow = arrow.get(vacation_date, "YYYY-MM-DD")
    usuario.vacaciones.append(vacation_arrow.date())
    datafile.write(almacen,formatter)
    logger.info("Vacation date '{}' has been added for user '{}'.", vacation_date, username)


@configuration.command()
def show():
    """
    Show the current configuration of the application.
    """
    config = FechasConfig()
    print("Data folder:", config.get_data_folder())
    print("Data file name:", config.get_data_file_name())
    print("Data file format:", config.get_data_file_format())

@configuration.command(name="initialize")
def initialize():
    """
    Initialize the application by creating the necessary data folder and data file if they do not exist.
    """
    # Crear carpeta configuration en la carpeta actual
    import os
    import omegaconf
    from app.utils import create_folder_if_not_exists
    carpeta_actual = os.getcwd()

    # Crear la ruta completa para la carpeta de configuración
    carpeta_configuration = os.path.join(carpeta_actual, "configuration")
    create_folder_if_not_exists(carpeta_configuration)

    # Crear la ruta completa para la carpeta de configuración
    carpeta_data = os.path.join(carpeta_actual, "data")
    create_folder_if_not_exists(carpeta_data)

    # Crear un documento yaml y escribir la configuración inicial
    default_config_path = os.path.join(carpeta_configuration, "default.yaml")
    
    if os.path.exists(default_config_path):
        logger.info("Configuration file 'default.yaml' already exists.")
        return
    
    conf_initial = omegaconf.OmegaConf.create({
        "data_folder": carpeta_data,
        "data_file": {
            "name": "data.json",
            "format": "json"
        }
    })
    with open(default_config_path, "w") as f:
        omegaconf.OmegaConf.save(conf_initial, f)

    logger.info("Configuration has been initialized and saved to 'default.yaml'.")
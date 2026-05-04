from .provincia import ProvinciaAdmin
from .municipio import MunicipioAdmin
from .entidad import EntidadAdmin
from .evento import EventoAdmin
from .tematica import TematicaAdmin
from .evento_tematica import EventoTematicaAdmin
from .participante import ParticipanteAdmin
from .evento_participante import EventoParticipanteAdmin
from .tribunal import TribunalAdmin
from .oponente import OponenteAdmin
from .trabajo import TrabajoAdmin
from .trabajo_aprobado import TrabajoAprobadoAdmin
from .version_trabajo import VersionTrabajoAdmin
from .no_conformidad import NoConformidadAdmin

__all__ = [
    'ProvinciaAdmin',
    'MunicipioAdmin',
    'EntidadAdmin',
    'EventoAdmin',
    'TematicaAdmin',
    'EventoTematicaAdmin',
    'ParticipanteAdmin',
    'EventoParticipanteAdmin',
    'TribunalAdmin',
    'OponenteAdmin',
    'TrabajoAdmin',
    'TrabajoAprobadoAdmin',
    'VersionTrabajoAdmin',
    'NoConformidadAdmin',
]

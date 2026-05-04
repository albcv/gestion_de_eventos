from .provincia import ProvinciaSerializer
from .municipio import MunicipioSerializer
from .entidad import EntidadSerializer
from .evento import EventoSerializer
from .tematica import TematicaSerializer
from .evento_tematica import EventoTematicaSerializer
from .participante import ParticipanteSerializer
from .evento_participante import EventoParticipanteSerializer
from .tribunal import TribunalSerializer
from .oponente import OponenteSerializer
from .trabajo import TrabajoSerializer
from .trabajo_aprobado import TrabajoAprobadoSerializer
from .version_trabajo import VersionTrabajoSerializer
from .no_conformidad import NoConformidadSerializer
from .user import UserSerializer  

__all__ = [
    'ProvinciaSerializer',
    'MunicipioSerializer',
    'EntidadSerializer',
    'EventoSerializer',
    'TematicaSerializer',
    'EventoTematicaSerializer',
    'ParticipanteSerializer',
    'EventoParticipanteSerializer',
    'TribunalSerializer',
    'OponenteSerializer',
    'TrabajoSerializer',
    'TrabajoAprobadoSerializer',
    'VersionTrabajoSerializer',
    'NoConformidadSerializer',
    'UserSerializer',  
]
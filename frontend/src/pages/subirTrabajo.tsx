import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { getEventoActual } from '../api/evento';
import type { EventoActual } from '../api/evento';
import {
  crearTrabajo,
  obtenerMiTrabajo,
  crearVersion,
  descargarVersion,
  subirPowerpoint,
  descargarPowerpoint,
  type Version
} from '../api/participante';
import trabajoImg from '../img/trabajo.png';

export function SubirTrabajo() {
  const [evento, setEvento] = useState<EventoActual | null>(null);
  const [trabajoExistente, setTrabajoExistente] = useState<any>(null);
  const [versiones, setVersiones] = useState<Version[]>([]);
  const [aprobado, setAprobado] = useState<boolean>(false);
  const [powerpointUrl, setPowerpointUrl] = useState<string | null>(null);
  const [cargandoInicial, setCargandoInicial] = useState(true);

  const [titulo, setTitulo] = useState('');
  const [tematicaId, setTematicaId] = useState<number | ''>('');
  const [archivo, setArchivo] = useState<File | null>(null);
  const [descripcion, setDescripcion] = useState('');

  const [archivoVersion, setArchivoVersion] = useState<File | null>(null);
  const [descripcionVersion, setDescripcionVersion] = useState('');

  const [powerpointFile, setPowerpointFile] = useState<File | null>(null);
  const [subiendoPPT, setSubiendoPPT] = useState(false);

  const [cargando, setCargando] = useState(false);
  const [error, setError] = useState('');
  const [exito, setExito] = useState('');
  const navigate = useNavigate();

  useEffect(() => {
    const cargarDatos = async () => {
      try {
        const data = await getEventoActual();
        if (data.rol_usuario !== 'participante') {
          setError('Acceso denegado. Solo participantes pueden subir trabajos.');
          setTimeout(() => navigate('/inicio'), 2000);
          return;
        }
        setEvento(data);

        const miTrabajo = await obtenerMiTrabajo();
        if (miTrabajo.trabajo_existe && miTrabajo.trabajo) {
          setTrabajoExistente(miTrabajo.trabajo);
          setVersiones(miTrabajo.trabajo.versiones);
          setAprobado(miTrabajo.trabajo.aprobado || false);
          setPowerpointUrl(miTrabajo.trabajo.powerpoint?.url || null); // ✅ Corregido
        }
      } catch (err: any) {
        setError(err.message);
      } finally {
        setCargandoInicial(false);
      }
    };
    cargarDatos();
  }, [navigate]);

  const handleSubmitNuevoTrabajo = async (e: React.SyntheticEvent) => {
    e.preventDefault();
    if (!titulo || !tematicaId || !archivo) {
      setError('Todos los campos son obligatorios');
      return;
    }
    setCargando(true);
    setError('');
    try {
      await crearTrabajo(titulo, tematicaId as number, archivo, descripcion);
      setExito('Trabajo creado correctamente. Recargando...');
      const miTrabajo = await obtenerMiTrabajo();
      if (miTrabajo.trabajo_existe && miTrabajo.trabajo) {
        setTrabajoExistente(miTrabajo.trabajo);
        setVersiones(miTrabajo.trabajo.versiones);
        setAprobado(miTrabajo.trabajo.aprobado || false);
        setPowerpointUrl(miTrabajo.trabajo.powerpoint?.url || null); // ✅
      }
      setTitulo('');
      setTematicaId('');
      setArchivo(null);
      setDescripcion('');
      setTimeout(() => setExito(''), 3000);
    } catch (err: any) {
      setError(err.message);
    } finally {
      setCargando(false);
    }
  };

  const handleSubmitNuevaVersion = async (e: React.SyntheticEvent) => {
    e.preventDefault();
    if (!archivoVersion) {
      setError('Debe seleccionar un archivo');
      return;
    }
    setCargando(true);
    setError('');
    try {
      await crearVersion(trabajoExistente.id, archivoVersion, descripcionVersion);
      setExito('Nueva versión subida correctamente');
      const miTrabajo = await obtenerMiTrabajo();
      if (miTrabajo.trabajo_existe && miTrabajo.trabajo) {
        setVersiones(miTrabajo.trabajo.versiones);
        setAprobado(miTrabajo.trabajo.aprobado || false);
        setPowerpointUrl(miTrabajo.trabajo.powerpoint?.url || null); // ✅
      }
      setArchivoVersion(null);
      setDescripcionVersion('');
      setTimeout(() => setExito(''), 3000);
    } catch (err: any) {
      setError(err.message);
    } finally {
      setCargando(false);
    }
  };

  const handleDescargarVersion = async (version: Version) => {
    try {
      const blob = await descargarVersion(version.id);
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = version.nombre_archivo;
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
      a.remove();
    } catch (err: any) {
      setError(err.message);
    }
  };

  const handleSubirPowerpoint = async () => {
    if (!powerpointFile) {
      setError('Seleccione un archivo PowerPoint');
      return;
    }
    setSubiendoPPT(true);
    try {
      const data = await subirPowerpoint(powerpointFile);
      setPowerpointUrl(data.url);
      setExito('PowerPoint subido correctamente');
      setPowerpointFile(null);
      const miTrabajo = await obtenerMiTrabajo();
      if (miTrabajo.trabajo_existe && miTrabajo.trabajo) {
        setPowerpointUrl(miTrabajo.trabajo.powerpoint?.url || null);
      }
      setTimeout(() => setExito(''), 3000);
    } catch (err: any) {
      setError(err.response?.data?.error || 'Error al subir PowerPoint');
    } finally {
      setSubiendoPPT(false);
    }
  };

  const handleDescargarPowerpoint = async () => {
    try {
      const blob = await descargarPowerpoint();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = 'presentacion.pptx';
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
      a.remove();
    } catch (err: any) {
      setError(err.response?.data?.error || 'Error al descargar PowerPoint');
    }
  };

  if (cargandoInicial) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-green-50 to-emerald-100">
        <div className="text-center text-gray-600">Cargando...</div>
      </div>
    );
  }

  if (error && !trabajoExistente && !evento) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-green-50 to-emerald-100">
        <div className="text-center text-red-600">{error}</div>
      </div>
    );
  }

  const tematicasList = Array.isArray(evento?.tematicas) ? evento.tematicas : [];

  return (
    <div className="min-h-screen bg-gradient-to-br from-green-50 to-emerald-100 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-3xl mx-auto bg-white rounded-2xl shadow-xl overflow-hidden">
        <div className="flex justify-center pt-8 pb-4">
          <div className="inline-flex items-center justify-center w-32 h-32 bg-green-100 rounded-full shadow-lg">
            <img src={trabajoImg} alt="Subir trabajo" className="w-20 h-20 object-contain" />
          </div>
        </div>
        <div className="p-8 pt-2">
          <h2 className="text-3xl font-bold text-center text-gray-800 mb-2">Gestión de trabajos</h2>
          <p className="text-center text-gray-600 mb-6">
            Evento: <span className="font-semibold">{evento?.nombre}</span>
          </p>

          {error && <div className="mb-4 p-3 bg-red-100 text-red-700 rounded-lg text-sm">{error}</div>}
          {exito && <div className="mb-4 p-3 bg-green-100 text-green-700 rounded-lg text-sm">{exito}</div>}

          {!trabajoExistente ? (
            <form onSubmit={handleSubmitNuevoTrabajo} className="space-y-5">
              <div>
                <label className="block text-gray-700 font-medium mb-1">Título del trabajo *</label>
                <input
                  type="text"
                  value={titulo}
                  onChange={(e) => setTitulo(e.target.value)}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500"
                  required
                />
              </div>
              <div>
                <label className="block text-gray-700 font-medium mb-1">Temática *</label>
                <select
                  value={tematicaId}
                  onChange={(e) => setTematicaId(Number(e.target.value))}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500"
                  required
                >
                  <option value="">Seleccione una temática</option>
                  {tematicasList.map((tem: any) => (
                    <option key={tem.id} value={tem.id}>{tem.nombre}</option>
                  ))}
                </select>
              </div>
              <div>
                <label className="block text-gray-700 font-medium mb-1">Documento (PDF o Word) *</label>
                <input
                  type="file"
                  accept=".pdf,.doc,.docx"
                  onChange={(e) => setArchivo(e.target.files?.[0] || null)}
                  required
                  className="w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-green-50 file:text-green-700 hover:file:bg-green-100"
                />
              </div>
              <div>
                <label className="block text-gray-700 font-medium mb-1">Descripción (opcional)</label>
                <textarea
                  value={descripcion}
                  onChange={(e) => setDescripcion(e.target.value)}
                  rows={3}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500"
                />
              </div>
              <button
                type="submit"
                disabled={cargando}
                className="w-full bg-gradient-to-r from-green-600 to-emerald-700 text-white font-semibold py-3 px-4 rounded-lg hover:from-green-700 hover:to-emerald-800 transition disabled:opacity-50"
              >
                {cargando ? 'Creando...' : 'Crear trabajo'}
              </button>
            </form>
          ) : (
            <div>
              <div className="bg-gray-50 p-4 rounded-lg mb-6">
                <h3 className="text-xl font-semibold text-gray-800">Trabajo actual</h3>
                <p><strong>Título:</strong> {trabajoExistente.titulo}</p>
                <p><strong>Temática:</strong> {trabajoExistente.tematica}</p>
                <div className="mt-2">
                  <span className={`inline-block px-3 py-1 rounded-full text-sm font-medium ${aprobado ? 'bg-green-100 text-green-800' : 'bg-yellow-100 text-yellow-800'}`}>
                    {aprobado ? '✓ Aprobado' : '⏳ Pendiente de aprobación'}
                  </span>
                </div>
              </div>

              <h3 className="text-xl font-semibold text-gray-800 mb-3">Versiones subidas</h3>
              {versiones.length === 0 ? (
                <p className="text-gray-500">No hay versiones aún.</p>
              ) : (
                <div className="space-y-3 mb-6">
                  {versiones.map((v) => (
                    <div key={v.id} className="border rounded-lg p-3">
                      <div className="flex justify-between items-start">
                        <div>
                          <p><strong>Versión {v.version_numero}</strong> - {v.nombre_archivo}</p>
                          <p className="text-sm text-gray-500">Tamaño: {v.tamanio} KB - Subido: {new Date(v.fecha_subida).toLocaleDateString()}</p>
                          {v.descripcion && <p className="text-sm text-gray-600">{v.descripcion}</p>}
                        </div>
                        <button
                          onClick={() => handleDescargarVersion(v)}
                          className="px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition text-sm"
                        >
                          Descargar versión {v.version_numero}
                        </button>
                      </div>
                      {v.no_conformidades && v.no_conformidades.length > 0 && (
                        <div className="mt-2 bg-red-50 p-2 rounded">
                          <p className="text-xs font-semibold text-red-700">No conformidades detectadas:</p>
                          <ul className="list-disc list-inside text-xs text-red-600">
                            {v.no_conformidades.map((nc) => (
                              <li key={nc.id}>{nc.no_conformidad}</li>
                            ))}
                          </ul>
                        </div>
                      )}
                    </div>
                  ))}
                </div>
              )}

              {aprobado && (
                <div className="mt-6 border-t pt-4">
                  <h3 className="text-xl font-semibold text-gray-800 mb-3">Presentación PowerPoint</h3>
                  {powerpointUrl ? (
                    <div className="mb-4 flex justify-between items-center">
                      <p className="text-sm text-gray-600">Archivo actual disponible.</p>
                      <button
                        onClick={handleDescargarPowerpoint}
                        className="px-3 py-1 bg-green-600 text-white rounded hover:bg-green-700 text-sm"
                      >
                        Descargar PowerPoint
                      </button>
                    </div>
                  ) : (
                    <p className="text-sm text-gray-500 mb-2">Aún no ha subido la presentación. Puede subirla ahora.</p>
                  )}
                  <div className="flex items-end gap-2">
                    <div className="flex-1">
                      <label className="block text-gray-700 font-medium mb-1">Subir/actualizar PowerPoint (.pptx o .ppt)</label>
                      <input
                        type="file"
                        accept=".ppt,.pptx"
                        onChange={(e) => setPowerpointFile(e.target.files?.[0] || null)}
                        className="w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-green-50 file:text-green-700 hover:file:bg-green-100"
                      />
                    </div>
                    <button
                      onClick={handleSubirPowerpoint}
                      disabled={subiendoPPT || !powerpointFile}
                      className="px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 disabled:opacity-50"
                    >
                      {subiendoPPT ? 'Subiendo...' : 'Subir PowerPoint'}
                    </button>
                  </div>
                </div>
              )}

              {!aprobado && (
                <>
                  <h3 className="text-xl font-semibold text-gray-800 mb-3 mt-6">Subir nueva versión</h3>
                  <form onSubmit={handleSubmitNuevaVersion} className="space-y-4">
                    <div>
                      <label className="block text-gray-700 font-medium mb-1">Documento (PDF o Word) *</label>
                      <input
                        type="file"
                        accept=".pdf,.doc,.docx"
                        onChange={(e) => setArchivoVersion(e.target.files?.[0] || null)}
                        required
                        className="w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-green-50 file:text-green-700 hover:file:bg-green-100"
                      />
                    </div>
                    <div>
                      <label className="block text-gray-700 font-medium mb-1">Descripción (opcional)</label>
                      <textarea
                        value={descripcionVersion}
                        onChange={(e) => setDescripcionVersion(e.target.value)}
                        rows={2}
                        className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500"
                      />
                    </div>
                    <button
                      type="submit"
                      disabled={cargando}
                      className="w-full bg-gradient-to-r from-green-600 to-emerald-700 text-white font-semibold py-3 px-4 rounded-lg hover:from-green-700 hover:to-emerald-800 transition disabled:opacity-50"
                    >
                      {cargando ? 'Subiendo...' : 'Subir nueva versión'}
                    </button>
                  </form>
                </>
              )}

              {aprobado && (
                <div className="mt-6 text-center text-gray-500 italic">
                  El trabajo ha sido aprobado. No se pueden subir más versiones.
                </div>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
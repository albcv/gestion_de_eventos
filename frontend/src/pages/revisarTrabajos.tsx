import { useEffect, useState } from 'react';
import {
  obtenerTrabajosTribunal,
  descargarVersionTribunal,
  aprobarTrabajo,
  agregarNoConformidad,
  obtenerNoConformidades,
  editarNoConformidad,
  eliminarNoConformidad,
  type TrabajoTribunal,
  type Version
} from '../api/oponente';
import { useNavigate } from 'react-router-dom';

export function RevisarTrabajos() {
  const [trabajos, setTrabajos] = useState<TrabajoTribunal[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [aprobando, setAprobando] = useState<number | null>(null);
  const [noConformidadText, setNoConformidadText] = useState<{ [key: number]: string }>({});
  const [noConformidades, setNoConformidades] = useState<{ [key: number]: any[] }>({});
  const [enviandoNC, setEnviandoNC] = useState<number | null>(null);
  const [editandoNC, setEditandoNC] = useState<{ [key: number]: boolean }>({});
  const [editTextNC, setEditTextNC] = useState<{ [key: number]: string }>({});
  const navigate = useNavigate();

  const cargarTrabajos = async () => {
    try {
      const data = await obtenerTrabajosTribunal();
      setTrabajos(data);
      // Cargar no conformidades para todas las versiones
      const ncMap: { [key: number]: any[] } = {};
      for (const trabajo of data) {
        for (const version of trabajo.versiones) {
          try {
            const ncs = await obtenerNoConformidades(version.id);
            ncMap[version.id] = ncs;
          } catch (err) {
            console.error(`Error cargando NC para versión ${version.id}`);
          }
        }
      }
      setNoConformidades(ncMap);
    } catch (err: any) {
      setError(err.message || 'Error al cargar trabajos');
      if (err.response?.status === 403 || err.response?.status === 401) {
        navigate('/login');
      }
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    cargarTrabajos();
  }, [navigate]);

  const handleAprobar = async (trabajoId: number) => {
    setAprobando(trabajoId);
    try {
      await aprobarTrabajo(trabajoId);
      alert('Trabajo aprobado correctamente');
      await cargarTrabajos();
    } catch (err: any) {
      alert(err.response?.data?.error || 'Error al aprobar trabajo');
    } finally {
      setAprobando(null);
    }
  };

  const handleAgregarNoConformidad = async (versionId: number) => {
    const texto = noConformidadText[versionId];
    if (!texto || texto.trim() === '') {
      alert('Escribe un texto para la no conformidad');
      return;
    }
    setEnviandoNC(versionId);
    try {
      await agregarNoConformidad(versionId, texto);
      const ncs = await obtenerNoConformidades(versionId);
      setNoConformidades(prev => ({ ...prev, [versionId]: ncs }));
      setNoConformidadText(prev => ({ ...prev, [versionId]: '' }));
    } catch (err: any) {
      alert(err.response?.data?.error || 'Error al agregar no conformidad');
    } finally {
      setEnviandoNC(null);
    }
  };

  const handleDescargarVersion = async (version: Version) => {
    try {
      const blob = await descargarVersionTribunal(version.id);
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = version.nombre_archivo;
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
      a.remove();
    } catch (err: any) {
      alert('Error al descargar el archivo');
    }
  };

  const handleEditarNC = (nc: any) => {
    setEditandoNC(prev => ({ ...prev, [nc.id]: true }));
    setEditTextNC(prev => ({ ...prev, [nc.id]: nc.no_conformidad }));
  };

  const handleGuardarEdicionNC = async (ncId: number, versionId: number) => {
    const nuevoTexto = editTextNC[ncId];
    if (!nuevoTexto?.trim()) {
      alert('El texto no puede estar vacío');
      return;
    }
    try {
      await editarNoConformidad(ncId, nuevoTexto);
      const ncs = await obtenerNoConformidades(versionId);
      setNoConformidades(prev => ({ ...prev, [versionId]: ncs }));
      setEditandoNC(prev => ({ ...prev, [ncId]: false }));
    } catch (err: any) {
      alert(err.response?.data?.error || 'Error al editar no conformidad');
    }
  };

  const handleEliminarNC = async (ncId: number, versionId: number) => {
    if (!confirm('¿Eliminar esta no conformidad permanentemente?')) return;
    try {
      await eliminarNoConformidad(ncId);
      const ncs = await obtenerNoConformidades(versionId);
      setNoConformidades(prev => ({ ...prev, [versionId]: ncs }));
    } catch (err: any) {
      alert(err.response?.data?.error || 'Error al eliminar no conformidad');
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-green-50 to-emerald-100">
        <div className="text-center text-gray-600">Cargando trabajos...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-green-50 to-emerald-100">
        <div className="text-center text-red-600">{error}</div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-green-50 to-emerald-100 py-12 px-4">
      <div className="max-w-6xl mx-auto">
        <h1 className="text-3xl font-bold text-gray-800 mb-8 text-center">Trabajos para revisión</h1>
        {trabajos.length === 0 ? (
          <p className="text-center text-gray-600">No hay trabajos asignados a tu tribunal.</p>
        ) : (
          <div className="grid gap-6 md:grid-cols-1">
            {trabajos.map((trabajo) => (
              <div key={trabajo.id} className="bg-white rounded-xl shadow-md overflow-hidden">
                <div className="p-6">
                  <div className="flex justify-between items-start">
                    <div>
                      <h2 className="text-xl font-bold text-gray-800">{trabajo.titulo}</h2>
                      <p className="text-sm text-gray-500">Evento: {trabajo.evento}</p>
                      <p className="text-sm"><span className="font-semibold">Participante:</span> {trabajo.participante}</p>
                      <p className="text-sm"><span className="font-semibold">Temática:</span> {trabajo.tematica}</p>
                    </div>
                    <button
                      onClick={() => handleAprobar(trabajo.id)}
                      disabled={aprobando === trabajo.id}
                      className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50"
                    >
                      {aprobando === trabajo.id ? 'Aprobando...' : 'Aprobar trabajo'}
                    </button>
                  </div>

                  <div className="mt-6">
                    <h3 className="font-semibold text-gray-700 mb-2">Versiones y No Conformidades</h3>
                    {trabajo.versiones.length === 0 ? (
                      <p className="text-sm text-gray-500">Sin versiones subidas</p>
                    ) : (
                      <ul className="space-y-4">
                        {trabajo.versiones.map((v) => (
                          <li key={v.id} className="border rounded-lg p-3">
                            <div className="flex justify-between items-start">
                              <div>
                                <p className="text-sm font-medium">Versión {v.version_numero}: {v.nombre_archivo} ({v.tamanio} KB)</p>
                                <p className="text-xs text-gray-400">Subido: {new Date(v.fecha_subida).toLocaleDateString()}</p>
                                {v.descripcion && <p className="text-xs text-gray-600 mt-1">{v.descripcion}</p>}
                              </div>
                              <button
                                onClick={() => handleDescargarVersion(v)}
                                className="px-3 py-1 bg-green-600 text-white text-sm rounded hover:bg-green-700"
                              >
                                Descargar
                              </button>
                            </div>

                            {/* Lista de no conformidades existentes con edición/eliminación */}
                            {noConformidades[v.id] && noConformidades[v.id].length > 0 && (
                              <div className="mt-2 bg-red-50 p-2 rounded">
                                <p className="text-xs font-semibold text-red-700 mb-1">No conformidades:</p>
                                <ul className="space-y-1">
                                  {noConformidades[v.id].map((nc) => (
                                    <li key={nc.id} className="flex items-center justify-between gap-2 text-xs text-red-600">
                                      {editandoNC[nc.id] ? (
                                        <div className="flex-1 flex gap-1">
                                          <input
                                            type="text"
                                            value={editTextNC[nc.id] || ''}
                                            onChange={(e) => setEditTextNC(prev => ({ ...prev, [nc.id]: e.target.value }))}
                                            className="border rounded px-1 py-0.5 text-sm flex-1"
                                          />
                                          <button
                                            onClick={() => handleGuardarEdicionNC(nc.id, v.id)}
                                            className="text-green-700 text-xs"
                                          >
                                            💾
                                          </button>
                                          <button
                                            onClick={() => setEditandoNC(prev => ({ ...prev, [nc.id]: false }))}
                                            className="text-gray-500 text-xs"
                                          >
                                            ✖
                                          </button>
                                        </div>
                                      ) : (
                                        <>
                                          <span className="flex-1">• {nc.no_conformidad}</span>
                                          <div className="flex gap-1">
                                            <button
                                              onClick={() => handleEditarNC(nc)}
                                              className="text-blue-500 text-xs"
                                              title="Editar"
                                            >
                                              ✏️
                                            </button>
                                            <button
                                              onClick={() => handleEliminarNC(nc.id, v.id)}
                                              className="text-red-500 text-xs"
                                              title="Eliminar"
                                            >
                                              🗑️
                                            </button>
                                          </div>
                                        </>
                                      )}
                                    </li>
                                  ))}
                                </ul>
                              </div>
                            )}

                            {/* Formulario para agregar nueva no conformidad */}
                            <div className="mt-3 flex items-start gap-2">
                              <textarea
                                rows={2}
                                className="flex-1 border rounded-lg p-2 text-sm focus:ring-green-500 focus:border-green-500"
                                placeholder="Escriba una nueva no conformidad para esta versión..."
                                value={noConformidadText[v.id] || ''}
                                onChange={(e) => setNoConformidadText(prev => ({ ...prev, [v.id]: e.target.value }))}
                              />
                              <button
                                onClick={() => handleAgregarNoConformidad(v.id)}
                                disabled={enviandoNC === v.id}
                                className="px-3 py-2 bg-yellow-600 text-white text-sm rounded hover:bg-yellow-700 disabled:opacity-50 self-center"
                              >
                                {enviandoNC === v.id ? 'Enviando...' : 'Agregar NC'}
                              </button>
                            </div>
                          </li>
                        ))}
                      </ul>
                    )}
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
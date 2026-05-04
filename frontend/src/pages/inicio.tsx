// src/pages/Inicio.tsx 
import { useEffect, useState } from 'react';
import logo from '../img/logo.png';
import { getEventoActual} from '../api/evento';
import type {EventoActual} from '../api/evento';
import { useNavigate } from 'react-router-dom'; 

export function Inicio() {
  const [evento, setEvento] = useState<EventoActual | null>(null);
  const [cargando, setCargando] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchEvento = async () => {
      try {
        const data = await getEventoActual();
        setEvento(data);
      } catch (err: any) {
        setError(err.message);
      } finally {
        setCargando(false);
      }
    };
    fetchEvento();
  }, []);

  const manejarSubirTrabajo = () => {
    navigate('/subir-trabajo'); 
  };

  const manejarRevisarTrabajos = () => {
    navigate('/revisar-trabajos'); 
  };

  if (cargando) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-green-50 to-emerald-100">
        <div className="text-center text-gray-600">Cargando evento...</div>
      </div>
    );
  }

  if (error || !evento) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-green-50 to-emerald-100">
        <div className="text-center text-red-600">
          {error || 'No se pudo cargar el evento'}
        </div>
      </div>
    );
  }

  // Formateo de fechas
  const fechaApertura = new Date(evento.fecha_apertura).toLocaleDateString();
  const fechaCierre = new Date(evento.fecha_cierre).toLocaleDateString();

  return (
    <div className="min-h-screen bg-gradient-to-br from-green-50 to-emerald-100 relative overflow-hidden">
      <div className="container mx-auto px-4 py-12 relative z-10">
        {/* Hero Section */}
        <div className="text-center mb-16">
          <div className="inline-flex items-center justify-center w-28 h-28 bg-gradient-to-r from-green-600 to-emerald-700 rounded-2xl mb-6 shadow-lg">
            <img src={logo} alt="Logo" className="w-20 h-20 object-contain" />
          </div>
          <h1 className="text-5xl font-bold text-gray-800 mb-4">
            Bienvenido a <span className="text-transparent bg-clip-text bg-gradient-to-r from-green-600 to-emerald-700">Eventos</span>
          </h1>
          <p className="text-xl text-gray-800 max-w-3xl mx-auto">
            La plataforma definitiva para organizar y participar en eventos.
          </p>
        </div>

        {/* Tarjeta del evento */}
        <div className="max-w-3xl mx-auto bg-white rounded-2xl shadow-xl overflow-hidden">
          <div className="p-6 md:p-8">
            <h2 className="text-3xl font-bold text-gray-800 mb-4">{evento.nombre}</h2>
            
            <div className="space-y-3 text-gray-700">
              <p><span className="font-semibold">Entidad patrocinadora:</span> {evento.entidad_patrocinadora}</p>
              <p><span className="font-semibold">Fecha de apertura:</span> {fechaApertura}</p>
              <p><span className="font-semibold">Fecha de cierre:</span> {fechaCierre}</p>
              <div>
                <span className="font-semibold">Temáticas:</span>
                <ul className="list-disc list-inside ml-4 mt-1">
                  {evento.tematicas.map((tem, idx) => (
                    <li key={idx}>{tem.nombre}</li>
                  ))}
                </ul>
              </div>
            </div>

            {/* Botones según rol */}
            <div className="mt-8 flex justify-center gap-4">
              {evento.rol_usuario === 'participante' && (
                <button
                  onClick={manejarSubirTrabajo}
                  className="px-6 py-3 bg-green-600 hover:bg-green-700 text-white font-semibold rounded-lg transition duration-200 shadow-md"
                >
                  Subir trabajo
                </button>
              )}
              {evento.rol_usuario === 'oponente' && (
                <button
                  onClick={manejarRevisarTrabajos}
                  className="px-6 py-3 bg-emerald-700 hover:bg-emerald-800 text-white font-semibold rounded-lg transition duration-200 shadow-md"
                >
                  Revisar trabajos
                </button>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}